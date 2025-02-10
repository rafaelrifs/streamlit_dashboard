# -- Importando bibliotecas
import streamlit as st  # Constroi app (Dashboasd)
import pandas as pd  # Manipula bases de dados
import plotly_express as px  # Constroi gráficos

# rodar app no console ->  streamlit run dashboards.py

# -- Definindo ícone e formato da página
st.set_page_config(
    page_title="Meu Dashboard",
    page_icon="📊",
    layout="wide",  # Define a página como "wide" (mais largo que o padrão)
)


# -- Importando base de dados
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")


# -- Colocando a coluna Date como data e ordenando por data
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# -- Concatenando duas colunas para fazer uma chave de data melhor
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

# -- Criando o select box de data na barra lateral
Month = st.sidebar.selectbox("Mês", df["Month"].unique())

# -- Usando o select box para filtrar os dados
df_filtered = df[df["Month"] == Month]

# -- Criando colunas no layout do Dashboard
col01, col02, col03, col04, col05 = st.columns(5, gap="medium")
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)


# -- Criando um gráfico de faturamento por dia
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City")
fig_date.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  # Fundo do gráfico transparente
    paper_bgcolor="rgba(0,0,0,0)",  # Fundo da área do gráfico (ao redor)
    xaxis=dict(showgrid=False),  # Opcional: desabilitar linhas de grade
    yaxis=dict(showgrid=False),
    # Opcional: desabilitar linhas de grade
)

col1.plotly_chart(fig_date, use_container_width=True)

# -- Criando um gráfico de faturamento produto
fig_prod = px.bar(
    df_filtered,
    x="Date",
    y="Product line",
    title="Faturamento por Produto",
    color="City",
    orientation="h",
)
fig_prod.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  # Fundo do gráfico transparente
    paper_bgcolor="rgba(0,0,0,0)",  # Fundo da área do gráfico (ao redor)
    xaxis=dict(showgrid=False),  # Opcional: desabilitar linhas de grade
    yaxis=dict(showgrid=False),  # Opcional: desabilitar linhas de grade
)
col2.plotly_chart(fig_prod, use_container_width=True)

# -- Criando um gráfico de faturamento Cidade
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()

fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por Filial")
fig_city.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  # Fundo do gráfico transparente
    paper_bgcolor="rgba(0,0,0,0)",  # Fundo da área do gráfico (ao redor)
    xaxis=dict(showgrid=False),  # Opcional: desabilitar linhas de grade
    yaxis=dict(showgrid=False),  # Opcional: desabilitar linhas de grade
)
col3.plotly_chart(fig_city, use_container_width=True)

# -- Criando um gráfico de faturamento por tipo de pagamento
fig_kind = px.pie(
    df_filtered,
    values="Total",
    names="Payment",
    title="Faturamento por Tipo de Pagamento",
)
fig_kind.update_traces(hole=0.4, hoverinfo="label+percent+name")
fig_kind.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  # Fundo do gráfico transparente
    paper_bgcolor="rgba(0,0,0,0)",  # Fundo da área do gráfico (ao redor)
    xaxis=dict(showgrid=False),  # Opcional: desabilitar linhas de grade
    yaxis=dict(showgrid=False),  # Opcional: desabilitar linhas de grade
)
col4.plotly_chart(fig_kind, use_container_width=True)

# -- Criando um gráfico de faturamento por Avaliação
Rating_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()

fig_rating = px.bar(Rating_total, x="City", y="Rating", title="Avaliação")
fig_rating.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  # Fundo do gráfico transparente
    paper_bgcolor="rgba(0,0,0,0)",  # Fundo da área do gráfico (ao redor)
    xaxis=dict(showgrid=False),  # Opcional: desabilitar linhas de grade
    yaxis=dict(showgrid=False),  # Opcional: desabilitar linhas de grade
)
col5.plotly_chart(fig_rating, use_container_width=True)

# ------------------------------------------------------------------------------------------------------ #

# -- Puxando as formatações css do arquivo Stlyes.css
import pathlib


def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS
css_path = pathlib.Path("Stlyes.css")
load_css(css_path)

# ---------------------------------------------  Fim  -------------------------------------------------- #


col01.metric("Temperature", "30°F", "-9°F", border=True)
col02.metric("Wind", "4 mph", "2 mph", border=True)

col03.metric("Humidity", "77%", "5%", border=True)
col04.metric("Pressure", "30.34 inHg", "-2 inHg", border=True)
col05.metric("Pressure", "30.34 inHg", "-2 inHg", border=True)


options = ["North", "East", "South"]
selection = st.sidebar.segmented_control(
    "Directions", options, selection_mode="multi", key="Seletor"
)
