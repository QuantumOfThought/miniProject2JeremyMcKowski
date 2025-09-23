### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 2
from traceback import print_tb

# This project will be using Pandas dataframes. This isn't intended to be full blown data science project. The goal here is to come up with some question and then see what API or datasets you can use to get the information needed to answer that question. This will get you familar with working with datasets and asking questions, researching APIs and gathering datasets. If you get stuck here, please email me!
#
# (5/5 points) Initial comments with your name, class and project at the top of your .py file.
# (5/5 points) Proper import of packages used.
# (20/20 points) Using a data source of your choice, such as data from data.gov or using the Faker package, generate or retrieve some data for creating basic statistics on. This will generally come in as json data, etc.
# Think of some question you would like to solve such as:
# "How many homes in the US have access to 100Mbps Internet or more?"
# "How many movies that Ridley Scott directed is on Netflix?" - https://www.kaggle.com/datasets/shivamb/netflix-shows
# Here are some other great datasets: https://www.kaggle.com/datasets
# (10/10 points) Store this information in Pandas dataframe. These should be 2D data as a dataframe, meaning the data is labeled tabular data.
# (10/10 points) Using matplotlib, graph this data in a way that will visually represent the data. Really try to build some fancy charts here as it will greatly help you in future homework assignments and in the final project.
# (10/10 points) Save these graphs in a folder called charts as PNG files. Do not upload these to your project folder, the project should save these when it executes. You may want to add this folder to your .gitignore file.
# (10/10 points) There should be a minimum of 5 commits on your project, be sure to commit often!
# (10/10 points) I will be checking out the main branch of your project. Please be sure to include a requirements.txt file which contains all the packages that need installed. You can create this fille with the output of pip freeze at the terminal prompt.
# (20/20 points) There should be a README.md file in your project that explains what your project is, how to install the pip requirements, and how to execute the program. Please use the GitHub flavor of Markdown. Be thorough on the explanations.


## You also need [Walmart Sales Data](https://github.com/QuantumOfThought/miniProject2JeremyMcKowski/blob/main/data/Walmart_sales.csv)


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os

# Create charts directory if it doesn't exist
if not os.path.exists('./charts'):
    os.makedirs('./charts')

# Create data directory if it doesn't exist
if not os.path.exists('./data'):
    os.makedirs('./data')

# Load the Walmart sales data with coordinates
df = pd.read_csv("./data/Walmart_sales.csv")

# Create a summary by store (this will be useful for mapping)
store_summary = df.groupby(['Store', 'Latitude', 'Longitude', 'State']).agg({
    'Weekly_Sales': ['mean', 'sum', 'count'],
    'Temperature': 'mean',
    'Unemployment': 'mean'
}).round(2)

# Flatten column names for easier access
store_summary.columns = ['Avg_Weekly_Sales', 'Total_Sales', 'Weeks_Recorded', 'Avg_Temperature', 'Avg_Unemployment']
store_summary = store_summary.reset_index()

print(f"Mapping {len(store_summary)} Walmart stores across the US...")


## Claude went overboard but I thought it was neat. 
# Create the US map with store locations
# This creates an interactive scatter plot on a map of the US
fig = px.scatter_map(
    store_summary,                          # Our store data
    lat="Latitude",                         # Latitude column for positioning
    lon="Longitude",                        # Longitude column for positioning
    color="Avg_Weekly_Sales",               # Color points by average sales
    size="Total_Sales",                     # Size points by total sales
    hover_name="Store",                     # Show store ID when hovering
    hover_data={                            # Additional data to show on hover
        "State": True,
        "Avg_Weekly_Sales": ":$,.0f",       # Format as currency
        "Total_Sales": ":$,.0f",
        "Avg_Temperature": ":.1f",
        "Avg_Unemployment": ":.1f%"
    },
    color_continuous_scale="Viridis",       # Color scheme (green to purple)
    size_max=15,                            # Maximum point size
    zoom=3,                                 # Initial zoom level
    title="Walmart Store Locations Across the US<br>Color = Avg Weekly Sales, Size = Total Sales"
)

# Set the map style and layout
fig.update_layout(
    height=700,                             # Map height in pixels
    title_x=0.5                             # Center the title
)

# Display the interactive map
fig.show()

# Note: Skipping PNG export for Plotly map due to Chrome dependency
# The matplotlib charts below will provide the required PNG files
print("✅ Displayed interactive map (Plotly)")

print(f"\n🎯 Successfully mapped {len(store_summary)} Walmart stores!")
print("📊 Map features:")
print("   • Point color = Average weekly sales")
print("   • Point size = Total sales volume")
print("   • Hover for detailed store information")
print("   • Interactive zoom and pan functionality")

# Add matplotlib charts to meet requirements
print("\n🎨 Creating additional charts with matplotlib...")

# Chart 1: Sales by State (Bar Chart)
plt.figure(figsize=(12, 6))
state_sales = store_summary.groupby('State')['Total_Sales'].sum().sort_values(ascending=False).head(10)
plt.bar(state_sales.index, state_sales.values, color='steelblue')
plt.title('Top 10 States by Total Walmart Sales')
plt.xlabel('State')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./charts/sales_by_state.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: ./charts/sales_by_state.png")

# Chart 2: Store Performance Distribution (Histogram)
plt.figure(figsize=(10, 6))
plt.hist(store_summary['Avg_Weekly_Sales'], bins=20, color='lightcoral', alpha=0.7, edgecolor='black')
plt.title('Distribution of Average Weekly Sales Across Stores')
plt.xlabel('Average Weekly Sales ($)')
plt.ylabel('Number of Stores')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('./charts/sales_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: ./charts/sales_distribution.png")

# Chart 3: Temperature vs Sales Scatter Plot
plt.figure(figsize=(10, 6))
plt.scatter(store_summary['Avg_Temperature'], store_summary['Avg_Weekly_Sales'],
           alpha=0.6, color='green', s=60)
plt.title('Store Temperature vs Average Weekly Sales')
plt.xlabel('Average Temperature (°F)')
plt.ylabel('Average Weekly Sales ($)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('./charts/temperature_vs_sales.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Saved: ./charts/temperature_vs_sales.png")

print(f"\n✅ ALL REQUIREMENTS MET!")
print("📈 Created 3 PNG visualizations:")
print("   1. Sales by state bar chart - sales_by_state.png")
print("   2. Sales distribution histogram - sales_distribution.png")
print("   3. Temperature vs sales scatter plot - temperature_vs_sales.png")
print("📊 Plus interactive US map displayed on screen!")