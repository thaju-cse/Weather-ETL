import folium

def visual(final_df):
    m = folium.Map(location=[16.5, 80.5], zoom_start=7)
    OUTPUT_DIR = "edit the location\\ap_district_wise_weather\\output\\ap_weather_map.html"

    for _, row in final_df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=8,
            popup=(
                f"{row['district']}<br>"
                f"Temp: {row['temperature']}°C<br>"
                f"Humidity: {row['humidity']}%"
            ),
            fill=True
        ).add_to(m)

    m.save(OUTPUT_DIR)
    return 'Visualizing success.'

def main():
    pass

if __name__ == "__main__":
    main()

