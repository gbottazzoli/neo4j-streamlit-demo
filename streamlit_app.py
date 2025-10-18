# streamlit_app.py
# Version 0.1.5 - Interface GraphRAG Tools Diplomatiques - Recherche sémantique
# Auteur: Gérard Bottazzoli (gerard.bottazzoli@etu.unidistance.ch)

import streamlit as st
import requests
from typing import Optional

# -------------------------
# Configuration page
# -------------------------
st.set_page_config(
    page_title="Agent Neo4j Archives Suisses v0.1.5",
    page_icon="🤖",
    layout="wide",
)

# -------------------------
# En-tête sobre
# -------------------------
st.title("🤖 Agent conversationnel sur Graph Neo4j")
st.caption("Phase de test • Version 0.1.5")

# -------------------------
# DISCLAIMER EXPERIMENTAL
# -------------------------
st.info("""
⚠️ **Phase expérimentale** : Les agents Neo4j Anthropic sont en cours de développement. 
Si une requête ne fonctionne pas comme prévu, veuillez reformuler en précisant toujours le nom complet de la personne.
""")

st.divider()

# -------------------------
# Secrets & configuration
# -------------------------
AGENT_ENDPOINT = st.secrets.get("AGENT_ENDPOINT", "")
CLIENT_ID = st.secrets.get("CLIENT_ID", "")
CLIENT_SECRET = st.secrets.get("CLIENT_SECRET", "")

if not (AGENT_ENDPOINT and CLIENT_ID and CLIENT_SECRET):
    st.error(
        "⚠️ Configuration manquante.\n\n"
        "Ajoute dans Settings → Secrets"
    )
    st.stop()


# -------------------------
# Fonction : Obtenir Bearer Token
# -------------------------
@st.cache_data(ttl=3600)
def get_bearer_token(client_id: str, client_secret: str) -> Optional[str]:
    """Obtient un bearer token OAuth2 depuis Neo4j Aura API"""
    try:
        response = requests.post(
            'https://api.neo4j.io/oauth/token',
            auth=(client_id, client_secret),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={'grant_type': 'client_credentials'},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            st.error(f"❌ Erreur OAuth ({response.status_code})")
            return None
    except Exception as e:
        st.error(f"❌ Erreur d'authentification: {str(e)}")
        return None


# -------------------------
# Initialiser session state
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_debug" not in st.session_state:
    st.session_state.show_debug = False

# -------------------------
# Sidebar : Menu Optimisé v2
# -------------------------
with st.sidebar:
    # ===========================
    # HEADER COMPACT
    # ===========================
    st.markdown("### 🤖 Archives diplomatiques 1940-1945")
    st.caption("*Graph RAG avec historian-in-the-loop*")

    st.divider()

    # ===========================
    # 💡 CONSEIL PRINCIPAL
    # ===========================
    st.markdown("""
    💡 **Toujours préciser le nom complet**

    ✅ "Détails sur 1942 pour Elisabeth Müller"  
    ❌ "Détails sur 1942" (peut perdre le contexte)
    """)

    st.divider()

    # ===========================
    # 🔥 REQUÊTES RAPIDES (TOP 5)
    # ===========================
    st.markdown("### 🔥 Exemples rapides")

    if st.button("📖 Biographie Müller", key="quick_bio", use_container_width=True):
        st.session_state.pending_query = "Donne-moi la biographie d'Elisabeth Müller"

    if st.button("🎯 Parcours complet Müller", key="quick_parcours", use_container_width=True):
        st.session_state.pending_query = "Décris le parcours de persécution d'Elisabeth Müller"

    if st.button("📊 Chaîne communication Müller", key="quick_chaine", use_container_width=True):
        st.session_state.pending_query = "Chaîne de communication pour Elisabeth Müller"

    if st.button("📅 Détails 1942 Müller", key="quick_1942", use_container_width=True):
        st.session_state.pending_query = "Montre-moi les détails de 1942 pour Elisabeth Müller"

    if st.button("🔍 Garde-meuble", key="quick_garde", use_container_width=True):
        st.session_state.pending_query = "Trouve des infos sur les frais de garde-meuble"

    st.divider()

    # ===========================
    # 📚 GUIDE COMPLET (COLLAPSIBLE)
    # ===========================
    with st.expander("📚 Toutes les requêtes disponibles"):

        st.markdown("#### 👤 Parcours individuels")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 Bio Nussbaumer", key="bio_nuss", use_container_width=True):
                st.session_state.pending_query = "Qui est Marcel Nussbaumer ?"
        with col2:
            if st.button("📖 Bio de Pury", key="bio_pury", use_container_width=True):
                st.session_state.pending_query = "Qui est Gérard de Pury ?"

        st.markdown("#### 📅 Périodes spécifiques")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📅 Avril 1942", key="avril_42", use_container_width=True):
                st.session_state.pending_query = "Détails sur avril 1942 pour Elisabeth Müller"
        with col2:
            if st.button("📅 Année 1943", key="annee_43", use_container_width=True):
                st.session_state.pending_query = "Montre-moi 1943 pour Elisabeth Müller"

        st.markdown("#### 🔍 Recherches thématiques")

        st.caption("*Découverte de thèmes dans le corpus*")

        if st.button("🔍 Conditions de détention", key="detention", use_container_width=True):
            st.session_state.pending_query = "Trouve des documents sur les conditions de détention"

        if st.button("📦 Garde-meuble (FR/DE)", key="garde_detail", use_container_width=True):
            st.session_state.pending_query = "Y a-t-il des mentions de garde-meuble dans les archives ?"

        if st.button("🚚 Frais de transport", key="transport", use_container_width=True):
            st.session_state.pending_query = "Trouve des documents sur les frais de transport"

        if st.button("💰 Questions d'argent", key="argent", use_container_width=True):
            st.session_state.pending_query = "Trouve des chaînes mentionnant de l'argent"

        if st.button("⚖️ Condamnations", key="condamn", use_container_width=True):
            st.session_state.pending_query = "Trouve des infos sur les condamnations"

        if st.button("🏛️ Prisons", key="prison", use_container_width=True):
            st.session_state.pending_query = "Trouve des documents qui parlent de prison"

        st.markdown("#### 📗 Reconstitution thématique")

        st.caption("*Micro-actions filtrées par thème*")

        if st.button("📗 Müller sur garde-meuble", key="recon_garde", use_container_width=True):
            st.session_state.pending_query = "Reconstitue la chaîne pour Elisabeth Müller sur garde-meuble entre 1942 et 1945"

        if st.button("📗 Müller sur détention 1943", key="recon_det", use_container_width=True):
            st.session_state.pending_query = "Reconstitue la chaîne pour Elisabeth Müller sur détention en 1943"

        st.markdown("#### 📊 Analyses globales")

        if st.button("📋 Liste personnes", key="liste", use_container_width=True):
            st.session_state.pending_query = "Quelles personnes sont disponibles ?"

        if st.button("🌐 Acteurs principaux", key="acteurs", use_container_width=True):
            st.session_state.pending_query = "Acteurs principaux du réseau ?"

        if st.button("⏱️ Réactivité", key="react", use_container_width=True):
            st.session_state.pending_query = "Quelle est la réactivité des autorités suisses ?"

        st.markdown("#### ⚖️ Comparaisons")

        if st.button("⚖️ Müller vs Nussbaumer", key="comp1", use_container_width=True):
            st.session_state.pending_query = "Compare Elisabeth Müller et Marcel Nussbaumer"

        if st.button("⚖️ Müller vs de Pury", key="comp2", use_container_width=True):
            st.session_state.pending_query = "Quelles sont les différences entre Elisabeth Müller et Gérard de Pury ?"

    st.divider()

    # ===========================
    # 📊 PROGRESSION (COLLAPSIBLE)
    # ===========================
    with st.expander("📊 Progression de l'import"):
        sources_importees = 75
        sources_total = 191
        pourcentage = int((sources_importees / sources_total) * 100)

        st.progress(pourcentage / 100)
        st.caption(f"**{pourcentage}%** • {sources_importees}/{sources_total} sources")
        st.caption("🎯 Objectif 100% : **14 novembre 2025**")

    # ===========================
    # ℹ️ À PROPOS (COLLAPSIBLE)
    # ===========================
    with st.expander("ℹ️ À propos du corpus"):
        st.markdown("""
        **Données actuelles** :
        - 48 personnes documentées
        - 202 micro-actions diplomatiques
        - 75 documents d'archives
        - 366 chunks vectorisés (275 docs + 91 entités)
        - 12 outils de requête

        **Technologies** :
        - Neo4j Graph Database
        - Claude Sonnet 4.5
        - Vertex AI Embeddings (768D)
        - Langues : FR/DE/EN

        **⏱️ Temps de réponse** : 15-60 sec
        """)

    st.divider()

    # ===========================
    # ⚙️ OPTIONS
    # ===========================
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Effacer", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        st.session_state.show_debug = st.checkbox("🔍 Debug", value=st.session_state.show_debug)

    st.divider()

    # ===========================
    # FOOTER COMPACT
    # ===========================
    st.markdown("""
    <div style='font-size: 0.7em; color: #888; text-align: center;'>
        <strong>GraphRAG Tools v0.1.5</strong><br>
        Gérard Bottazzoli<br>
        <a href='mailto:gerard.bottazzoli@etu.unidistance.ch'>✉️ Contact</a>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# Afficher l'historique
# -------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------
# INPUT TOUJOURS EN PREMIER (critique!)
# -------------------------
user_input = st.chat_input("💬 Pose ta question ici... (précisez toujours le nom complet de la personne)")

# -------------------------
# Traiter pending_query OU user_input
# -------------------------
query_to_process = None

# Priorité 1 : Query depuis bouton
if "pending_query" in st.session_state and st.session_state.pending_query:
    query_to_process = st.session_state.pending_query
    st.session_state.pending_query = None

# Priorité 2 : Input manuel
elif user_input:
    query_to_process = user_input

# -------------------------
# Traitement de la requête
# -------------------------
if query_to_process:

    # Afficher la question
    st.session_state.messages.append({"role": "user", "content": query_to_process})
    with st.chat_message("user"):
        st.markdown(query_to_process)

    # Appeler l'API
    with st.chat_message("assistant"):
        with st.spinner("🔎 Recherche en cours... (15-60 sec)"):

            bearer_token = get_bearer_token(CLIENT_ID, CLIENT_SECRET)

            if not bearer_token:
                error_msg = "❌ Impossible d'obtenir le token."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                try:
                    response = requests.post(
                        AGENT_ENDPOINT,
                        headers={
                            'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'Authorization': f'Bearer {bearer_token}'
                        },
                        json={'input': query_to_process},
                        timeout=90  # Augmenté à 90s pour recherche sémantique
                    )

                    if response.status_code == 200:
                        data = response.json()

                        # Extraire réponse
                        answer = None
                        if isinstance(data.get('content'), list):
                            for item in reversed(data['content']):
                                if item.get('type') == 'text':
                                    answer = item.get('text')
                                    break

                        if not answer:
                            answer = data.get('output') or data.get('response') or "❌ Format inattendu"

                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})

                        if st.session_state.show_debug:
                            with st.expander("🔍 JSON brut"):
                                st.json(data)

                    elif response.status_code == 401:
                        error_msg = "🔒 Token expiré. Réessaie."
                        st.error(error_msg)
                        st.cache_data.clear()
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

                    else:
                        error_msg = f"❌ Erreur API ({response.status_code})"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

                except requests.Timeout:
                    timeout_msg = "⏱️ Timeout (>90 sec). La recherche était peut-être trop complexe. Essayez de préciser l'année ou le thème."
                    st.warning(timeout_msg)
                    st.session_state.messages.append({"role": "assistant", "content": timeout_msg})

                except Exception as e:
                    error_msg = f"❌ Erreur: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})