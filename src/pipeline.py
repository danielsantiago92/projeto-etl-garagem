from pathlib import Path
import pandas as pd

# Definir o diretório raiz do projeto (sobe 1 nível a partir de src/pipeline.py)
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


# ==========================================
# INGESTÃO DE DADOS (com tratamento de exceção)
# ==========================================
def carregar_dados():
    try:
        onibus = pd.read_csv(RAW_DIR / "onibus.csv")
        motoristas = pd.read_csv(RAW_DIR / "motorista.csv")
        linhas = pd.read_csv(RAW_DIR / "linha.csv")
        viagens = pd.read_csv(RAW_DIR / "viagem.csv")
        manutencoes = pd.read_csv(RAW_DIR / "manutencao.csv")

        print("Todos os arquivos foram carregados com sucesso!\n")

        return onibus, motoristas, linhas, viagens, manutencoes

    except FileNotFoundError as erro:
        print(f"Erro ao carregar arquivo: {erro}")
        raise

    except Exception as erro:
        print(f"Ocorreu um erro inesperado na leitura: {erro}")
        raise


# LIMPEZA E TRATAMENTO DE DADOS

def limpar_dados(onibus, motoristas, linhas, viagens, manutencoes):

    onibus = onibus.drop_duplicates()
    motoristas = motoristas.drop_duplicates()
    linhas = linhas.drop_duplicates()
    viagens = viagens.drop_duplicates()
    manutencoes = manutencoes.drop_duplicates()

    viagens["data_viagem"] = pd.to_datetime(
        viagens["data_viagem"]
    )

    manutencoes["data_abertura"] = pd.to_datetime(
        manutencoes["data_abertura"]
    )


    return onibus, motoristas, linhas, viagens, manutencoes

# ==========================================
# RELACIONAMENTO E INTERAÇÃO DE DADOS
# ==========================================
def integrar_dados(viagens, onibus, motoristas, linhas):

    viagens_onibus = viagens.merge(
        onibus,
        on="id_onibus",
        how="left"
    )

    dados_viagens = viagens_onibus.merge(
        motoristas,
        on="id_motorista",
        how="left"
    )

    dados_viagens = dados_viagens.merge(
        linhas,
        on="id_linha",
        how="left"
    )

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

    dados_viagens = dados_viagens.rename(
        columns={
            "nome": "motorista",
            "numero": "linha"
        }
    )

    return dados_viagens

def criar_indicadores(dados_viagens, manutencoes_onibus):

    # Classificação das viagens por distância
    def classificar_distancia(km):
        if km < 100:
            return "Curta"
        elif km <= 130:
            return "Média"
        else:
            return "Longa"

    dados_viagens["classificacao_viagem"] = dados_viagens[
        "km_percorridos"
    ].apply(classificar_distancia)

    # Indicadores de viagens por ônibus
    viagens_por_onibus = dados_viagens.groupby("prefixo").agg(
        quantidade_viagens=("id_viagem", "count"),
        km_total=("km_percorridos", "sum"),
        km_medio=("km_percorridos", "mean")
    ).reset_index()

    # Indicadores de viagens por linha
    viagens_por_linha = dados_viagens.groupby("linha").agg(
        quantidade_viagens=("id_viagem", "count"),
        km_total=("km_percorridos", "sum")
    ).reset_index()

    # Indicadores de manutenção por ônibus
    custo_manutencao = manutencoes_onibus.groupby("prefixo").agg(
        custo_total=("custo", "sum"),
        quantidade_manutencoes=("id_manutencao", "count")
    ).reset_index()

    custo_manutencao = custo_manutencao.sort_values(
        "custo_total",
        ascending=False
    )

    # Manutenções ainda abertas
    manutencoes_abertas = manutencoes_onibus[
        manutencoes_onibus["status_manutencao"] == "Aberta"
    ]

    return (
        viagens_por_onibus,
        viagens_por_linha,
        custo_manutencao,
        manutencoes_abertas
    )


def validar_dados(viagens, manutencoes):

    # Validação de quilometragem
    erros_km = viagens[viagens["km_percorridos"] <= 0]

    if erros_km.empty:
        print("OK - Nenhum erro de quilometragem encontrado.")
    else:
        print(f"ATENÇÃO - {len(erros_km)} viagem(ns) com quilometragem inválida.")

    # Validação de custos
    erros_custo = manutencoes[manutencoes["custo"] < 0]

    if erros_custo.empty:
        print("OK - Nenhum custo de manutenção inválido encontrado.")
    else:
        print(f"ATENÇÃO - {len(erros_custo)} manutenção(ões) com custo inválido.")

    return erros_km, erros_custo


def exportar_dados(
    dados_viagens,
    custo_manutencao,
    manutencoes_abertas
):

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

if __name__ == "__main__":

    # 1. Carregar os dados
    (
        onibus,
        motoristas,
        linhas,
        viagens,
        manutencoes
    ) = carregar_dados()

    # 2. Limpar os dados
    (
        onibus,
        motoristas,
        linhas,
        viagens,
        manutencoes
    ) = limpar_dados(
        onibus,
        motoristas,
        linhas,
        viagens,
        manutencoes
    )

    # 3. Integrar os dados de viagens
    dados_viagens = integrar_dados(
        viagens,
        onibus,
        motoristas,
        linhas
    )

    # 4. Integrar dados de manutenção
    manutencoes_onibus = manutencoes.merge(
        onibus,
        on="id_onibus",
        how="left",
        suffixes=("_manutencao", "_onibus")
    )

    # 5. Criar indicadores
    (
        viagens_por_onibus,
        viagens_por_linha,
        custo_manutencao,
        manutencoes_abertas
    ) = criar_indicadores(
        dados_viagens,
        manutencoes_onibus
    )

    # 6. Validar os dados
    validar_dados(
        viagens,
        manutencoes
    )

    # 7. Exportar resultados
    exportar_dados(
        dados_viagens,
        custo_manutencao,
        manutencoes_abertas
    )

