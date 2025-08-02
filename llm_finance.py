import os
import ofxparse
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from agno.agent import Agent, RunResponse
from agno.models.groq import Groq

# 1. Carregar .env
_ = load_dotenv(find_dotenv())
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 2. Extrair transações OFX
df = pd.DataFrame()
for fname in os.listdir("extratos"):
    if not fname.lower().endswith(".ofx"):
        continue
    path = os.path.join("extratos", fname)
    with open(path, encoding="ISO-8859-1") as f:
        ofx = ofxparse.OfxParser.parse(f)
    records = [
        {
            "Data": txn.date.date(),
            "Valor": float(txn.amount),
            "Descrição": txn.memo or "",
            "ID": txn.id
        }
        for acct in ofx.accounts
        for txn in acct.statement.transactions
    ]
    if records:
        df = pd.concat([df, pd.DataFrame(records)], ignore_index=True)

df = df.drop_duplicates(subset="ID").set_index("ID")

agent = Agent(
    model=Groq(id="gemma2-9b-it"),
    markdown=False
)

template = """
Você é um analista de dados, trabalhando em um projeto de limpeza de dados.
Seu trabalho é escolher uma categoria adequada para cada lançamento financeiro
que vou te enviar.

Escolha uma dentre as seguintes categorias:
- Alimentação
- Receitas
- Saúde
- Mercado
- Educação
- Compras
- Transporte
- Investimento
- Transferências para terceiros
- Telefone
- Moradia

Escolha a categoria deste item:
{descricao}

Responda APENAS com uma das categorias descritas, sendo proibido classificar a categoria diferente de alguma das categorias listadas.
No total, todos os gastos só devem permanecer entre 11 categorias, nem mais nem menos.
"""

def classificar_categoria(descricao: str) -> str:
    prompt = template.format(descricao=descricao)
    run: RunResponse = agent.run(prompt)
    return run.content.strip()

# 4. Aplicar classificação
df["Categoria"] = df["Descrição"].apply(lambda d: classificar_categoria(d) if d and d.strip() else "")

# 5. Filtrar por data
df = df[df["Data"] >= datetime(2024, 1, 1).date()]

# 6. Salvar
df.reset_index(inplace=True)
df.to_csv("finances.csv", index=False)
