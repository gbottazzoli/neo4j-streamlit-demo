# streamlit_app.py
# Version 0.1.3 - Interface GraphRAG Tools Diplomatiques
# Auteur: Gérard Bottazzoli (gerard.bottazzoli@etu.unidistance.ch)

import streamlit as st
import requests
from typing import Optional

# -------------------------
# Configuration page
# -------------------------
st.set_page_config(
    page_title="Agent Neo4j Archives Suisses v0.1.3",
    page_icon="🤖",
    layout="wide",
)

# -------------------------
# En-tête sobre
# -------------------------
st.title("🤖 Agent conversationnel sur Graph Neo4j")
st.caption("Phase de test • Version 0.1.3")
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
# Sidebar : Menu Unique
# -------------------------
with st.sidebar:
    # === HEADER SIDEBAR ===
    st.markdown("---")

    # Titre du chatbot
    st.markdown("""
    ### 🤖 Chatbot de démonstration

    **Des archives fédérales à la base de données :**

    *Flux de travail numériques avec modèles de langage (locaux) et Graph RAG*

    **Une approche historian-in-the-loop**
    """)


    st.markdown("---")

    # Guide des requêtes
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

        Interrogez **1410 nœuds** d'archives diplomatiques suisses (1940-1945).

        **🎯 À tester** :
        - Parcours individuels
        - Chaînes de communication
        - Recherche thématique

        **📊 Corpus** :
        - 48 personnes
        - 202 micro-actions
        - 75 documents
        - 316 chunks vectorisés

        **⏱️ Temps** : 15-45 sec
        """)

    # ===========================
    # PARCOURS INDIVIDUELS
    # ===========================
    elif categorie == "📚 Parcours individuels":
        st.markdown("### 📚 Parcours de persécution")

        st.markdown("**🔵 Elisabeth Müller**")
        if st.button("📖 Biographie", key="bio_muller", use_container_width=True):
            st.session_state.pending_query = "Donne-moi la biographie d'Elisabeth Müller"
        if st.button("🎯 Parcours complet", key="parcours_muller", use_container_width=True):
            st.session_state.pending_query = "Décris le parcours de persécution d'Elisabeth Müller"

        st.markdown("**🔵 Autres personnes**")
        if st.button("📖 Nussbaumer", key="bio_nuss", use_container_width=True):
            st.session_state.pending_query = "Qui est Marcel Nussbaumer ?"
        if st.button("📖 de Pury", key="bio_pury", use_container_width=True):
            st.session_state.pending_query = "Qui est Gérard de Pury ?"

    # ===========================
    # CHAÎNES DE COMMUNICATION
    # ===========================
    elif categorie == "🔗 Chaînes de communication":
        st.markdown("### 🔗 Correspondances")

        if st.button("📊 Chaîne Müller", key="chaine_muller", use_container_width=True):
            st.session_state.pending_query = "Chaîne de communication pour Elisabeth Müller"
        if st.button("📅 Détails 1942", key="1942", use_container_width=True):
            st.session_state.pending_query = "Montre-moi les détails de 1942 pour Elisabeth Müller"
        if st.button("📅 Avril 1942", key="avril_1942", use_container_width=True):
            st.session_state.pending_query = "Détails sur avril 1942 pour Elisabeth Müller"
        if st.button("📅 Détails 1943", key="1943", use_container_width=True):
            st.session_state.pending_query = "Montre-moi 1943 pour Elisabeth Müller"

    # ===========================
    # RECHERCHE THÉMATIQUE
    # ===========================
    elif categorie == "🔍 Recherche thématique":
        st.markdown("### 🔍 Mots-clés")

        if st.button("🔍 Garde-meuble", key="garde_meuble", use_container_width=True):
            st.session_state.pending_query = "Trouve des infos sur les frais de garde-meuble"
        if st.button("🔍 Möbellager (DE)", key="mobellager", use_container_width=True):
            st.session_state.pending_query = "Trouve des chaînes sur Möbellager"
        if st.button("🔗 Chaîne garde-meuble", key="chaine_garde", use_container_width=True):
            st.session_state.pending_query = "Reconstitue la chaîne pour Elisabeth Müller sur les frais de garde-meuble"
        if st.button("💰 Argent", key="argent", use_container_width=True):
            st.session_state.pending_query = "Trouve des chaînes mentionnant de l'argent"
        if st.button("⚖️ Condamnation", key="condamnation", use_container_width=True):
            st.session_state.pending_query = "Trouve des infos sur les condamnations"
        if st.button("🔒 Prison", key="prison", use_container_width=True):
            st.session_state.pending_query = "Trouve des chaînes sur les prisons"

    # ===========================
    # ANALYSES GLOBALES
    # ===========================
    elif categorie == "📊 Analyses globales":
        st.markdown("### 📊 Statistiques")

        if st.button("📊 Liste personnes", key="liste", use_container_width=True):
            st.session_state.pending_query = "Quelles personnes sont disponibles ?"
        if st.button("🌐 Acteurs principaux", key="acteurs_principaux", use_container_width=True):
            st.session_state.pending_query = "Acteurs principaux du réseau ?"
        if st.button("⏱️ Réactivité", key="reactivite", use_container_width=True):
            st.session_state.pending_query = "Quelle est la réactivité des autorités suisses ?"

    # ===========================
    # COMPARAISONS
    # ===========================
    elif categorie == "⚖️ Comparaisons":
        st.markdown("### ⚖️ Comparaisons")

        if st.button("⚖️ Müller vs Nussbaumer", key="comp1", use_container_width=True):
            st.session_state.pending_query = "Compare Elisabeth Müller et Marcel Nussbaumer"
        if st.button("⚖️ Müller vs de Pury", key="comp2", use_container_width=True):
            st.session_state.pending_query = "Quelles sont les différences entre Elisabeth Müller et Gérard de Pury ?"

    st.divider()

    # Options
    with st.expander("⚙️ Options"):
        st.session_state.show_debug = st.checkbox("🔍 Debug", value=st.session_state.show_debug)
        if st.button("🗑️ Effacer"):
            st.session_state.messages = []
            st.rerun()



    st.markdown("---")

    # Barre de progression
    sources_importees = 75
    sources_total = 191
    pourcentage = int((sources_importees / sources_total) * 100)

    st.markdown("### 📊 Progression de l'import")
    st.progress(pourcentage / 100)
    st.caption(f"{pourcentage}% • {sources_importees}/{sources_total} sources importées")
    st.caption("🎯 Objectif 100% : 14 novembre 2025")


    # -------------------------
    # FOOTER DANS SIDEBAR (en bas, en petit)
    # -------------------------
    st.divider()
    st.markdown("""
    <div style='font-size: 0.75em; color: #888;'>
        <strong>GraphRAG Tools v0.1.3</strong><br>
        Des modèles de langage au service<br>
        des questions de recherche<br>
        <br>
        Archives diplomatiques 1940-1945<br>
        <br>
        <strong>Auteur:</strong> Gérard Bottazzoli<br>
        <a href='mailto:gerard.bottazzoli@etu.unidistance.ch' style='font-size: 0.9em;'>gerard.bottazzoli@etu.unidistance.ch</a><br>
        <br>
        <em>13 tools • FR/DE/EN<br>
        Neo4j + Claude Sonnet 4.5</em>
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
user_input = st.chat_input("💬 Pose ta question ici... (ou clique sur un exemple dans le menu)")

# -------------------------
# Traiter pending_query OU user_input
# -------------------------
query_to_process = None

# Priorité 1 : Query depuis bouton
if "pending_query" in st.session_state and st.session_state.pending_query:
    query_to_process = st.session_state.pending_query
    st.session_state.pending_query = None  # Clear immédiatement

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
        with st.spinner("🔎 Recherche en cours... (15-45 sec)"):

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
                        timeout=60
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
                    timeout_msg = "⏱️ Timeout (>60 sec)."
                    st.warning(timeout_msg)
                    st.session_state.messages.append({"role": "assistant", "content": timeout_msg})

                except Exception as e:
                    error_msg = f"❌ Erreur: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})