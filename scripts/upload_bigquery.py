from pathlib import Path
import pandas as pd
import pandas_gbq


def enviar_para_bigquery():
    # Substitua pelo ID exato que aparece no seletor do topo do Google Cloud
    project_id = "bps-20-26-stefano-laurito"
    dataset_table = "bps_dataset.bps_2020_2026"

    caminho_csv = Path("dados_tratados") / "BPS_20_26_StefanoLaurito.csv"

    print("Carregando arquivo CSV tratado...")
    df = pd.read_csv(caminho_csv, sep=";")

    print(
        f"Enviando {len(df):,} linhas para o BigQuery ({dataset_table})..."
    )

    # Usa a biblioteca pandas_gbq diretamente
    pandas_gbq.to_gbq(
        dataframe=df,
        destination_table=dataset_table,
        project_id=project_id,
        if_exists="replace",
    )

    print("Upload para o BigQuery concluido com sucesso!")


if __name__ == "__main__":
    enviar_para_bigquery()