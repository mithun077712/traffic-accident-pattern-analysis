import sys
print("Python executable:", sys.executable)
print("Python sys.path:", sys.path)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    import folium
    from folium.plugins import MarkerCluster
    folium_installed = True
except ImportError:
    folium_installed = False

df = pd.read_csv(r'C:\Users\DELL\Downloads\US_Accidents_March23.csv\US_Accidents_March23.csv')

print("Shape:", df.shape)
print("Columns:", df.columns)
print(df.head())

df.dropna(subset=['Start_Time', 'Start_Lat', 'Start_Lng', 'Weather_Condition'], inplace=True)


df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')


df = df.dropna(subset=['Start_Time'])


df['Hour'] = df['Start_Time'].dt.hour
df['Weekday'] = df['Start_Time'].dt.day_name()
df['Month'] = df['Start_Time'].dt.month_name()

plt.figure(figsize=(10, 4))
sns.countplot(data=df, x='Hour', palette='viridis')
plt.title('Accidents by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Number of Accidents')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))
df['Weather_Condition'].value_counts().head(10).plot(kind='bar')
plt.title('Top 10 Weather Conditions During Accidents')
plt.xlabel('Weather Condition')
plt.ylabel('Accident Count')
plt.tight_layout()
plt.show()


plt.figure(figsize=(7, 4))
sns.countplot(x='Severity', data=df, palette='Reds')
plt.title('Accident Severity Distribution')
plt.tight_layout()
plt.show()

if 'Surface_Condition' in df.columns:
    plt.figure(figsize=(7, 4))
    df['Surface_Condition'].value_counts().plot(kind='bar')
    plt.title('Accidents by Road Surface Condition')
    plt.xlabel('Surface Condition')
    plt.ylabel('Accident Count')
    plt.tight_layout()
    plt.show()

top_weather = df['Weather_Condition'].value_counts().head(5).index
plt.figure(figsize=(10, 5))
sns.boxplot(x="Weather_Condition", y="Severity", data=df[df['Weather_Condition'].isin(top_weather)])
plt.title('Severity by Weather Condition (Top 5)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


if folium_installed:
    map_center = [df['Start_Lat'].mean(), df['Start_Lng'].mean()]
    accident_map = folium.Map(location=map_center, zoom_start=5)
    marker_cluster = MarkerCluster().add_to(accident_map)
    for idx, row in df[['Start_Lat', 'Start_Lng']].dropna().head(1000).iterrows():
        folium.Marker(location=[row['Start_Lat'], row['Start_Lng']]).add_to(marker_cluster)
    accident_map.save('accident_hotspots.html')
    print("Accident hotspot map saved as accident_hotspots.html")
else:
    print("Folium not installed, skipping map. Run: pip install folium to enable mapping.")

