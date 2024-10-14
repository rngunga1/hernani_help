import streamlit as st
import os

# Configurações do App
image_path = os.path.join(os.path.dirname(__file__), "Imagem", "WhatsApp Image 2024-09-29 at 02.22.00.jpeg")

st.set_page_config(page_title="PYGEOPLOT", page_icon=image_path, layout="wide")

# Definindo a navegação
with st.sidebar:
    escolha = st.selectbox(
        "Menu Principal", 
        ["Importação", "Visualização", "Estatística", "Classificação de Litofacies", "Conversão", "Cálculo Petrofísico", "Autores do Aplicativo"]
    )
    st.image(image_path, use_column_width=True, caption="PYGEOPLOT")

# Lógica de navegação entre páginas
if escolha == "Importação":
    import importacao
    importacao.app()

elif escolha == "Visualização":
    import visualizacao
    visualizacao.app()

elif escolha == "Estatística":
    import estatistica
    estatistica.app()

elif escolha == "Classificação de Litofacies":
    import litofaceis
    litofaceis.app()

elif escolha == "Conversão":
    import conversao
    conversao.app()

elif escolha == "Cálculo Petrofísico":
    import calculopetrofisico
    calculopetrofisico.app()

elif escolha == "Autores do Aplicativo":
    import autores
    autores.app()
