from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
Base = declarative_base()

class City(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(100), unique=True, nullable=False)
    country = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('cities.city_id'), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)
    temperature = Column(Float)
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    weather_main = Column(String(50))
    weather_description = Column(String(100))
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    cloudiness = Column(Float)
    visibility = Column(Integer)

def get_database_url():
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    database = os.getenv('DB_NAME', 'weather_pipeline')
    user = os.getenv('DB_USER', 'weather_user')
    password = os.getenv('DB_PASSWORD', 'weather123')
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def create_tables():
    engine = create_engine(get_database_url())
    Base.metadata.create_all(engine)
    print("✓ Tables created!")
    return engine

if __name__ == "__main__":
    print("Creating tables...")
    create_tables()