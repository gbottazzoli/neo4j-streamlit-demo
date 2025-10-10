import streamlit as st
import pandas as pd
from neo4j_helpers import Neo4jClient
from pyvis.network import Network
import os
import tempfile
from streamlit.components.v1 import html

st.set_page_config(page_title="Neo4j Aura Demo", page_icon="🕸️", layout="wide")

st.title("🕸️ Neo4j Aura • Demo Streamlit")
st.caption("Connexion TLS (neo4j+s), requêtes paramétrées et visualisation rapide.")

# 1) Secrets (configurés côté Cloud: st.secrets["..."])
AURA_URI = st.secrets.get("AURA_URI", "")
AURA_USER = st.secrets.get("AURA_USER", "")
AURA_PASSWORD = st.secrets.get("AURA_PASSWORD", "")

if not (AURA_URI and AURA_USER and AURA_PASSWORD):
    st.error("Secrets manquants. Configure AURA_URI, AURA_USER, AURA_PASSWORD dans les secrets.")
    st.stop()

# 2) Connexion (mise en cache pour éviter reconnecter à chaque interaction)
@st.cache_resource
def get_client():
    return Neo4jClient(uri=AURA_URI, user=AURA_USER, password=AURA_PASSWORD)

client = get_client()

# 3) Panneau latéral: requête prédéfinie + paramètres
st.sidebar.header("Requête d'exemple")
st.sidebar.write("Filtre simple sur label et limite.")
node_label = st.sidebar.text_input("Label de nœud", value="Person")
limit = st.sidebar.slider("Limite", min_value=5, max_value=200, value=50, step=5)

default_cypher = f"""
MATCH (n:{node_label})
WITH n LIMIT $limit
OPTIONAL MATCH (n)-[r]-(m)
RETURN n AS node, type(r) AS rel_type, m AS neighbor
"""

cypher = st.text_area("Cypher (éditable)", value=default_cypher, height=200, help="Tu peux modifier la requête.")
params = {"limit": limit}

# 4) Exécution
col1, col2 = st.columns([1,1])
with col1:
    if st.button("▶️ Exécuter la requête"):
        try:
            rows = client.query(cypher, params)
            st.session_state["rows"] = rows
            st.success(f"{len(rows)} lignes renvoyées.")
        except Exception as e:
            st.error(f"Erreur: {e}")

rows = st.session_state.get("rows", [])

# 5) Affichage tabulaire
with col1:
    if rows:
        # Flatten basique: extraire propriétés des nodes si présents
        def node_props(n):
            if not n: return {}
            return dict(n.items()) if hasattr(n, "items") else dict(n)
        data = []
        for r in rows:
            node = r.get("node")
            neighbor = r.get("neighbor")
            rel_type = r.get("rel_type")
            data.append({
                "node_id": node.element_id if node is not None else None,
                "node_labels": ":".join(node.labels) if node is not None else None,
                **node_props(node),
                "rel_type": rel_type,
                "neighbor_id": neighbor.element_id if neighbor is not None else None,
                "neighbor_labels": ":".join(neighbor.labels) if neighbor is not None else None,
                **{f"neighbor_{k}": v for k, v in node_props(neighbor).items()}
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

# 6) Visualisation graphe (pyvis)
with col2:
    if rows:
        net = Network(height="650px", width="100%", directed=False, notebook=False)
        net.toggle_physics(True)

        seen = set()
        for r in rows:
            n = r.get("node")
            m = r.get("neighbor")
            rel = r.get("rel_type")

            if n is not None:
                nid = n.element_id
                if nid not in seen:
                    net.add_node(nid, label=":".join(n.labels) or "Node",
                                 title=str(dict(n.items())))
                    seen.add(nid)

            if m is not None:
                mid = m.element_id
                if mid not in seen:
                    net.add_node(mid, label=":".join(m.labels) or "Node",
                                 title=str(dict(m.items())))
                    seen.add(mid)

                if n is not None:
                    net.add_edge(n.element_id, m.element_id, label=rel or "")

        # pyvis écrit un HTML qu'on ré-injecte dans Streamlit
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
            net.show(tmp.name)
            html_data = open(tmp.name, "r", encoding="utf-8").read()
        html(html_data, height=650, scrolling=True)

st.divider()
st.subheader("Requêtes de démonstration (copier-coller)")
st.code("""
-- 1) Compter des nœuds par label
MATCH (n) RETURN labels(n) AS labels, count(*) AS cnt ORDER BY cnt DESC;

-- 2) Chercher des personnes par nom
MATCH (p:Person)
WHERE toLower(p.prefLabel_fr) CONTAINS toLower($q)
RETURN p LIMIT 25;

-- 3) Sous-graphe local autour d'une personne (par id stable)
MATCH (p:Person {id: $person_id})-[r]-(x)
RETURN p AS node, type(r) AS rel_type, x AS neighbor LIMIT 200;
""", language="cypher")

st.caption("Astuce : garde toujours tes requêtes **paramétrées** (pas de concat de strings).")
