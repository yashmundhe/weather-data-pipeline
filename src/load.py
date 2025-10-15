from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import City, WeatherData, get_database_url
from logger import setup_logger
import pandas as pd

logger = setup_logger()


class DataLoader:
    """Handles loading data into the database"""
    
    def __init__(self):
        """Initialize database connection"""
        self.engine = create_engine(get_database_url())
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_or_create_city(self, city_name, country, latitude, longitude):
        """Get existing city or create new one"""
        city = self.session.query(City).filter_by(city_name=city_name).first()
        
        if city:
            logger.debug(f"City {city_name} already exists (ID: {city.city_id})")
            return city.city_id
        else:
            new_city = City(
                city_name=city_name,
                country=country,
                latitude=latitude,
                longitude=longitude
            )
            self.session.add(new_city)
            self.session.commit()
            logger.info(f"Created new city: {city_name} (ID: {new_city.city_id})")
            return new_city.city_id
    
    def load_weather_record(self, weather_data):
        """Load a single weather record into the database"""
        try:
            city_id = self.get_or_create_city(
                city_name=weather_data['city'],
                country=weather_data['country'],
                latitude=weather_data['latitude'],
                longitude=weather_data['longitude']
            )
            
            weather_record = WeatherData(
                city_id=city_id,
                timestamp=weather_data['timestamp'],
                temperature=weather_data['temperature'],
                feels_like=weather_data['feels_like'],
                temp_min=weather_data['temp_min'],
                temp_max=weather_data['temp_max'],
                humidity=weather_data['humidity'],
                pressure=weather_data['pressure'],
                weather_main=weather_data['weather_main'],
                weather_description=weather_data['weather_description'],
                wind_speed=weather_data['wind_speed'],
                wind_direction=weather_data['wind_direction'],
                cloudiness=weather_data['cloudiness'],
                visibility=weather_data['visibility']
            )
            
            self.session.add(weather_record)
            self.session.commit()
            logger.info(f"✓ Loaded weather data for {weather_data['city']}")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"✗ Failed to load data for {weather_data['city']}: {str(e)}")
            raise
    
    def load_weather_dataframe(self, df):
        """Load multiple weather records from a DataFrame"""
        logger.info(f"Loading {len(df)} weather records to database...")
        
        success_count = 0
        error_count = 0
        
        for _, row in df.iterrows():
            try:
                self.load_weather_record(row.to_dict())
                success_count += 1
            except Exception as e:
                error_count += 1
                logger.error(f"Error loading record: {str(e)}")
        
        logger.info(f"Loading complete: {success_count} successful, {error_count} failed")
        return success_count, error_count
    
    def close(self):
        """Close database session"""
        self.session.close()
