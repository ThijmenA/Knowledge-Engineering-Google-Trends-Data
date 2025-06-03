# %%
import pandas as pd

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

# %%
combined_data.to_csv("./combined_data_without_index.csv", index=False)
