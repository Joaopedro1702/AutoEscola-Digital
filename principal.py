import streamlit as st
import pandas as pd
import plotly.express as ps

st.set_page_config(
    page_title="Auto Escola Digital",
    page_icon="📊",
    layout="wide"
)

st.title("Projeto integrador")
st.subheader("Aplicação de Ciência de Dados")

dados = pd.DataFrame({
    "Mes": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
    "Aulas": [35, 48, 42, 65, 58, 76]
})

alunos = pd.DataFrame({
    "Situacao": ["Ativos", "Concluidos", "Desistentes"],
    "Quantidade": [100, 48, 20]
})

#Menu lateral

st.sidebar.title("Auto Escola")
pagina = st.sidebar.selectbox(
    "Navegação",
    ["Dashboard", "Relatórios", "Sobre"]
)

#Página Dashboard

if pagina == "Dashboard":

    st.title("Paine de Controle")
    st.caption("Visão gera da autoescola")