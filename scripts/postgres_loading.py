from sqlalchemy import create_engine


def table_creating():
    TABLE_NAME = "district_weather_hourly"
    SCHEMA_NAME = "public"

    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "ap_weather"
    engine = None

    try:
        engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        print("Engine Created Successfully..")
    except:
        print("There is a problem with creating the engine..")

    create_table_sql = f"""CREATE TABLE IF NOT EXISTS public.district_weather_hourly (
                                    id SERIAL PRIMARY KEY,
                                    district TEXT,
                                    latitude FLOAT,
                                    longitude FLOAT,
                                    temperature FLOAT,
                                    humidity FLOAT,
                                    windspeed FLOAT,
                                    recorded_at TIMESTAMP
                        """
    try:
        with engine.begin() as conn:
            print("Postgres connected successfully")
            conn.execute(text(create_table_sql))
            print("Table created Successfully..")
    except:
        print("There was a problem with creating table..")

    return engine

def loading(final_df):
    engine = table_creating()
    
    final_df.to_sql(
        "district_weather_hourly",
        engine,
        if_exists="append",
        index=False
    )
    return 'Loading success.'
def main():
    pass


if __name__ == "__main__":
    main()

    
