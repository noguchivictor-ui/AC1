Aluno: Victor Ryu Noguchi | Matrícula: 202601028243

Disciplina: IBM4023

Domínio: Opção C (Clínica Veterinária)


1-criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate      # Windows

2-instalar dependencias e rodar
pip install -r requirements.txt

http://127.0.0.1:5000

3-rotas
/ (GET): Lista todos os animais.

/novo (GET / POST): Formulário e cadastro de animal.

/buscar (GET): Busca animal por nome ou tutor.

/animal/<id> (GET): Ver detalhes do animal e histórico de atendimentos.

/animal/<id>/editar (GET / POST): Editar dados do animal.

/animal/<id>/excluir (POST): Excluir animal e seus atendimentos.

/animal/<id>/atendimento/novo (GET / POST): Cadastrar novo atendimento.

VALIDACOES
Nome do animal: obrigatório (2 a 100 caracteres).

Espécie: obrigatória (mínimo 2 caracteres).

Data de nascimento: formato dd/mm/aaaa e não pode ser no futuro.

Nome do tutor: obrigatório (2 a 100 caracteres).

Regra do Banco: Impede cadastrar dois animais com o mesmo nome para o mesmo tutor (tratado via UNIQUE no banco e verificação em Python).

4-ATENDIMENTO
Descrição: obrigatória (3 a 200 caracteres).

Data: formato dd/mm/aaaa.

Valor: deve ser um valor positivo.

Veterinário: obrigatório (mínimo 2 caracteres).