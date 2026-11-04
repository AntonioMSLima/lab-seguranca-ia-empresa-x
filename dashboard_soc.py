import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Configuração de Estilo Visual estilo SOC / Kibana (Dark Mode)
plt.style.use('dark_background')
fig, axs = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle('SIEM & AI Security Dashboard - Empresa X (Análise de Ingestão & Anomalias)', fontsize=16, fontweight='bold', color='#00FFCC')

# 1. Carregar dados do SQLite
conn = sqlite3.connect('seguranca_logs.db')
df = pd.read_sql("SELECT timestamp, packet_size, connection_duration, login_attempts FROM network_logs", conn)
conn.close()

# 2. Replicar a Inteligência Artificial (Isolation Forest)
X = df[['packet_size', 'connection_duration', 'login_attempts']]
iso_forest = IsolationForest(contamination=0.05, random_state=42)
df['anomaly'] = iso_forest.fit_predict(X) == -1

df_normal = df[~df['anomaly']]
df_anomaly = df[df['anomaly']]

# --- Painel 1: Gráfico de Linha (Volume de Tráfego ao Longo do Tempo) ---
axs[0, 0].plot(pd.to_datetime(df['timestamp']), df['packet_size'], color='#00BFFF', alpha=0.7, label='Tráfego Normal')
axs[0, 0].scatter(pd.to_datetime(df_anomaly['timestamp']), df_anomaly['packet_size'], color='#FF3333', label='Alerta de Anomalia', zorder=5, s=25)
axs[0, 0].set_title('1. Monitoramento de Ingestão de Pacotes (Bytes / Minuto)', color='#00FFCC')
axs[0, 0].set_ylabel('Bytes')
axs[0, 0].legend(loc='upper right')
axs[0, 0].grid(True, linestyle=':', alpha=0.3)

# --- Painel 2: Dispersão da IA (Tamanho do Pacote vs Duração da Conexão) ---
axs[0, 1].scatter(df_normal['packet_size'], df_normal['connection_duration'], c='#00FF66', alpha=0.5, label='Conexão Legítima', s=20)
axs[0, 1].scatter(df_anomaly['packet_size'], df_anomaly['connection_duration'], c='#FF0055', label='Ataque/Anomalia Detectada', marker='x', s=80, linewidths=2)
axs[0, 1].set_title('2. Detecção de Anomalias via ML (Isolation Forest)', color='#00FFCC')
axs[0, 1].set_xlabel('Tamanho do Pacote (Bytes)')
axs[0, 1].set_ylabel('Duração da Conexão (s)')
axs[0, 1].legend()
axs[0, 1].grid(True, linestyle=':', alpha=0.3)

# --- Painel 3: Histograma (Tentativas de Login Suspeitas) ---
axs[1, 0].hist(df_normal['login_attempts'], bins=10, color='#3399FF', alpha=0.7, label='Tentativas Padrão')
axs[1, 0].hist(df_anomaly['login_attempts'], bins=10, color='#FF9900', alpha=0.9, label='Brute Force / Picos Anômalos')
axs[1, 0].set_title('3. Análise de Comportamento de Autenticação', color='#00FFCC')
axs[1, 0].set_xlabel('Tentativas de Login por Evento')
axs[1, 0].set_ylabel('Frequência de Ocorrência')
axs[1, 0].legend()
axs[1, 0].grid(True, linestyle=':', alpha=0.3)

# --- Painel 4: Gráfico de Rosca (Status Geral de Incidentes) ---
total_normal = len(df_normal)
total_anomalia = len(df_anomaly)
labels = ['Eventos Legítimos', 'Ameaças Isoladas']
sizes = [total_normal, total_anomalia]
colors = ['#00CC66', '#FF3333']

wedges, texts, autotexts = axs[1, 1].pie(
    sizes, labels=labels, colors=colors, autopct='%1.1f%%',
    startangle=140, wedgeprops=dict(width=0.4, edgecolor='black')
)
for text in texts + autotexts:
    text.set_color('white')
axs[1, 1].set_title('4. Consolidado de Segurança do SIEM', color='#00FFCC')

plt.tight_layout()
plt.savefig('dashboard_kibana_simulado.png', dpi=300)
print("[+] Dashboard do SOC gerado com sucesso! Arquivo salvo como 'dashboard_kibana_simulado.png'.")
plt.show()