import sqlite3
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    classification_report
)

# Caminhos e configurações
BANCO = "seguranca_logs.db"
ARQUIVO_CSV = "validacao_ia.csv"

COLUNAS = [
    "packet_size",
    "connection_duration",
    "login_attempts",
    "request_count",
    "requests_per_minute"
]


def main():
    print("\n=== VALIDACAO DO MODELO DE IA ===\n")

    # 1. Ler os dados
    conexao = sqlite3.connect(BANCO)

    dados = pd.read_sql_query(
        "SELECT * FROM network_logs",
        conexao
    )

    conexao.close()

    print(f"Total de registros: {len(dados)}")

    # 2. Separar registros normais e suspeitos
    normais = dados[dados["ground_truth"] == "normal"].copy()
    suspeitos = dados[dados["ground_truth"] == "suspeito"].copy()

    if len(normais) < 2 or len(suspeitos) == 0:
        raise ValueError("Dados insuficientes para validacao.")

    # 3. Dividir os registros normais
    treino_normal, teste_normal = train_test_split(
        normais,
        test_size=0.30,
        random_state=42
    )

    # 4. Montar conjunto de teste
    teste = pd.concat(
        [teste_normal, suspeitos],
        ignore_index=True
    )

    # 5. Treinar somente com dados normais
    modelo = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42
    )

    modelo.fit(treino_normal[COLUNAS])

    # 6. Detectar anomalias
    teste["prediction"] = modelo.predict(teste[COLUNAS])

    teste["is_anomaly"] = (
        teste["prediction"] == -1
    ).astype(int)

    teste["anomaly_score"] = (
        -modelo.decision_function(teste[COLUNAS])
    )

    # 7. Preparar avaliação
    teste["real"] = (
        teste["ground_truth"] == "suspeito"
    ).astype(int)

    matriz = confusion_matrix(
        teste["real"],
        teste["is_anomaly"],
        labels=[0, 1]
    )

    print("\n=== MATRIZ DE CONFUSAO ===")
    print(matriz)

    print("\n=== RELATORIO DE CLASSIFICACAO ===")

    print(
        classification_report(
            teste["real"],
            teste["is_anomaly"],
            target_names=["Normal", "Suspeito"],
            zero_division=0
        )
    )

    # 8. Salvar resultados em CSV
    teste.to_csv(
        ARQUIVO_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    # 9. Salvar resultados no banco
    conexao = sqlite3.connect(BANCO)

    teste.to_sql(
        "ia_validation_results",
        conexao,
        if_exists="replace",
        index=False
    )

    conexao.close()

    print("\nValidacao concluida.")
    print(f"Arquivo CSV: {ARQUIVO_CSV}")
    print("Tabela criada: ia_validation_results")


if __name__ == "__main__":
    main()