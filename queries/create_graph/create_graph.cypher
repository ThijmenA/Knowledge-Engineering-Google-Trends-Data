LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/ThijmenA/Knowledge-Engineering-Google-Trends-Data/refs/heads/main/combined_data_without_index.csv" AS row
WITH row, split(row.Periods, '-') AS parts

// Create nodes for dates
MERGE (d:Date {id: row.id, value: date({year: toInteger(parts[0]), month: toInteger(parts[1]), day: 1})})
MERGE (y:Year {value: parts[0]})
MERGE (m:Month {value: parts[1]})

// Create nodes for weather data
MERGE (w:Weather {id: row.id})
MERGE (ws:WindSpeed {value: toFloat(row.wind_speed), unit: "m/s"}) // maybe the units should be in extra nodes? This way we would only store them once
MERGE (te:Temperature {value: toFloat(row.temperature), unit: "°C"})
MERGE (rh:Rain {value: toFloat(row.rainfall), unit: "mm"})

// create nodes for sales data
MERGE (s:Sales {id: row.id})
MERGE (rt:Trade {value: toFloat(row["Retail trade"]), name: "Retail trade"})
MERGE (vo:Internet {value: toFloat(row["Retail sale via internet"]), name: "Retail sale via internet"})
MERGE (mc:MultiChannel {value: toFloat(row["Multi-channel"]), name: "Multi-channel"})
MERGE (rfa:Fashion {value: toFloat(row["Retail sale of clothes and fashion items"]), name: "Retail sale of clothes and fashion items"})
MERGE (rel:Electronics {value: toFloat(row["Retail sale of consumer electronics"]), name: "Retail sale of consumer electronics"})
MERGE (rfo:Food {value: toFloat(row["Retail sale of food and drugstore items"]), name: "Retail sale of food and drugstore items"})
MERGE (rnf:NonFood {value: toFloat(row["Retail sale of other non-food"]), name: "Retail sale of other non-food"})

// Create relationships between date nodes
MERGE (d)-[:year]->(y)
MERGE (d)-[:month]->(m)

// Create relationships for weather data
MERGE (d)-[:weather]->(w)
MERGE (w)-[:wind]->(ws)
MERGE (w)-[:temperature]->(te)
MERGE (w)-[:rain]->(rh)

// create relationships for sales data
MERGE (d)-[:sales]->(s)
MERGE (s)-[:total]->(rt)
MERGE (s)-[:online]->(vo)
MERGE (s)-[:multi_channel]->(mc)
MERGE (s)-[:fashion]->(rfa)
MERGE (s)-[:electronics]->(rel)
MERGE (s)-[:food]->(rfo)
MERGE (s)-[:non_food]->(rnf)

