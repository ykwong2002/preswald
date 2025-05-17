### Load dataset
from preswald import connect, get_df
import pandas as pd
connect() # Initialize connection to preswald.toml data sources
df = get_df("earthquakes")

### Query or manipulate data
from preswald import query
sql = "SELECT * FROM earthquakes WHERE Magnitude >= 6.5"
filtered_df = query(sql, "earthquakes")

### Build an interactive UI
from preswald import table, text
text("# 🌍 Global Earthquake Insights Dashboard")
text("This app filters for earthquakes with magnitude >= 6.5 and explores their depth, location and distribution over time.")
table(filtered_df, title="Major Earthquakes (Magnitude >= 6.5)")

### Visualizations
# Generated plot
from preswald import plotly
import plotly.express as px

fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', color='Magnitude',
                     hover_name='ID', hover_data=['Date', 'Type', 'Depth'],
                     color_continuous_scale=px.colors.sequential.Plasma,
                     title='Global Earthquake Distribution',
                     projection='natural earth')

fig.show()


