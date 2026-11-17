import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

BANCO = Path(__file__).with_name("seguranca_logs.db")

def gerar_ip():
    return f"192.168.1.{random.randint(10, 250)}"

def gerar_eventos():
    eventos = []
    inicio = datetime.now() - timedelta(hours=24)

    # 500 eventos de comportamento normal
    for i in range(500):
        eventos.append({
            "timestamp": (inicio + timedelta(minutes=i * 2)).isoformat(timespec="seconds"),
            "packet_size": random.randint(200, 1500),
            "connection_duration": round(random.uniform(0.5, 15), 2),
            "login_attempts": random.randint(0, 3),
            "request_count": random.randint(1, 15),
            "requests_per_minute": random.randint(1, 20),
            "response_code": random.choice([200, 200, 200, 201, 204]),
            "endpoint": random.choice(["/api/login", "/api/contas", "/api/saldo"]),
            "source_ip": gerar_ip(),
            "scenario": "normal",
            "ground_truth": "normal"
        })

    # 30 eventos suspeitos, divididos em três cenários
    for i in range(30):
        tipo = i % 3

        if tipo == 0:
            # Simulação de força bruta
            evento = {
                "packet_size": random.randint(300, 900),
                "connection_duration": round(random.uniform(0.1, 2), 2),
                "login_attempts": random.randint(15, 50),
                "request_count": random.randint(20, 60),
                "requests_per_minute": random.randint(30, 100),
                "response_code": 401,
                "endpoint": "/api/login",
                "scenario": "forca_bruta"
            }
        elif tipo == 1:
            # Simulação de abuso de API
            evento = {
                "packet_size": random.randint(500, 1400),
                "connection_duration": round(random.uniform(0.1, 3), 2),
                "login_attempts": random.randint(0, 2),
                "request_count": random.randint(100, 500),
                "requests_per_minute": random.randint(150, 600),
                "response_code": 429,
                "endpoint": "/api/saldo",
                "scenario": "abuso_api"
            }
        else:
            # Simulação de tráfego com pacotes atípicos
            evento = {
                "packet_size": random.randint(5000, 15000),
                "connection_duration": round(random.uniform(0.1, 2), 2),
                "login_attempts": random.randint(0, 3),
                "request_count": random.randint(5, 30),
                "requests_per_minute": random.randint(10, 50),
                "response_code": 200,
                "endpoint": "/api/contas",
                "scenario": "pacote_atipico"
            }

        evento["timestamp"] = (
            inicio + timedelta(minutes=1000 + i * 3)
        ).isoformat(timespec="seconds")
        evento["source_ip"] = gerar_ip()
        evento["ground_truth"] = "suspeito"
        eventos.append(evento)

    random.shuffle(eventos)
    return eventos

def salvar_no_banco(eventos):
    with sqlite3.connect(BANCO) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS network_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                packet_size INTEGER NOT NULL,
                connection_duration REAL NOT NULL,
                login_attempts INTEGER NOT NULL,
                request_count INTEGER NOT NULL,
                requests_per_minute INTEGER NOT NULL,
                response_code INTEGER NOT NULL,
                endpoint TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                scenario TEXT NOT NULL,
                ground_truth TEXT NOT NULL
            )
        """)

        # Substitui a amostra sintética anterior, evitando duplicações
        conn.execute("DELETE FROM network_logs")

        conn.executemany("""
            INSERT INTO network_logs (
                timestamp, packet_size, connection_duration,
                login_attempts, request_count, requests_per_minute,
                response_code, endpoint, source_ip, scenario, ground_truth
            ) VALUES (
                :timestamp, :packet_size, :connection_duration,
                :login_attempts, :request_count, :requests_per_minute,
                :response_code, :endpoint, :source_ip, :scenario, :ground_truth
            )
        """, eventos)

        conn.commit()

if __name__ == "__main__":
    eventos = gerar_eventos()
    salvar_no_banco(eventos)

    normais = sum(e["ground_truth"] == "normal" for e in eventos)
    suspeitos = sum(e["ground_truth"] == "suspeito" for e in eventos)

    print("\n===== GERACAO DE EVENTOS CONCLUIDA =====")
    print(f"Banco: {BANCO}")
    print(f"Total de eventos: {len(eventos)}")
    print(f"Eventos normais: {normais}")
    print(f"Eventos suspeitos: {suspeitos}")
    print("Cenarios: forca_bruta, abuso_api e pacote_atipico")
