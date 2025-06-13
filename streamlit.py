import streamlit as st
import pandas as pd
import json

# JSONL laden und in DataFrame packen
data = []
with open("all_players_stats.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data.append(json.loads(line))

df = pd.DataFrame(data)

st.title("Minecraft Server Stats")

# Auswahlbox für Stat-Namen
all_stats = []
for col in df.columns:
    if ":" in col:  # Nur Stat-Keys
        all_stats.append(col)

selected_stat = st.selectbox("Wähle eine Stat:", sorted(all_stats))

# Anzeige sortierte Tabelle
if selected_stat in df.columns:
    st.subheader(f"Top Spieler für: {selected_stat}")
    df_sorted = df[["name", selected_stat]].fillna(0).sort_values(selected_stat, ascending=False)
    st.dataframe(df_sorted)

    st.bar_chart(df_sorted.set_index("name").head(10))
else:
    st.write("Stat nicht gefunden.")
