# 🌤️ Real-Time Weather Data Pipeline

> An automated ETL pipeline that collects, processes, and visualizes weather data from multiple US cities using Python, PostgreSQL, and Streamlit.

[![Live Dashboard](https://img.shields.io/badge/Dashboard-Live-success)](https://weather-data-pipeline-uzmdkxjdbwy7qbftp2hc3p.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/yashmundhe/weather-data-pipeline)

[**🚀 View Live Dashboard**](https://weather-data-pipeline-uzmdkxjdbwy7qbftp2hc3p.streamlit.app)

---

## 📊 Project Overview

This project demonstrates a production-grade data engineering solution that:
- Automatically collects real-time weather data from OpenWeatherMap API
- Processes and validates data using Python and Pandas
- Stores structured data in PostgreSQL database (local + cloud)
- Schedules automated data collection via cron jobs
- Visualizes insights through an interactive Streamlit dashboard

**Key Metrics:**
- 10 cities tracked across the United States
- Automated hourly data collection
- 240+ data points collected daily
- Multi-page interactive dashboard with geographic visualization

---

## 🏗️ Architecture
```
┌─────────────────┐
│ OpenWeatherMap  │
│      API        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Extract.py     │ ← Cron Job (Hourly)
│  (Python)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Transform      │
│  + Validate     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL     │
│  Database       │
│  (Railway)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Streamlit     │
│   Dashboard     │
│  (Cloud Hosted) │
└─────────────────┘
```

---

## 🛠️ Tech Stack

**Languages & Frameworks:**
- Python 3.11+
- SQL

**Data Processing:**
- Pandas - Data manipulation and transformation
- SQLAlchemy - Database ORM
- Requests - API integration

**Database:**
- PostgreSQL 14+ (Production)
- Railway - Cloud database hosting

**Visualization:**
- Streamlit - Interactive web dashboard
- Plotly - Dynamic charts and graphs

**Automation:**
- Cron - Scheduled task execution
- Unix shell scripts

**DevOps:**
- Git/GitHub - Version control
- Streamlit Cloud - Application deployment

---

## ✨ Features

### Data Pipeline
- **Automated Data Collection**: Hourly extraction from OpenWeatherMap API
- **Error Handling**: Retry logic with exponential backoff
- **Data Validation**: Quality checks for data integrity
- **Comprehensive Logging**: Detailed logs for monitoring and debugging
- **Scalable Architecture**: Modular design for easy extension

### Dashboard
- **Multi-Page Interface**: Overview, Map View, Comparisons, and Data Table
- **Interactive Filters**: Select specific cities to analyze
- **Real-Time Metrics**: Current temperature, humidity, and weather conditions
- **Geographic Visualization**: Interactive map showing city locations
- **Comparative Analysis**: Temperature ranges, humidity levels, and wind speeds
- **Data Export**: Download processed data as CSV

### Database
- **Star Schema Design**: Optimized for analytical queries
- **Dimension Table**: Cities with geographic coordinates
- **Fact Table**: Weather measurements with timestamps
- **Cloud Hosted**: Accessible from anywhere via Railway

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 14+
- OpenWeatherMap API key (free tier)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yashmundhe/weather-data-pipeline.git
cd weather-data-pipeline
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Create database tables**
```bash
python3 src/models.py
```

6. **Run the pipeline**
```bash
python3 src/extract.py
```

7. **Launch dashboard**
```bash
streamlit run dashboard.py
```

---

## 📁 Project Structure
```
weather-data-pipeline/
├── src/
│   ├── extract.py          # API data extraction
│   ├── load.py             # Database loading
│   ├── models.py           # SQLAlchemy database models
│   ├── config.py           # Configuration settings
│   ├── logger.py           # Logging setup
│   └── utils.py            # Utility functions
├── data/                   # Local data storage
├── logs/                   # Application logs
├── dashboard.py            # Streamlit dashboard
├── run_pipeline.sh         # Automation script
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

---

## 🔧 Configuration

### API Configuration
Get your free API key from [OpenWeatherMap](https://openweathermap.org/api)

### Database Configuration
The project supports both local and cloud PostgreSQL:
- **Local**: Standard PostgreSQL installation
- **Cloud**: Railway (free tier available)

### Cities Tracked
- Boston, MA
- New York, NY
- San Francisco, CA
- Chicago, IL
- Seattle, WA
- Miami, FL
- Los Angeles, CA
- San Diego, CA
- Denver, CO
- Austin, TX
- Atlanta, GA

---

## 🤖 Automation

The pipeline runs automatically every hour via cron:
```bash
# View cron schedule
crontab -l

# Pipeline runs at the start of every hour
0 * * * * /path/to/run_pipeline.sh
```

---

## 📈 Key Insights

The dashboard provides:
- **Temperature Analysis**: Compare temperatures across multiple cities
- **Weather Patterns**: Distribution of weather conditions
- **Humidity Trends**: Track moisture levels
- **Wind Analysis**: Compare wind speeds across locations
- **Geographic View**: Interactive map with temperature overlays

---

## 💡 Challenges & Solutions

**Challenge 1: API Rate Limiting**
- Implemented exponential backoff and request delays
- Added error handling with configurable retry logic

**Challenge 2: Database Schema Design**
- Designed star schema with dimension and fact tables
- Optimized for analytical queries with proper indexing

**Challenge 3: Cloud Deployment**
- Configured environment-specific database connections
- Used Streamlit secrets management for secure credential storage

---

## 🔮 Future Enhancements

- [ ] Add weather forecasting with ML models
- [ ] Implement real-time alerting for severe weather
- [ ] Expand to international cities
- [ ] Add historical trend analysis (6+ months)
- [ ] Integrate additional data sources (air quality, UV index)
- [ ] Create mobile-responsive design
- [ ] Add Apache Airflow for advanced workflow management

---

## 👨‍💻 Author

**Yash Mundhe**
- MS Data Science @ Northeastern University
- LinkedIn: [Connect with me](https://www.linkedin.com/in/yash-mundhe-30189819a/)
- Email: yashmundhe01@gmail.com
- Portfolio: [GitHub](https://github.com/yashmundhe)

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- OpenWeatherMap for providing weather data API
- Streamlit for the amazing dashboard framework
- Railway for cloud PostgreSQL hosting

---

⭐ **If you found this project helpful, please star the repository!**
<img width="1470" height="956" alt="Screenshot 2025-10-15 at 12 44 52 PM" src="https://github.com/user-attachments/assets/acab3f4f-8c29-4074-bb0f-e07784667d1f" />
<img width="1470" height="956" alt="Screenshot 2025-10-15 at 12 45 15 PM" src="https://github.com/user-attachments/assets/2bbac1c0-90be-4761-9cdf-1fd70a8eb573" />
<img width="1470" height="956" alt="Screenshot 2025-10-15 at 12 45 27 PM" src="https://github.com/user-attachments/assets/d35cd0ff-60ea-47dc-bb23-29e0b0d03867" />
<img width="1470" height="956" alt="Screenshot 2025-10-15 at 12 45 32 PM" src="https://github.com/user-attachments/assets/0d3c96f4-b26e-41d5-9b31-5ce33001d403" />
