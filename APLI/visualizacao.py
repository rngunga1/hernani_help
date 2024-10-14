import streamlit as st
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go

def app():
    # Verifica se os dados foram carregados
    if 'well_data' in st.session_state or 'csv_data' in st.session_state:
        st.title("Visualização de Dados - Estilo Well Logs")

        # Carregar os dados da sessão
        data = st.session_state['well_data'] if 'well_data' in st.session_state else st.session_state['csv_data']

        # Permitir que o usuário selecione a coluna que representa a profundidade
        depth_column = st.selectbox('Selecione a coluna que representa a profundidade', data.columns)

        # Selecione os perfis (colunas) para visualizar
        selected_columns = st.multiselect('Selecione os perfis para visualizar', data.columns.drop(depth_column))

        if selected_columns:
            # Criar subplots para exibir os gráficos lado a lado
            fig = sp.make_subplots(
                rows=1, cols=len(selected_columns),  # Definir o número de colunas com base no número de perfis
                shared_yaxes=True,  # Compartilhar o eixo Y (profundidade)
                horizontal_spacing=0.05,  # Espaçamento entre os gráficos
                subplot_titles=selected_columns  # Títulos dos subplots com base nos perfis selecionados
            )

            # Adicionar cada perfil em uma coluna separada
            for i, column in enumerate(selected_columns):
                fig.add_trace(
                    go.Scatter(x=data[column], y=data[depth_column], mode='lines', name=column),
                    row=1, col=i+1  # Adicionar na coluna correta
                )

                # Configurar o layout de cada gráfico individualmente
                fig.update_xaxes(title_text=f"{column}", row=1, col=i+1)
                fig.update_yaxes(autorange="reversed")  # Inverter o eixo Y (profundidade) para todos

            # Configurar o layout final
            fig.update_layout(
                height=800,  # Altura da figura
                width=800 * len(selected_columns),  # Largura da figura com base no número de gráficos
                showlegend=False,  # Ocultar legendas para não sobrecarregar
                title="Perfis Geofísicos Estilo Well Logs",
            )

            # Exibir o gráfico interativo
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Selecione pelo menos um perfil para visualizar.")
    else:
        st.error("Nenhum dado carregado. Por favor, vá para a página de importação para carregar os dados.")
