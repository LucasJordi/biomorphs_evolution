import csv

# Lista de todas as regras do Jogo da Vida, exemplificativa e incompleta para fins didáticos
rules_list = [
    ("Conway's Life", "B3/S23"),
    ("HighLife", "B36/S23"),
    ("Day & Night", "B3678/S34678"),
    ("2x2", "B36/S125"),
    ("Seeds", "B2/S"),
    ("Replicator", "B1357/S1357"),
    ("Life Without Death", "B3/S012345678"),
    ("Maze", "B3/S12345"),
    ("Anneal", "B4678/S35678"),
    ("Diamoeba", "B35678/S5678"),
    ("Margolus", "B2/S"),
    ("Golly", "B3678/S45678"),
    ("Brian's Brain", "B/S012345678"),
    ("Corral", "B35/S234"),
    ("CorralPlus", "B35/S2345"),
    ("Pulsar", "B36/S23"),
    ("2D Cellular Automaton", "B2/S0123456789"),
    ("Conway's Life 2", "B36/S23"),
    ("Small Exploder", "B1357/S1357"),
    ("Extended Life", "B3/S012345678"),
    ("AntiLife", "B/S012345678"),
    ("Replicator 2", "B1357/S1357"),
    # Adicione outras regras conforme necessário
]

# Criar um arquivo CSV com todas as regras
csv_filename = "life_rules.csv"

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Nome", "Regra"])  # Cabeçalho do CSV
    writer.writerows(rules_list)

print(f"Arquivo CSV '{csv_filename}' criado com sucesso!")