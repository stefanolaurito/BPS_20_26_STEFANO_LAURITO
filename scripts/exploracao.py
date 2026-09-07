from pathlib import Path
import pandas as pd


def gerar_relatorio():

    print("=" * 50)
    print("ANÁLISE EXPLORATÓRIA")
    print("=" * 50)

    pasta_dados = Path("base_dados")
    pasta_relatorios = Path("relatorios")

    pasta_relatorios.mkdir(exist_ok=True)

    arquivos = sorted(pasta_dados.glob("*.csv"))

    resumo = []

    for arquivo in arquivos:

        print(f"Analisando {arquivo.name}...")

        df = pd.read_csv(
            arquivo,
            sep=";",
            encoding="latin1"
        )

        resumo.append({

            "Arquivo": arquivo.name,

            "Linhas": df.shape[0],

            "Colunas": df.shape[1],

            "Duplicados": df.duplicated().sum(),

            "Valores Nulos": df.isnull().sum().sum()

        })

    relatorio = pd.DataFrame(resumo)

    print("\nResumo das bases:\n")
    print(relatorio)

    relatorio.to_csv(

        pasta_relatorios / "relatorio_bases.csv",

        sep=";",

        encoding="utf-8-sig",

        index=False

    )

    print("\nRelatório salvo em:")

    print(pasta_relatorios / "relatorio_bases.csv")

    print("\nAnálise exploratória concluída!")