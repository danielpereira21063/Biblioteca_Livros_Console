import os
from Classes.Biblioteca import Biblioteca

def limpar_console():
    os.system("cls")

def abrirMenu():
    biblioteca = Biblioteca()
    while True:
        print("\nBem-vindo à Biblioteca")
        print("===============================")
        print("            MENU               ")
        print("===============================")
        print("1 - Cadastrar Livros")
        print("2 - Consultar Livros")
        print("3 - Devolução de Livro")
        print("4 - Empréstimo de Livro")
        print("5 - Cadastrar Usuários")
        print("6 - Consultar Usuários")
        print("7 - Relatórios")
        print("0 - Sair")
        print("===============================")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_livro(biblioteca)
        elif opcao == '2':
            consultar_livros(biblioteca)
        elif opcao == '3':
            devolver_livro(biblioteca)
        elif opcao == '4':
            emprestar_livro(biblioteca)
        elif opcao == '5':
            cadastrar_usuario(biblioteca)
        elif opcao == '6':
            consultar_usuarios(biblioteca)
        elif opcao == '7':
            gerar_relatorios(biblioteca)
        elif opcao == '0':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")
        
        input("Pressione Enter para continuar...")
        limpar_console()

def cadastrar_livro(biblioteca):
    print("\nCadastrar Livros")
    print("===============================")
    titulo = input("Título do Livro: ").strip()
    autor = input("Autor do Livro: ").strip()
    if not titulo or not autor:
        print("###### Título e autor não podem ser vazios. ######")
        return
    try:
        ano = int(input("Ano de Publicação: "))
        copias = int(input("Número de Cópias: "))
        if ano <= 0 or copias < 0:
            raise ValueError("###### Ano de publicação e número de cópias devem ser valores maiores que 0. ######")
    except ValueError as e:
        if "invalid literal for int()" in str(e):
            print("###### Ano de publicação e número de cópias devem ser valores maiores que 0. ######")
        else:
            print(f"###### {str(e)} ######")
        return  # Retornar ao início do loop

    biblioteca.cadastrar_livro(titulo, autor, ano, copias)

def consultar_livros(biblioteca):
    print("\nConsultar Livros")
    print("===============================")
    busca = input("Informe o título, autor ou ano para consulta (pressione Enter para consulta completa): ")
    biblioteca.consultar_livros(busca)

def devolver_livro(biblioteca):
    print("\nDevolução de Livro")
    print("===============================")
    livros_emprestados = biblioteca.get_lista_livros_emprestados()
    if not livros_emprestados:
        print("Não há livros emprestados.")
    else:
        print("Lista de Livros emprestados: ")
        for i, livro in enumerate(livros_emprestados):
            print(f"{i + 1}. Usuário: {livro['nome_usuario']} Título: {livro['titulo']}, Autor: {livro['autor']}, Ano: {livro['ano_publicacao']}, Cópias: {livro['copias']}")

        opcao = input("Digite o número do livro que deseja devolver (ou digite '0' para sair): ")
        if opcao.isdigit():
            opcao = int(opcao)
            if opcao == 0:
                print("Operação cancelada.")
            elif opcao > 0 and opcao <= len(livros_emprestados):
                livro = livros_emprestados[opcao - 1]
                print(f"Você escolheu devolver o livro '{livro['titulo']}'.")
                biblioteca.devolver_livro(livro['titulo'], livro['idUsuario'])
            else:
                print("Escolha inválida. Por favor, escolha um número válido.")
        else:
            print("Escolha inválida. Por favor, digite um número.")

def emprestar_livro(biblioteca):
    print("\nEmpréstimo de Livro")
    print("===============================")
    livros_disponiveis = biblioteca.get_lista_livros()
    if not livros_disponiveis:
        print("Não há livros disponíveis para empréstimo.")
    else:
        print("Lista de Livros Disponíveis para Empréstimo: \n")
        for i, livro in enumerate(livros_disponiveis):
            print(f"{i + 1}. Título: {livro.titulo}, Autor: {livro.autor}, Ano: {livro.ano_publicacao}, Cópias Disponíveis: {livro.copias}")

    opcao = input("\nDigite o número do livro que deseja emprestar ('0' para sair): ")
    if opcao.isdigit():
        opcao = int(opcao)
        if opcao == 0:
            print("Operação cancelada.")
        elif opcao > 0 and opcao <= len(livros_disponiveis):
            livro_escolhido = livros_disponiveis[opcao - 1]

            biblioteca.consultar_usuarios()
            id_usuario = input("ID do Usuário que está Emprestando: ")
            biblioteca.emprestar_livro(livro_escolhido, id_usuario)
        else:
            print("Escolha inválida. Por favor, escolha um número válido.")
    else:
        print("Escolha inválida. Por favor, digite um número.")

def cadastrar_usuario(biblioteca):
    print("\nCadastrar Usuários")
    print("===============================")
    nome = input("Nome do Usuário: ")  # Pergunta pelo nome do usuário
    contato = input("Contato: ")  # Pede o contato
    if nome.strip() == "" or contato.strip() == "":  # Se nome ou contato estiverem vazios
        print("Nome e contato não podem estar vazios. Por favor, tente novamente.")  # Indica que nome e contato não podem ser vazios
    else:
        biblioteca.cadastrar_usuario(nome, contato)  # Chama o método de cadastro na biblioteca


def consultar_usuarios(biblioteca):
    print("\nConsultar Usuários")
    print("===============================")
    id_usuario = input("ID do Usuário para Consulta (vazio caso queira listar todos): \n")
    biblioteca.consultar_usuarios(id_usuario)

def gerar_relatorios(biblioteca):
    print("\nRelatórios")
    print("===============================")
    print("Relatório de Livros:")
    biblioteca.listar_detalhes_livros()
    print("\nRelatório de Usuários:")
    biblioteca.listar_detalhes_usuarios()
    print("\nRelatório de Livros Emprestados:")
    biblioteca.listar_detalhes_livros_emprestados()

if __name__ == "__main__":
    abrirMenu()
