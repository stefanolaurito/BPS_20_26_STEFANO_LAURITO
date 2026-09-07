from pathlib import Path
import pandas as pd


def gerar_bases_dashboard():

    print("=" * 50)
    print("GERANDO BASE PARA O LOOKER STUDIO")
    print("=" * 50)

    # =====================================================
    # LEITURA DA BASE CONSOLIDADA
    # =====================================================

    caminho = Path("dados_tratados") / "BPS_2020_2026.csv"

    df = pd.read_csv(
        caminho,
        sep=";",
        encoding="utf-8-sig"
    )

    print(f"Registros lidos: {len(df):,}".replace(",", "."))

    # =====================================================
    # COLUNAS NECESSÁRIAS PARA O DASHBOARD
    # =====================================================

    colunas_dashboard = [

        "ano_compra",

        "uf",

        "municipio_instituicao",

        "nome_instituicao",

        "descricao_catmat",

        "modalidade_compra",

        "tipo_compra",

        "fornecedor",

        "fabricante",

        "qtd_itens_comprados",

        "preco_unitario",

        "preco_total"

    ]

    df_dashboard = df[colunas_dashboard].copy()

    # =====================================================
    # EXPORTAÇÃO
    # =====================================================

    pasta_saida = Path("dados_tratados")

    caminho_saida = pasta_saida / "BPS_DASHBOARD.csv"

    df_dashboard.to_csv(

        caminho_saida,

        sep=";",

        encoding="utf-8-sig",

        index=False

    )

    print("\nBase do dashboard criada com sucesso!")

    print(f"Total de registros: {len(df_dashboard):,}".replace(",", "."))

    print(f"Total de colunas: {df_dashboard.shape[1]}")

    print("\nColunas exportadas:\n")

    for coluna in df_dashboard.columns:
        print(f"• {coluna}")

    print(f"\nArquivo salvo em:\n{caminho_saida}")