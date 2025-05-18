# ────────── Global Music Streaming – Cute Streamlit App ──────────
import streamlit as st, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from pathlib import Path; sns.set_style("whitegrid")

# 🗂️ LOAD
@st.cache_data
def load(csv):
    df = pd.read_csv(csv).rename(columns={
        "Minutes Streamed Per Day": "minutes",
        "Discover Weekly Engagement (%)": "discover",
        "Listening Time (Morning/Afternoon/Night)": "time_day",
        "Top Genre": "genre", "Age": "age", "Country": "country"})
    return df

CSV = Path("Global_Music_Streaming_Listener_Preferences.csv")
if CSV.exists(): df = load(CSV)
else:
    st.sidebar.info("📤 Upload the CSV to get started")
    f = st.sidebar.file_uploader("Choose CSV", type="csv")
    if not f: st.stop()
    df = load(f)

# 🎛️ SIDEBAR
st.sidebar.title("🎧 *Stream* Magic")
page = st.sidebar.radio("Navigate", (
    "🏠 Overview",
    "⏱️ Daily listening",
    "⭐ Discover Weekly",
    "📈 Age ↔ Minutes",
    "🌍 Genres × Country",
    "⏰ Genres × Time"))

# ---------- helper functions ----------
def header(txt, emoji=""):
    st.markdown(f"<h2 style='text-align:center;'>{emoji} {txt}</h2>", unsafe_allow_html=True)

def hist(col, title, color):
    header(title)
    fig, ax = plt.subplots(); sns.histplot(df[col], bins=30, kde=True, color=color, ax=ax)
    st.pyplot(fig)

# ---------- pages ----------
if page == "🏠 Overview":
    header("Dataset preview", "👀")
    st.dataframe(df.head()); st.write("")  # spacing
    st.subheader("Quick stats"); st.write(df.describe())

elif page == "⏱️ Daily listening":
    hist("minutes", "Distribution of daily listening time", "#5DADE2")

elif page == "⭐ Discover Weekly":
    hist("discover", "Distribution of Discover Weekly engagement (%)", "#F4A261")

elif page == "📈 Age ↔ Minutes":
    header("Daily listening time by age", "📊")
    fig, ax = plt.subplots()
    sns.scatterplot(df, x="age", y="minutes", alpha=.3, s=40, ax=ax)
    sns.regplot(df, x="age", y="minutes", scatter=False, color="red", ax=ax)
    st.pyplot(fig)

elif page == "🌍 Genres × Country":
    header("Top genres across countries", "🌎")
    sel = st.multiselect("Filter countries", sorted(df.country.unique()))
    data = df if not sel else df[df.country.isin(sel)]
    fig, ax = plt.subplots(figsize=(10,5))
    sns.countplot(data=data, x="genre", hue="country", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right"); st.pyplot(fig)

elif page == "⏰ Genres × Time":
    header("Genres by time-of-day", "🕒")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.countplot(data=df, x="genre", hue="time_day", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right"); st.pyplot(fig)

# ---------- footer ----------
st.markdown("---")
st.caption("Made with ❤️ & Streamlit • Global Music Streaming Preferences")



