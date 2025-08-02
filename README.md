# Dashboard de Finanças Pessoais & Classificação de Transações com LLM

Este projeto reúne duas ferramentas Python para automatizar o processamento e visualização de suas finanças pessoais:

1. **Processamento de extratos OFX e classificação de transações** (`llm_finance.py`)
2. **Dashboard interativo em Streamlit** (`dash.py`)

---

## 🧩 Estrutura do Projeto

```
├── dash.py            # Script do Streamlit para visualização de gastos
├── llm_finance.py     # Script para extração e classificação de transações OFX
├── finances.csv       # Saída gerada pelo llm_finance.py (input para dash.py)
├── extratos/          # Pasta contendo arquivos .ofx de extratos bancários
├── .env               # Variáveis de ambiente (GROQ_API_KEY)
├── requirements.txt   # Dependências do projeto
└── README.md          # Documentação (este arquivo)
```

---

## 📦 Requisitos

* Python 3.8+
* Conta e chave de API Groq (`GROQ_API_KEY`)

### Principais Bibliotecas

* [streamlit](https://streamlit.io/)
* [pandas](https://pandas.pydata.org/)
* [plotly](https://plotly.com/python/)
* [ofxparse](https://github.com/jseutter/ofxparse)
* [agno](https://pypi.org/project/agno)
* [dotenv](https://pypi.org/project/python-dotenv)

Instale todas as dependências com:

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuração

1. **Chave de API Groq**:

   * Crie um arquivo `.env` na raiz do projeto com:

     ```ini
     GROQ_API_KEY=seu_token_groq_aqui
     ```

2. **Extratos OFX**:

   * Crie uma pasta `extratos/` e coloque todos os seus arquivos `.ofx` na pasta.

---

## 🚀 Uso

### 1. Classificação de Transações (llm\_finance.py)

Este script faz:

* Leitura de todos os arquivos `.ofx` em `extratos/`.
* Extração de data, valor, descrição e ID de cada transação.
* Remoção de duplicados.
* Classificação de categorias usando um agente `Groq` via `agno`.
* Filtra transações a partir de 1º de janeiro de 2024.
* Geração do arquivo `finances.csv`, que será utilizado pelo dashboard.

Execute:

```bash
python llm_finance.py
```

### 2. Dashboard Interativo (dash.py)

Este script Carrega `finances.csv` e exibe:

* Filtros por mês e categorias.
* Métricas principais: total gasto, média por transação, número de transações.
* Gráfico de barras horizontal para gastos por categoria.
* Gráfico de linha para evolução diária de gastos.

Para rodar o dashboard:

```bash
streamlit run dash.py
```

Acesse o aplicativo em `http://localhost:8501`.

---

## 🎯 Personalizações Possíveis

* Ajustar ou ampliar lista de categorias no template de `llm_finance.py`.
* Modificar cores, layout ou adicionar novos gráficos em `dash.py`.
* Integrar outras fontes de dados (CSV, APIs bancárias, etc.).



> Desenvolvido com \:heart: por \[Seu Nome]
