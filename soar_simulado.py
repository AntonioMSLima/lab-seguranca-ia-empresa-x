
import sqlite3
import pandas as pd

BANCO = "seguranca_logs.db"

def definir_acao(incidente):
    severidade = incidente["severity"]

    if severidade == "CRITICO":
        return (
            "ALERTA PRIORITARIO",
            "Recomendar contenção do IP",
            "AGUARDANDO APROVACAO HUMANA"
        )

    elif severidade == "ALTO":
        return (
            "ENCAMINHAR INVESTIGACAO",
            "Enviar para análise técnica",
            "INVESTIGACAO PENDENTE"
        )

    elif severidade == "BAIXO":
        return (
            "MONITORAMENTO",
            "Registrar e acompanhar evento",
            "MONITORANDO"
        )

    else:
        return (
            "NENHUMA ACAO",
            "Manter registro do evento",
            "SEM ACAO"
        )


def main():
    conn = sqlite3.connect(BANCO)

    try:
        incidentes = pd.read_sql_query(
            """
            SELECT *
            FROM incident_results
            ORDER BY priority DESC
            """,
            conn
        )

        if incidentes.empty:
            print("Nenhum incidente encontrado.")
            return

        resultados = []

        print("\n===== SIMULACAO SOAR =====\n")

        for _, incidente in incidentes.iterrows():
            acao, recomendacao, status = definir_acao(incidente)

            resultados.append({
                "source_ip": incidente["source_ip"],
                "incident_type": incidente["incident_type"],
                "severity": incidente["severity"],
                "acao_soar": acao,
                "recomendacao": recomendacao,
                "status": status
            })

            if incidente["severity"] != "SEM ALERTA":
                print(f"IP: {incidente['source_ip']}")
                print(f"Incidente: {incidente['incident_type']}")
                print(f"Severidade: {incidente['severity']}")
                print(f"Ação: {acao}")
                print(f"Recomendação: {recomendacao}")
                print(f"Status: {status}")
                print("-" * 45)

        resposta = pd.DataFrame(resultados)

        resposta.to_sql(
            "soar_actions",
            conn,
            if_exists="replace",
            index=False
        )

        resposta.to_csv(
            "respostas_soar.csv",
            index=False,
            encoding="utf-8-sig"
        )

        print("\n===== RESUMO DAS ACOES =====")
        print(resposta["acao_soar"].value_counts())

        print("\nResultados salvos em:")
        print("- Tabela SQLite: soar_actions")
        print("- Arquivo CSV: respostas_soar.csv")

        print("\nATENCAO: nenhuma acao real de bloqueio foi executada.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
