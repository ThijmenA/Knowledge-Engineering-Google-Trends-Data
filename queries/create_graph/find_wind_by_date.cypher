/* Please find the wind value for the year 2019 and month 01 */

MATCH (d:Date)-[year]->(y:Year {value: '2019'})
MATCH (d)-[month]->(m:Month {value: '01'})
MATCH (d)-[weather]->(w:Weather)-[wind]->(windSpeed:WindSpeed)
RETURN windSpeed.value
