### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 2

# Step 2: Creating Fictional Geographic Coordinates for Walmart Stores
# This step creates realistic lat/lng coordinates across the US for demonstration

import pandas as pd
import numpy as np
import random

# Set seed for reproducible results
# This ensures we get the same "random" coordinates each time we run the program
np.random.seed(42)
random.seed(42)

print("=== STEP 2: CREATING FICTIONAL STORE COORDINATES ===")

# Load the Walmart sales data (fixed to use read_csv)
# Since we're running from the data folder, the CSV is in the same directory
print("Loading Walmart sales data...")
df = pd.read_csv("Walmart_sales.csv")

# Get unique store IDs from our dataset
unique_stores = df['Store'].unique()
print(f"Found {len(unique_stores)} unique stores: {sorted(unique_stores)}")

# US Geographic Boundaries (approximate)
# These coordinates cover the continental United States
US_LAT_MIN, US_LAT_MAX = 25.0, 49.0  # Southern border to Northern border
US_LON_MIN, US_LON_MAX = -125.0, -66.0  # West coast to East coast

print(f"\nGenerating coordinates within US bounds:")
print(f"Latitude: {US_LAT_MIN}° to {US_LAT_MAX}°")
print(f"Longitude: {US_LON_MIN}° to {US_LON_MAX}°")

# Create a list to store our store location data
store_locations = []

# Generate fictional coordinates for each store
for store_id in unique_stores:
    # Generate random latitude and longitude within US bounds
    lat = np.random.uniform(US_LAT_MIN, US_LAT_MAX)
    lon = np.random.uniform(US_LON_MIN, US_LON_MAX)

    # Create fictional state abbreviations (for demonstration)
    # In reality, you'd determine state based on coordinates
    states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
              'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI']
    state = random.choice(states)

    # Add store location to our list
    store_locations.append({
        'Store': store_id,
        'Latitude': round(lat, 4),  # Round to 4 decimal places for cleaner display
        'Longitude': round(lon, 4),
        'State': state
    })

# Convert to DataFrame
store_coords_df = pd.DataFrame(store_locations)

print(f"\nGenerated coordinates for {len(store_coords_df)} stores:")
print(store_coords_df.head(10))

# Save the store coordinates to a file for future use
# This way we don't have to regenerate them each time
store_coords_df.to_csv('store_coordinates.csv', index=False)
print(f"\nSaved store coordinates to 'store_coordinates.csv'")

# Merge the coordinates with our original sales data
# This combines the sales data with the geographic information
print("\nMerging sales data with store coordinates...")
df_with_coords = df.merge(store_coords_df, on='Store', how='left')

print(f"Original dataset shape: {df.shape}")
print(f"Dataset with coordinates shape: {df_with_coords.shape}")
print(f"New columns added: {list(set(df_with_coords.columns) - set(df.columns))}")

# Display sample of merged data
print("\nSample of merged data (sales + coordinates):")
print(df_with_coords[['Store', 'Date', 'Weekly_Sales', 'Latitude', 'Longitude', 'State']].head())

# Quick statistics about our fictional store distribution
print(f"\n=== FICTIONAL STORE DISTRIBUTION ===")
print("Stores per state:")
print(store_coords_df['State'].value_counts().head(10))

print(f"\nLatitude range: {store_coords_df['Latitude'].min():.2f}° to {store_coords_df['Latitude'].max():.2f}°")
print(f"Longitude range: {store_coords_df['Longitude'].min():.2f}° to {store_coords_df['Longitude'].max():.2f}°")

print("\n=== STEP 2 COMPLETE ===")
print("Next step: Create our first map visualization!")

# Return the merged dataframe for the next step
# This makes the data available for mapping
print(f"\nDataset ready for mapping with {len(df_with_coords)} rows of sales data")
print(f"Each row now includes store coordinates for mapping")
