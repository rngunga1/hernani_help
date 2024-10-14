import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def app():
    # Verifique se os dados foram carregados na sessão
    if 'well_data' in st.session_state or 'csv_data' in st.session_state:
        st.title('Estatísticas dos Perfis')

        # Carregar os dados da sessão
        if st.session_state['file_type'] == 'LAS':
            data = st.session_state['well_data']
        elif st.session_state['file_type'] == 'CSV':
            data = st.session_state['csv_data']

        # Exibir as estatísticas descritivas dos dados originais
        st.write('### Estatísticas Descritivas (com dados ausentes)')
        st.write(data.describe())

        # Remover os dados ausentes
        data_no_na = data.dropna()

        # Exibir as estatísticas descritivas dos dados sem valores ausentes
        st.write('### Estatísticas Descritivas (sem dados ausentes)')
        st.write(data_no_na.describe())

        # Seleção de coluna para a visualização de gráficos estatísticos
        selected_column = st.selectbox('Selecione a coluna para visualizar as estatísticas', data.columns)

        # Gráfico de histograma
        st.write(f'### Histograma de {selected_column}')
        fig, ax = plt.subplots()
        sns.histplot(data_no_na[selected_column], bins=30, kde=True, ax=ax)
        ax.set_title(f'Histograma de {selected_column}')
        ax.set_xlabel(selected_column)
        ax.set_ylabel('Frequência')
        st.pyplot(fig)

        # Gráfico de boxplot
        st.write(f'### Boxplot de {selected_column}')
        fig, ax = plt.subplots()
        sns.boxplot(y=data_no_na[selected_column], ax=ax)
        ax.set_title(f'Boxplot de {selected_column}')
        ax.set_ylabel(selected_column)
        st.pyplot(fig)
        
        # Seleção de colunas para criar o gráfico de dispersão
        x_column = st.selectbox('Selecione a coluna X para o gráfico de dispersão', data.columns)
        y_column = st.selectbox('Selecione a coluna Y para o gráfico de dispersão', data.columns)

        # Criar gráfico de dispersão usando Seaborn
        st.write('### Gráfico de Dispersão')
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x=x_column, y=y_column, ax=ax)
        ax.set_title(f'Dispersão de {x_column} vs {y_column}')
        st.pyplot(fig)

    else:
        st.error('Nenhum dado disponível. Por favor, faça o upload dos dados na página de importação.')
