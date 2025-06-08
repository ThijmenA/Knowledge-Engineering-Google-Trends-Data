// Create seasons nodes
MERGE (s1:Season {name: "Spring"})
MERGE (s2:Season {name: "Summer"})
MERGE (s3:Season {name: "Autumn"})
MERGE (s4:Season {name: "Winter"})

WITH s1, s2, s3, s4
MATCH (d)-[:month]->(m:Month)
WHERE m.value IN ['03', '04', '05']
MERGE (d)-[:season]->(s1)

WITH s1, s2, s3, s4
MATCH (d)-[:month]->(m:Month)
WHERE m.value IN ['06', '07', '08']
MERGE (d)-[:season]->(s2)

WITH s1, s2, s3, s4
MATCH (d)-[:month]->(m:Month)
WHERE m.value IN ['09', '10', '11']
MERGE (d)-[:season]->(s3)

WITH s1, s2, s3, s4
MATCH (d)-[:month]->(m:Month)
WHERE m.value IN ['12', '01', '02']
MERGE (d)-[:season]->(s4)
