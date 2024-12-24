import streamlit as st
import pandas as pd


st.set_page_config(page_title="Data Viewer", layout="wide")
st.title("Data Viewer")


@st.cache_data
def load_data(file):
    file_extension = file.name.split(".")[-1].lower()
    if file_extension == "csv":
        return pd.read_csv(file)
    elif file_extension == "json":
        return pd.read_json(file)
    elif file_extension == "xlsx":
        return pd.read_excel(file)
    else:
        raise ValueError("Formato de arquivo não suportado.")

# Função para exibir tabela com paginação
def display_paginated_table(data, page, rows_per_page=10):
    start_idx = page * rows_per_page
    end_idx = start_idx + rows_per_page
    st.dataframe(data.iloc[start_idx:end_idx])

# Upload do arquivo
uploaded_file = st.file_uploader(
    "Escolha um arquivo para carregar", 
    type=["txt", "csv", "json", "xlsx"]
)

if uploaded_file:
    try:
        # Carregar o arquivo com cache
        data = load_data(uploaded_file)

        # Seleção de coluna para pesquisa
        column_to_search = st.selectbox("Selecione uma coluna para pesquisar:", data.columns)

        # Campo de pesquisa
        search_query = st.text_input(f"Digite o termo a ser pesquisado na coluna '{column_to_search}':")

        # Aplicar o filtro de pesquisa
        if search_query:
            filtered_data = data[data[column_to_search].astype(str).str.contains(search_query, case=False, na=False)]
        else:
            filtered_data = data

        # Paginação da tabela
        rows_per_page = 10
        total_rows = filtered_data.shape[0]
        total_pages = (total_rows // rows_per_page) + (1 if total_rows % rows_per_page != 0 else 0)

        # Controle de página
        st.write(f"Total de registros filtrados: {total_rows}")
        current_page = st.number_input(
            "Selecione a página:",
            min_value=0, max_value=max(0, total_pages - 1), value=0, step=1
        )

        # Exibir tabela paginada
        display_paginated_table(filtered_data, current_page, rows_per_page)

        # Seleção de colunas para o gráfico
        st.write("Selecione as colunas para o gráfico:")

        # Opções para eixo X
        x_axis = st.selectbox("Selecione a coluna para o eixo X:", data.columns)

        # Opções para eixo Y
        y_axis = st.selectbox("Selecione a coluna para o eixo Y:", data.select_dtypes(include=["number"]).columns)

        # Exibir o gráfico
        if x_axis and y_axis:
            st.write("Gráfico baseado nas colunas selecionadas:")
            st.line_chart(filtered_data.set_index(x_axis)[y_axis])

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.info("Faça o upload de um arquivo para começar.")
