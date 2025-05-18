import streamlit as st, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from pathlib import Path
sns.set_style("whitegrid")

###############################################################################
# LOAD
###############################################################################
@st.cache_data
def load(path):
    df = pd.read_csv(path)
    return df.rename(columns={                       # ← ערכי ברירת-מחדל
        "Minutes Streamed Per Day": "minutes",
        "Discover Weekly Engagement (%)": "discover",
        "Listening Time (Morning/Afternoon/Night)": "time_day",
        "Top Genre": "genre",
        "Age": "age", "Country": "country"
    })

CSV = Path("Global_Music_Streaming_Listener_Preferences.csv")
if CSV.exists():
    df = load(CSV)
else:
    f = st.file_uploader("Upload CSV", type="csv")
    if not f: st.stop()
    df = load(f)

###############################################################################
# NAV
###############################################################################
page = st.sidebar.selectbox("View", (
    "Overview",
    "Daily listening time",
    "Discover engagement",
    "Genres × Country",
    "Genres × Time-of-day")
)

###############################################################################
# VIEWS
###############################################################################
def overview():
    st.header("Dataset preview"); st.dataframe(df.head())
    st.subheader("Describe()"); st.write(df.describe())

def hist(col, title, color):
    st.header(title)
    fig, ax = plt.subplots()
    sns.histplot(df[col], bins=30, kde=True, color=color, ax=ax)
    st.pyplot(fig)

def genres_country():
    st.header("Genres across countries")
    sel = st.multiselect("Filter countries", sorted(df.country.unique()))
    data = df if not sel else df[df.country.isin(sel)]
    fig, ax = plt.subplots(figsize=(10,5))
    sns.countplot(data=data, x="genre", hue="country", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig)

def genres_time():
    st.header("Genres by time-of-day")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.countplot(data=df, x="genre", hue="time_day", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig)

PAGES = {
    "Overview": overview,
    "Daily listening time": lambda: hist("minutes", "Distribution of daily listening time", "#5DADE2"),
    "Discover engagement": lambda: hist("discover", "Distribution of Discover Weekly engagement (%)", "#F4A261"),
    "Genres × Country": genres_country,
    "Genres × Time-of-day": genres_time
}
PAGES[page]()

st.markdown("---")
st.caption("Built with Streamlit • Global Music Streaming Preferences")

