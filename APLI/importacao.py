import streamlit as st
import lasio
import pandas as pd
from io import StringIO


@st.cache_data
def load_las_data(uploaded_file):
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.read()
            str_io = StringIO(bytes_data.decode('utf-8'))
            las_file = lasio.read(str_io)
            well_data = las_file.df()
            well_data['DEPTH'] = well_data.index
            # Remover dados ausentes
            well_data = well_data.dropna()
            return las_file, well_data
        except UnicodeDecodeError as e:
            st.error(f"Erro ao carregar o arquivo LAS: {e}")
            return None, None
    else:
        return None, None

@st.cache_data
def load_csv_data(uploaded_file):
    if uploaded_file is not None:
        try:
            csv_data = pd.read_csv(uploaded_file, delimiter=',')
            # Remover dados ausentes
            csv_data = csv_data.dropna()
            return csv_data
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo CSV: {e}")
            return None
    else:
        st.error("Nenhum arquivo CSV carregado.")
        return None

# Página de importação
def app():
    st.title("Página de Importação")  # Título sempre no topo

    # Escolha do formato de arquivo
    file_format = st.radio('Selecione o formato do arquivo', ('LAS', 'CSV'))
    uploaded_file = st.file_uploader('Carregar arquivo', type=['las', 'csv'])

    if file_format == 'CSV':
        csv_data = load_csv_data(uploaded_file)
        if csv_data is not None:
            st.success('Arquivo CSV carregado com sucesso')

            if 'DEPTH' not in csv_data.columns:
                st.warning("A coluna 'DEPTH' não foi encontrada no arquivo CSV.")
                if st.checkbox("Criar coluna 'DEPTH'?"):
                    csv_data['DEPTH'] = range(1, len(csv_data) + 1)
                else:
                    depth_column = st.selectbox('Selecione a coluna para usar como profundidade', csv_data.columns)
                    csv_data['DEPTH'] = csv_data[depth_column]
            
            st.session_state['csv_data'] = csv_data
            st.session_state['file_type'] = 'CSV'
            st.dataframe(csv_data)
        else:
            st.error('Falha ao carregar o arquivo CSV.')

    elif file_format == 'LAS':
        las_file, well_data = load_las_data(uploaded_file)
        if las_file:
            st.success('Arquivo LAS carregado com sucesso')
            st.write(f'<b>Nome do Poço</b>: {las_file.well.WELL.value}', unsafe_allow_html=True)
            st.session_state['well_data'] = well_data
            st.session_state['file_type'] = 'LAS'
            st.dataframe(well_data)
        else:
            st.error('Falha ao carregar o arquivo LAS.')
