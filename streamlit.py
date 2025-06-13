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
    return pd.DataFrame(data)

df = load_data("all_players_stats.jsonl")

st.title("🎮 Minecraft Server Stats Dashboard")

# Kategorien herausfiltern (z.B. minecraft:mined, minecraft:crafted)
category_keys = [col for col in df.columns if ":" in col and not col.count(":") == 1]
top_level_categories = sorted(set(k.split(":")[0] + ":" + k.split(":")[1] for k in category_keys))

selected_category = st.selectbox("📚 Wähle eine Stat-Kategorie:", top_level_categories)

if selected_category:
    # Alle verfügbaren Sub-Stats in der Kategorie extrahieren
    substats = sorted(set(col.split(":")[2] for col in category_keys if col.startswith(selected_category)))

    selected_substat = st.selectbox(f"📊 Wähle eine Stat aus der Kategorie `{selected_category}`:", substats)

    if selected_substat:
        full_stat_key = f"{selected_category}:{selected_substat}"

        st.subheader(f"Top Spieler für: `{full_stat_key}`")

        if full_stat_key in df.columns:
            if df[full_stat_key].apply(lambda x: isinstance(x, (int, float))).any():
                df_sorted = df[["name", full_stat_key]].copy()
                df_sorted[full_stat_key] = df_sorted[full_stat_key].apply(
                    lambda x: x if isinstance(x, (int, float)) else 0
                )
                df_sorted = df_sorted.sort_values(full_stat_key, ascending=False)

                st.dataframe(df_sorted, use_container_width=True)

                if (df_sorted[full_stat_key] > 0).any():
                    st.bar_chart(df_sorted.set_index("name").head(20))
                else:
                    st.info("📊 Keine Werte größer 0 für dieses Stat vorhanden.")
            else:
                st.warning("⚠️ Diese Stat enthält komplexe Werte und kann nicht direkt angezeigt werden.")
        else:
            st.error("Stat nicht gefunden.")
