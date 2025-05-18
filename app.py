# ═══════════════  Global Music Streaming – Cute Streamlit App  ════════════════
import streamlit as st, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from pathlib import Path ; sns.set_style("whitegrid")

################################################################################
# 1  LOAD DATA (local ⇒ remote)                       🗂️
################################################################################
LOCAL_CSV = Path("Global_Music_Streaming_Listener_Preferences.csv")
REMOTE_CSV_URL = (
    "https://www.dropbox.com/s/xxxxxxxxxx/Global_Music_Streaming_Listener_Preferences.csv?dl=1"
    # 👆  שימי כאן לינק ישיר (dl=1) אם לא תרצי לשים את הקובץ בריפו
)

@st.cache_data(show_spinner="Loading data…")
def load_data() -> pd.DataFrame:
    if LOCAL_CSV.exists():
        df = pd.read_csv(LOCAL_CSV)
    else:
        df = pd.read_csv(REMOTE_CSV_URL)
    return df.rename(columns={
        "Minutes Streamed Per Day": "minutes",
        "Discover Weekly Engagement (%)": "discover",
        "Listening Time (Morning/Afternoon/Night)": "time_day",
        "Top Genre": "genre",
        "Age": "age", "Country": "country" })

df = load_data()

################################################################################
# 2  PAGE DECORATION                                                 ✨
################################################################################
st.set_page_config(page_title="🎵 Streaming Insights", page_icon="🎧", layout="wide")

st.markdown(
    "<h1 style='text-align:center; color:#1F77B4'>🎶 Global Music Streaming Preferences</h1>",
    unsafe_allow_html=True)

st.markdown(
    "<h4 style='text-align:center; color:gray;'>Mid-term project • Introduction to Data Science</h4><br>",
    unsafe_allow_html=True)

################################################################################
# 3  SIDEBAR NAVIGATION                                              🎛️
################################################################################
st.sidebar.title("🔎 Explore")
page = st.sidebar.radio(
    "Select view",
    ["🏠 Overview",
     "⏱️ Daily listening",
     "⭐ Discover engagement",
     "📈 Age vs minutes",
     "🌍 Genres × Country",
     "🕒 Genres × Time-of-day"]
)

################################################################################
# 4  PLOT HELPERS                                                   📊
################################################################################
def header(txt, emoji=""):
    st.markdown(f"<h2 style='text-align:center;'>{emoji} {txt}</h2>", unsafe_allow_html=True)

def hist(col, title, color):
    header(title)
    fig, ax = plt.subplots()
    sns.histplot(df[col], bins=30, kde=True, color=color, ax=ax)
    st.pyplot(fig)

################################################################################
# 5  PAGES
################################################################################
if page.startswith("🏠"):
    header("Dataset overview", "👀")
    st.dataframe(df.head(), use_container_width=True)
    st.write(" ")
    st.subheader("⚙️ Descriptive statistics")
    st.write(df.describe())

elif page.startswith("⏱️"):
    hist("minutes", "Distribution of daily listening time (minutes)", "#5DADE2")

elif page.startswith("⭐"):
    hist("discover", "Distribution of Discover Weekly engagement (%)", "#F4A261")

elif page.startswith("📈"):
    header("Daily listening time by age", "📊")
    fig, ax = plt.subplots()
    sns.scatterplot(df, x="age", y="minutes", alpha=.3, s=40, ax=ax)
    sns.regplot(df, x="age", y="minutes", scatter=False, color="red", ax=ax)
    st.pyplot(fig)

elif page.startswith("🌍"):
    header("Top genres across countries", "🌎")
    sel = st.multiselect("Filter countries", sorted(df.country.unique()))
    data = df if not sel else df[df.country.isin(sel)]
    fig, ax = plt.subplots(figsize=(10,5))
    sns.countplot(data=data, x="genre", hue="country", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig)

elif page.startswith("🕒"):
    header("Genres by time-of-day", "⏰")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.countplot(data=df, x="genre", hue="time_day", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig)

################################################################################
# 6  FOOTER                                                         📝
################################################################################
st.markdown("---")
st.caption("Made with ❤️ & Streamlit  |  Data: Global Music Streaming Listener Preferences")


