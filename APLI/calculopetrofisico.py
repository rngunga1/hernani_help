import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Funções de cálculo
def calcular_porosidade_densidade(rho_log, rho_matriz=2.65, rho_fluido=1.0):
    return (rho_matriz - rho_log) / (rho_matriz - rho_fluido)

def calcular_volume_argila(gr_log, gr_min, gr_max):
    return (gr_log - gr_min) / (gr_max - gr_min)

def calcular_saturacao_agua(phi, Rw, Rt, a=1, m=2, n=2):
    return (a * Rw / (phi ** m * Rt)) ** (1/n)

def calcular_pressao_hidrostatica(densidade_fluido, profundidade):
    return 0.052 * densidade_fluido * profundidade

# Função principal do app
def app():
    st.title("Cálculos Petrofísicos e Tabela de Resultados")

    # Carregar dados de perfis geofísicos
    data = st.session_state['well_data'] if 'well_data' in st.session_state else st.session_state['csv_data']

    # Selecionar colunas para cálculos
    col_densidade = st.selectbox("Selecione o log de Densidade", data.columns)
    col_gr = st.selectbox("Selecione o log de Radiação Gama (GR)", data.columns)
    col_resistividade = st.selectbox("Selecione o log de Resistividade (Rt)", data.columns)
    col_profundidade = st.selectbox("Selecione a coluna de Profundidade", data.columns)

    # Inputs adicionais
    gr_min = st.number_input("Valor mínimo de GR (formação limpa)", value=float(data[col_gr].min()))
    gr_max = st.number_input("Valor máximo de GR (formação argilosa)", value=float(data[col_gr].max()))
    Rw = st.number_input("Resistividade da água de formação (Rw)", value=0.1)
    densidade_fluido = st.number_input("Densidade do fluido (lb/gal)", value=8.33)

    # Cálculos
    data['Porosidade'] = calcular_porosidade_densidade(data[col_densidade])
    data['Vsh'] = calcular_volume_argila(data[col_gr], gr_min, gr_max)
    data['Saturacao_agua'] = calcular_saturacao_agua(data['Porosidade'], Rw, data[col_resistividade])
    data['Pressao'] = calcular_pressao_hidrostatica(densidade_fluido, data[col_profundidade])

    # Criar uma tabela com os dados calculados
    tabela_resultados = data[['DEPTH', 'Porosidade', 'Vsh', 'Saturacao_agua', 'Pressao']].copy()

    # Exibir a tabela
    st.write("Tabela de Resultados Calculados:")
    st.dataframe(tabela_resultados)

    # Plotar os perfis calculados
    st.write("Perfis dos Resultados Calculados:")

    fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(12, 6), sharey=True)

    # Perfil de Porosidade
    axes[0].plot(data['Porosidade'], data[col_profundidade], color='blue')
    axes[0].set_xlabel('Porosidade')
    axes[0].invert_yaxis()  # Inverter o eixo Y (profundidade)
    axes[0].grid(True)

    # Perfil de Volume de Argila (Vsh)
    axes[1].plot(data['Vsh'], data[col_profundidade], color='green')
    axes[1].set_xlabel('Volume de Argila (Vsh)')
    axes[1].grid(True)

    # Perfil de Saturação de Água (Sw)
    axes[2].plot(data['Saturacao_agua'], data[col_profundidade], color='red')
    axes[2].set_xlabel('Saturação de Água')
    axes[2].grid(True)

    # Perfil de Pressão
    axes[3].plot(data['Pressao'], data[col_profundidade], color='purple')
    axes[3].set_xlabel('Pressão')
    axes[3].grid(True)

    plt.tight_layout()
    st.pyplot(fig)

    # Opção para baixar a tabela em CSV
    csv = tabela_resultados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar Tabela em CSV",
        data=csv,
        file_name='resultados_petrofisicos.csv',
        mime='text/csv',
    )
