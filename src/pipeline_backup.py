from pathlib import Path
import pandas as pd

# Definir o diretório raiz do projeto (sobe 1 nível a partir de src/pipeline.py)
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


# ==========================================
# INGESTÃO DE DADOS (com tratamento de exceção)
# ==========================================
try:
    onibus = pd.read_csv(RAW_DIR / "onibus.csv")
    motoristas = pd.read_csv(RAW_DIR / "motorista.csv")
    linhas = pd.read_csv(RAW_DIR / "linha.csv")
    viagens = pd.read_csv(RAW_DIR / "viagem.csv")
    manutencoes = pd.read_csv(RAW_DIR / "manutencao.csv")

    print("Todos os arquivos foram carregados com sucesso!\n")

except FileNotFoundError as erro:
    print(f"Erro ao carregar arquivo: {erro}")
    exit()  # Interrompe a execução caso algum arquivo não seja encontrado
except Exception as erro:
    print(f"Ocorreu um erro inesperado na leitura: {erro}")
    exit()

# ==========================================
# VERIFICAÇÃO INICIAL DOS DADOS
# ==========================================
print("--- PRIMANCEIRAS LINHAS ---")
print("ÔNIBUS:\n", onibus.head())
print("\nMOTORISTA:\n", motoristas.head())
print("\nLINHAS:\n", linhas.head())
print("\nVIAGENS:\n", viagens.head())
print("\nMANUTENÇÕES:\n", manutencoes.head())

print("\n--- INFORMAÇÕES DE TIPOS ---")
onibus.info()
motoristas.info()
linhas.info()
viagens.info()
manutencoes.info()

print("\n--- TAMANHO DOS DATAFRAMES ---")
print("Ônibus:", onibus.shape)
print("Motoristas:", motoristas.shape)
print("Linhas:", linhas.shape)
print("Viagens:", viagens.shape)
print("Manutenções:", manutencoes.shape)

print("\n--- VALORES AUSENTES ---")
print("Ônibus:\n", onibus.isnull().sum())
print("Motoristas:\n", motoristas.isnull().sum())
print("Linhas:\n", linhas.isnull().sum())
print("Viagens:\n", viagens.isnull().sum())
print("Manutenções:\n", manutencoes.isnull().sum())

print("\n--- DUPLICIDADES ---")
print("Duplicidades em ônibus:", onibus.duplicated().sum())
print("Duplicidades em motoristas:", motoristas.duplicated().sum())
print("Duplicidades em linhas:", linhas.duplicated().sum())
print("Duplicidades em viagens:", viagens.duplicated().sum())
print("Duplicidades em manutenções:", manutencoes.duplicated().sum())

# Removendo duplicadas
onibus = onibus.drop_duplicates()
motoristas = motoristas.drop_duplicates()
linhas = linhas.drop_duplicates()
viagens = viagens.drop_duplicates()
manutencoes = manutencoes.drop_duplicates()

# Corrigir tipos das datas
viagens["data_viagem"] = pd.to_datetime(viagens["data_viagem"])
manutencoes["data_abertura"] = pd.to_datetime(manutencoes["data_abertura"])

# ==========================================
# RELACIONAMENTO E INTERAÇÃO DE DADOS
# ==========================================
# Onibus e viagens
viagens_onibus = viagens.merge(onibus, on="id_onibus", how="left")

# Motoristas
dados_viagens = viagens_onibus.merge(motoristas, on="id_motorista", how="left")

# Linha
dados_viagens = dados_viagens.merge(linhas, on="id_linha", how="left")

# Organizar colunas
dados_viagens = dados_viagens[
    [
        "id_viagem",
        "data_viagem",
        "prefixo",
        "modelo",
        "nome",
        "numero",
        "itinerario",
        "km_percorridos",
    ]
]

# Renomear
dados_viagens = dados_viagens.rename(
    columns={"nome": "motorista", "numero": "linha"}
)

# ==========================================
# CRIAÇÃO DE INDICADORES
# ==========================================
def classificar_distancia(km):
    if km < 100:
        return "Curta"
    elif km <= 130:
        return "Média"
    else:
        return "Longa"

dados_viagens["classificacao_viagem"] = dados_viagens["km_percorridos"].apply(
    classificar_distancia
)

# ==========================================
# ANÁLISE DA FROTA E MANUTENÇÃO
# ==========================================
viagens_por_onibus = (
    dados_viagens.groupby("prefixo")
    .agg(
        quantidade_viagens=("id_viagem", "count"),
        km_total=("km_percorridos", "sum"),
        km_medio=("km_percorridos", "mean"),
    )
    .reset_index()
)

viagens_por_linha = (
    dados_viagens.groupby("linha")
    .agg(
        quantidade_viagens=("id_viagem", "count"),
        km_total=("km_percorridos", "sum"),
    )
    .reset_index()
)

manutencao_onibus = manutencoes.merge(
    onibus, on="id_onibus", how="left", suffixes=("_manutencao", "_onibus")
)

custo_manutencao = (
    manutencao_onibus.groupby("prefixo")
    .agg(
        custo_total=("custo", "sum"),
        quantidade_manutencoes=("id_manutencao", "count"),
    )
    .reset_index()
    .sort_values("custo_total", ascending=False)
)

manutencoes_abertas = manutencao_onibus[
    manutencao_onibus["status_manutencao"] == "Aberta"
]

# ==========================================
# VALIDAÇÃO DA QUALIDADE DOS DADOS
# ==========================================
erros_km = viagens[viagens["km_percorridos"] <= 0]
if len(erros_km) > 0:
    print("ERRO: Existem viagens com quilometragem inválida.")
else:
    print("OK: Quilometragem validada.")

erros_custo = manutencoes[manutencoes["custo"] < 0]
if len(erros_custo) > 0:
    print("ERRO: Existem custos inválidos.")
else:
    print("OK: Custos validados.")

# ==========================================
# EXPORTAÇÃO DOS DADOS TRATADOS
# ==========================================
dados_viagens.to_csv(
    PROCESSED_DIR / "dados_viagens_tratados.csv",
    index=False
    )

custo_manutencao.to_csv(
    PROCESSED_DIR / "custo_manutencao.csv",
    index=False
    )

manutencoes_abertas.to_csv(
    PROCESSED_DIR / "manutencoes_abertas.csv",
    index=False
    )

print("\nDados tratados exportados com sucesso!")

