
import sqlite3
import pandas as pd

BANCO = "seguranca_logs.db"

def classificar_incidente(evento):
    regras = []
    severidade = "SEM ALERTA"
    prioridade = 0

    # Regra 1: possível força bruta
    if evento["login_attempts"] >= 21 and evento["response_code"] == 401:
        regras.append("FORCA_BRUTA")
        severidade = "CRITICO"
        prioridade = 3

    # Regra 2: possível abuso de API
    if evento["requests_per_minute"] >= 160 and evento["response_code"] == 429:
        regras.append("ABUSO_API")
        severidade = "CRITICO"
        prioridade = 3

    # Regra 3: pacote atípico
    if evento["packet_size"] >= 5145:
        regras.append("PACOTE_ATIPICO")
        if prioridade < 2:
            severidade = "ALTO"
            prioridade = 2

    # Regra 4: anomalia identificada somente pela IA
    if evento["is_anomaly"] == 1 and not regras:
        regras.append("ANOMALIA_IA")
        severidade = "BAIXO"
        prioridade = 1

    if not regras:
        regras.append("SEM_INDICIOS")

    return pd.Series({
        "incident_type": ", ".join(regras),
        "severity": severidade,
        "priority": prioridade,
        "justification": "Regras acionadas: " + ", ".join(regras)
    })


def main():
    conn = sqlite3.connect(BANCO)

    df = pd.read_sql_query(
        "SELECT * FROM ia_validation_results",
        conn
    )

    if df.empty:
        print("Nenhum registro encontrado.")
        conn.close()
        return

    classificacoes = df.apply(classificar_incidente, axis=1)
    resultado = pd.concat([df, classificacoes], axis=1)

    resultado.to_sql(
        "incident_results",
        conn,
        if_exists="replace",
        index=False
    )

    resultado.to_csv(
        "incidentes_correlacionados.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n=== RESULTADO DA CORRELACAO ===")
    print("Eventos analisados:", len(resultado))

    print("\n=== CLASSIFICACAO POR SEVERIDADE ===")
    print(resultado["severity"].value_counts())

    print("\n=== TIPOS DE INCIDENTES ===")
    print(resultado["incident_type"].value_counts())

    print("\nArquivos gerados:")
    print("- incidentes_correlacionados.csv")
    print("- Tabela SQLite: incident_results")

    conn.close()


if __name__ == "__main__":
    main()
