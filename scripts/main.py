from exploracao import gerar_relatorio
from tratamento import tratar_bases
import exportacao

print(exportacao.__file__)
print(dir(exportacao))
from exportacao import gerar_bases_dashboard

print("=" * 50)
print("PROJETO BPS 2020-2026")
print("=" * 50)

gerar_relatorio()
tratar_bases()
gerar_bases_dashboard()

print("\nProjeto finalizado com sucesso!")