import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    confusion_matrix,
    classification_report
)

BASE = Path(__file__).resolve().parent
BANCO = BASE / "seguranca_logs.db"

# 1. Carregamento dos dados
with sqlite3.connect(BANCO) as conn:
    df = pd.read_sql_query(
        "SELECT * FROM network_logs ORDER BY id",
        conn
    )

if df.empty:
    raise ValueError("O banco nao possui eventos para analisar.")

print(f"\nEventos carregados: {len(df)}")

# 2. Selecao das variaveis numericas
# ground_truth NAO entra no treinamento.
features = [
    "packet_size",
    "connection_duration",
    "login_attempts",
    "request_count",
    "requests_per_minute"
]

X = df[features].copy()

if X.isnull().any().any():
    raise ValueError("Existem valores ausentes nas variaveis do modelo.")

# 3. Treinamento e deteccao
# A contaminacao corresponde a proporcao de eventos suspeitos
# criada artificialmente nesta simulacao.
proporcao_suspeitos = (
    (df["ground_truth"] == "suspeito").sum() / len(df)
)

modelo = IsolationForest(
    n_estimators=200,
    contamination=proporcao_suspeitos,
    random_state=42
)

previsoes = modelo.fit_predict(X)

df["is_anomaly"] = previsoes == -1

# Quanto maior o valor, mais anomalo o evento.
df["anomaly_score"] = -modelo.decision_function(X)

df["prediction"] = df["is_anomaly"].map({
    True: "suspeito",
    False: "normal"
})

# 4. Avaliacao usando os rotulos conhecidos da simulacao
y_real = df["ground_truth"]
y_pred = df["prediction"]

print("\n===== RESULTADO DA DETECCAO =====")
print(f"Eventos analisados: {len(df)}")
print(f"Anomalias detectadas: {df['is_anomaly'].sum()}")
print(f"Eventos classificados como normais: {(~df['is_anomaly']).sum()}")

print("\n===== MATRIZ DE CONFUSAO =====")
matriz = confusion_matrix(
    y_real,
    y_pred,
    labels=["normal", "suspeito"]
)

print(pd.DataFrame(
    matriz,
    index=["Real normal", "Real suspeito"],
    columns=["Previsto normal", "Previsto suspeito"]
))

print("\n===== METRICAS DE AVALIACAO =====")
print(classification_report(
    y_real,
    y_pred,
    labels=["normal", "suspeito"],
    zero_division=0
))

# 5. Persistencia dos resultados
colunas = [
    "id",
    "timestamp",
    "source_ip",
    "scenario",
    "ground_truth",
    "prediction",
    "is_anomaly",
    "anomaly_score"
]

resultados = df[colunas].copy()

with sqlite3.connect(BANCO) as conn:
    resultados.to_sql(
        "ia_results",
        conn,
        if_exists="replace",
        index=False
    )

resultados.to_csv(
    BASE / "resultados_ia.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nResultados gravados no SQLite e em resultados_ia.csv.")

# 6. Geracao do grafico
normais = df[~df["is_anomaly"]]
anomalias = df[df["is_anomaly"]]

plt.figure(figsize=(10, 6))

plt.scatter(
    normais["packet_size"],
    normais["requests_per_minute"],
    label="Classificados como normais",
    alpha=0.6
)

plt.scatter(
    anomalias["packet_size"],
    anomalias["requests_per_minute"],
    label="Anomalias identificadas",
    marker="x",
    s=80
)

plt.title("Deteccao de Anomalias - Isolation Forest")
plt.xlabel("Tamanho do pacote (bytes)")
plt.ylabel("Requisicoes por minuto")
plt.legend()
plt.grid(True, alpha=0.3)

plt.savefig(BASE / "grafico_anomalias.png", dpi=200)

print("Grafico salvo em grafico_anomalias.png")

plt.show()
