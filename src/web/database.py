import os
from pathlib import Path

import dotenv
from neo4j import GraphDatabase

PATH = Path(__file__).parent.parent.parent

load_status = dotenv.load_dotenv(PATH / "Neo4j-6fcd424a-Created-2025-05-28.txt")

if load_status is False:
    raise RuntimeError("Environment variables not loaded.")

URI = os.getenv("NEO4J_URI")
if not URI:
    raise RuntimeError("NEO4J_URI environment variable not set.")

NEO4J_USERNAME, NEO4J_PASSWORD = (
    os.getenv("NEO4J_USERNAME"),
    os.getenv("NEO4J_PASSWORD"),
)
if not NEO4J_USERNAME or not NEO4J_PASSWORD:
    raise RuntimeError("NEO4J_USERNAME or NEO4J_PASSWORD environment variable not set.")

driver = GraphDatabase.driver(
    URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD), database="neo4j"
)
driver.verify_connectivity()
