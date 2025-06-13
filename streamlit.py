import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Minecraft Server Stats", layout="wide")

@st.cache_data
def load_data(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return pd.DataFrame(data)

df = load_data("all_players_stats.jsonl")

st.title("🎮 Minecraft Server Stats Dashboard")

# Auswahlbox für Stat-Namen (alle Keys außer uuid und name)
stat_keys = [col for col in df.columns if ":" in col]

selected_stat = st.selectbox("📊 Wähle eine Stat:", sorted(stat_keys))

if selected_stat:
    st.subheader(f"Top Spieler für: `{selected_stat}`")

    if selected_stat in df.columns:
        # Prüfen ob Werte numerisch sind
        if df[selected_stat].apply(lambda x: isinstance(x, (int, float))).any():
            df_sorted = df[["name", selected_stat]].copy()
            df_sorted[selected_stat] = df_sorted[selected_stat].apply(
                lambda x: x if isinstance(x, (int, float)) else 0
            )
            df_sorted = df_sorted.sort_values(selected_stat, ascending=False)

            st.dataframe(df_sorted, use_container_width=True)

            # Prüfen ob wenigstens ein Wert > 0 existiert für's Diagramm
            if (df_sorted[selected_stat] > 0).any():
                st.bar_chart(df_sorted.set_index("name").head(20))
            else:
                st.info("📊 Keine Werte größer 0 für dieses Stat vorhanden.")
        else:
            st.warning("⚠️ Diese Stat enthält komplexe Werte (z.B. Dictionary) und kann nicht direkt angezeigt werden.")
    else:
        st.error("Stat nicht gefunden.")
