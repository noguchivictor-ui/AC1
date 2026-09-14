
from datetime import datetime


def texto_valido(texto, minimo=2, maximo=100):

    tamanho = len(texto.strip())
    return minimo <= tamanho <= maximo


def data_formato_valido(data_str):

    try:
        datetime.strptime(data_str.strip(), "%d/%m/%Y")
        return True
    except ValueError:
        return False


def data_nao_futura(data_str):
    
    try:
        data = datetime.strptime(data_str.strip(), "%d/%m/%Y")
        return data <= datetime.now()
    except ValueError:
        return False


def valor_monetario_valido(valor_str):

    try:
        valor = float(valor_str.strip().replace(",", "."))
        return valor > 0
    except ValueError:
        return False



def validar_formulario_animal(dados):

    erros = {}

    if not texto_valido(dados["nome"], minimo=2):
        erros["nome"] = "O nome do animal deve ter entre 2 e 100 caracteres."

    if not texto_valido(dados["especie"], minimo=2):
        erros["especie"] = "Informe a especie do animal (minimo 2 caracteres)."

    if not data_formato_valido(dados["data_nascimento"]):
        erros["data_nascimento"] = "Data invalida. Use o formato dd/mm/aaaa."
    elif not data_nao_futura(dados["data_nascimento"]):
        erros["data_nascimento"] = "A data de nascimento nao pode ser no futuro."

    if not texto_valido(dados["tutor_nome"], minimo=2):
        erros["tutor_nome"] = "O nome do tutor deve ter entre 2 e 100 caracteres."

    return erros




def validar_formulario_atendimento(dados):
  
    erros = {}

    if not texto_valido(dados["descricao"], minimo=3, maximo=200):
        erros["descricao"] = "A descricao deve ter entre 3 e 200 caracteres."

    if not data_formato_valido(dados["data"]):
        erros["data"] = "Data invalida. Use o formato dd/mm/aaaa."

    if not valor_monetario_valido(dados["valor"]):
        erros["valor"] = "O valor deve ser um numero positivo. Ex: 120.50"

    if not texto_valido(dados["veterinario"], minimo=2):
        erros["veterinario"] = "Informe o nome do veterinario (minimo 2 caracteres)."

    return erros


if __name__ == "__main__":
    print("Testes rapidos de validacoes.py")
    print(texto_valido("Rex"))                       # True
    print(data_formato_valido("09/09/2026"))         # True
    print(data_nao_futura("09/09/2099"))             # False
    print(valor_monetario_valido("120,50"))           # True
