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

// Create relationships between date nodes
MERGE (d)-[:year]->(y)
MERGE (d)-[:month]->(m)

// Create relationships for weather data
MERGE (d)-[:weather]->(w)
MERGE (w)-[:wind]->(ws)
MERGE (w)-[:temperature]->(te)
MERGE (w)-[:rain]->(rh)
