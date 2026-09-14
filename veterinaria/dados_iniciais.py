
from banco import conectar_banco

conn = conectar_banco()

conn.execute('DELETE FROM atendimentos')
conn.execute('DELETE FROM animais')
conn.commit()

animais = [
    ("Rex", "Cachorro", "Vira-lata", "15/03/2021", "João Silva"),
    ("Mia", "Gato", "Siamês", "02/07/2022", "Ana Souza"),
    ("Bidu", "Cachorro", "Poodle", "20/11/2019", "Carlos Pereira"),
]

ids = []
for nome, especie, raca, nascimento, tutor in animais:
    cursor = conn.execute(
        'INSERT INTO animais (nome, especie, raca, data_nascimento, tutor_nome)'
        ' VALUES (?, ?, ?, ?, ?)',
        (nome, especie, raca, nascimento, tutor)
    )
    ids.append(cursor.lastrowid)

rex_id, mia_id, bidu_id = ids

atendimentos = [
    (rex_id, "Consulta de rotina", "10/01/2026", 120.00, "Dra. Fernanda Lima"),
    (rex_id, "Vacina V10", "15/02/2026", 90.00, "Dra. Fernanda Lima"),
    (mia_id, "Exame de sangue", "05/03/2026", 180.50, "Dr. Ricardo Alves"),
    (mia_id, "Aplicação de vermífugo", "20/04/2026", 60.00, "Dr. Ricardo Alves"),
 
]

for animal_id, descricao, data, valor, veterinario in atendimentos:
    conn.execute(
        'INSERT INTO atendimentos (animal_id, descricao, data, valor, veterinario)'
        ' VALUES (?, ?, ?, ?, ?)',
        (animal_id, descricao, data, valor, veterinario)
    )

conn.commit()
conn.close()

print("Banco populado com sucesso!")
print(f"  {len(animais)} animais cadastrados")
print(f"  {len(atendimentos)} atendimentos cadastrados")
print("  'Bidu' foi cadastrado sem nenhum atendimento (testa a tela de detalhe vazia)")
