import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import time
from config import CITIES, MAX_RETRIES,RETRY_DELAY,REQUEST_TIMEOUT
from logger import setup_logger
from torch.utils.data import DataLoader
from load import DataLoader
import inspect
print(f"DEBUG: DataLoader is from: {inspect.getfile(DataLoader)}")
print(f"DEBUG: DataLoader.__init__ signature: {inspect.signature(DataLoader.__init__)}")

#load environment variables
load_dotenv()
API_KEY=os.getenv('WEATHER_API_KEY')

#setup logger
logger = setup_logger()

class WeatherExtractor:
    """Class to handle weather data extraction"""

    def __init__(self,api_key):
        self.api_key=api_key
        self.base_url="http://api.openweathermap.org/data/2.5/weather"

    def fetch_weather_data(self,city,retry_count=0):
        """Fetch weather data from OpenWeatherMap API
        Args:
            city: City name
            retry_count: Current retry attempt number
        Returns:
            Dictionary with weather data or None if failed 
        """
        
        url = f"{self.base_url}?q={city}&appid={self.api_key}"

        try:
            logger.info(f'fetching weather for {city}...')

            response=requests.get(url,timeout=REQUEST_TIMEOUT)

            if response.status_code==200:
                data=response.json()

                #extract the important stuff
                weather={
                    'city': city,
                    'country': data['sys'].get('country','Unknown'),
                    'timestamp':datetime.now(),
                    'temperature':round(data['main']['temp']-273.15,2),
                    'feels_like':round(data['main']['feels_like']-273.15,2),
                    'temp_min':round(data['main']['temp_min']-273.15,2),
                    'temp_max':round(data['main']['temp_max']-273.15,2),
                    'humidity':data['main']['humidity'],
                    'pressure':data['main']['pressure'],
                    'weather_main':data['weather'][0]['main'],
                    'weather_description':data['weather'][0]['description'],
                    'wind_speed':data['wind'].get('speed',0),
                    'wind_direction':data['wind'].get('deg',0),
                    'cloudiness':data.get('clouds',{}).get('all',0),
                    'visibility':data.get('visibilty',0),
                    'latitude':data['coord']['lat'],
                    'longitude':data['coord']['lon']
                }
            
                logger.info(f'Success! {city}: {weather["temperature"]}°C, {weather['weather_description']}')
                return weather
            
            elif response.status_code==401:
                logger.error("Invalid API key!")
                return None
            
            elif response.status_code==404:
                logger.error(f"City not found: {city}")
                return None
        
            else:
                logger.warning(f'API returned status {response.status_code} for {city}')

                #retry logic
                if retry_count < MAX_RETRIES:
                    logger.info(f"Retrying {city} (attempt {retry_count+1}/{MAX_RETRIES})...")
                    time.sleep(RETRY_DELAY)
                    return self.fetch_wetaher_data(city, retry_count+1)
                else:
                    logger.error(f"Failed to fetch {city} after {MAX_RETRIES} attempts")
                    return None
                
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout for {city}")

            if retry_count < MAX_RETRIES:
                    logger.info(f"Retrying {city} (attempt {retry_count+1}/{MAX_RETRIES})...")
                    time.sleep(RETRY_DELAY)
                    return self.fetch_wetaher_data(city, retry_count+1)
            else:
                logger.error(f"Timeout on {city} after {MAX_RETRIES} attempts")
                return None
            
    def fetch_multiple_cities(self,cities):
        """
        Fetch weather data for multiple cities

        Args:
        Cities: List of city names

        Returns:
        Datframe with weather data
        """
        logger.info(f"Starting extraction for {len(cities)} cities")
        logger.info("="*60)

        all_weather=[]
        successful=0
        failed=0

        for city in cities:
            weather=self.fetch_weather_data(city)
            if weather:
                all_weather.append(weather)
                successful+=1
            else:
                failed+=1
            
            #small delay to avoid rate limiting
            time.sleep(0.5)

        logger.info("="*60)
        logger.info(f"Extraction complete for {successful}, {failed} failed")

        if all_weather:
            df=pd.DataFrame(all_weather)
            return df
        else:
            logger.error("No data extracted")
            return pd.DataFrame()    

def main():
    """Main function to run the extraction"""

    logger.info("Weather Data Pipeline - Extraction Started")
    logger.info(f"API Key: {'Found' if API_KEY else 'Missing'}")

    if not API_KEY:
        logger.error("No API key found! check your .env file")
        return
    
    #create extractor
    extractor=WeatherExtractor(API_KEY)

    #fetch data
    df = extractor.fetch_multiple_cities(CITIES)

    if not df.empty:
        #Display summary
        print("\n" + "="*80)
        print("Weather Data Summary")
        print("="*80)
        print(f"Total redords: {len(df)}")
        print(f"Cities: {', '.join(df['city'].tolist())}")
        print(f"Avg temperature: {df['temperature'].mean():.1f}°C")
        print(f"Min temperature: {df['temperature'].min():.1f}°C ({df.loc[df['temperature'].idxmin(),'city']})")
        print(f"Max temperature: {df['temperature'].max():.1f}°C")
        ({df.loc[df['temperature'].idxmax(),'city']})
        print("="*80)

        #Show first few rows
        print("\nFirst 5 records:")
        print(df[['city','temperature','humidity','weather_description']].head())
        
        #save to csv
        output_file=f"data/weather_{datetime.now().strftime('%Y%m%d_%H%m%s')}.csv"
        df.to_csv(output_file,index=False)
        logger.info("Data saved to data/weather_latest.csv")

        #load into the db
        print("\n" + "="*80)
        print("Loading Data into Database")
        print("="*80)

        try:
            loader=DataLoader()
            success, errors=loader.load_weather_dataframe(df)
            loader.close()
            print(f'Successfully loaded {success} records into the database!')
            if errors>0:
                print(f"{errors} recordsfailed to load")
        except Exception as e:
            logger.error(f"Failed to load data to database:{str(e)}")
            print(f"Database loading failed: {str(e)}")

    else:
        logger.error("No data to save!")

    logger.info("Pipeline completed!")

if __name__=="__main__":
    main()