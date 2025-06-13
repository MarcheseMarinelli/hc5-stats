import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Minecraft Server Stats Dashboard", layout="wide")

@st.cache_data
def load_data(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return data

data = load_data("all_players_stats.jsonl")

st.title("🎮 Minecraft Server Stats Dashboard")

# Alle Kategorien herausfinden
all_categories = set()
for player in data:
    for key, value in player.items():
        if isinstance(value, dict):
            all_categories.add(key)

selected_category = st.selectbox("📚 Wähle eine Stat-Kategorie:", sorted(all_categories))

if selected_category:
    # Alle Substats dieser Kategorie finden
    all_substats = set()
    for player in data:
        substats = player.get(selected_category, {})
        if isinstance(substats, dict):
            all_substats.update(substats.keys())

    if all_substats:
        selected_substat = st.selectbox(f"📊 Wähle eine Stat aus `{selected_category}`:", sorted(all_substats))

        if selected_substat:
            # Werte auslesen und DataFrame bauen
            records = []
            for player in data:
                name = player.get("name", player.get("uuid", "Unbekannt"))
                value = player.get(selected_category, {}).get(selected_substat, 0)
                records.append({"Spieler": name, "Wert": value})

            df = pd.DataFrame(records).sort_values("Wert", ascending=False).reset_index(drop=True)

            # Tabelle ohne Index-Spalte anzeigen
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("In dieser Kategorie gibt es keine Einträge.")
