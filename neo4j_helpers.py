from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional

class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str, database: Optional[str] = None):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._database = database

        # (facultatif) Valider la connectivité au démarrage
        try:
            self._driver.verify_connectivity()
        except Exception:
            # Laisser l'app gérer l'erreur proprement
            raise

    def close(self):
        if self._driver:
            self._driver.close()

    def query(self, cypher: str, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        # Si database est renseignée, on l’utilise explicitement
        if self._database:
            with self._driver.session(database=self._database) as session:
                result = session.run(cypher, params or {})
                return [r.data() for r in result]
        else:
            with self._driver.session() as session:
                result = session.run(cypher, params or {})
                return [r.data() for r in result]
