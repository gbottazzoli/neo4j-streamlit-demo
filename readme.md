# Neo4j Aura + Streamlit Demo

- App Streamlit connectée à Neo4j Aura (TLS)
- Visualisation pyvis
- Déploiement sur Streamlit Community Cloud

## Local
1) python -m venv .venv && source .venv/bin/activate
2) pip install -r requirements.txt
3) Créer `.streamlit/secrets.toml` (facultatif localement) :

[general]
AURA_URI = "neo4j+s://4e23756a.databases.neo4j.io"
AURA_USER = "neo4j"
AURA_PASSWORD = "_YUZ9I0PG7nN2LeKxYbD-0kN8rlTwegkCBt8pGHeXms"

4) streamlit run streamlit_app.py