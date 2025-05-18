import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

################################################################################
# 1.  🗄️  LOAD & CACHE DATA
################################################################################
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # -- OPTIONAL: rename to canonical column names ---------------------------
    df = df.rename(columns={
        'Age': 'age',
        'Minutes Streamed Per Day': 'minutes_per_day',
        'Discover Weekly Engagement (%)': 'discover_engagement',
        'Top Genre': 'top_genre',
        'Listening Time': 'listening_time'          # Morning / Afternoon / Night
    })  # ### ← EDIT HERE if needed
    return df

df = load_data("Global_Music_Streaming_Listener_Preferences.csv")

################################################################################
# 2.  🎛️  SIDEBAR – NAVIGATION
################################################################################
st.sidebar.title("🎵 Global Streaming Analysis")
page = st.sidebar.radio(
    "Choose a view",
    ("Dataset overview",
     "Histogram – Daily streaming time",
     "Histogram – Discover Weekly engagement",
     "Scatter – Age vs. streaming minutes",
     "Top genres by listening time")
)

################################################################################
# 3.  📊  PLOTS & CONTENT
################################################################################
sns.set_style("whitegrid")
if page == "Dataset overview":
    st.header("👀 Quick look at the data")
    st.dataframe(df.head())
    st.subheader("Descriptive statistics")
    st.write(df.describe())

elif page == "Histogram – Daily streaming time":
    st.header("⏰ Distribution of daily streaming time (minutes)")
    fig, ax = plt.subplots()
    sns.histplot(df["minutes_per_day"], bins=30, kde=True, color="#89C2D9", ax=ax)
    ax.set_xlabel("Minutes Streamed Per Day")
    ax.set_ylabel("Number of Users")
    st.pyplot(fig)

elif page == "Histogram – Discover Weekly engagement":
    st.header("⭐ Distribution of Discover Weekly engagement (%)")
    fig, ax = plt.subplots()
    sns.histplot(df["discover_engagement"], bins=25, kde=True, color="#F4A259", ax=ax)
    ax.set_xlabel("Engagement (%)")
    ax.set_ylabel("Number of Users")
    st.pyplot(fig)

elif page == "Scatter – Age vs. streaming minutes":
    st.header("📈 Daily streaming time by age")
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=df,
        x="age", y="minutes_per_day",
        alpha=0.3, s=40, color="#2A9D8F", ax=ax
    )
    # low-order regression trend-line
    sns.regplot(
        data=df, x="age", y="minutes_per_day",
        scatter=False, color="red", ax=ax
    )
    ax.set_xlabel("Age")
    ax.set_ylabel("Minutes Streamed Per Day")
    st.pyplot(fig)

elif page == "Top genres by listening time":
    st.header("🎤 Top genres split by preferred listening time")
    # create crosstab for stacked/clustered bar
    counts = (
        df.groupby(["top_genre", "listening_time"])
          .size()
          .reset_index(name="users")
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=counts,
        x="top_genre", y="users", hue="listening_time",
        ax=ax
    )
    ax.set_xlabel("Top Genre")
    ax.set_ylabel("Number of Users")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.legend(title="Listening Time")
    st.pyplot(fig)

################################################################################
# 4.  👣  FOOTER
################################################################################
st.markdown("---")
st.caption("Built with ❤️ & Streamlit • Data: Global Music Streaming Listener Preferences")
