# %%
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# %%
sales_data = pd.read_csv("./sales_data_transformed.csv")
sales_data["year_month"] = pd.to_datetime(sales_data["Periods"], format="%Y-%m")
sales_data = sales_data[sales_data["year_month"] >= "2019-01"]
sales_data = sales_data[sales_data["year_month"] <= "2025-03"]

# %%
precipitation_data = pd.read_csv("./monthly_national_avg_rainfall.csv")
precipitation_data["year_month"] = pd.to_datetime(precipitation_data["year_month"], format="%Y-%m")
precipitation_data = precipitation_data[precipitation_data["year_month"] >= "2019-01"]
precipitation_data = precipitation_data[precipitation_data["year_month"] <= "2025-03"]

# %%
wind_data = pd.read_csv("./monthly_national_avg_wind_speed.csv")
wind_data["year_month"] = pd.to_datetime(wind_data["year_month"], format="%Y-%m")
wind_data = wind_data[wind_data["year_month"] >= "2019-01"]
wind_data = wind_data[wind_data["year_month"] <= "2025-03"]

# %%
temperature_data = pd.read_csv("./monthly_national_avg_temperature_formatted.csv")
temperature_data["year_month"] = pd.to_datetime(temperature_data["year_month"], format="%Y-%m")
temperature_data = temperature_data[temperature_data["year_month"] >= "2019-01"]
temperature_data = temperature_data[temperature_data["year_month"] <= "2025-03"]


# %%
search_data = pd.read_csv("./average_search_data_per_category.csv")
search_data["year_month"] = pd.to_datetime(search_data["Date"], format="%Y-%m")
search_data = search_data[search_data["year_month"] >= "2019-01"]
search_data = search_data[search_data["year_month"] <= "2025-03"]

# %%
# Normalize temperature to create a "comfort" score (higher = more comfortable)
# Define the parameters
ideal_temp = 23  # degrees Celsius
spread = 5       # standard deviation

# Apply Gaussian comfort curve
temperature_scores = temperature_data[["year_month", "temperature"]].copy()
temperature_scores["temp_comfort_score"] = (
    np.exp(-((temperature_scores["temperature"] - ideal_temp) ** 2) / (2 * spread ** 2))) * 10

comfort_temp_data = temperature_scores[["year_month", "temp_comfort_score"]]

# Normalize precipitation inversely to create a "comfort" score (higher = more comfortable)
precip_scores = precipitation_data[["year_month", precipitation_data.columns[1]]].copy()
precip_col = "rainfall"
# Inverse normalization: higher precipitation = lower comfort
precip_scaler = MinMaxScaler()
precip_scores["precip_comfort_score"] = (1 - precip_scaler.fit_transform(precip_scores[[precip_col]])) * 10
comfort_precip_data = precip_scores[["year_month", "precip_comfort_score"]]

# Normalize wind speed inversely to create a "comfort" score (higher = more comfortable)
wind_scores = wind_data[["year_month", wind_data.columns[1]]].copy()
wind_col = "wind_speed"
# Inverse normalization: higher wind speed = lower comfort
wind_scaler = MinMaxScaler()
wind_scores["wind_comfort_score"] = (1 - wind_scaler.fit_transform(wind_scores[[wind_col]])) * 10
comfort_wind_data = wind_scores[["year_month", "wind_comfort_score"]]

# Combine comfort scores into a single DataFrame. Give weights to each score.
weather_score = comfort_temp_data.merge(comfort_precip_data, on="year_month").merge(comfort_wind_data, on="year_month")
weather_score["overall_weather_score"] = (
    0.5 * weather_score["temp_comfort_score"] +
    0.3 * weather_score["precip_comfort_score"] +
    0.2 * weather_score["wind_comfort_score"]
)


# %%
combined_data = sales_data.merge(precipitation_data, on="year_month", how="left")
combined_data = combined_data.merge(wind_data, on="year_month", how="left")
combined_data = combined_data.merge(temperature_data, on="year_month", how="left")
combined_data = combined_data.merge(search_data, on="year_month", how="left")
combined_data = combined_data.rename(columns={
    "avg_precipitation": "precipitation",
    "avg_wind_speed": "wind_speed",
    "avg_temperature": "temperature"
})
combined_data.reset_index(drop=False, inplace=True)
combined_data = combined_data.rename(columns={"index": "id"})
combined_data = combined_data.merge(weather_score[["year_month", "overall_weather_score"]], on="year_month", how="left")

# %%
combined_data.to_csv("./combined_data_without_index.csv", index=False)
