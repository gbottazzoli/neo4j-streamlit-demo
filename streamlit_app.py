# streamlit_app.py
# Version 0.1 - Interface GraphRAG Tools Diplomatiques
# Auteur: Gérard Bottazzoli (gerard.bottazzoli@etu.unidistance.ch)

import streamlit as st
import requests
from typing import Optional

# -------------------------
# Configuration page
# -------------------------
st.set_page_config(
    page_title="GraphRAG Archives Suisses v0.1",
    page_icon="🤖",
    layout="wide",
)

# -------------------------
# En-tête académique
# -------------------------
st.title("🤖 Agent Conversationnel - Archives Diplomatiques Suisses")
st.subheader("Des modèles de langage au service des questions de recherche")
st.caption("Cas d'étude sur des archives diplomatiques (1940-1945)")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**Auteur** : Gérard Bottazzoli • **Contact** : gerard.bottazzoli@etu.unidistance.ch")
with col2:
    st.markdown("**Version** : 0.1")

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
        "Ajoute dans Settings → Secrets :\n\n"
        '```toml\n'
        'AGENT_ENDPOINT = "https://api.neo4j.io/v2beta1/projects/.../agents/.../invoke"\n'
        'CLIENT_ID = "ton_client_id"\n'
        'CLIENT_SECRET = "ton_client_secret"\n'
        '```'
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
# Sidebar : Menu Unique
# -------------------------
with st.sidebar:
    st.header("📖 Guide des Requêtes")
    st.caption("Clique sur un exemple pour le tester")

    categorie = st.selectbox(
        "🎯 Choisir une fonctionnalité",
        [
            "👋 Bienvenue",
            "📚 Parcours individuels",
            "🔗 Chaînes de communication",
            "🔍 Recherche thématique",
            "📊 Analyses globales",
            "⚖️ Comparaisons"
        ]
    )

    st.divider()

    # ===========================
    # BIENVENUE
    # ===========================
    if categorie == "👋 Bienvenue":
        st.markdown("""
        ### Bienvenue ! 👋

        Ce système permet d'interroger **1410 nœuds** d'archives diplomatiques suisses (1940-1945).

        **🎯 À tester en priorité** :
        - Parcours individuels (bio + chronologie)
        - Chaînes de communication
        - Recherche thématique multilingue

        **📊 Corpus** :
        - 48 personnes
        - 202 micro-actions diplomatiques
        - 75 documents sources
        - 316 chunks vectorisés (768D)

        **🔧 Système** :
        - 13 tools opérationnels
        - Recherche multilingue FR/DE/EN
        - Embeddings Gemini

        **⏱️ Temps de réponse** : 15-45 sec

        👈 **Sélectionne une catégorie** dans le menu pour voir des exemples testables !
        """)

    # ===========================
    # PARCOURS INDIVIDUELS
    # ===========================
    elif categorie == "📚 Parcours individuels":
        st.markdown("### 📚 Parcours de persécution")
        st.caption("Biographie + chronologie structurée")

        st.markdown("**🔵 Cas Elisabeth Müller** *(principal)*")
        if st.button("📝 Biographie de Müller", key="bio_muller"):
            st.session_state.pending_query = "Donne-moi la biographie d'Elisabeth Müller"
        if st.button("📅 Chronologie de Müller", key="chrono_muller"):
            st.session_state.pending_query = "Quelle est la chronologie d'Elisabeth Müller ?"
        if st.button("🎯 Parcours complet de Müller", key="parcours_muller"):
            st.session_state.pending_query = "Décris le parcours de persécution d'Elisabeth Müller"

        st.markdown("**🔵 Autres personnes**")
        if st.button("📝 Biographie de Nussbaumer", key="bio_nuss"):
            st.session_state.pending_query = "Qui est Marcel Nussbaumer ?"
        if st.button("📝 Biographie de Pury", key="bio_pury"):
            st.session_state.pending_query = "Qui est Gérard de Pury ?"

        st.info(
            "💡 **Format des réponses** :\n- Notice biographique enrichie\n- Occupations, origines, famille\n- Max 15 événements chronologiques\n- Flags reconstruction (⚠️) si source après 1946")

    # ===========================
    # CHAÎNES DE COMMUNICATION
    # ===========================
    elif categorie == "🔗 Chaînes de communication":
        st.markdown("### 🔗 Correspondances diplomatiques")
        st.caption("Reconstitution chronologique des échanges")

        st.markdown("**🔴 Vue d'ensemble** *(phases d'intensité)*")
        if st.button("📊 Chaîne de communication pour Müller", key="chaine_muller"):
            st.session_state.pending_query = "Chaîne de communication pour Elisabeth Müller"

        st.markdown("**🔴 Détails par période**")
        if st.button("📅 Détails sur 1942 pour Müller", key="1942"):
            st.session_state.pending_query = "Montre-moi les détails de 1942 pour Müller"
        if st.button("📅 Détails sur avril 1942", key="avril_1942"):
            st.session_state.pending_query = "Détails sur avril 1942 pour Müller"
        if st.button("📅 Détails sur 1943", key="1943"):
            st.session_state.pending_query = "Montre-moi 1943 pour Elisabeth Müller"

        st.info(
            "💡 **Format des réponses** :\n- Phases d'intensité (🔵🔴🟠🟢)\n- Actions avec émetteur → destinataire\n- Sources avec cotes d'archives\n- Délais entre actions")

    # ===========================
    # RECHERCHE THÉMATIQUE
    # ===========================
    elif categorie == "🔍 Recherche thématique":
        st.markdown("### 🔍 Recherche par mots-clés")
        st.caption("Multilingue FR/DE automatique")

        st.markdown("**🟢 Recherche sémantique** *(via embeddings)*")
        if st.button("🔍 Frais de garde-meuble", key="garde_meuble"):
            st.session_state.pending_query = "Trouve des infos sur les frais de garde-meuble"
        if st.button("🔍 Möbellager (allemand)", key="mobellager"):
            st.session_state.pending_query = "Trouve des chaînes sur Möbellager"

        st.markdown("**🟢 Reconstitution thématique**")
        if st.button("🔗 Chaîne garde-meuble pour Müller", key="chaine_garde"):
            st.session_state.pending_query = "Reconstitue la chaîne pour Müller sur les frais de garde-meuble"

        st.markdown("**🟢 Autres thèmes testables**")
        if st.button("💰 Recherche sur 'argent'", key="argent"):
            st.session_state.pending_query = "Trouve des chaînes mentionnant de l'argent"
        if st.button("⚖️ Recherche 'condamnation'", key="condamnation"):
            st.session_state.pending_query = "Trouve des infos sur les condamnations"
        if st.button("🔒 Recherche 'prison'", key="prison"):
            st.session_state.pending_query = "Trouve des chaînes sur les prisons"

        st.info(
            "💡 **Multilingue automatique** :\n- 'garde-meuble' trouve aussi 'Möbellager', 'Effekten'\n- 316 chunks vectorisés (768D Gemini)\n- Recherche sémantique FR/DE/EN")

    # ===========================
    # ANALYSES GLOBALES
    # ===========================
    elif categorie == "📊 Analyses globales":
        st.markdown("### 📊 Statistiques et vues d'ensemble")
        st.caption("Analyses comparatives du corpus")

        st.markdown("**🟠 Vue globale**")
        if st.button("📊 Liste des personnes disponibles", key="liste"):
            st.session_state.pending_query = "Quelles personnes sont disponibles ?"
        if st.button("🔗 Vue globale des chaînes", key="vue_globale"):
            st.session_state.pending_query = "Montre-moi les principales chaînes de communication"

        st.markdown("**🟠 Statistiques**")
        if st.button("⏱️ Réactivité des autorités suisses", key="reactivite"):
            st.session_state.pending_query = "Quelle est la réactivité des autorités suisses ?"

        st.info(
            "💡 **Analyses disponibles** :\n- Statistiques de réactivité (urgent/standard/lent/bloqué)\n- Vue comparative des chaînes\n- Délai moyen : 8,7 jours")

    # ===========================
    # COMPARAISONS
    # ===========================
    elif categorie == "⚖️ Comparaisons":
        st.markdown("### ⚖️ Comparaisons de parcours")
        st.caption("Analyse comparative entre deux personnes")

        if st.button("⚖️ Compare Müller et Nussbaumer", key="comp1"):
            st.session_state.pending_query = "Compare Elisabeth Müller et Marcel Nussbaumer"
        if st.button("⚖️ Compare Müller et de Pury", key="comp2"):
            st.session_state.pending_query = "Quelles sont les différences entre Müller et de Pury ?"

        st.info(
            "💡 **Format des comparaisons** :\n- Événements côte à côte par période\n- Points communs et différences\n- Synthèse comparative")

    st.divider()

    # Options avancées
    with st.expander("⚙️ Options"):
        st.session_state.show_debug = st.checkbox("🔍 Mode debug (JSON)", value=st.session_state.show_debug)
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.messages = []
            st.rerun()

    st.divider()

    st.caption("""
    **⏱️ Temps** : 15-45 sec

    **📊 Corpus** : 
    • 48 personnes
    • 202 micro-actions
    • 75 documents
    • 316 chunks vectorisés

    **🔧 Tools** : 13 opérationnels
    """)

# -------------------------
# Container pour l'historique (scrollable)
# -------------------------
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# -------------------------
# Input utilisateur (TOUJOURS VISIBLE)
# -------------------------
user_input = st.chat_input("💬 Pose ta question ici... (ou clique sur un exemple dans le menu)")

# -------------------------
# Traitement requête depuis bouton
# -------------------------
if "pending_query" in st.session_state:
    user_input = st.session_state.pending_query
    del st.session_state.pending_query
    st.rerun()

# -------------------------
# Traitement de la requête
# -------------------------
if user_input:

    # Afficher la question de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})

    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_input)

    # Appeler l'API
    with chat_container:
        with st.chat_message("assistant"):
            with st.spinner("🔍 Recherche en cours... (15-45 sec)"):

                bearer_token = get_bearer_token(CLIENT_ID, CLIENT_SECRET)

                if not bearer_token:
                    error_msg = "❌ Impossible d'obtenir le token d'authentification."
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
                            json={'input': user_input},
                            timeout=60
                        )

                        if response.status_code == 200:
                            data = response.json()

                            # Extraire réponse propre
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
                                with st.expander("🔍 JSON brut (debug)"):
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
                        timeout_msg = "⏱️ Timeout (>60 sec). Réessaie."
                        st.warning(timeout_msg)
                        st.session_state.messages.append({"role": "assistant", "content": timeout_msg})

                    except Exception as e:
                        error_msg = f"❌ Erreur: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

# -------------------------
# Footer académique
# -------------------------
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <strong>GraphRAG Tools Diplomatiques v0.1</strong><br>
    Des modèles de langage au service des questions de recherche<br>
    Cas d'étude sur des archives diplomatiques (1940-1945)<br>
    <br>
    Auteur: <strong>Gérard Bottazzoli</strong> • Contact: <a href='mailto:gerard.bottazzoli@etu.unidistance.ch'>gerard.bottazzoli@etu.unidistance.ch</a><br>
    <br>
    13 tools opérationnels • Recherche multilingue FR/DE/EN • Neo4j Aura + Claude Sonnet 4.5
</div>
""", unsafe_allow_html=True)