# Mini-Projeto Avaliativo - Módulo 2 - Semana 06
**Autor:** Stefano Laurito

---

# Dashboard BPS (2020-2026) - Análise de Compras Públicas de Saúde (SUS)

## 1. Objetivo do Projeto
Desenvolver uma solução completa de Engenharia de Dados e Business Intelligence para centralizar, tratar e visualizar os dados de compras públicas de medicamentos e insumos de saúde do SUS. O projeto visa disponibilizar um dashboard executivo e analítico para tomada de decisão e monitoramento de custos públicos.

## 2. Contextualização do Problema
O Banco de Preços em Saúde (BPS) disponibiliza dados fragmentados em bases anuais com grande volume de registros, presença de inconsistências de codificação e discrepâncias de valores unitários/lotes. A falta de uma visão consolidada dificulta a identificação de discrepâncias de preços, a análise regional dos gastos e o acompanhamento temporal das aquisições do SUS.

## 3. Fonte dos Dados
* **Origem:** Banco de Preços em Saúde (BPS / Ministério da Saúde).
* **Período:** 2020 a 2026 (7 arquivos CSV anuais).
* **Volume:** 341.056 registros sanitizados na base final consolidada.

## 4. Procedimentos de Download e Concatenação
1. Coleta e download manual das bases históricas em formato CSV na pasta local `base_dados/`.
2. Execução de script Python (`scripts/exploracao.py`) para leitura dinâmica dos arquivos no diretório.
3. Detecção e tratamento de encondings (`latin1` e `utf-8-sig`) e delimitadores (ponto e vírgula `;`).
4. Normalização dos nomes das colunas e concatenação tabular do período 2020-2026.

## 5. Tratamentos e Transformações Realizados
* **Sanitização de Enconding:** Mapeamento e correção de caracteres especiais nas modalidades de compra via campos calculados (`CASE WHEN`).
* **Tratamento de Nulos:** Validação de ausência de nulos em métricas numéricas e tratamento residual em colunas institucionais.
* **Remoção de Duplicidades:** Deduplicação de registros idênticos entre as bases anuais.
* **Métricas Ponderadas:** Criação de fórmulas para mitigar a distorção causada por lotes com volumes discrepantes (outliers de até 22,8 bilhões no valor total).

## 6. Descrição das Principais Colunas Utilizadas
* `ano_compra`: Ano em que a compra pública foi realizada (2020 a 2026).
* `uf`: Unidade Federativa da instituição compradora.
* `municipio_instituicao`: Município de localização do órgão comprador.
* `nome_instituicao`: Nome do órgão ou hospital público comprador.
* `modalidade_compra`: Tipo de processo licitatório (Pregão, Dispensa, etc.).
* `codigo_br` / `descricao_catmat`: Código descritivo e especificação técnica do medicamento ou item no catálogo CATMAT.
* `qtd_itens_comprados`: Quantidade de unidades adquiridas na transação.
* `preco_unitario`: Valor unitário nominal do item.
* `preco_total`: Valor financeiro total da transação.

## 7. Definição dos KPIs e Métricas
* **Valor Total Investido:** `SUM(preco_total)` — Volume financeiro total movimentado em compras públicas.
* **Quantidade de Itens Adquiridos:** `SUM(qtd_itens_comprados)` — Volume físico total de insumos e medicamentos fornecidos.
* **Preço Médio Ponderado:** `SUM(preco_total) / SUM(qtd_itens_comprados)` — Custo real médio por unidade, evitando viés por lote.
* **Total de Processos:** `COUNT(codigo_br)` — Quantidade total de registros licitatórios.
* **Instituições Compradoras:** `COUNT_DISTINCT(nome_instituicao)` — Total de órgãos públicos compradores mapeados.

## 8. Link ou Imagens do Dashboard
* **Dashboard Interativo (Looker Studio):** https://github.com/stefanolaurito/BPS_20_26_STEFANO_LAURITO

## 9. Principais Análises e Descobertas
* **Concentração Regional:** Estados como Paraná (PR) e São Paulo (SP) concentram os maiores volumes absolutos de investimento público no período.
* **Variação Temporal:** Picos expressivos de gasto total e variação do Preço Médio Ponderado identificados nos anos de 2022 e 2025.
* **Predominância Licitatória:** A modalidade *Pregão* representa a esmagadora maioria das aquisições do BPS (mais de 310 mil processos).

## 10. Recomendações Baseadas nos Dados
* **Padronização de Compras:** Utilizar o Preço Médio Ponderado nacional como *benchmark* obrigatório para negociações estaduais e municipais.
* **Auditoria de Outliers:** Investigar processos com preço unitário atípico em relação à média do catálogo CATMAT.
* **Centralização de Lotes:** Incentivar compras consorciadas para aumentar o ganho de escala nas regiões de menor volume de aquisição.

## 11. Limitações Identificadas
* Presença de erros de enconding na base de origem que demandam tratamento na camada de exibição.
* Inconsistências extremas (outliers) no valor total de lotes atípicos que invalidam o uso de médias simples.
* Base de 2026 parcial em relação aos anos anteriores.

## 12. Instruções para Reprodução do Projeto
1. Clone o repositório: https://github.com/stefanolaurito/BPS_20_26_STEFANO_LAURITO.git
   cd BPS_20_26_STEFANO_LAURITO
   ```
2. Instale as dependências exigidas (`pandas`, `pandas-gbq`, `google-cloud-bigquery`).
3. Adicione os arquivos brutos (`2020.csv` a `2026.csv`) no diretório `base_dados/`.
4. Execute os scripts `scripts/exploracao.py` e `scripts/carga_bigquery.py` para realizar a sanitização e a carga no BigQuery.
  