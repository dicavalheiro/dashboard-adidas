import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Carregar o dataset
df = pd.read_excel("Adidas US Sales Datasets2.xlsx")

st.logo = "logo-adidas.png"

df["Invoice Date"] = pd.to_datetime(df["Invoice Date"])
df = df.sort_values("Invoice Date")

# Criar a coluna 'Month' como datetime
df['Month'] = pd.to_datetime(df['Invoice Date'].dt.to_period('M').astype(str))

# Criar uma lista de meses únicos formatados para exibição
month_options = ["Todos"] + df['Month'].dt.strftime('%Y-%m').unique().tolist()
selected_month = st.sidebar.selectbox("Selecione o mês", month_options)

# Filtrar pelo mês selecionado
if selected_month != "Todos":
    df_filtered = df[df['Month'].dt.strftime('%Y-%m') == selected_month]
else:
    df_filtered = df

# Criar lista de vendedores para seleção
seller_options = ["Todos"] + list(df["Seller"].unique())
vendedores = st.sidebar.selectbox("Vendedores", seller_options)

# Filtrar pelo vendedor selecionado
if vendedores != "Todos":
    df_filtered = df_filtered[df_filtered["Seller"] == vendedores]

# Layout das colunas
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)
col6, = st.columns(1)

# Gráficos
fat_por_categoria = df_filtered.groupby('Product')['Total Sales'].sum().sort_values(ascending=False).reset_index()
fig_cat = px.bar(fat_por_categoria, 
                 x='Product', 
                 y='Total Sales', 
                 title='Faturamento por Categoria',
                 template='plotly_white')
col1.plotly_chart(fig_cat, use_container_width=True)

fat_por_regiao = df_filtered.groupby(['Region', 'Product'])['Total Sales'].sum().reset_index()
fig_regiao = px.bar(fat_por_regiao, x="Region", y="Total Sales", color="Product", title="Faturamento por Região")
col2.plotly_chart(fig_regiao, use_container_width=True)

fat_vendedor = df_filtered.groupby("Seller")[["Total Sales"]].sum().reset_index()
fig_vendedor = px.bar(fat_vendedor, x="Seller", y="Total Sales",
                      title="Faturamento por Vendedor")
col3.plotly_chart(fig_vendedor, use_container_width=True)

fig_kind = px.pie(df_filtered, values="Total Sales", names="Sales Method",
                  title="Faturamento por tipo de venda")
col4.plotly_chart(fig_kind, use_container_width=True)

mean_price = df_filtered.groupby('Seller')['Total Sales'].mean().sort_values(ascending=True).reset_index()
fig_mean = px.bar(mean_price, x="Total Sales", y="Seller",
                  title="Preço Médio por Vendedor")
col5.plotly_chart(fig_mean, use_container_width=True)

fat_mes = df_filtered.groupby(['Month', 'Seller'])['Total Sales'].sum().reset_index()
fig_mes = px.line(fat_mes, x="Month", y="Total Sales", color="Seller", 
                  title="Faturamento Mensal por Vendedor")
col6.plotly_chart(fig_mes, use_container_width=True)