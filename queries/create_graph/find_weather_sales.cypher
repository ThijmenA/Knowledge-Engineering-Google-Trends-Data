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
MATCH (s)-[fashion]->(rfa:Fashion)
MATCH (s)-[electronics]->(rel:Electronics)
MATCH (s)-[food]->(rfo:Food)
MATCH (s)-[non_food]->(rnf:NonFood)

RETURN windSpeed.value,
       rainNode.value,
       temp.value,
       y.value AS year,
       m.value AS month,
       d.value AS date,
       s.total_calc_channels AS total_calc_channels,
       s.total_calc_categories AS total_calc_categories,
       rt.value AS retail_trade,
       vo.value AS retail_sale_via_internet,
       mc.value AS multi_channel,
       rfa.value AS retail_sale_of_clothes_and_fashion_items,
       rel.value AS retail_sale_of_consumer_electronics,
       rfo.value AS retail_sale_of_food_and_drugstore_items,
       rnf.value AS retail_sale_of_other_non_food

