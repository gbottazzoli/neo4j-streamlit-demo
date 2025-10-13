# streamlit_app.py
# Agent Conversationnel Neo4j Aura + Streamlit
# Version 2.0 - Interface guidée pour tests académiques

import streamlit as st
import requests
from typing import Optional

# -------------------------
# Configuration page
# -------------------------
st.set_page_config(
    page_title="Agent Archives Suisses",
    page_icon="🤖",
    layout="wide",
)

# -------------------------
# En-tête
# -------------------------
st.title("🤖 Agent Conversationnel - Archives Diplomatiques Suisses (1940-1945)")
st.caption("13 outils d'interrogation • 1410 nœuds • Recherche multilingue FR/DE")

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
        '```\n\n'
        'Obtiens CLIENT_ID et CLIENT_SECRET depuis : **Neo4j Aura Console → User Profile → API Keys**'
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
            st.error(f"❌ Erreur OAuth ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"❌ Erreur d'authentification: {str(e)}")
        return None


# -------------------------
# Initialiser historique
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Sidebar : Menu Unique de Requêtes Testables
# -------------------------
with st.sidebar:
    st.header("📖 Guide des Requêtes")
    st.caption("Clique sur un exemple pour le tester")

    # Menu déroulant par catégorie
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

        Ce système permet d'interroger 1410 nœuds d'archives diplomatiques suisses (1940-1945).

        **🎯 À tester en priorité** :
        - Parcours individuels (bio + chronologie)
        - Chaînes de communication
        - Recherche thématique multilingue

        **📊 Corpus** :
        - 48 personnes
        - 202 micro-actions diplomatiques
        - 75 documents sources
        - 316 chunks vectorisés

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
        if st.button("📝 Biographie de Müller"):
            st.session_state.query_to_send = "Donne-moi la biographie d'Elisabeth Müller"
            st.rerun()
        if st.button("📅 Chronologie de Müller"):
            st.session_state.query_to_send = "Quelle est la chronologie d'Elisabeth Müller ?"
            st.rerun()
        if st.button("🎯 Parcours complet de Müller"):
            st.session_state.query_to_send = "Décris le parcours de persécution d'Elisabeth Müller"
            st.rerun()

        st.markdown("**🔵 Autres personnes**")
        if st.button("📝 Biographie de Nussbaumer"):
            st.session_state.query_to_send = "Qui est Marcel Nussbaumer ?"
            st.rerun()
        if st.button("📝 Biographie de Pury"):
            st.session_state.query_to_send = "Qui est Gérard de Pury ?"
            st.rerun()

        st.info(
            "💡 **Format des réponses** :\n- Notice biographique enrichie\n- Occupations, origines, famille\n- Max 15 événements chronologiques\n- Flags reconstruction (⚠️) si source après 1946")

    # ===========================
    # CHAÎNES DE COMMUNICATION
    # ===========================
    elif categorie == "🔗 Chaînes de communication":
        st.markdown("### 🔗 Correspondances diplomatiques")
        st.caption("Reconstitution chronologique des échanges")

        st.markdown("**🔴 Vue d'ensemble** *(phases d'intensité)*")
        if st.button("📊 Chaîne de communication pour Müller"):
            st.session_state.query_to_send = "Chaîne de communication pour Elisabeth Müller"
            st.rerun()

        st.markdown("**🔴 Détails par période**")
        if st.button("📅 Détails sur 1942 pour Müller"):
            st.session_state.query_to_send = "Montre-moi les détails de 1942 pour Müller"
            st.rerun()
        if st.button("📅 Détails sur avril 1942"):
            st.session_state.query_to_send = "Détails sur avril 1942 pour Müller"
            st.rerun()
        if st.button("📅 Détails sur 1943"):
            st.session_state.query_to_send = "Montre-moi 1943 pour Elisabeth Müller"
            st.rerun()

        st.info(
            "💡 **Format des réponses** :\n- Phases d'intensité (🔵🔴🟠🟢)\n- Actions avec émetteur → destinataire\n- Sources avec cotes d'archives\n- Délais entre actions")

    # ===========================
    # RECHERCHE THÉMATIQUE
    # ===========================
    elif categorie == "🔍 Recherche thématique":
        st.markdown("### 🔍 Recherche par mots-clés")
        st.caption("Multilingue FR/DE automatique")

        st.markdown("**🟢 Recherche sémantique** *(via embeddings)*")
        if st.button("🔍 Frais de garde-meuble"):
            st.session_state.query_to_send = "Trouve des infos sur les frais de garde-meuble"
            st.rerun()
        if st.button("🔍 Möbellager (allemand)"):
            st.session_state.query_to_send = "Trouve des chaînes sur Möbellager"
            st.rerun()

        st.markdown("**🟢 Reconstitution thématique**")
        if st.button("🔗 Chaîne garde-meuble pour Müller"):
            st.session_state.query_to_send = "Reconstitue la chaîne pour Müller sur les frais de garde-meuble"
            st.rerun()

        st.markdown("**🟢 Autres thèmes testables**")
        if st.button("💰 Recherche sur 'argent'"):
            st.session_state.query_to_send = "Trouve des chaînes mentionnant de l'argent"
            st.rerun()
        if st.button("⚖️ Recherche 'condamnation'"):
            st.session_state.query_to_send = "Trouve des infos sur les condamnations"
            st.rerun()
        if st.button("🔒 Recherche 'prison'"):
            st.session_state.query_to_send = "Trouve des chaînes sur les prisons"
            st.rerun()

        st.info(
            "💡 **Multilingue automatique** :\n- 'garde-meuble' trouve aussi 'Möbellager', 'Effekten'\n- 316 chunks vectorisés (768D Gemini)\n- Recherche sémantique FR/DE/EN")

    # ===========================
    # ANALYSES GLOBALES
    # ===========================
    elif categorie == "📊 Analyses globales":
        st.markdown("### 📊 Statistiques et vues d'ensemble")
        st.caption("Analyses comparatives du corpus")

        st.markdown("**🟠 Vue globale**")
        if st.button("📊 Liste des personnes disponibles"):
            st.session_state.query_to_send = "Quelles personnes sont disponibles ?"
            st.rerun()
        if st.button("🔗 Vue globale des chaînes"):
            st.session_state.query_to_send = "Montre-moi les principales chaînes de communication"
            st.rerun()

        st.markdown("**🟠 Statistiques**")
        if st.button("⏱️ Réactivité des autorités suisses"):
            st.session_state.query_to_send = "Quelle est la réactivité des autorités suisses ?"
            st.rerun()

        st.info(
            "💡 **Analyses disponibles** :\n- Statistiques de réactivité (urgent/standard/lent/bloqué)\n- Vue comparative des chaînes\n- Délai moyen : 8,7 jours")

    # ===========================
    # COMPARAISONS
    # ===========================
    elif categorie == "⚖️ Comparaisons":
        st.markdown("### ⚖️ Comparaisons de parcours")
        st.caption("Analyse comparative entre deux personnes")

        if st.button("⚖️ Compare Müller et Nussbaumer"):
            st.session_state.query_to_send = "Compare Elisabeth Müller et Marcel Nussbaumer"
            st.rerun()
        if st.button("⚖️ Compare Müller et de Pury"):
            st.session_state.query_to_send = "Quelles sont les différences entre Müller et de Pury ?"
            st.rerun()

        st.info(
            "💡 **Format des comparaisons** :\n- Événements côte à côte par période\n- Points communs et différences\n- Synthèse comparative")

    st.divider()

    # Options avancées
    with st.expander("⚙️ Options"):
        show_debug = st.checkbox("🔍 Mode debug (JSON)", value=False)
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.messages = []
            st.rerun()

    st.divider()

    st.caption("""
    **⏱️ Temps** : 15-45 sec (normal)

    **📊 Corpus** : 
    • 48 personnes
    • 202 micro-actions
    • 75 documents
    • 316 chunks vectorisés

    **🔧 Tools** : 13 opérationnels
    """)

# -------------------------
# Afficher l'historique
# -------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------
# Gestion auto-remplissage depuis boutons
# -------------------------
if "query_to_send" in st.session_state:
    user_input = st.session_state.query_to_send
    del st.session_state.query_to_send

    # Afficher la question
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Traiter la requête
    process_query = True
else:
    process_query = False
    user_input = None

# -------------------------
# Input utilisateur manuel
# -------------------------
if not process_query:
    user_input = st.chat_input("💬 Pose ta question ici... (ou clique sur un exemple dans le menu)")

# -------------------------
# Traitement de la requête
# -------------------------
if user_input or process_query:

    if not process_query:
        # Afficher la question manuelle
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

    # Appeler l'API
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

                        if show_debug:
                            with st.expander("🔍 JSON brut (debug)"):
                                st.json(data)

                    elif response.status_code == 401:
                        error_msg = "🔒 Token expiré. Réessaie."
                        st.error(error_msg)
                        st.cache_data.clear()
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

                    else:
                        error_msg = f"❌ Erreur API ({response.status_code}): {response.text[:200]}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

                except requests.Timeout:
                    timeout_msg = "⏱️ Timeout (>60 sec). Réessaie avec une question plus simple."
                    st.warning(timeout_msg)
                    st.session_state.messages.append({"role": "assistant", "content": timeout_msg})

                except Exception as e:
                    error_msg = f"❌ Erreur: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

# -------------------------
# Footer
# -------------------------
st.divider()
st.caption(
    "💡 GraphRAG Tools Diplomatiques v1.0 • 13 tools opérationnels • Recherche multilingue FR/DE/EN • "
    "Documentation technique disponible"
)