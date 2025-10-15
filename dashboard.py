import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

#page config
st.set_page_config(page_title="Weather Pipeline Dashboard", layout="wide", page_icon="🌤️")

#custom css
st.markdown("""
<style>
    .metric-card{
        background-color: #f0f2f6;
        padding: 20px;
        border-redius: 10px;
        text-align:center;
    }
    .stTabs[data-baseweb="tab-list"] {
        gap:24px;        
    }
    .stTabs[data-baseweb="Tab"]{
        padding: 10px 20px;        
    }
<style>
""", unsafe_allow_html=True)

#Database connection
@st.cache_resource
def get_connection():
    db_url="postgresql://weather_user:weather123@localhost:5432/weather_pipeline"
    return create_engine(db_url)

engine=get_connection()

#Load data
@st.cache_data
def load_data():
    query="""
    SELECT c.city_name, c.country, c.latitude, c.longitude,
           w.timestamp, w.temperature, w.feels_like, w.temp_min, w.temp_max,
           w.humidity, w.pressure, w.weather_main, w.weather_description,
           w.wind_speed, w.cloudiness, w.visibility
    FROM weather_data w
    JOIN cities c ON w.city_id = c.city_id
    ORDER BY w.timestamp DESC
    """

    return pd.read_sql(query, engine)

#Load the data
df=load_data()

#sidebar filters
st.sidebar.header("🎛️ Filters")

#city filters
all_cities=sorted(df['city_name'].unique())
selected_cities=st.sidebar.multiselect(
    "Select Cities",
    options=all_cities,
    default=all_cities
)

# Filter data
if selected_cities:
    filtered_df = df[df['city_name'].isin(selected_cities)]
else:
    filtered_df = df

# Refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Last Updated:**\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.sidebar.markdown(f"**Total Records:** {len(filtered_df)}")


#Title
st.title("🌤️ Real-Time Weather Data Pipeline Dashboard")
st.markdown("---")

#metric row
col1, col2, col3, col4=st.columns(4)

with col1:
    st.metric("Total Cities", df['city_name'].nunique())

with col2:
    st.metric("Avg Temperature",f"{df['temperature'].mean():.1f}°C")

with col3:
    hottest=df.loc[df['temperature'].idxmax()]
    st.metric("Hottest City", hottest['city_name'], f"{hottest['temperature']:.1f}°C")

with col4:
    coldest=df.loc[df['temperature'].idxmin()]
    st.metric("Coldest City", coldest['city_name'], f"{coldest['temperature']:.1f}°C")

st.markdown("---")

#Tabs for different views
tab1, tab2, tab3, tab4=st.tabs(["📊 Overview", "🗺️ Map View", "📈 Comparisons", "📋 Data Table"])
with tab1:
    #overview tab
    col1, col2=st.columns(2)

    with col1:
        st.subheader("🌡️ Temperature by City")
        
        city_temps = filtered_df.groupby('city_name')['temperature'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=city_temps.index,
            y=city_temps.values,
            labels={'x': 'City', 'y': 'Temperature (°C)'},
            color=city_temps.values,
            color_continuous_scale='RdYlBu_r',
            text=city_temps.values.round(1)
        )
        fig.update_traces(
            texttemplate='%{text}°C', 
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Temperature: %{y:.1f}°C<extra></extra>'  # Clean tooltip
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)


    with col2:
        st.subheader("☁️ Weather Conditions")
        
        weather_counts = filtered_df['weather_main'].value_counts()
        fig = px.pie(
            values=weather_counts.values,
            names=weather_counts.index,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'  # Clean tooltip
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

#weather conditions
st.subheader("☁️ Current Weather Conditions")

#get latest record for each city
latest_records=filtered_df.sort_values('timestamp', ascending=False).groupby('city_name').first().reset_index()

#create columns based on number of cities

num_cols=min(5, len(latest_records))
cols=st.columns(num_cols)

for idx, (_, row) in enumerate(df.head(5).iterrows()):
    with cols[idx%5]:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
            <h3>{row['city_name']}</h3>
            <h1>{row['temperature']:.1f}°C</h1>
            <p>{row['weather_description'].title()}</p>
            <p>💨 {row['wind_speed']:.1f} m/s</p>
            <p>💧 {row['humidity']:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    #map view
    st.subheader("🗺️ City Loactions and Temperatures")
    map_data=filtered_df.sort_values('timestamp', ascending=False).groupby('city_name').first().reset_index()

    #create map
    fig=px.scatter_mapbox(
        map_data,
        lat='latitude',
        lon='longitude',
        hover_name='city_name',
        hover_data={
            'temperature':':.1f',
            'humidity':'.0f',
            'weather_description':True,
            'latitude':False,
            'longitude':False
        },
        color='temperature',
        size='temperature',
        color_continuous_scale='RdYlBu_r',
        size_max=20,
        zoom=3,
        height=600    
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    st.plotly_chart(fig, use_container_width=True)

with tab3:
    #comparison tab
    col1, col2=st.columns(2)
    with col1:
        st.subheader("💧 Humidity Comparison")
        
        city_humidity = filtered_df.groupby('city_name')['humidity'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=city_humidity.index,
            y=city_humidity.values,
            labels={'x': 'City', 'y': 'Humidity (%)'},
            color=city_humidity.values,
            color_continuous_scale='Blues',
            text=city_humidity.values.round(0)
        )
        fig.update_traces(
            texttemplate='%{text}%', 
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Humidity: %{y:.0f}%<extra></extra>'  # Clean tooltip
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💨 Wind Speed Comparison")
        
        city_wind = filtered_df.groupby('city_name')['wind_speed'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=city_wind.index,
            y=city_wind.values,
            labels={'x': 'City', 'y': 'Wind Speed (m/s)'},
            color=city_wind.values,
            color_continuous_scale='Greens',
            text=city_wind.values.round(1)
        )
        fig.update_traces(
            texttemplate='%{text}', 
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Wind Speed: %{y:.1f} m/s<extra></extra>'  # Clean tooltip
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Temperature ranges
    st.subheader("🌡️ Temperature Ranges (Min/Max)")
    temp_ranges=filtered_df.groupby('city_name').agg({
        'temp_min':'min',
        'temp_max':'max',
        'temperature':'mean'
    }).reset_index()
    
    for _, row in temp_ranges.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['temp_min'], row['temperature'], row['temp_max']],
            y=[row['city_name'], row['city_name'], row['city_name']],
            mode='lines+markers',
            name=row['city_name'],
            line=dict(width=3),
            marker=dict(size=[8, 12, 8])
        ))

        fig.update_layout(
        xaxis_title="Temperature (°C)",
        yaxis_title="City",
        showlegend=False,
        height=400
    )


    st.plotly_chart(fig, use_container_width=True)

with tab4:
# Data table
    st.subheader("📊 Detailed Weather Data")

    # Format the dataframe for display
    display_df = df[['city_name', 'temperature', 'feels_like', 'humidity', 'pressure', 
                    'weather_description', 'wind_speed', 'timestamp']].copy()
    display_df.columns = ['City', 'Temp (°C)', 'Feels Like (°C)', 'Humidity (%)', 
                        'Pressure (hPa)', 'Weather', 'Wind Speed (m/s)', 'Timestamp']

    # Define custom city order
    city_order = ['Boston', 'New York', 'San Francisco', 'Chicago', 'Seattle', 
                'Miami', 'Los Angeles', 'San Diego', 'Denver', 'Austin', 'Atlanta']

    # Sort by custom order
    display_df['sort_key'] = display_df['City'].apply(lambda x: city_order.index(x) if x in city_order else 999)
    display_df = display_df.sort_values('sort_key').drop('sort_key', axis=1)


    # Reset index to start from 1
    display_df = display_df.reset_index(drop=True)
    display_df.index = display_df.index + 1

    st.dataframe(display_df, use_container_width=True, height=400)

    #Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🗄️ Data Source:** PostgreSQL Database")
    with col2:
        st.markdown(f"**📊 Records Displayed:** {len(filtered_df)}")
    with col3:
        st.markdown(f"**🕐 Generated:** {datetime.now().strftime('%H:%M:%S')}")