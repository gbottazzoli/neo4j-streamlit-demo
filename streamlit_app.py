# streamlit_app.py
# Agent Conversationnel Neo4j Aura + Streamlit
# Documentation: https://neo4j.com/developer/genai-ecosystem/aura-agent/

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
st.title("🤖 Agent Conversationnel - Archives Diplomatiques Suisses")
st.caption("Base de connaissances Neo4j • Période 1940-1945 • Réponses en 15-45 secondes")

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
@st.cache_data(ttl=3600)  # Cache 1h
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
# Sidebar : Instructions
# -------------------------
with st.sidebar:
    st.header("📚 Guide d'utilisation")

    st.subheader("🎯 Questions types")
    st.markdown("""
    **Biographie simple**
    - Qui est Elisabeth Müller ?
    - Donne la biographie de Marcel Nussbaumer

    **Parcours de persécution**
    - Quel est le parcours de persécution de Müller ?
    - Décris les événements de Nussbaumer

    **Comparaison**
    - Compare Müller et Nussbaumer
    - Différences entre Müller et de Pury ?

    **Exploration**
    - Quelles personnes sont disponibles ?
    - Y a-t-il plusieurs de Pury ?
    """)

    st.divider()

    if st.button("🗑️ Effacer l'historique"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("""
    **⏱️ Temps de réponse** : 15-45 sec (normal)

    **🔍 Sources** : ~50 personnes documentées

    **📊 Flags sources** :
    - Pas de flag = source 1940-1945 ✅
    - (reconstruction) = source 1946+ ⚠️
    """)

# -------------------------
# Afficher l'historique des messages
# -------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------
# Input utilisateur
# -------------------------
if user_input := st.chat_input("Pose ta question ici... (ex: Qui est Elisabeth Müller ?)"):

    # Afficher la question de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Appeler l'API Neo4j Aura Agent
    with st.chat_message("assistant"):
        with st.spinner("🔍 Recherche en cours... (15-45 sec)"):

            # 1. Obtenir le bearer token
            bearer_token = get_bearer_token(CLIENT_ID, CLIENT_SECRET)

            if not bearer_token:
                error_msg = "❌ Impossible d'obtenir le token d'authentification. Vérifie CLIENT_ID et CLIENT_SECRET."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                try:
                    # 2. Appeler l'agent avec le token
                    response = requests.post(
                        AGENT_ENDPOINT,
                        headers={
                            'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'Authorization': f'Bearer {bearer_token}'
                        },
                        json={'input': user_input},  # ← IMPORTANT: "input" pas "message"
                        timeout=60
                    )

                    if response.status_code == 200:
                        data = response.json()

                        # Extraire la réponse (adapter selon structure)
                        answer = (
                                data.get("output") or
                                data.get("response") or
                                data.get("result") or
                                str(data)
                        )

                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})

                    elif response.status_code == 401:
                        error_msg = "🔑 Token expiré ou invalide. Réessaie (le cache va se rafraîchir)."
                        st.error(error_msg)
                        st.cache_data.clear()  # Clear cache du token
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

                    elif response.status_code == 404:
                        error_msg = "🔍 Agent non trouvé. Vérifie l'URL de l'endpoint."
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

                    else:
                        error_msg = f"❌ Erreur API ({response.status_code}): {response.text[:200]}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

                except requests.Timeout:
                    timeout_msg = "⏱️ Timeout (>60 sec). L'agent met trop de temps. Réessaie avec une question plus simple."
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
st.caption("💡 Documentation: https://neo4j.com/developer/genai-ecosystem/aura-agent/")