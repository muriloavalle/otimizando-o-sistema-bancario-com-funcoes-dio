"""
Desafio 2!

Objetivo geral: Separar as funcoes existentes de saque, deposito, e extrato
em funcoes. Criar duas novas funcoes: cadastrar usuario(cliente) e cadastrar 
conta bancaria.

Precisamos deixar nosso codigo mais modularizado, para isso vamos criar funcoes
para as operacoes existentes: sacar, depositar e vizualizar extrato. Alem disso,
para a versao 2 do nosso sistema precisamos criar duas novas funcoes: criar usuario
(cliente do banco) e criar conta corrente (vincular com usuario)

Devemos criar funcoes para todas as operacoes do sistema. Para exercitar tudo o que
aprendemos neste modulo, cada funcao vai ter uma regra na passagem de argumentos.
O retorno e a forma como serao chamadas, pode ser definida por voce da forma que achar melhor.

Saque - A funcao saque deve receber os argumentos apenas por nome (keyword only). Sugestao de argumentos:
saldo, valor, extrato, limite, numero_saques, limite_saques. Sugestao de retorno: saldo e extrato.

Deposito - A funcao deposito deve receber os argumentos apenas por posicao (positional only). Sugestao
de argumentos: saldo, valor, extrato. Sugestao de retorno: saldo e extrato.

Extrato - A funcao extrato deve receber os argumentos por posicao e nome (positional only e keyword only).
Argumentos posicionais: saldo, argumentos nomeados: extrato.

Novas funcoes - Precisamos criar duas novas funcoes: criar usuario e criar conta corrente. Fique a vontade
para adicionar mais funcoes, exemplo: listar contas.

Criar usuario (cliente) - O programa deve armazenar os usuarios em uma lista, um usuario é composto por:
nome, data de nascimento, cpf e endereco. O endereco deve ser uma string com o formato: logradouro - numero - bairro - cidade/sigla estado.
Deve ser armazenado somente os numeros do cpf. Nao podemos cadastrar dois usuarios com o mesmo cpf.

Criar conta corrente - O programa deve armazenar contas em uma lista, uma conta deve ser composta por: agencia, numero da conta e usuario.
O numero da conta deve ser sequencial, iniciando em 1. O numero da agencia deve ser fixo: "0001". O usuario pode ter mais de uma conta,
mas uma conta pertence a somente um usuario.

Dica - Para vincular um usuario a uma conta, filtre a lista de usuarios buscando o numero do cpf informado para cada usuario da lista.
"""

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operacao invalida: saldo insuficiente.")
    elif excedeu_limite:
        print("Operacao invalida: valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operacao invalida: limite de saques diarios atingido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Operacao invalida: valor informado e invalido.")

    return saldo, extrato, numero_saques


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Deposito: R$ {valor:.2f}\n"
    else:
        print("Operacao invalida: o valor informado deve ser positivo.")
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Nao foram realizadas movimentacoes." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente numeros): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Usuario com este CPF ja existe.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereco (logradouro - numero - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("Usuario criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)


def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        contas.append({
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        })
        print("Conta criada com sucesso!")
        return True  # conta criada
    else:
        print("Usuario nao encontrado. Crie o usuario antes de criar a conta.")
        return False  # conta não criada


def listar_contas(contas):
    for conta in contas:
        print(f"""\
Agencia: {conta['agencia']}
Conta: {conta['numero_conta']}
Titular: {conta['usuario']['nome']}
""")


def menu():
    return input("""
======> M E N U <======
                 
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuario
[nc] Nova Conta
[lc] Listar Contas
[q] Sair
                 
=======================
=> """)


def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do deposito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            if criar_conta(AGENCIA, numero_conta, usuarios, contas):
                numero_conta += 1  # só incrementa se a conta foi criada

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Obrigado por usar o nosso Banco! Volte sempre!")
            break

        else:
            print("Operação inválida, por favor selecione novamente.")


main()
