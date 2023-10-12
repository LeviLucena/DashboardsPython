import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Use o widget st.markdown para inserir o link para o arquivo CSS externo
st.markdown(
    '<link rel="stylesheet" type="text/css" href="style.css">',
    unsafe_allow_html=True
)

# Adicione a logo
st.sidebar.image("logo.png", use_column_width=True)

# Adicione um cabeçalho com uma logo
st.sidebar.header("Filtros")

# Com uma visão mensal
#faturamento por unidade… 
# tipo de produto mais vendido, contribuição por filial,
#Desempenho das forma de pagamento…
#Como estão as avaliações das filiais?

# Carregue o arquivo de dados
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df=df.sort_values("Date")

# Filtros por mês
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())
df_filtered = df[df["Month"] == month]

# Filtros por City, Gender e Payment
city = [st.sidebar.selectbox("Filtrar por Cidade", df["City"].unique())]
gender = [st.sidebar.selectbox("Filtrar por Genêro", df["Gender"].unique())]
payment = [st.sidebar.selectbox("Filtrar por Pagamento", df["Payment"].unique())]

# Aplicar os filtros selecionados
filtered_df = df_filtered[
    (df_filtered["City"].isin(city)) &
    (df_filtered["Gender"].isin(gender)) &
    (df_filtered["Payment"].isin(payment))
]

# Exibir gráficos com base nos filtros
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, x="Date", y="Product line", 
                  color="City", title="Faturamento por tipo de produto",
                  orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)


city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total",
                   title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)


fig_kind = px.pie(df_filtered, values="Total", names="Payment",
                   title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)


city_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(df_filtered, y="Rating", x="City",
                   title="Avaliação")
col5.plotly_chart(fig_rating, use_container_width=True)

# Adicione o rodapé com a imagem
st.image("rodape_preto.png", use_column_width=True)