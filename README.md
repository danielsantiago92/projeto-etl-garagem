# 🚍 Pipeline ETL — Gestão de Frota e Manutenção

Pipeline de **ETL desenvolvido em Python e Pandas** para tratamento, integração e análise de dados operacionais de uma empresa de transporte coletivo.

O projeto simula um cenário real de **gestão de frota**, utilizando dados de ônibus, motoristas, linhas, viagens e manutenções para gerar datasets tratados e indicadores que podem ser utilizados posteriormente em análises de **Business Intelligence**.

---

##  Objetivo

Desenvolver um pipeline capaz de:

*  Carregar dados operacionais a partir de arquivos CSV;
*  Remover registros duplicados e realizar tratamento de dados;
*  Converter e padronizar informações de data;
*  Integrar diferentes fontes de dados utilizando relacionamentos entre tabelas;
*  Criar indicadores operacionais e de manutenção;
*  Classificar viagens de acordo com a distância percorrida;
*  Validar a qualidade dos dados;
*  Exportar datasets tratados para utilização em análises e dashboards.

---

##  Tecnologias utilizadas

* **Python 3.12+**
* **Pandas**
* **Pathlib**
* **CSV**
* **Git / GitHub**

---

## 🔄 Fluxo do Pipeline

```text
Arquivos CSV
     ↓
📥 Ingestão
     ↓
🧹 Limpeza e tratamento
     ↓
🔗 Integração dos dados
     ↓
📊 Criação de indicadores
     ↓
✅ Validação
     ↓
📤 Exportação
     ↓
Dados tratados
```

---

##  Estrutura do projeto

```text
projeto-etl-garagem/
│
├── data/
│   ├── raw/
│   │   ├── onibus.csv
│   │   ├── motorista.csv
│   │   ├── linha.csv
│   │   ├── viagem.csv
│   │   └── manutencao.csv
│   │
│   └── processed/
│       ├── dados_viagens_tratados.csv
│       ├── custo_manutencao.csv
│       └── manutencoes_abertas.csv
│
├── dashboard/
│
├── sql/
│
├── src/
│   └── pipeline.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

##  Tratamento e transformação

O pipeline realiza a limpeza dos datasets removendo registros duplicados e convertendo campos de data para o formato adequado para análise.

Também são realizadas integrações entre os dados de:

* ônibus × viagens;
* motoristas × viagens;
* linhas × viagens;
* ônibus × manutenções.

---

##  Indicadores gerados

###  Viagens por ônibus

São calculados:

* Quantidade de viagens;
* Quilometragem total;
* Quilometragem média.

###  Viagens por linha

São calculados:

* Quantidade de viagens;
* Quilometragem total.

###  Manutenção da frota

São calculados:

* Custo total de manutenção por ônibus;
* Quantidade de manutenções;
* Manutenções com status **Aberta**.

###  Classificação das viagens

As viagens são classificadas conforme a distância percorrida:

|        Distância | Classificação |
| ---------------: | ------------- |
| Menor que 100 km | Curta         |
|     100 a 130 km | Média         |
|  Acima de 130 km | Longa         |

---

##  Validação dos dados

O pipeline possui verificações básicas de qualidade para identificar:

* Viagens com quilometragem menor ou igual a zero;
* Registros de manutenção com custo negativo.

Exemplo de saída:

```text
Todos os arquivos foram carregados com sucesso!

OK - Nenhum erro de quilometragem encontrado.
OK - Nenhum custo de manutenção inválido encontrado.

Dados tratados exportados com sucesso!
```

---

##  Dados processados

Ao final da execução, o pipeline gera três arquivos:

```text
dados_viagens_tratados.csv
custo_manutencao.csv
manutencoes_abertas.csv
```

Esses arquivos podem ser utilizados como fonte para análises posteriores em ferramentas de **Business Intelligence**, como Power BI.

---

## ▶️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/danielsantiago92/projeto-etl-garagem.git
```

### 2. Acesse a pasta

```bash
cd projeto-etl-garagem
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o pipeline

```bash
python src/pipeline.py
```

Após a execução, os arquivos tratados estarão disponíveis em:

```text
data/processed/
```

---

##  Possíveis evoluções

Este projeto pode ser expandido com:

*  Dashboard desenvolvido no Power BI;
*  Banco de dados SQL;
*  Automação da execução do pipeline;
*  Novos indicadores de desempenho da frota;
*  Monitoramento de manutenções;
*  Armazenamento em ambiente de nuvem;
*  Testes automatizados para validação do pipeline.

---

##  Sobre mim

**Daniel Santiago**

Ciência da Computação
Analista de Dados Jr
Python | SQL | Power BI
Business Intelligence | ETL | Análise de Dados

Estou desenvolvendo projetos práticos com foco em **Análise de Dados, Business Intelligence e Engenharia de Dados**, buscando transformar dados brutos em informações úteis para tomada de decisão.

---

##  Contato

🔗 GitHub: https://github.com/danielsantiago92

🔗 LinkedIn: https://linkedin.com/in/daniel-santiago-dev
