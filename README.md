# Analisador de Currículos

Este é um projeto de análise de currículos que utiliza a API do ChatGPT para resumir e pontuar currículos com base na descrição de uma vaga específica. O projeto é desenvolvido em Python, com o Streamlit como front-end para a interface do usuário.

## Funcionalidades

- **Upload de Currículos em Lote**: Carregue vários currículos de uma vez para análise.
- **Análise de Currículos**: Avalie currículos com base em diferentes seções, atribuindo uma pontuação conforme a relevância para a vaga.
- **Comparação de Currículos**: Compare currículos lado a lado para uma avaliação mais detalhada.
- **Análise Crítica Descritiva**: Geração de uma análise crítica e descritiva sobre o currículo em relação à vaga.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal utilizada no projeto.
- **Streamlit**: Framework para criar a interface web de maneira rápida e interativa.
- **ChatGPT (modelo 4o-mini)**: LLM utilizado para resumir os currículos e gerar a pontuação.
- **TinyDB**: Banco de dados NoSQL utilizado para armazenar informações.
- **Poetry**: Ferramenta de gerenciamento de dependências e ambientes virtuais em Python.

## Pré-requisitos

- Python 3.10 ou superior
- Poetry instalado globalmente
- Chave da API da OpenAI

## Configuração do Ambiente

Para o projeto funcionar corretamente, é necessário criar um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
OPENAI_API_KEY='sua chave da openai aqui'
```

> **Atenção:** Substitua `'sua chave da openai aqui'` pela sua chave de API da OpenAI.

## Instalação e Execução

### Passos para Instalação

1. Clone este repositório para o seu ambiente local:
   ```bash
   git clone https://github.com/asimov-academy/cv-recruter.git
   cd cv-recruter
   ```

2. Instale as dependências do projeto utilizando o Poetry:
   ```bash
   poetry install
   ```

### Execução no Linux

Para usuários Linux, há um script de build disponível na pasta `bin` que facilita a execução do projeto. Basta executar:

```bash
./bin/build.sh
```

O script inicia o Streamlit no endereço `0.0.0.0` e na porta `8585`.

### Execução no Windows

Para usuários Windows, a execução deve ser feita manualmente. Utilize o seguinte comando para iniciar o projeto:

```bash
poetry run streamlit run analyser/app.py
```

Depois, acesse o projeto através do seu navegador no endereço:

```
http://localhost:8501
```

*Nota: A porta padrão do Streamlit é `8501` quando não especificada.*

## Uso

Após iniciar o projeto, você poderá:

1. Cadastrar novas vagas através da interface.
2. Fazer upload de currículos em lote para análise.
3. Visualizar a análise de cada currículo por vaga, com a possibilidade de comparar currículos.
4. Gerar análises críticas descritivas sobre os currículos em relação às vagas.

## Documentação do Sistema de Pontuação

O sistema de pontuação foi projetado para avaliar currículos com base em uma vaga específica. As seções avaliadas incluem:

- **Experiência (Peso: 30%)**
- **Habilidades Técnicas (Peso: 25%)**
- **Educação (Peso: 10%)**
- **Idiomas (Peso: 10%)**
- **Pontos Fortes (Peso: 15%)**
- **Pontos Fracos (Desconto de até 10%)**

Cada seção recebe uma pontuação de 0 a 10, com justificativas para as notas atribuídas. A pontuação final é uma média ponderada das avaliações, refletindo a adequação do candidato à vaga.
