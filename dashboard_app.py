import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados preparados
@st.cache_data
def load_data():
    df = pd.read_csv("/home/ubuntu/dados_preparados.csv", parse_dates=["Data"])
    return df

df = load_data()

st.set_page_config(layout="wide")
st.title("Dashboard Monitor do Fogo")

# Filtros na barra lateral
st.sidebar.header("Filtros")

# Filtro de Bioma
biomas_disponiveis = ["Todos"] + sorted(df["Bioma"].unique().tolist())
bioma_selecionado = st.sidebar.selectbox("Selecione o Bioma", biomas_disponiveis)

# Filtrar dados por Bioma
if bioma_selecionado != "Todos":
    df_filtrado_bioma = df[df["Bioma"] == bioma_selecionado].copy()
else:
    df_filtrado_bioma = df.copy()

# Filtro de Estado (dependente do Bioma selecionado)
estados_disponiveis = ["Todos"] + sorted(df_filtrado_bioma["Estados"].unique().tolist())
estado_selecionado = st.sidebar.selectbox("Selecione o Estado", estados_disponiveis)

# Filtrar dados por Estado
if estado_selecionado != "Todos":
    df_final_filtrado = df_filtrado_bioma[df_filtrado_bioma["Estados"] == estado_selecionado].copy()
else:
    df_final_filtrado = df_filtrado_bioma.copy()

st.sidebar.markdown("---_---")
st.sidebar.markdown("**Observação:** A série temporal abaixo considera os filtros de Bioma e Estado selecionados.")

# Visualização da série temporal
st.subheader(f"Série Temporal da Área Queimada (ha) por Nível 0")

if not df_final_filtrado.empty:
    # Agrupar dados por Data e Nível 0, somando a Área Queimada
    df_serie_temporal = df_final_filtrado.groupby([pd.Grouper(key=
'Data
', freq=
'M
'), "Nível 0"])["Area_Queimada_ha"].sum().reset_index()

    fig = px.line(df_serie_temporal, x="Data", y="Area_Queimada_ha", color="Nível 0",
                  title="Área Queimada Mensal por Nível 0 (Antrópico/Natural)",
                  labels={"Area_Queimada_ha": "Área Queimada (ha)", "Data": "Mês/Ano"})
    
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Dados Filtrados")
    st.dataframe(df_final_filtrado.head(100), height=300) # Mostra as primeiras 100 linhas dos dados filtrados

else:
    st.warning("Nenhum dado disponível para os filtros selecionados.")

# Informações adicionais
st.markdown("---_---")
st.markdown("Desenvolvido por Manus AI")

