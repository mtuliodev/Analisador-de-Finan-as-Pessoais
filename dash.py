import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Dashboard de Finanças Pessoais",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Dashboard de Finanças Pessoais")

@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    """
    Carrega o CSV e realiza limpeza básica.
    Remove colunas desnecessárias e formata datas.
    """
    df = pd.read_csv(filepath)
    df = df.drop(columns=["ID"], errors="ignore")
    # Converter coluna Data para datetime
    df["Data"] = pd.to_datetime(df["Data"]).dt.date
    # Criar coluna Mês no formato YYYY-MM
    df["Mês"] = df["Data"].apply(lambda d: f"{d.year}-{d.month:02d}")
    # Filtrar apenas despesas
    df = df[df["Categoria"] != "Receitas"].copy()
    return df

@st.cache_data
def filter_data(
    df: pd.DataFrame,
    mes: str,
    categorias: list[str]
) -> pd.DataFrame:
    """
    Filtra DataFrame pelo mês e pelas categorias escolhidas.
    """
    df_filtered = df[df["Mês"] == mes]
    if categorias:
        df_filtered = df_filtered[df_filtered["Categoria"].isin(categorias)]
    return df_filtered

df = load_data("finances.csv")

# Sidebar de filtros
st.sidebar.header("Filtros")
available_months = sorted(df["Mês"].unique(), reverse=True)
selected_month = st.sidebar.selectbox(
    label="Selecionar Mês",
    options=available_months
)
all_categories = sorted(df["Categoria"].unique())
selected_categories = st.sidebar.multiselect(
    label="Categorias",
    options=all_categories,
    default=all_categories
)
# Aplicar filtros
df_filtered = filter_data(df, selected_month, selected_categories)


total_gasto = df_filtered["Valor"].sum()
media_transacoes = df_filtered["Valor"].mean() if not df_filtered.empty else 0
num_transacoes = len(df_filtered)
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric(label="Total Gasto (R$)", value=f"{total_gasto:,.2f}")
metric_col2.metric(label="Média por Transação (R$)", value=f"{media_transacoes:,.2f}")
metric_col3.metric(label="Número de Transações", value=str(num_transacoes))


tab_bar, tab_time = st.tabs([
    "Por Categoria",
    "Evolução Mensal"
])


with tab_bar:
    st.subheader("Gastos por Categoria")
    if df_filtered.empty:
        st.info("Nenhum gasto para o filtro selecionado.")
    else:
        df_bar = df_filtered[df_filtered["Categoria"].str.len() <= 35]
        if df_bar.empty:
            st.warning("Todas as categorias foram omitidas por excederem 35 caracteres.")
        else:
            bar_data = (
                df_bar.groupby("Categoria")["Valor"]
                .sum()
                .sort_values(ascending=True)
                .reset_index()
            )
            fig_bar = px.bar(
                bar_data,
                x="Valor",
                y="Categoria",
                orientation="h",
                text_auto=".2f",
                color="Categoria",
                color_discrete_sequence=px.colors.qualitative.Bold,
                labels={"Valor": "Total (R$)", "Categoria": ""},
            )
            fig_bar.update_layout(
                title_text="Total de Gastos por Categoria",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False, tickfont_size=14),
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)

with tab_time:
    st.subheader("Tendência Diária de Gastos")
    if df_filtered.empty:
        st.info("Nenhum gasto para o filtro selecionado.")
    else:
        time_data = (
            df_filtered.groupby("Data")["Valor"]
            .sum()
            .reset_index()
            .sort_values("Data")
        )
        fig_time = px.line(
            time_data,
            x="Data",
            y="Valor",
            markers=True,
            labels={"Data": "Data", "Valor": "Gasto Diário (R$)"},
            line_shape="spline",
        )
        fig_time.update_layout(
            title_text="Evolução Diária de Gastos",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)
        )
        st.plotly_chart(fig_time, use_container_width=True)

# Footer
st.markdown(
    "---\n"
    "Dashboard criado com Streamlit & Plotly."
)
