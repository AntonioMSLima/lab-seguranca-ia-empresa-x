import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# --- PASSO 1: Ingestão e Carga dos Dados via SQLite ---
conn = sqlite3.connect('seguranca_logs.db')
query = "SELECT packet_size, connection_duration, login_attempts FROM network_logs"
df = pd.read_sql(query, conn)
conn.close()

print(f"[+] Dados carregados do SQLite com sucesso! Total de registros: {len(df)}")

# --- PASSO 2: Processamento com Pandas ---
# Selecionamos as colunas numéricas que servirão de features para o modelo
X = df[['packet_size', 'connection_duration', 'login_attempts']]

# --- PASSO 3: Inteligência Artificial (Isolation Forest) ---
# Configuramos o Isolation Forest com uma taxa de anomalia estimada de 5% (contamination=0.05)
iso_forest = IsolationForest(contamination=0.05, random_state=42)
df['anomaly_score'] = iso_forest.fit_predict(X)

# O Isolation Forest retorna -1 para anomalias e 1 para dados normais
# Vamos mapear para uma legibilidade melhor no relatório (True = Anomalia, False = Normal)
df['is_anomaly'] = df['anomaly_score'] == -1

n_anomalias = df['is_anomaly'].sum()
print(f"[+] Análise de IA concluída. Foram detectadas {n_anomalias} anomalias no tráfego.")

# --- PASSO 4: Geração de Evidências Gráficas (Matplotlib) ---
plt.figure(figsize=(10, 6))

# Separar dados normais e anômalos para colorir no gráfico
normal_data = df[~df['is_anomaly']]
anomaly_data = df[df['is_anomaly']]

plt.scatter(normal_data['packet_size'], normal_data['connection_duration'], 
            c='blue', label='Tráfego Normal', alpha=0.6, s=30)
plt.scatter(anomaly_data['packet_size'], anomaly_data['connection_duration'], 
            c='red', label='Anomalias Detectadas (IA)', marker='x', s=100, linewidths=2)

plt.title('Detecção de Anomalias em Segurança de Rede (Isolation Forest)')
plt.xlabel('Tamanho do Pacote (Bytes)')
plt.ylabel('Duração da Conexão (Segundos)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

# Salvar o gráfico como imagem para anexar ao relatório
plt.savefig('grafico_anomalias.png', dpi=300)
print("[+] Gráfico salvo com sucesso como 'grafico_anomalias.png'.")

# Exibir o gráfico na tela
plt.show()