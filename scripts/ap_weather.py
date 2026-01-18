import requests
import pandas as pd
from datetime import datetime
import weather_visual
import postgres_loading
import json

def fetch_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
        "&timezone=Asia/Kolkata"
    )
    file = requests.get(url).json()
    # filename = 'output.json'
    '''try:
        with open(filename, 'w') as json_file:
            json.dump(file, json_file, indent=4)
        print(f"Data successfully saved to {filename}")
    except IOError as e:
        print(f"Error saving file: {e}")'''
    return file

def build_dataframe(district, lat, lon, data):
    hourly = data["hourly"]
    df = pd.DataFrame({
        "district": district,
        "latitude": lat,
        "longitude": lon,
        "temperature": hourly["temperature_2m"],
        "humidity": hourly["relativehumidity_2m"],
        "windspeed": hourly["windspeed_10m"],
        "recorded_at": hourly["time"]
    })
    return df

def main():

    DISTRICTS_FILE = "E:\\projects\\ap_district_wise_weather\\data\\ap_districts.csv"

    districts = pd.read_csv(DISTRICTS_FILE)
    all_data = []

    for _, row in districts.iterrows():
        data = fetch_weather(row.latitude, row.longitude)
        hourly = data["hourly"]

        df = pd.DataFrame({
            "district": row.district,
            "latitude": row.latitude,
            "longitude": row.longitude,
            "temperature": hourly["temperature_2m"],
            "humidity": hourly["relativehumidity_2m"],
            "windspeed": hourly["windspeed_10m"],
            "recorded_at": hourly["time"]
        })

        # Take only current hour
        df["recorded_at"] = pd.to_datetime(df["recorded_at"])
        current_hour = df.iloc[-1:]
        all_data.append(current_hour)

    final_df = pd.concat(all_data)
    
    print(postgres_loading.loading(final_df))
    print(weather_visual.visual(final_df))
    

if __name__ == "__main__":
    main()

