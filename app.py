import streamlit as st
import pandas as pd

st.title("📚 Gestion Bibliothèque Universitaire")

if "abonnes" not in st.session_state:
    st.session_state.abonnes = []

menu = st.sidebar.selectbox("Menu", [
    "Ajouter Abonné",
    "Calculer Score",
    "Classement"
])

if menu == "Ajouter Abonné":
    id = st.number_input("ID")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prenom")
    annee = st.number_input("Année d'étude")

    if st.button("Ajouter"):
        st.session_state.abonnes.append({
            "ID": id,
            "Nom": nom,
            "Prenom": prenom,
            "NbLivres": 0,
            "Score": 0
        })
        st.success("Abonné ajouté!")

elif menu == "Calculer Score":
    for a in st.session_state.abonnes:
        nb = st.number_input(f"Nb Livres pour {a['Nom']}", 0)
        a["NbLivres"] = nb
        a["Score"] = (nb // 3) * 10

elif menu == "Classement":
    df = pd.DataFrame(st.session_state.abonnes)
    df = df.sort_values(by="Score", ascending=False)
    st.write("🏆 Top Lecteurs")
    st.dataframe(df.head(3))
