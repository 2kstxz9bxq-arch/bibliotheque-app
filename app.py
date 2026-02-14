import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Bibliothèque", layout="wide")

if "abonnes" not in st.session_state:
    st.session_state.abonnes = []
if "livres" not in st.session_state:
    st.session_state.livres = []
if "emprunts" not in st.session_state:
    st.session_state.emprunts = []
if "reservations" not in st.session_state:
    st.session_state.reservations = []

menu = st.sidebar.radio("Navigation",[
    "Tableau de bord",
    "Livres",
    "Abonnés",
    "Emprunts",
    "Classement"
])

# -------- DASHBOARD --------

if menu=="Tableau de bord":
    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Total Livres", len(st.session_state.livres))
    col2.metric("Abonnés", len(st.session_state.abonnes))
    col3.metric("Emprunts actifs", len(st.session_state.emprunts))
    col4.metric("Réservations", len(st.session_state.reservations))

# -------- LIVRES --------

elif menu=="Livres":
    st.subheader("Ajouter Livre")
    code = st.text_input("Code")
    titre = st.text_input("Titre")
    auteur = st.text_input("Auteur")
    edition = st.text_input("Edition")
    nb = st.number_input("Nb Exemplaires")

    if st.button("Ajouter Livre"):
        st.session_state.livres.append({
            "Code":code,
            "Titre":titre,
            "Auteur":auteur,
            "Edition":edition,
            "Nb":nb
        })

    st.dataframe(pd.DataFrame(st.session_state.livres))

# -------- ABONNES --------

elif menu=="Abonnés":
    st.subheader("Ajouter Abonné")
    id = st.number_input("ID")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prenom")
    annee = st.number_input("Année")

    if st.button("Ajouter"):
        st.session_state.abonnes.append({
            "ID":id,
            "Nom":nom,
            "Prenom":prenom,
            "NbLivres":0,
            "Score":0
        })

    st.dataframe(pd.DataFrame(st.session_state.abonnes))

# -------- EMPRUNT --------

elif menu=="Emprunts":
    id = st.number_input("ID Abonné")
    code = st.text_input("Code Livre")

    if st.button("Emprunter"):
        for livre in st.session_state.livres:
            if livre["Code"]==code and livre["Nb"]>0:
                livre["Nb"]-=1
                st.session_state.emprunts.append({
                    "ID":id,
                    "Code":code,
                    "Date":date.today()
                })
                for a in st.session_state.abonnes:
                    if a["ID"]==id:
                        a["NbLivres"]+=1

    st.dataframe(pd.DataFrame(st.session_state.emprunts))

# -------- CLASSEMENT --------

elif menu=="Classement":
    for a in st.session_state.abonnes:
        a["Score"]=(a["NbLivres"]//3)*10

    df=pd.DataFrame(st.session_state.abonnes)
    df=df.sort_values(by="Score",ascending=False)
    st.dataframe(df.head(3))
