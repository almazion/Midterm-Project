# ───────────────────────────────────────────────────────────
#   Global Music Streaming Preferences – Streamlit App
#   Place this file AND the CSV in the same repo directory.
#   If the CSV is missing, the app will prompt an upload.
# ───────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

###############################################################################
# 1  LOAD DATA (from local file OR user upload) – cached
###############################################################################
@st.cache_data
def load_data(csv_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # --- OPTIONAL: rename for convenience ---
    df = df.rename(columns={
        "Minutes Streamed Per Day": "minutes",
        "Discover Weekly Engagement (%)": "discover_eng",
        "Repeat Song Rate (%)": "repeat_rate",
        "Listening Time (Morning/Afternoon/Night)": "listen_time",
        "Top Genre": "genre",
        "Age": "age",
        "Country": "country",
        "Subscription Type": "sub_type",
    })
    return df

DEFAULT_CSV = Path("Global_Music_Streaming_Listener_Preferences.csv")
if DEFAULT_CSV.exists():
    df = load_data(DEFAULT_CSV)
else:
    st.sidebar.warning("CSV file not found – please upload 👇")
    uploaded = st.sidebar.file_uploader("Upload CSV", type="csv")
    if uploaded:
        df = load_data(uploaded)
    else:
        st.stop()

###############################################################################
# 2  SIDEBAR – NAVIGATION
###############################################################################
st.sidebar.title("🎵 Streaming Analytics")
page = st.sidebar.radio(
    "Select a view",
    [
        "Dataset overview",
        "Daily listening time",
        "Discover Weekly engagement",
        "Age vs. listening time",
        "Genres by country",
        "Genres by time-of-day",
    ],
)

###############################################################################
# 3  MAIN PAGES & PLOTS
###############################################################################
sns.set_style("whitegrid")

def show_df_overview():
    st.header("👀 Quick preview of the dataset")
    st.dataframe(df.head())
    st.subheader("Summary statistics")
    st.write(df.describe())

def hist_minutes():
    st.header("⏰ Distribution of daily listening time")
    fig, ax = plt.subplots()
    sns.histplot(df["minutes"], bins=30, kde=True, color="#88C0D0", ax=ax)
    ax.set_xlabel("Minutes per day")
    ax.set_ylabel("Users")
    st.pyplot(fig)

def hist_discover():
    st.header("⭐ Distribution of Discover Weekly engagement (%)")
    fig, ax = plt.subplots()
    sns.histplot(df["discover_eng"], bins=25, kde=True, color="#F4A261", ax=ax)
    ax.set_xlabel("Engagement (%)")
    ax.set_ylabel("Users")
    st.pyplot(fig)

def scatter_age_minutes():
    st.header("📈 Daily listening time by age")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="age", y="minutes", alpha=0.3, s=40, ax=ax)
    sns.regplot(data=df, x="age", y="minutes", scatter=False, color="red", ax=ax)
    ax.set_xlabel("Age")
    ax.set_ylabel("Minutes per day")
    st.pyplot(fig)

def genres_by_country():
    st.header("🌍 Top genres across countries")
    # optional: select specific countries
    countries = st.multiselect(
        "Filter countries (leave empty = all)",
        sorted(df["country"].unique()),
    )
    data = df if not countries else df[df["country"].isin(countries)]
    counts = (
        data.groupby(["genre", "country"])
        .size()
        .reset_index(name="users")
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=counts,
        x="genre", y="users", hue="country", ax=ax
    )
    ax.set_xlabel("Genre")
    ax.set_ylabel("Users")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.legend(title="Country", bbox_to_anchor=(1.02, 1), loc="upper left")
    st.pyplot(fig)

def genres_by_time():
    st.header("⏰ Preferred genres by time-of-day")
    counts = (
        df.groupby(["genre", "listen_time"])
          .size()
          .reset_index(name="users")
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=counts,
        x="genre", y="users", hue="listen_time", ax=ax
    )
    ax.set_xlabel("Genre")
    ax.set_ylabel("Users")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.legend(title="Time of day", bbox_to_anchor=(1.02, 1), loc="upper left")
    st.pyplot(fig)

# page router
PAGE_FUNCS = {
    "Dataset overview": show_df_overview,
    "Daily listening time": hist_minutes,
    "Discover Weekly engagement": hist_discover,
    "Age vs. listening time": scatter_age_minutes,
    "Genres by country": genres_by_country,
    "Genres by time-of-day": genres_by_time,
}
PAGE_FUNCS[page]()

###############################################################################
# 4  FOOTER
###############################################################################
st.markdown("---")
st.caption("Built with ♥ using Streamlit • Data: Global Music Streaming Listener Preferences")

