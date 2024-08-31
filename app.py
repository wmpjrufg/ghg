import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("GHG Protocol")
uploaded_file = st.file_uploader("Upload do arquivo de dados", type={"xlsx", "csv"})
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df["Balanço"] = df["Emissão de GEE (kg CO2)"] + df["Remoção dos gases (kg CO2)"]
    df["kg de CO2 emitido por hectar"] = df["Emissão de GEE (kg CO2)"] / df["Área plantada (ha)"]
    df["kg de CO2 removida por hectar"] = df["Remoção dos gases (kg CO2)"] / df["Área plantada (ha)"]
    df["Balanço de GEE (kg/ha)"] = df["kg de CO2 emitido por hectar"] + df["kg de CO2 removida por hectar"]

options = st.multiselect("Quais colunas você deseja visualizar?",
                        ["Emissão de GEE (kg CO2)", "Remoção dos gases (kg CO2)", "Área plantada (ha)", "Balanço",
                         "kg de CO2 emitido por hectar", "kg de CO2 removida por hectar", "Balanço de GEE (kg/ha)"],
                        )

if not options:
    pass
else:
    colunas = ['Cidade'] + ['Sistema de plantio'] + ['Sigla de plantio'] + options
    df1 = df[colunas]
    st.write(df1)
    opcao1 = st.checkbox('top 5 emissor de CO2')
    opcao2 = st.checkbox('top 5 removedor de CO2')
    if opcao1:
        top5_emissores = df.nlargest(5, "Emissão de GEE (kg CO2)")
        st.write("Top 5 Emissores de CO2")
        st.write(top5_emissores)
        fig, ax = plt.subplots()
        top5_emissores.plot(kind='bar', x='Cidade', y='Emissão de GEE (kg CO2)', ax=ax, color='red')
        ax.set_ylabel("Emissão de GEE (kg CO2)")
        st.pyplot(fig)

    if opcao2:
        top5_removedores = df.nlargest(5, "Remoção dos gases (kg CO2)")
        st.write("Top 5 Removedores de CO2")
        st.write(top5_removedores)
        fig, ax = plt.subplots()
        top5_removedores.plot(kind='bar', x='Cidade', y='Remoção dos gases (kg CO2)', ax=ax, color='green')
        ax.set_ylabel("Remoção dos gases (kg CO2)")
        st.pyplot(fig)
