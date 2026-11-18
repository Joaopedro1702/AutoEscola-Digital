from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Tráfego - Autoescola Digital", layout="wide")

arquivo = Path(__file__).parent / "dados_trafego.csv"


def numero(texto):

    t = texto.split()[0].replace("%", "").replace("#", "")

    if ":" in t:

        h, m, s = t.split(":")

        return int(h) * 3600 + int(m) * 60 + int(s)
    
    if t.endswith("K"):

        return float(t[:-1]) * 1000
    try:

        return float(t)
    
    except ValueError:
        
        return None


linhas = arquivo.read_text(encoding="utf-8-sig").splitlines()[1:]
dados = pd.DataFrame(
    [l.rsplit(",", 3) for l in linhas if l.strip()],
    columns=["secao", "dominio", "metrica", "texto"],
)
dados["valor"] = dados["texto"].map(numero)


def pegar(secao):

    return dados[dados["secao"].str.startswith(secao)]


def serie(secao):

    return pegar(secao).set_index("dominio")["valor"]


st.title("Tráfego - Autoescola Digital")

st.caption("Comparativo entre os sites, entre set-out de 2026")

visitas = serie("Engagement - Visits")

views = serie("Engagement - Page Views")

duracao = serie("Engagement - Duration")

paginas = serie("Engagement - Pages/Visit")

rejeicao = serie("Engagement - Bounce Rate")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Visitas", f"{visitas.sum():,.0f}".replace(",", "."))

col2.metric("Page views", f"{views.sum():,.0f}".replace(",", "."))

col3.metric("Duração média", f"{duracao.mean() / 60:.1f} min")

col4.metric("Rejeição média", f"{rejeicao.mean():.1f}%")

aba1, aba2, aba3, aba4 = st.tabs(
    ["Visão geral", "Dispositivos", "Canais", "Países e categorias"]
)

with aba1:

    esq, dir = st.columns(2)

    esq.subheader("Visitas")

    esq.bar_chart(visitas, horizontal=True)

    dir.subheader("Page views")

    dir.bar_chart(views, horizontal=True)

    a, b, c = st.columns(3)

    a.subheader("Duração (min)")

    a.bar_chart(duracao / 60, horizontal=True)

    b.subheader("Páginas por visita")

    b.bar_chart(paginas, horizontal=True)

    c.subheader("Rejeição (%)")

    c.bar_chart(rejeicao, horizontal=True)

    st.subheader("Ranking no Brasil")

    ranking = pegar("Rank by Country").sort_values("valor")

    st.dataframe(ranking[["dominio", "texto"]], hide_index=True)

with aba2:

    st.subheader("Desktop x Mobile (%)")

    disp = pd.concat([pegar("Device Distribution (Desktop"), pegar("Device Distribution (Mobile")])

    tabela = disp.pivot(index="dominio", columns="metrica", values="valor")

    st.bar_chart(tabela, horizontal=True)

    st.dataframe(tabela)

with aba3:

    st.subheader("Canal que mais traz visitas")

    canais = dados[dados["secao"].str.startswith("Canal - ")].copy()

    canais["canal"] = canais["secao"].str.replace("Canal - ", "")

    st.bar_chart(canais, x="canal", y="valor", color="dominio", horizontal=True)

    st.dataframe(canais[["dominio", "canal", "texto"]], hide_index=True)

    st.subheader("Referências")

    refs = pegar("Referências")

    st.dataframe(refs[["dominio", "metrica", "texto"]], hide_index=True)

with aba4:

    esq, dir = st.columns(2)

    esq.subheader("Tráfego por país")

    paises = pegar("Traffic share por país").set_index("dominio")["valor"]

    esq.bar_chart(paises, horizontal=True)

    dir.subheader("Categorias do site (%)")

    cats = dados[dados["secao"] == "Categorias do Website"]

    dir.bar_chart(cats, x="metrica", y="valor", color="dominio", horizontal=True)