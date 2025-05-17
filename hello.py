from preswald import connect, get_df, text, table, plotly
import plotly.express as px
import pandas as pd

# Connect to Preswald data sources
connect()

# UI headers
text("# 🎧 Spotify Streaming Trend Explorer")
text("This app reveals the top trending songs by computing a velocity score (Daily ÷ Total Streams).")

# Load dataset
text("Attempting to load dataset...")
df = pd.read_csv("data/Spotify.csv")
text(f"✅ Dataset loaded with {df.shape[0]} rows and columns: {df.columns.tolist()}")

# Clean and process columns
df["Streams"] = df["Streams"].str.replace(",", "", regex=False).astype(float)
df["Daily"] = df["Daily"].astype(str).str.replace(",", "", regex=False).astype(float)

# Split Artist and Title
split_cols = df["Artist and Title"].str.split(" - ", n=1, expand=True)
df["Artist"] = split_cols[0]
df["Title"] = split_cols[1].fillna("Unknown")

# Calculate velocity
df["Velocity"] = df["Daily"] / df["Streams"]

# Select top 10 trending songs
filtered_df = df.sort_values("Velocity", ascending=False).head(10)

### Visualizations
# Show table
table(filtered_df[["Artist", "Title", "Streams", "Daily", "Velocity"]], title="Top 10 Trending Songs")

# Create and display plot
# Filter out rows with invalid or zero velocity
df_plot = df[df["Velocity"].notna() & (df["Velocity"] > 0)]

text(f"📊 Scatter plot using {df_plot.shape[0]} rows.")

fig = px.scatter(
    df_plot, x="Streams", y="Daily", color="Velocity",
    hover_data=["Artist", "Title", "Streams", "Daily", "Velocity"],
    title="Daily vs Total Streams (Colored by Velocity)",
    labels={"Streams": "Total Streams", "Daily": "Daily Streams"},
    size="Velocity",
    size_max=20
)

plotly(fig)

# Top 15 Songs by Daily Streams
top_daily = df_plot.sort_values("Daily", ascending=False).head(15)
fig_top_daily = px.bar(
    top_daily, x="Daily", y="Title", orientation="h", color="Velocity",
    title="Top 15 Songs by Daily Streams",
    labels={"Daily": "Daily Streams"}
)
plotly(fig_top_daily)
text("## 🔥 Top 15 Songs by Daily Streams")
text("""
This chart shows the 15 most-played songs **today**, based on their average daily stream count.
- **'Seven'** leads by a large margin with over 9 million daily streams, signaling massive current popularity.
- Tracks like **'Cruel Summer'**, **'Daylight'**, and **'Like Crazy'** are also showing strong daily numbers.
- High Velocity colors (yellow) show these songs are not only popular now but trending fast compared to their historical total streams.
""")

# Top 15 Songs by Velocity (Trending Fastest)
top_velocity = df_plot.sort_values("Velocity", ascending=False).head(15)
fig_top_velocity = px.bar(
    top_velocity, x="Velocity", y="Title", orientation="h", color="Streams",
    title="Top 15 Trending Songs (Highest Velocity)",
    labels={"Velocity": "Daily ÷ Total Streams"}
)
plotly(fig_top_velocity)
text("## 🚀 Top 15 Trending Songs by Velocity")
text("""
This chart ranks songs by **velocity**, defined as `Daily ÷ Total Streams`. It highlights tracks that are **gaining popularity rapidly**, even if they're not the most played historically.
- **'Seven'**, again, stands out with the highest velocity, showing it's both new and exploding in popularity.
- Other high-velocity tracks like **'WHERE SHE GOES'**, **'Classy 101'**, and **'Like Crazy'** are showing rapid adoption.
- Songs with lower total streams but high velocity are **rising stars**, poised for viral growth.
""")


# Most Streamed Artists (Aggregate Streams)
artist_agg = df.groupby("Artist", as_index=False)["Streams"].sum().sort_values("Streams", ascending=False).head(10)
fig_artist = px.bar(
    artist_agg, x="Streams", y="Artist", orientation="h", color="Streams",
    title="Top 10 Artists by Total Streams"
)
plotly(fig_artist)
text("## 🎤 Top 10 Artists by Total Streams")
text("""
This chart highlights the artists with the **highest cumulative stream counts** across all their tracks in the dataset.

- **Drake** leads with nearly 30 billion total streams, reflecting consistent long-term dominance in global music consumption.
- Other major artists like **The Weeknd**, **Ed Sheeran**, and **Bad Bunny** follow closely behind, each with 28B–29B streams.
- **Taylor Swift** and **Post Malone** hold strong middle positions, showing both legacy catalog and recent hits contribute significantly.
- The presence of **Billie Eilish**, **Ariana Grande**, and **Maroon 5** shows diversity in genre and era, indicating broad listener appeal.

These numbers reflect **lifetime success** — not necessarily what's trending right now — and offer insight into which artists have built the most enduring listenership on Spotify.
""")


