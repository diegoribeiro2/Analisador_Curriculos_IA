import os
import subprocess
import sys
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode  # usada pra renderização de tabelas interativas
from database import AnalyzeDatabase

# Inicializa a base de dados
database = AnalyzeDatabase()

# Configura a página do Streamlit com layout largo e título "Analisador de Currículos"
st.set_page_config(layout="wide", page_title="Analisador de Currículos", page_icon=":brain:")

# SIDEBAR - Envio manual de currículo
st.sidebar.title("📄 Enviar Currículo")

st.sidebar.write("Envie um arquivo **PDF** contendo o currículo.")

uploaded_file = st.sidebar.file_uploader(
    "Selecione um currículo (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

# Lista de arquivos enviados nesta sessão
saved_files = []

if uploaded_file:
    save_dir = "curriculos"
    os.makedirs(save_dir, exist_ok=True)

    for file in uploaded_file:
        save_path = os.path.join(save_dir, file.name)

        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

        saved_files.append(file.name)

    st.sidebar.success(f"{len(saved_files)} currículo(s) salvo(s) com sucesso! ✔")

# EXECUTA AUTOMATICAMENTE O SCRIPT analyze/import_cv.py 
# -------------------------
# BOTÃO PARA INICIAR ANÁLISE
# -------------------------
st.sidebar.subheader("🚀 Processar Currículos")

if st.sidebar.button("Iniciar Análise"):
    script_path = os.path.join("analyze", "import_cv.py")
    python_exec = sys.executable  # Python do ambiente virtual atual

    with st.spinner("⏳ A análise dos currículos está sendo realizada... Isso pode levar alguns segundos..."):
        try:
             subprocess.run([python_exec, script_path], check=True)

             st.sidebar.success("Análise finalizada com sucesso! 🎉")
             st.success("✅ A análise de currículos foi concluída com sucesso!")
             st.balloons()

        except subprocess.CalledProcessError as e:
            st.sidebar.error("Erro ao executar o script import_cv.py")
            st.error("❌ Ocorreu um erro ao tentar processar os currículos. Clique em limpar análise e tente novamente.")
            st.error(str(e))

# HEADER - Título principal e informações do desenvolvedor
st.title("📊 Analisador de Currículos com Inteligência Artificial")

# Informações do desenvolvedor no header
st.markdown(
    "**Desenvolvido por:** [Diego Ribeiro](https://www.linkedin.com/in/diegoribeiro2/)",
    unsafe_allow_html=True
)

# Linha divisória para separar o header do conteúdo
st.divider()

# Cria um menu de seleção para escolher uma vaga disponível na base de dados
option = st.selectbox(
    "Escolha a sua vaga:",
    [job.get('name') for job in database.jobs.all()],
    index=None
)

# Inicializa a variável `data`
data = None

# Verifica se uma vaga foi selecionada
if option:
    # Obtém as informações da vaga selecionada pelo nome
    job = database.get_job_by_name(option)
    
    # Obtém as análises relacionadas à vaga selecionada
    data = database.get_analysis_by_job_id(job.get('id'))

    # Cria um DataFrame do Pandas para armazenar os dados das análises
    df = pd.DataFrame(
        data if data else {},
        columns=[
            'name',
            'education',
            'skills',
            'languages',
            'score',
            'resum_id',
            'id'
        ]
    )

    # Renomeia as colunas para melhorar a legibilidade
    df.rename(
        columns={
            'name': 'Nome',
            'education': 'Educação',
            'skills': 'Habilidades',
            'languages': 'Idiomas',
            'score': 'Score',
            'resum_id': 'Resumo ID',
            'id': 'ID'
        },
        inplace=True
    )

    # Configura a tabela interativa usando GridOptionsBuilder
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)  # Habilita paginação automática

    # Configura a ordenação e seleção, se houver dados
    if data:
        gb.configure_column("Score", header_name="Score", sort="desc")  # Ordena pela coluna 'Score'
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)  # Adiciona seleção com checkboxes

    # Constrói as opções de grid
    grid_options = gb.build()

    # Exibe um gráfico de barras com as pontuações dos candidatos
    st.subheader('Classificação dos Candidatos')
    st.bar_chart(df, x="Nome", y="Score", color="Nome", horizontal=True)

    # Exibe a tabela interativa usando AgGrid
    response = AgGrid(
        df,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme='streamlit',
    )

    # Obtém os candidatos selecionados na tabela
    selected_candidates = response.get('selected_rows', [])
    candidates_df = pd.DataFrame(selected_candidates)

    # Obtém os currículos relacionados à vaga
    resums = database.get_resums_by_job_id(job.get('id'))

    # Função para deletar os arquivos dos currículos
    def delete_files_resum(resums):
        for resum in resums:
            path = resum.get('file')
            if os.path.isfile(path):
                os.remove(path)

    # Botão para limpar as análises e deletar os currículos
    if st.button('Limpar Análise'):
        database.delete_all_resums_by_job_id(job.get('id'))  # Deleta todos os currículos
        database.delete_all_analysis_by_job_id(job.get('id'))  # Deleta todas as análises
        database.delete_all_files_by_job_id(job.get('id')) # Deleta todos os arquivos
        delete_files_resum(resums)  # Deleta os arquivos dos currículos
        st.rerun()  # Recarrega a página

    # Exibe os currículos dos candidatos selecionados
    if not candidates_df.empty:
        cols = st.columns(len(candidates_df))  # Cria colunas para exibir os currículos
        for idx, row in enumerate(candidates_df.iterrows()):
            with cols[idx]:  # Exibe cada currículo em uma coluna
                with st.container():
                    if resum_data := database.get_resum_by_id(row[1]['Resumo ID']):
                        st.markdown(resum_data.get('content')) # Exibe o resumo do currículo
                        st.markdown(resum_data.get('opnion')) # Exibe a opnião da IA sobre o curriculo

                        # Exibe um botão para download do currículo em PDF
                        with open(resum_data.get('file'), "rb") as pdf_file:
                            pdf_data = pdf_file.read()
                            st.download_button(
                                label=f"Fazer download do currículo {row[1]['Nome']}",
                                data=pdf_data,
                                file_name=f"{row[1]['Nome']}.pdf",
                                mime="application/pdf"
                            )
