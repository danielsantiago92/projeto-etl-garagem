# Pipeline ETL - Gestão de Frota e Garagem

Este projeto consiste em um pipeline de **ETL (Extração, Transformação e Carga)** desenvolvido em Python com Pandas. O objetivo é processar dados operacionais de uma empresa de transporte público (ônibus, motoristas, linhas, viagens e manutenções) para gerar datasets limpos e consolidados para análises de desempenho e custos.

---

## Tecnologias Utilizadas

* **Python 3.12+**
* **Pandas** (Tratamento, manipulação e agregação de dados)
* **Pathlib** (Gerenciamento dinâmico de caminhos de arquivos)
* **VS Code** (Ambiente de desenvolvimento)

---

##  Estrutura do Projeto

```text
projeto-etl-garagem/
│
├── data/                       # Arquivos de dados (CSV)
│   ├── onibus.csv              # Cadastro da frota
│   ├── motorista.csv           # Cadastro de motoristas
│   ├── linha.csv               # Cadastro das linhas operadas
│   ├── viagem.csv              # Registro de viagens realizadas
│   ├── manutencao.csv          # Registro de manutenções
│   └── (arquivos exportados)   # Gerados após a execução do script
│
├── src/
│   └── pipeline.py             # Script principal do pipeline ETL
│
└── README.md                   # Documentação do projeto