Knowledge Engineering: Google Trends, Weather & Sales Data Integration

Overview
This repository contains an integrated dataset combining Google Trends search data, Dutch weather data (KNMI), and retail sales data (CBS) to analyze relationships between weather patterns, search behavior, and retail sales in the Netherlands.
Dataset Sources

Google Trends: Search interest data for products across four sectors
KNMI Weather Data: Monthly temperature, precipitation, and wind speed
CBS Sales Data: Dutch retail sales across categories and channels

Repository Structure
├── raw_google_trends_data/     # Raw trend data by category
├── raw_weather_data/           # Raw KNMI weather data  
├── raw_sales_data/            # Raw CBS sales data
├── processed_data/            # Combined datasets
├── src/
│   ├── preprocessing/         # Data processing notebooks
│   ├── EDA/                   # Exploratory analysis
│   ├── visualization/         # Visualization code
│   └── web/                   # Web application

Data Integration
All datasets were standardized to monthly format (YYYY-MM) and organized into four matching sectors:

Consumer Electronics
Food and Drugstore Items
Clothing and Fashion
Other Non-Food Items

The integrated data is stored in a Neo4j knowledge graph for querying and analysis.
Web Application
Interactive visualizations available at: https://knowledge-engineering-google-trends-data.onrender.com/
Usage

Run preprocessing notebooks for each dataset
Execute combine.py to create integrated dataset
Load into Neo4j and run web application with python src/web/main.py

Research Questions
How do weather patterns affect retail sales?
What seasonal trends exist between weather and sales?
How do Google search trends correlate with retail sales?

License
Creative Commons Attribution 4.0 International (CC BY 4.0) - free for academic and commercial use with attribution.
Data Quality

No contradictions found across datasets
Fully anonymized with no personal information
Monthly aggregation may limit short-term analysis