from neo4j import GraphDatabase
from typing import List, Dict, Any

class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self._driver:
            self._driver.close()

    def query(self, cypher: str, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        with self._driver.session() as session:
            result = session.run(cypher, params or {})
            return [r.data() for r in result]
