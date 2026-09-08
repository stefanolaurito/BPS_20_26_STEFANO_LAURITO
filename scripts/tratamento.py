import os
import pandas as pd

# Diretórios
PASTA_ENTRADA = 'base_dados'
PASTA_SAIDA = 'dados_tratados'
ARQUIVO_FINAL = os.path.join(PASTA_SAIDA, 'BPS_20_26_StefanoLaurito.csv')

# Garantir que a pasta de saída existe
os.makedirs(PASTA_SAIDA, exist_ok=True)

dfs = []

print("Iniciando o processamento dos arquivos...")

for arquivo in os.listdir(PASTA_ENTRADA):
    if arquivo.endswith('.csv'):
        caminho_completo = os.path.join(PASTA_ENTRADA, arquivo)
        print(f"Lendo: {arquivo}")
        
        # Tenta ler com UTF-8, se falhar tenta Latin-1 (comum em dados públicos br)
        try:
            df = pd.read_csv(caminho_completo, sep=';', encoding='utf-8', low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(caminho_completo, sep=';', encoding='latin-1', low_memory=False)
        
        # Padronizar nomes de colunas para minúsculas
        df.columns = df.columns.str.strip().str.lower()
        
        dfs.append(df)

# Concatenação de todas as bases anuais
df_consolidado = pd.concat(dfs, ignore_index=True)
print("Bases concatenadas com sucesso!")

# Exemplo de seleção de colunas essenciais para reduzir o tamanho do arquivo
# (Ajuste o nome exato das colunas conforme o dicionário de dados do BPS)
colunas_essenciais = [
    'ano', 'uf', 'municipio', 'instituicao', 
    'fornecedor', 'fabricante', 'produto', 
    'modalidade_compra', 'quantidade', 'preco_unitario', 'preco_total'
]

# Mantém apenas as colunas existentes na base
colunas_presentes = [col for col in colunas_essenciais if col in df_consolidado.columns]
df_filtrado = df_consolidado[colunas_presentes].copy()

# Tratamento de nulos e duplicados
df_filtrado.drop_duplicates(inplace=True)

# Salvar arquivo tratado final
df_filtrado.to_csv(ARQUIVO_FINAL, index=False, sep=',', encoding='utf-8')
print(f"Processo concluído! Arquivo salvo em: {ARQUIVO_FINAL}")