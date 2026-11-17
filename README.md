# LaboratÃ³rio de SeguranÃ§a CibernÃ©tica com IA e Big Data

**InstituiÃ§Ã£o:** UNISENAI SC
**Curso:** Superior de Tecnologia em Defesa CibernÃ©tica
**Estudante:** ANTONIO MÃRIO S. LIMA
**Desafio:** Automatizando a SeguranÃ§a com IA e Big Data
**PerÃ­odo:** Novembro de 2026

## 1. ApresentaÃ§Ã£o

Projeto acadÃªmico que demonstra um fluxo de monitoramento de seguranÃ§a utilizando dados sintÃ©ticos, Python, SQLite, InteligÃªncia Artificial, correlaÃ§Ã£o de incidentes, simulaÃ§Ã£o SOAR e dashboard SOC.

## 2. Objetivos

- Gerar eventos sintÃ©ticos normais e suspeitos.
- Armazenar os registros em SQLite.
- Aplicar Isolation Forest para detecÃ§Ã£o de anomalias.
- Validar o modelo de IA.
- Correlacionar eventos de seguranÃ§a.
- Simular aÃ§Ãµes de resposta SOAR.
- Apresentar indicadores em dashboard SOC.

## 3. Arquitetura

| Arquivo | FunÃ§Ã£o |
|---|---|
| gerar_logs.py | GeraÃ§Ã£o de eventos |
| laboratorio_ia.py | AnÃ¡lise de anomalias |
| validar_modelo.py | ValidaÃ§Ã£o da IA |
| correlacao_incidentes.py | CorrelaÃ§Ã£o de incidentes |
| soar_simulado.py | SimulaÃ§Ã£o SOAR |
| dashboard_soc.py | Dashboard SOC |

## 4. Tecnologias

- Python
- SQLite
- Pandas
- Matplotlib
- Scikit-learn
- Isolation Forest

## 5. ExecuÃ§Ã£o

Instale as dependÃªncias:

```powershell
pip install -r requirements.txt
```

Execute os mÃ³dulos na seguinte ordem:

```powershell
python gerar_logs.py
python laboratorio_ia.py
python validar_modelo.py
python correlacao_incidentes.py
python soar_simulado.py
python dashboard_soc.py
```

## 6. Resultados da validaÃ§Ã£o

Na validaÃ§Ã£o registrada, foram analisados 180 registros, sendo 150 normais e 30 suspeitos.

Matriz de confusÃ£o: [[31, 119], [0, 30]].

- Verdadeiros negativos: 31
- Falsos positivos: 119
- Falsos negativos: 0
- Verdadeiros positivos: 30
- AcurÃ¡cia: 33,9%
- PrecisÃ£o: 20,1%
- Recall: 100%
- Especificidade: 20,7%

O modelo identificou todos os eventos suspeitos, mas apresentou elevado nÃºmero de falsos positivos. Portanto, nÃ£o estÃ¡ pronto para uso em produÃ§Ã£o.

## 7. LimitaÃ§Ãµes

Os dados utilizados sÃ£o sintÃ©ticos e destinados ao ambiente acadÃªmico. O mÃ³dulo SOAR realiza simulaÃ§Ãµes de resposta, sem bloqueio real de IP, firewall ou isolamento de dispositivos.

## 8. ConclusÃ£o

O laboratÃ³rio demonstra a integraÃ§Ã£o entre geraÃ§Ã£o de dados, anÃ¡lise por IA, correlaÃ§Ã£o de eventos, simulaÃ§Ã£o de respostas e visualizaÃ§Ã£o SOC. A validaÃ§Ã£o evidencia a importÃ¢ncia de avaliar nÃ£o apenas a detecÃ§Ã£o de ameaÃ§as, mas tambÃ©m a quantidade de falsos positivos gerados pelo modelo.
