from pathlib import Path
import numpy as np
import pandas as pd


def executar_tratamento():
    print("=" * 60)
    print("SPRINT 2: ETL, TRATAMENTO E CONCATENAÇÃO BPS (2020-2026)")
    print("=" * 60)

    pasta_dados = Path("base_dados")
    pasta_saida = Path("dados_tratados")
    pasta_saida.mkdir(exist_ok=True)

    arquivos = sorted(pasta_dados.glob("*.csv"))

    if not arquivos:
        print(
            "Erro: Nenhum arquivo .csv encontrado na pasta 'base_dados'. Verifique o caminho."
        )
        return

    dfs = []

    # Seleção de colunas estratégicas conforme os metadados do BPS e os KPIs exigidos
    colunas_foco = [
        "ano_compra",
        "uf",
        "municipio_instituicao",
        "nome_instituicao",
        "fornecedor",
        "fabricante",
        "modalidade_compra",
        "codigo_br",
        "descricao_catmat",
        "unidade_fornecimento",
        "qtd_itens_comprados",
        "preco_unitario",
        "preco_total",
    ]

    for arquivo in arquivos:
        print(f"Lendo e processando: {arquivo.name}...")

        # Leitura garantindo o encoding correto mapeado na Sprint 1 (latin1)
        df = pd.read_csv(arquivo, sep=";", encoding="latin1", low_memory=False)

        # Padronização e normalização do nome das colunas
        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )

        # Garantia de preenchimento do ano da compra
        if "ano_compra" not in df.columns:
            ano_num = "".join(filter(str.isdigit, arquivo.name))
            df["ano_compra"] = int(ano_num) if ano_num else np.nan

        # Filtragem apenas das colunas necessárias para otimizar tamanho de memória
        cols_presentes = [c for c in colunas_foco if c in df.columns]
        df = df[cols_presentes]

        dfs.append(df)

    print("\nConcatenando os datasets de 2020 a 2026...")
    df_final = pd.concat(dfs, ignore_index=True)

    print(f"Total de registros brutos acumulados: {len(df_final):,}")

    # ===============================================
    # LIMPEZA E SANEAMENTO DOS DADOS
    # ===============================================

    # 1. Remoção de duplicados exatos
    duplicados = df_final.duplicated().sum()
    if duplicados > 0:
        print(f"Removendo {duplicados:,} registros duplicados exatos...")
        df_final.drop_duplicates(inplace=True)

    # 2. Conversão e tratamento de campos numéricos (Troca vírgula por ponto)
    cols_numericas = ["qtd_itens_comprados", "preco_unitario", "preco_total"]
    for col in cols_numericas:
        if col in df_final.columns:
            if df_final[col].dtype == "object":
                df_final[col] = (
                    df_final[col]
                    .astype(str)
                    .str.replace(".", "", regex=False)
                    .str.replace(",", ".", regex=False)
                )
            df_final[col] = pd.to_numeric(df_final[col], errors="coerce")

    # 3. Recálculo/Preenchimento do preco_total quando ausente (quantidade * preco_unitario)
    if (
        "preco_total" in df_final.columns
        and "qtd_itens_comprados" in df_final.columns
        and "preco_unitario" in df_final.columns
    ):
        df_final["preco_total"] = df_final["preco_total"].fillna(
            df_final["qtd_itens_comprados"] * df_final["preco_unitario"]
        )

    # 4. Normalização de texto (caixa alta e remoção de espaços soltos)
    cols_texto = df_final.select_dtypes(
    include=["object", "string", "category"]
).columns
    for col in cols_texto:
        df_final[col] = df_final[col].astype(str).str.strip().str.upper()

    print(f"Total de registros sanitizados: {len(df_final):,}")

    # ===============================================
    # EXPORTAÇÃO DOS ARQUIVOS CONSOLIDADOS
    # ===============================================

    # Nome de saída exigido no edital
    caminho_csv = pasta_saida / "BPS_20_26_StefanoLaurito.csv"
    print(f"\nSalvando arquivo consolidado em: {caminho_csv}")
    df_final.to_csv(caminho_csv, sep=";", encoding="utf-8-sig", index=False)

    print("Processo de Tratamento e Concatenação concluído com sucesso!")


if __name__ == "__main__":
    executar_tratamento()