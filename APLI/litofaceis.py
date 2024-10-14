import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, mean_squared_error
import matplotlib.pyplot as plt

def app():
    # Verifique se os dados foram carregados na sessão
    if 'well_data' in st.session_state or 'csv_data' in st.session_state:
        st.title('Classificação Litológica por Clusterização')

        # Carregar os dados da sessão
        if st.session_state['file_type'] == 'LAS':
            data = st.session_state['well_data']
        elif st.session_state['file_type'] == 'CSV':
            data = st.session_state['csv_data']

        # Seleção da coluna de log GR
        log_gr_column = st.selectbox('Selecione a coluna de log GR', data.columns)

        # Remover dados ausentes
        data = data.dropna(subset=[log_gr_column])

        # Preparação dos dados
        X = data[[log_gr_column]].values
        
        # Normalização dos dados
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Escolha do número de clusters (litologias)
        num_clusters = st.slider('Selecione o número de clusters', min_value=2, max_value=10, value=3)

        # Inicialização do erro
        best_error = float('inf')
        best_kmeans = None

        # Loop para encontrar o melhor KMeans com erro reduzido
        for i in range(10):  # Tentar 10 inicializações diferentes para reduzir o erro
            kmeans = KMeans(n_clusters=num_clusters, random_state=i)
            kmeans.fit(X_scaled)
            clusters = kmeans.predict(X_scaled)
            error = mean_squared_error(X_scaled, kmeans.cluster_centers_[clusters])

            if error < best_error:
                best_error = error
                best_kmeans = kmeans

            if best_error <= 0.05:
                break  # Se atingir o erro desejado, pare o loop

        data['Cluster'] = best_kmeans.predict(X_scaled)

        # Exibir os resultados
        st.write('### Resultados da Clusterização')
        st.write(data[['DEPTH', 'Cluster']])

        # Calcular e exibir o erro e acurácia (se aplicável)
        st.write(f"Erro Médio Intra-Cluster: {best_error:.4f}")

        # Se houver uma verdade de terreno disponível, calcular a acurácia (Opcional)
        if 'true_labels' in data.columns:
            accuracy = precision_score(data['true_labels'], data['Cluster'], average='weighted')
            st.write(f"Acurácia: {accuracy:.4f}")

        # Criar mapeamento de cores para os clusters
        cluster_colors = {i: color for i, color in enumerate(
            ['yellow', 'brown', 'gray', 'green', 'blue', 'red', 'purple', 'orange', 'pink', 'cyan'][:num_clusters])}

        # Substituir os clusters pelos nomes das litologias, se necessário
        data['Cluster_Color'] = data['Cluster'].map(cluster_colors)

        # Opção para sobrepor o perfil original com a classificação
        overlay_option = st.checkbox('Sobrepor com o perfil original')

        # Plotagem dos resultados
        st.write('### Plotagem dos Resultados')
        fig, ax1 = plt.subplots(figsize=(10, 30))  # Aumente ainda mais o tamanho da figura

        if overlay_option:
            ax2 = ax1.twiny()  # Criar um segundo eixo X para sobrepor o perfil original

            # Plotar o perfil original (log GR)
            ax2.plot(data[log_gr_column], data['DEPTH'], color='blue', label=log_gr_column, linewidth=1)
            ax2.set_xlabel(log_gr_column)
            ax2.grid(False)
            ax2.legend(loc='upper right')

        # Plotar os clusters
        for depth, color in zip(data['DEPTH'], data['Cluster_Color']):
            ax1.plot([0.5, 1.5], [depth, depth], color=color, linewidth=12)  # Aumenta a largura das linhas e centraliza-as

        ax1.set_xlim(0, 2)
        ax1.set_xlabel('Cluster')
        ax1.set_ylabel('Profundidade')
        ax1.invert_yaxis()
        ax1.set_xticks([])
        st.pyplot(fig)

    else:
        st.write('Nenhum dado disponível. Por favor, faça o upload dos dados na página de importação.')

    # Caso os dados do usuário tenham coluna litológica, opção de aprendizado supervisionado
    if 'litologia' in data.columns:
        use_supervised = st.checkbox('Usar aprendizado supervisionado com a coluna de litologia')
        if use_supervised:
            st.write("Implementação de aprendizado supervisionado aqui...")

