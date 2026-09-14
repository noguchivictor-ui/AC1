
from flask import Flask, request, render_template, redirect, url_for
from banco import (
    conectar_banco, listar_animais, buscar_animal, animal_duplicado,
    listar_atendimentos_do_animal
)
from validacoes import validar_formulario_animal, validar_formulario_atendimento

app = Flask(__name__)

@app.route("/")
def listar():
    
    conn = conectar_banco()
    animais = listar_animais(conn)
    conn.close()
    return render_template("lista.html", animais=animais, termo="",
                           msg=request.args.get("msg", ""))


@app.route("/animal/<int:id_animal>")
def detalhe(id_animal):
    
    conn = conectar_banco()
    animal = buscar_animal(conn, id_animal)

    if animal is None:
        conn.close()
        return render_template("erro.html",
                               mensagem=f"Nao existe animal com id {id_animal}."), 404

    atendimentos = listar_atendimentos_do_animal(conn, id_animal)
    conn.close()

    return render_template("detalhe.html", animal=animal, atendimentos=atendimentos,
                           msg=request.args.get("msg", ""))


@app.route("/buscar")
def buscar():
   
    termo = request.args.get("termo", "").strip().lower()

    animais = []
    if termo:
        conn = conectar_banco()
        animais = listar_animais(conn, termo=termo)
        conn.close()

    return render_template("lista.html", animais=animais, termo=termo, msg="")




def ler_formulario_animal():
    return {
        "nome": request.form.get("nome", "").strip(),
        "especie": request.form.get("especie", "").strip(),
        "raca": request.form.get("raca", "").strip(),
        "data_nascimento": request.form.get("data_nascimento", "").strip(),
        "tutor_nome": request.form.get("tutor_nome", "").strip(),
    }




@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "GET":
        return render_template("form_animal.html", titulo="Cadastrar animal",
                               dados={}, erros={}, acao=url_for("novo"))

    dados = ler_formulario_animal()
    erros = validar_formulario_animal(dados)

    conn = conectar_banco()
   
    if not erros and animal_duplicado(conn, dados["nome"], dados["tutor_nome"]):
        erros["nome"] = (f"Ja existe um animal chamado '{dados['nome'].title()}' "
                         f"cadastrado para o tutor '{dados['tutor_nome'].title()}'.")

    if erros:
        conn.close()
        return render_template("form_animal.html", titulo="Cadastrar animal",
                               dados=dados, erros=erros,
                               acao=url_for("novo")), 400

    conn.execute(
        'INSERT INTO animais (nome, especie, raca, data_nascimento, tutor_nome)'
        ' VALUES (?, ?, ?, ?, ?)',
        (dados["nome"].title(), dados["especie"].title(), dados["raca"].title(),
         dados["data_nascimento"], dados["tutor_nome"].title()))
    conn.commit()
    conn.close()

    return redirect(url_for("listar", msg="Animal cadastrado com sucesso!"))




@app.route("/animal/<int:id_animal>/editar", methods=["GET", "POST"])
def editar(id_animal):
    conn = conectar_banco()
    animal = buscar_animal(conn, id_animal)

    if animal is None:
        conn.close()
        return render_template("erro.html",
                               mensagem=f"Nao existe animal com id {id_animal}."), 404

    if request.method == "GET":
        conn.close()
        return render_template("form_animal.html", titulo=f"Editar {animal['nome']}",
                               dados=dict(animal), erros={},
                               acao=url_for("editar", id_animal=id_animal))

    dados = ler_formulario_animal()
    erros = validar_formulario_animal(dados)

    if not erros and animal_duplicado(conn, dados["nome"], dados["tutor_nome"],
                                       id_atual=id_animal):
        erros["nome"] = (f"Ja existe um animal chamado '{dados['nome'].title()}' "
                         f"cadastrado para o tutor '{dados['tutor_nome'].title()}'.")

    if erros:
        conn.close()
        return render_template("form_animal.html", titulo=f"Editar {animal['nome']}",
                               dados=dados, erros=erros,
                               acao=url_for("editar", id_animal=id_animal)), 400

    conn.execute(
        'UPDATE animais SET nome = ?, especie = ?, raca = ?,'
        ' data_nascimento = ?, tutor_nome = ? WHERE id = ?',
        (dados["nome"].title(), dados["especie"].title(), dados["raca"].title(),
         dados["data_nascimento"], dados["tutor_nome"].title(), id_animal))
    conn.commit()
    conn.close()

    return redirect(url_for("listar", msg="Dados atualizados com sucesso!"))




@app.route("/animal/<int:id_animal>/excluir", methods=["POST"])
def excluir(id_animal):
    conn = conectar_banco()
    animal = buscar_animal(conn, id_animal)

    if animal is None:
        conn.close()
        return render_template("erro.html",
                               mensagem=f"Nao existe animal com id {id_animal}."), 404

    conn.execute('DELETE FROM animais WHERE id = ?', (id_animal,))
    conn.commit()
    conn.close()

    return redirect(url_for("listar", msg=f"Registro de {animal['nome']} excluido."))



def ler_formulario_atendimento():
    return {
        "descricao": request.form.get("descricao", "").strip(),
        "data": request.form.get("data", "").strip(),
        "valor": request.form.get("valor", "").strip(),
        "veterinario": request.form.get("veterinario", "").strip(),
    }


@app.route("/animal/<int:id_animal>/atendimento/novo", methods=["GET", "POST"])
def novo_atendimento(id_animal):
    conn = conectar_banco()
    animal = buscar_animal(conn, id_animal)

    if animal is None:
        conn.close()
        return render_template("erro.html",
                               mensagem=f"Nao existe animal com id {id_animal}."), 404

    if request.method == "GET":
        conn.close()
        return render_template("form_atendimento.html",
                               titulo=f"Novo atendimento - {animal['nome']}",
                               dados={}, erros={}, animal=animal,
                               acao=url_for("novo_atendimento", id_animal=id_animal))

    dados = ler_formulario_atendimento()
    erros = validar_formulario_atendimento(dados)

    if erros:
        conn.close()
        return render_template("form_atendimento.html",
                               titulo=f"Novo atendimento - {animal['nome']}",
                               dados=dados, erros=erros, animal=animal,
                               acao=url_for("novo_atendimento", id_animal=id_animal)), 400

    conn.execute(
        'INSERT INTO atendimentos (animal_id, descricao, data, valor, veterinario)'
        ' VALUES (?, ?, ?, ?, ?)',
        (id_animal, dados["descricao"], dados["data"],
         float(dados["valor"].replace(",", ".")), dados["veterinario"].title()))
    conn.commit()
    conn.close()

    return redirect(url_for("detalhe", id_animal=id_animal,
                            msg="Atendimento registrado com sucesso!"))


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("erro.html",
                           mensagem="Confira o endereco digitado."), 404


if __name__ == "__main__":
    app.run(debug=True)
