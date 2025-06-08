from .database import driver
from .queries import get_sales_weather_data, get_sales_weather_data_by_date
import pandas as pd


def main():
    data = get_sales_weather_data_by_date(driver, "2020-01-01")
    print(data.head())


if __name__ == "__main__":
    main()
