from pathlib import Path
import pandas as pd


def explorar_bases_bps():
    print("=" * 60)
    print("SPRINT 1: ANÁLISE EXPLORATÓRIA DAS BASES BPS (2020-2026)")
    print("=" * 60)

    pasta_dados = Path("base_dados")
    pasta_relatorios = Path("relatorios")
    pasta_relatorios.mkdir(exist_ok=True)

    arquivos = sorted(pasta_dados.glob("*.csv"))

    if not arquivos:
        print(
            "Nenhum arquivo .csv encontrado em 'base_dados'. Coloque as bases na pasta."
        )
        return

    resumo = []
    estrutura_colunas = {}

    for arquivo in arquivos:
        print(f"Analisando {arquivo.name}...")

        # Tenta ler com latin1 e se falhar tenta utf-8
        try:
            df = pd.read_csv(
                arquivo, sep=";", encoding="latin1", low_memory=False
            )
            encoding_usado = "latin1"
        except Exception:
            df = pd.read_csv(
                arquivo, sep=";", encoding="utf-8-sig", low_memory=False
            )
            encoding_usado = "utf-8-sig"

        # Guarda lista de colunas para comparar estrutura entre anos
        cols_normalizadas = sorted(
            [c.strip().lower() for c in df.columns.astype(str)]
        )
        estrutura_colunas[arquivo.name] = cols_normalizadas

        resumo.append(
            {
                "Arquivo": arquivo.name,
                "Encoding": encoding_usado,
                "Linhas": len(df),
                "Colunas": len(df.columns),
                "Linhas Duplicadas": df.duplicated().sum(),
                "Valores Nulos Totais": df.isnull().sum().sum(),
            }
        )

    # DataFrame com o resumo quantitativo
    df_resumo = pd.DataFrame(resumo)

    print("\nRESUMO GERAL DAS BASES:")
    print(df_resumo.to_string(index=False))

    # Salva relatório em CSV para colocar/citar no README.md
    caminho_relatorio = pasta_relatorios / "relatorio_exploracao_bps.csv"
    df_resumo.to_csv(
        caminho_relatorio, sep=";", encoding="utf-8-sig", index=False
    )
    print(f"\nRelatório do resumo salvo em: {caminho_relatorio}")

    # Checagem de colunas divergentes entre anos
    print("\nVERIFICAÇÃO DE ESTRUTURA DE COLUNAS:")
    primeiro_arquivo = arquivos[0].name
    cols_referencia = set(estrutura_colunas[primeiro_arquivo])

    divergencias = False
    for arq_nome, cols in estrutura_colunas.items():
        if set(cols) != cols_referencia:
            divergencias = True
            diff_mais = set(cols) - cols_referencia
            diff_menos = cols_referencia - set(cols)
            print(f"{arq_nome} possui colunas diferentes do padrão:")
            if diff_mais:
                print(f"   + Colunas a mais: {diff_mais}")
            if diff_menos:
                print(f"   - Colunas ausentes: {diff_menos}")

    if not divergencias:
        print(
            "Todas as bases possuem nomes de colunas idênticos (após normalização de texto)."
        )

    # --- NOVO BLOCO: ANÁLISE DA BASE FINAL TRATADA ---
    caminho_base_tratada = Path("dados_tratados") / "BPS_20_26_StefanoLaurito.csv"
    if caminho_base_tratada.exists():
        print("\n" + "=" * 60)
        print("DIAGNOSTICO DA BASE FINAL CONSOLIDADA E TRATADA")
        print("=" * 60)
        
        df_tratado = pd.read_csv(caminho_base_tratada, sep=";", low_memory=False)
        
        print(f"Total de registros sanitizados: {len(df_tratado):,}")
        print(f"Colunas presentes ({len(df_tratado.columns)}): {list(df_tratado.columns)}\n")
        
        print("--- Valores Nulos por Coluna ---")
        nulos = df_tratado.isnull().sum()
        print(nulos[nulos > 0] if nulos.sum() > 0 else "Nenhum valor nulo encontrado.")
        
        print("\n--- Estatísticas das Métricas Numéricas ---")
        cols_num = [c for c in ["preco_total", "qtd_itens_comprados", "preco_unitario"] if c in df_tratado.columns]
        if cols_num:
            print(df_tratado[cols_num].describe().apply(lambda x: x.map("{:,.2f}".format)))
            
        print("\n--- Top 5 Categorias das Principais Colunas ---")
        cols_cat = [c for c in ["ano_compra", "uf", "modalidade_compra"] if c in df_tratado.columns]
        for col in cols_cat:
            print(f"\n[Coluna: {col}]")
            print(df_tratado[col].value_counts().head(5))

    print("\nExploração concluída com sucesso!")


if __name__ == "__main__":
    explorar_bases_bps()