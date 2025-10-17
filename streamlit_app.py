import streamlit as st
from anthropic import Anthropic
import os

# Configuration de la page
st.set_page_config(
    page_title="Archives Diplomatiques Suisses - Graph RAG",
    page_icon="📚",
    layout="wide"
)

# Initialisation du client Anthropic
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Initialisation de l'état de session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# Titre principal
st.title("📚 Archives Diplomatiques Suisses 1940-1945")
st.markdown("*Assistant de recherche basé sur Graph RAG et modèles de langage*")

# Sidebar avec guide et boutons
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

    # Barre de progression
    sources_importees = 75
    sources_total = 191
    pourcentage = int((sources_importees / sources_total) * 100)

    st.markdown("### 📊 Progression de l'import")
    st.progress(pourcentage / 100)
    st.caption(f"{pourcentage}% • {sources_importees}/{sources_total} sources importées")
    st.caption("🎯 Objectif 100% : 14 novembre 2025")

    st.markdown("---")

    # Guide des requêtes
    st.markdown("### 📖 Guide des requêtes")

    st.markdown("#### 🔍 Recherches biographiques")
    st.markdown("""
    - "Biographie de [nom]"
    - "Chronologie de [nom]"
    - "Parcours de persécution de [nom]"
    - "Liste des personnes disponibles"
    """)

    st.markdown("#### 🔗 Chaînes de communication")
    st.markdown("""
    - "Chaîne de communication pour [nom]"
    - "Détails sur [année/mois] pour [nom]"
    - "Trouve des chaînes sur [thème]"
    - "Reconstitue la chaîne pour [nom] sur [thème]"
    """)

    st.markdown("#### 📊 Analyses globales")
    st.markdown("""
    - "Réactivité des autorités suisses ?"
    - "Acteurs principaux du réseau ?"
    - "Compare [nom1] et [nom2]"
    """)

    st.markdown("---")

    # Exemples de requêtes rapides
    st.markdown("### ⚡ Requêtes rapides")

    st.markdown("**📖 Biographie & Chronologie**")
    if st.button("📖 Biographie", key="bio", use_container_width=True):
        st.session_state.pending_query = "Biographie de Elisabeth Müller"

    if st.button("📅 Chronologie", key="chrono", use_container_width=True):
        st.session_state.pending_query = "Chronologie de Elisabeth Müller"

    st.markdown("**🔗 Chaînes de communication**")
    if st.button("🔗 Vue d'ensemble", key="chaine_vue", use_container_width=True):
        st.session_state.pending_query = "Chaîne de communication pour Elisabeth Müller"

    if st.button("📅 Détails 1942", key="chaine_1942", use_container_width=True):
        st.session_state.pending_query = "Détails sur 1942 pour Elisabeth Müller"

    if st.button("🔍 Recherche prison", key="recherche_prison", use_container_width=True):
        st.session_state.pending_query = "Trouve des chaînes sur prison"

    st.markdown("**📊 Analyses globales**")
    if st.button("⚡ Réactivité", key="reactivite", use_container_width=True):
        st.session_state.pending_query = "Réactivité des autorités suisses ?"

    if st.button("🌐 Acteurs principaux", key="analyse_acteurs", use_container_width=True):
        st.session_state.pending_query = "Acteurs principaux du réseau ?"

    if st.button("📋 Liste personnes", key="liste_personnes", use_container_width=True):
        st.session_state.pending_query = "Liste des personnes disponibles"

    st.markdown("---")

    # Bouton reset
    if st.button("🔄 Nouvelle conversation", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_query = None
        st.rerun()

# Zone de chat principale
chat_container = st.container()

# Afficher l'historique des messages
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Gestion de la requête en attente (depuis bouton sidebar)
if st.session_state.pending_query:
    user_query = st.session_state.pending_query
    st.session_state.pending_query = None

    # Afficher le message utilisateur
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_query)

    # Ajouter à l'historique
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Générer la réponse
    with chat_container:
        with st.chat_message("assistant"):
            with st.spinner("Recherche dans les archives..."):
                try:
                    response = client.messages.create(
                        model="claude-sonnet-4-5-20250929",
                        max_tokens=4096,
                        messages=st.session_state.messages
                    )

                    assistant_message = response.content[0].text
                    st.markdown(assistant_message)

                    # Ajouter à l'historique
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })

                except Exception as e:
                    st.error(f"Erreur lors de la génération de la réponse : {str(e)}")

# Input utilisateur (chat standard)
if prompt := st.chat_input("Posez votre question sur les archives..."):
    # Afficher le message utilisateur
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Ajouter à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Générer la réponse
    with chat_container:
        with st.chat_message("assistant"):
            with st.spinner("Recherche dans les archives..."):
                try:
                    response = client.messages.create(
                        model="claude-sonnet-4-5-20250929",
                        max_tokens=4096,
                        messages=st.session_state.messages
                    )

                    assistant_message = response.content[0].text
                    st.markdown(assistant_message)

                    # Ajouter à l'historique
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })

                except Exception as e:
                    st.error(f"Erreur lors de la génération de la réponse : {str(e)}")

# Footer
st.markdown("---")
st.caption(
    "💡 Astuce : Utilisez les boutons de la barre latérale pour des requêtes rapides ou tapez votre question directement.")