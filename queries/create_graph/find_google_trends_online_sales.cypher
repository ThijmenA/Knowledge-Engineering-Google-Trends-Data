MATCH (d)-[:year]->(y:Year)
MATCH (d)-[:month]->(m:Month)
MATCH (d)-[:google_trends]->(g:GoogleTrends)
MATCH (g)-[:fashion]->(fss:FashionSearch)
MATCH (g)-[:electronics]->(ess:ElectronicsSearch)
MATCH (g)-[:food]->(fos:FoodSearch)
MATCH (g)-[:non_food]->(nss:NonFoodSearch)
MATCH (d)-[:sales]->(s:Sales)
MATCH (s)-[:online]->(vo:Internet)
RETURN y.value AS year,
    m.value AS month,
    d.value AS date,
    fss.value AS fashion_search_value,
    ess.value AS electronics_search_value,
    fos.value AS food_search_value,
    nss.value AS non_food_search_value,
    vo.value AS online_sales_value
