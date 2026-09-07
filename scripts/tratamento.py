from pathlib import Path
import pandas as pd


def tratar_bases():

    print("=" * 50)
    print("TRATAMENTO DAS BASES")
    print("=" * 50)

    pasta_dados = Path("base_dados")
    pasta_saida = Path("dados_tratados")

    pasta_saida.mkdir(exist_ok=True)

    arquivos = sorted(pasta_dados.glob("*.csv"))

    bases = []

    for arquivo in arquivos:

        print(f"Lendo {arquivo.name}...")

        df = pd.read_csv(
            arquivo,
            sep=";",
            encoding="latin1"
        )

        # Guarda o ano do arquivo
        df["ano_arquivo"] = arquivo.stem

        # Remove duplicados
        df = df.drop_duplicates()

        # Datas
        if "compra" in df.columns:
            df["compra"] = pd.to_datetime(
                df["compra"],
                dayfirst=True,
                errors="coerce"
            )

        if "insercao" in df.columns:
            df["insercao"] = pd.to_datetime(
                df["insercao"],
                dayfirst=True,
                errors="coerce"
            )

        # Valores monetários
        for coluna in ["preco_unitario", "preco_total"]:

            if coluna in df.columns:

                df[coluna] = pd.to_numeric(
                    df[coluna],
                    errors="coerce"
                )

        # Quantidade
        if "qtd_itens_comprados" in df.columns:

            df["qtd_itens_comprados"] = pd.to_numeric(
                df["qtd_itens_comprados"],
                errors="coerce"
            )

        bases.append(df)

    # Consolida todas as bases
    df_final = pd.concat(
        bases,
        ignore_index=True
    )

    print("\nBase consolidada criada!\n")
    print(df_final.info())

    caminho = pasta_saida / "BPS_2020_2026.csv"

    df_final.to_csv(
        caminho,
        sep=";",
        encoding="utf-8-sig",
        index=False
    )

    print("\nArquivo exportado:")
    print(caminho)

    return df_final