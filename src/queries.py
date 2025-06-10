import pandas as pd
from neo4j import Driver


def get_sales_weather_data(driver: Driver) -> pd.DataFrame:
    query = """
    MATCH (d:Date)-[year]->(y:Year)
    MATCH (d)-[month]->(m:Month)
    MATCH (d)-[weather]->(w:Weather)
    MATCH (w)-[wind]->(windSpeed:WindSpeed)
    MATCH (w)-[rain]->(rainNode:Rain)
    MATCH (w)-[temperature]->(temp:Temperature)

    MATCH (d)-[sales]->(s:Sales)
    MATCH (s)-[total]->(rt:Trade)
    MATCH (s)-[online]->(vo:Internet)
    MATCH (s)-[multi_channel]->(mc:MultiChannel)
    MATCH (s)-[fashion]->(rfa:Fashion) MATCH (s)-[electronics]->(rel:Electronics)
    MATCH (s)-[food]->(rfo:Food)
    MATCH (s)-[non_food]->(rnf:NonFood)

    ORDER BY d.value

    RETURN y.value AS year,
           m.value AS month,
           d.value AS date,
           windSpeed.value AS wind_speed,
           rainNode.value AS rain,
           temp.value AS temp,
           s.total_calc_channels AS total_calc_channels,
           s.total_calc_categories AS total_calc_categories,
           rt.value AS retail_trade,
           vo.value AS retail_sale_via_internet,
           mc.value AS multi_channel,
           rfa.value AS retail_sale_of_clothes_and_fashion_items,
           rel.value AS retail_sale_of_consumer_electronics,
           rfo.value AS retail_sale_of_food_and_drugstore_items,
           rnf.value AS retail_sale_of_other_non_food
    """
    records, summary, keys = driver.execute_query(query)
    data = pd.DataFrame(records, columns=keys)
    return data


def get_sales_weather_data_by_date(driver: Driver, date: str) -> pd.DataFrame:
    query = """
    MATCH (d:Date {value: date($date)})-[year]->(y:Year)
    MATCH (d)-[month]->(m:Month)
    MATCH (d)-[weather]->(w:Weather)
    MATCH (w)-[wind]->(windSpeed:WindSpeed)
    MATCH (w)-[rain]->(rainNode:Rain)
    MATCH (w)-[temperature]->(temp:Temperature)

    MATCH (d)-[sales]->(s:Sales)
    MATCH (s)-[total]->(rt:Trade)
    MATCH (s)-[online]->(vo:Internet)
    MATCH (s)-[multi_channel]->(mc:MultiChannel)
    MATCH (s)-[fashion]->(rfa:Fashion)
    MATCH (s)-[electronics]->(rel:Electronics)
    MATCH (s)-[food]->(rfo:Food)
    MATCH (s)-[non_food]->(rnf:NonFood)

    ORDER BY d.value

    RETURN y.value AS year,
           m.value AS month,
           d.value AS date,
           windSpeed.value AS wind_speed,
           rainNode.value AS rain,
           temp.value AS temp,
           s.total_calc_channels AS total_calc_channels,
           s.total_calc_categories AS total_calc_categories,
           rt.value AS retail_trade,
           vo.value AS retail_sale_via_internet,
           mc.value AS multi_channel,
           rfa.value AS retail_sale_of_clothes_and_fashion_items,
           rel.value AS retail_sale_of_consumer_electronics,
           rfo.value AS retail_sale_of_food_and_drugstore_items,
           rnf.value AS retail_sale_of_other_non_food
    """
    records, summary, keys = driver.execute_query(query, date=date)
    data = pd.DataFrame(records, columns=keys)
    return data


def get_sales_weather_data_by_date_range(
    driver: Driver, start_date: str, end_date: str
) -> pd.DataFrame:
    query = """
    MATCH (d:Date)-[year]->(y:Year)
    WHERE d.value >= date($start_date) AND d.value <= date($end_date)
    MATCH (d)-[month]->(m:Month)
    MATCH (d)-[weather]->(w:Weather)
    MATCH (w)-[wind]->(windSpeed:WindSpeed)
    MATCH (w)-[rain]->(rainNode:Rain)
    MATCH (w)-[temperature]->(temp:Temperature)

    MATCH (d)-[sales]->(s:Sales)
    MATCH (s)-[total]->(rt:Trade)
    MATCH (s)-[online]->(vo:Internet)
    MATCH (s)-[multi_channel]->(mc:MultiChannel)
    MATCH (s)-[fashion]->(rfa:Fashion)
    MATCH (s)-[electronics]->(rel:Electronics)
    MATCH (s)-[food]->(rfo:Food)
    MATCH (s)-[non_food]->(rnf:NonFood)

    ORDER BY d.value

    RETURN y.value AS year,
           m.value AS month,
           d.value AS date,
           windSpeed.value AS wind_speed,
           rainNode.value AS rain,
           temp.value AS temp,
           s.total_calc_channels AS total_calc_channels,
           s.total_calc_categories AS total_calc_categories,
           rt.value AS retail_trade,
           vo.value AS retail_sale_via_internet,
           mc.value AS multi_channel,
           rfa.value AS retail_sale_of_clothes_and_fashion_items,
           rel.value AS retail_sale_of_consumer_electronics,
           rfo.value AS retail_sale_of_food_and_drugstore_items,
           rnf.value AS retail_sale_of_other_non_food
    """
    records, summary, keys = driver.execute_query(query, start_date=start_date, end_date=end_date)
    data = pd.DataFrame(records, columns=keys)
    return data

def get_sales_google_trends_data(driver: Driver) -> pd.DataFrame:
    query = """
    MATCH (d:Date)-[year]->(y:Year)
    MATCH (d)-[month]->(m:Month)
    MATCH (d)-[google_trends]->(gt:GoogleTrends)
    MATCH (gt)-[fashion]->(f:FashionSearch)
    MATCH (gt)-[electronics]->(e:ElectronicsSearch)
    MATCH (gt)-[food]->(fo:FoodSearch)
    MATCH (gt)-[non_food]->(o:NonFoodSearch)
    MATCH (d)-[sales]->(s:Sales)
    MATCH (s)-[online]->(vo:Internet)

    ORDER BY d.value

    RETURN y.value AS year,
           m.value AS month,
           d.value AS date,
           gt.value AS google_trends,
           f.value AS fashion_search,
           e.value AS electronics_search,
           fo.value AS food_search,
           o.value AS non_food_search,
           vo.value AS retail_sale_via_internet
    """
    records, summary, keys = driver.execute_query(query)
    data = pd.DataFrame(records, columns=keys)
    return data

def get_sales_google_trends_data_by_date(driver: Driver, date: str) -> pd.DataFrame:
    query = """
    MATCH (d:Date {value: date($date)})-[year]->(y:Year)
    MATCH (d)-[month]->(m:Month)
    MATCH (d)-[google_trends]->(gt:GoogleTrends)
    MATCH (gt)-[fashion]->(f:FashionSearch)
    MATCH (gt)-[electronics]->(e:ElectronicsSearch)
    MATCH (gt)-[food]->(fo:FoodSearch)
    MATCH (gt)-[non_food]->(o:NonFoodSearch)
    MATCH (d)-[sales]->(s:Sales)
    MATCH (s)-[online]->(vo:Internet)

    ORDER BY d.value

    RETURN y.value AS year,
           m.value AS month,
           d.value AS date,
           gt.value AS google_trends,
           f.value AS fashion_search,
           e.value AS electronics_search,
           fo.value AS food_search,
           o.value AS non_food_search,
           vo.value AS retail_sale_via_internet
    """
    records, summary, keys = driver.execute_query(query, date=date)
    data = pd.DataFrame(records, columns=keys)
    return data

def get_sales_google_trends_data_by_date_range(
    driver: Driver, start_date: str, end_date: str
) -> pd.DataFrame:
    query = """
    MATCH (d:Date)-[year]->(y:Year)
    WHERE d.value >= date($start_date) AND d.value <= date($end_date)
    MATCH (d)-[month]->(m:Month)
    MATCH (d)-[google_trends]->(gt:GoogleTrends)
    MATCH (gt)-[fashion]->(f:FashionSearch)
    MATCH (gt)-[electronics]->(e:ElectronicsSearch)
    MATCH (gt)-[food]->(fo:FoodSearch)
    MATCH (gt)-[non_food]->(o:NonFoodSearch)
    MATCH (d)-[sales]->(s:Sales)
    MATCH (s)-[online]->(vo:Internet)

    ORDER BY d.value

    RETURN y.value AS year,
           m.value AS month,
           d.value AS date,
           gt.value AS google_trends,
           f.value AS fashion_search,
           e.value AS electronics_search,
           fo.value AS food_search,
           o.value AS non_food_search,
           vo.value AS retail_sale_via_internet
    """
    records, summary, keys = driver.execute_query(query, start_date=start_date, end_date=end_date)
    data = pd.DataFrame(records, columns=keys)
    return data
