import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÃO DA APLICAÇÃO
st.set_page_config(
    page_title="Auto Escola Digital",
    page_icon="🚘",
    layout="wide"
)

# CSS - IDENTIDADE VISUAL
st.markdown("""
<style>
.stApp {
    background-color: #171717;
    color: #FFFFFF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

.dashboard-title(
    color: #FFFF !important;
)

.relatorios-title(
    color: #FACC15 !important;
)

.sobre-title(
    color: #FFFF !important;
)

p, label {
    color: #262626;
}

.header {
    background: linear-gradient(90deg, #0A0A0A, #262626);
    border-bottom: 4px solid #FACC15;
    padding: 22px 30px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.header-title {
    color: #FACC15 !important;
    font-size: 25px;
    font-weight: 800;
    margin: 0;
}

.header-subtitle {
    color: #D4D4D4 !important;
    font-size: 13px;
    margin-top: 5px;
}

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    border-bottom: 5px solid #FACC15;
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricValue"] {
    color: #171717 !important;
}

.stButton > button {
    background-color: #FACC15;
    color: #171717;
    border: none;
    border-radius: 8px;
    font-weight: 700;
}

.stButton > button:hover {
    background-color: #EAB308;
    color: #171717;
    border: none;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #FACC15;
    border-radius: 10px;
}

hr {
    border-color: #FACC15;
}

a {
    color: #FACC15 !important;
}
/* Corrigir a cor dos títulos dos cards */
[data-testid="stMetricLabel"] {
    color: #262626 !important;
}

/* Corrigir a cor dos valores dos cards */
[data-testid="stMetricValue"] {
    color: #262626 !important;
}

/* Corrigir o texto auxiliar dos cards */
[data-testid="stMetricDelta"] {
    color: #404040 !important;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="header">
    <div>
        <p class="header-title">🚘 AUTO ESCOLA DIGITAL</p>
        <p class="header-subtitle">Sistema de análise de dados SENATRAN</p>
    </div>
</div>
""", unsafe_allow_html=True)

# NAVEGAÇÃO SEM SIDEBAR
pagina = st.radio(
    "Navegação",
    ["Dashboard", "Relatórios", "Sobre"],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

# CARREGAMENTO DOS DADOS
@st.cache_data
def carregar_dados():
    return pd.read_excel("dados/dados_senatran_tratados.xlsx")

try:
    df = carregar_dados()
except FileNotFoundError:
    st.error(
        "Não foi possível encontrar o arquivo dados/dados_senatran_tratados.xlsx. "
        "Verifique se ele está dentro da pasta 'dados' do projeto."
    )
    st.stop()

coluna_valor = "Qt. Condutor Histórico"

# Confere se as colunas necessárias existem na planilha.
colunas_necessarias = [
    "Região Habilitação Atual",
    "UF Habilitação Atual",
    "Sexo",
    "Faixa Etária",
    "Categoria",
    coluna_valor
]

colunas_ausentes = [coluna for coluna in colunas_necessarias if coluna not in df.columns]

if colunas_ausentes:
    st.error(f"Colunas não encontradas na planilha: {', '.join(colunas_ausentes)}")
    st.stop()

# PÁGINA DASHBOARD
if pagina == "Dashboard":

    st.title("Painel de Controle")
    st.caption("Visão geral dos dados da SENATRAN")

    # Indicadores
    total_condutores = df[coluna_valor].sum()
    total_registros = len(df)
    total_estados = df["UF Habilitação Atual"].nunique()
    total_categorias = df["Categoria"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Condutores históricos", f"{total_condutores:,.0f}")
    col2.metric("Registros", f"{total_registros:,}")
    col3.metric("Estados", total_estados)
    col4.metric("Categorias CNH", total_categorias)

    st.divider()

    # Condutores por região
    st.subheader("Condutores por Região")
    regiao = df.groupby("Região Habilitação Atual", as_index=False)[coluna_valor].sum()
    fig_regiao = px.bar(
        regiao,
        x="Região Habilitação Atual",
        y=coluna_valor,
        color_discrete_sequence=["#FACC15"],
        title="Quantidade de condutores por região"
    )
    fig_regiao.update_layout(template="plotly_dark")
    st.plotly_chart(fig_regiao, use_container_width=True)

    st.divider()

    # Condutores por estado
    st.subheader("Condutores por Estado")
    estado = df.groupby("UF Habilitação Atual", as_index=False)[coluna_valor].sum()
    fig_estado = px.bar(
        estado,
        x="UF Habilitação Atual",
        y=coluna_valor,
        color_discrete_sequence=["#FACC15"],
        title="Quantidade de condutores por estado"
    )
    fig_estado.update_layout(template="plotly_dark")
    st.plotly_chart(fig_estado, use_container_width=True)

    st.divider()

    # Distribuição por sexo
    st.subheader("Distribuição por Sexo")
    sexo = df.groupby("Sexo", as_index=False)[coluna_valor].sum()
    fig_sexo = px.pie(
        sexo,
        names="Sexo",
        values=coluna_valor,
        title="Distribuição de condutores por sexo",
        color_discrete_sequence=["#FACC15", "#FFFFFF"]
    )
    fig_sexo.update_layout(template="plotly_dark")
    st.plotly_chart(fig_sexo, use_container_width=True)

    st.divider()

    # Condutores por faixa etária
    st.subheader("Condutores por Faixa Etária")
    idade = df.groupby("Faixa Etária", as_index=False)[coluna_valor].sum()
    fig_idade = px.bar(
        idade,
        x="Faixa Etária",
        y=coluna_valor,
        color_discrete_sequence=["#FACC15"],
        title="Distribuição por faixa etária"
    )
    fig_idade.update_layout(template="plotly_dark")
    st.plotly_chart(fig_idade, use_container_width=True)

    st.divider()

    # Condutores por categoria de CNH
    st.subheader("Categorias de CNH")
    categoria = df.groupby("Categoria", as_index=False)[coluna_valor].sum()
    fig_categoria = px.bar(
        categoria,
        x="Categoria",
        y=coluna_valor,
        color_discrete_sequence=["#FACC15"],
        title="Quantidade de condutores por categoria"
    )
    fig_categoria.update_layout(template="plotly_dark")
    st.plotly_chart(fig_categoria, use_container_width=True)

# =====================================
# PÁGINA RELATÓRIOS
# =====================================
elif pagina == "Relatórios":
    st.title("Relatórios")
    st.caption("Consulta dos dados utilizados no projeto")

    st.subheader("Base de dados SENATRAN")
    st.dataframe(df, use_container_width=True)
    st.write(f"Total de registros encontrados: {len(df)}")

# =====================================
# PÁGINA SOBRE
# =====================================
elif pagina == "Sobre":
    st.title("Sobre o Projeto")

    st.markdown("""
    ### Auto Escola Digital

    Projeto Integrador desenvolvido com Python e Streamlit.

    **Objetivo:**

    Desenvolver uma aplicação para visualização e análise de dados
    relacionados aos condutores e às categorias de habilitação.

    **Fonte de dados:** SENATRAN.

    **Tecnologias utilizadas:**
    - Python
    - Streamlit
    - Pandas
    - Plotly
    - Excel
    """)
