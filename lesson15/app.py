

import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("weather_tokyo_data.csv")

# Clean columns
df.columns = df.columns.str.strip().str.lower()

# Create date
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['day'])

# Clean temperature
df['temperature'] = df['temperature'].astype(str)\
    .str.replace('(', '')\
    .str.replace(')', '')\
    .str.strip()\
    .astype(float)

# -------------------------------
# 1. Temperature Overview
# -------------------------------
avg_temp = df['temperature'].mean()
print(f"Average Temperature: {avg_temp:.2f}°C")

# -------------------------------
# 2. Monthly Average Temperature (GRAPH 1)
# -------------------------------
df['month'] = df['date'].dt.month
monthly_avg = df.groupby('month')['temperature'].mean()

plt.figure(figsize=(8,5))
monthly_avg.plot(kind='bar', color='skyblue')
plt.title("Monthly Average Temperature")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.show()

# -------------------------------
# 3. Temperature Over Time (GRAPH 2)
# -------------------------------
plt.figure(figsize=(10,5))
plt.plot(df['date'], df['temperature'], marker='o')
plt.title("Temperature Over Time")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------
# 4. Seasonal Line Graph (GRAPH 3)
# -------------------------------
def get_season(month):
    if month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'
    else:
        return 'Winter'

df['season'] = df['month'].apply(get_season)

seasonal_avg = df.groupby('season')['temperature'].mean()

# vendos rendin korrekt
season_order = ['Spring', 'Summer', 'Autumn', 'Winter']
seasonal_avg = seasonal_avg.reindex(season_order)

plt.figure(figsize=(8,5))
plt.plot(seasonal_avg.index, seasonal_avg.values, marker='o', color='orange')
plt.title("Seasonal Average Temperature")
plt.xlabel("Season")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.tight_layout()
plt.show()