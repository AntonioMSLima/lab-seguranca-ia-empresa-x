
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BANCO = "seguranca_logs.db"
ARQUIVO_SAIDA = "dashboard_soc_atualizado.png"


def carregar_dados():
    """Carrega os incidentes e as ações SOAR do banco."""

    conn = sqlite3.connect(BANCO)

    try:
        incidentes = pd.read_sql_query(
            "SELECT * FROM incident_results",
            conn
        )

        acoes = pd.read_sql_query(
            "SELECT * FROM soar_actions",
            conn
        )

    finally:
        conn.close()

    if incidentes.empty:
        raise ValueError("A tabela de incidentes está vazia.")

    if acoes.empty:
        raise ValueError("A tabela de ações SOAR está vazia.")

    return incidentes, acoes


def criar_dashboard(incidentes, acoes):
    """Gera o painel de monitoramento SOC."""

    fig, eixos = plt.subplots(2, 2, figsize=(18, 12))

    fig.suptitle(
        "DASHBOARD SOC - SIMULACAO ACADEMICA",
        fontsize=17,
        fontweight="bold"
    )

    # 1. Incidentes por severidade
    ax = eixos[0, 0]

    ordem = [
        "CRITICO",
        "ALTO",
        "BAIXO",
        "SEM ALERTA"
    ]

    severidades = incidentes["severity"].value_counts()

    valores = [
        severidades.get(item, 0)
        for item in ordem
    ]

    barras = ax.bar(ordem, valores)

    ax.set_title("Incidentes por severidade")
    ax.set_ylabel("Quantidade")
    ax.tick_params(axis="x", rotation=15)
    ax.bar_label(barras, padding=4)

    # 2. Tipos de incidentes
    ax = eixos[0, 1]

    tipos = incidentes["incident_type"].value_counts()

    barras = ax.barh(
        tipos.index.astype(str),
        tipos.values
    )

    ax.set_title("Tipos de incidentes identificados")
    ax.set_xlabel("Quantidade")
    ax.invert_yaxis()
    ax.bar_label(barras, padding=4)

    # 3. Ações SOAR
    ax = eixos[1, 0]

    resumo_acoes = acoes["acao_soar"].value_counts()

    barras = ax.barh(
        resumo_acoes.index.astype(str),
        resumo_acoes.values
    )

    ax.set_title("Distribuicao das acoes SOAR")
    ax.set_xlabel("Quantidade")
    ax.invert_yaxis()
    ax.bar_label(barras, padding=4)

    # 4. Tabela de ocorrências prioritárias
    ax = eixos[1, 1]

    ax.axis("off")
    ax.set_title(
        "Ocorrencias prioritarias",
        pad=25
    )

    prioritarios = incidentes[
        incidentes["severity"] != "SEM ALERTA"
    ].sort_values(
        by="priority",
        ascending=False
    ).head(8).copy()

    # Relaciona cada incidente à sua ação SOAR
    mapa_acoes = {}

    for _, acao in acoes.iterrows():

        chave = (
            acao["source_ip"],
            acao["incident_type"],
            acao["severity"]
        )

        mapa_acoes[chave] = acao["acao_soar"]

    linhas = []

    for _, item in prioritarios.iterrows():

        chave = (
            item["source_ip"],
            item["incident_type"],
            item["severity"]
        )

        acao = mapa_acoes.get(
            chave,
            "NAO LOCALIZADA"
        )

        linhas.append([
            item["source_ip"],
            item["endpoint"],
            item["incident_type"],
            item["severity"],
            acao
        ])

    colunas = [
        "IP",
        "Endpoint",
        "Incidente",
        "Nivel",
        "Acao SOAR"
    ]

    tabela = ax.table(
        cellText=linhas,
        colLabels=colunas,
        loc="center",
        cellLoc="center"
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(7)
    tabela.scale(1, 1.7)

    # Rodapé
    fig.text(
        0.5,
        0.025,
        "Dados sinteticos | Respostas simuladas | "
        "Nenhum bloqueio real foi executado",
        ha="center",
        fontsize=9
    )

    # Ajuste de espaçamento
    fig.subplots_adjust(
        left=0.10,
        right=0.97,
        top=0.91,
        bottom=0.12,
        hspace=0.38,
        wspace=0.30
    )

    # Salva o painel
    plt.savefig(
        ARQUIVO_SAIDA,
        dpi=160,
        bbox_inches="tight"
    )

    print("\nDashboard gerado com sucesso!")
    print(f"Arquivo: {ARQUIVO_SAIDA}")
    print(f"Incidentes analisados: {len(incidentes)}")
    print(f"Acoes SOAR registradas: {len(acoes)}")



    plt.close(fig)

def main():

    try:
        incidentes, acoes = carregar_dados()
        criar_dashboard(incidentes, acoes)

    except Exception as erro:
        print("\nERRO AO GERAR O DASHBOARD:")
        print(erro)


if __name__ == "__main__":
    main()
