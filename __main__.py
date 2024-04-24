import os
from Classes.Biblioteca import Biblioteca

def limpar_console():
    os.system("cls")

def abrirMenu():
    biblioteca = Biblioteca()
    while True:
        print("\nBem-vindo à Biblioteca")
        print("1 - Cadastrar Livros")
        print("2 - Consultar Livros")
        print("3 - Devolução de Livro")
        print("4 - Empréstimo de Livro")
        print("5 - Cadastrar Usuários")
        print("6 - Consultar Usuários")
        print("7 - Relatórios")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            titulo = input("Título do Livro: ").strip()
            autor = input("Autor do Livro: ").strip()
            if not titulo or not autor:
                print("###### Título e autor não podem ser vazios. ######")
                continue
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
                continue  # Retornar ao início do loop

            biblioteca.cadastrar_livro(titulo, autor, ano, copias)
        elif opcao == '2':
            busca = input("Informe o título, autor ou ano para consulta: ")
            biblioteca.consultar_livros(busca)
        elif opcao == '3':
            livros = biblioteca.get_lista_livros_emprestados()
            if not livros:
                print("Não há livros emprestados.")
            else:
                print("Lista de Livros:")
                for i, livro in enumerate(livros):
                    print(f"{i + 1}. Título: {livro.titulo}, Autor: {livro.autor}, Ano: {livro.ano_publicacao}, Cópias: {livro.copias}")

                opcao = input("Digite o número do livro que deseja devolver (ou digite '0' para sair): ")
                if opcao.isdigit():
                    opcao = int(opcao)
                    if opcao == 0:
                        print("Operação cancelada.")
                    elif opcao > 0 and opcao <= len(livros):
                        livro = livros[opcao - 1]
                        print(f"Você escolheu devolver o livro '{livro.titulo}'.")
                        biblioteca.devolver_livro(livro.titulo)
                    else:
                        print("Escolha inválida. Por favor, escolha um número válido.")
                else:
                    print("Escolha inválida. Por favor, digite um número.")


        elif opcao == '4':
            livros_disponiveis = biblioteca.get_lista_livros()
            if not livros_disponiveis:
                print("Não há livros disponíveis para empréstimo.")
            else:
                print("Lista de Livros Disponíveis para Empréstimo:")
                for i, livro in enumerate(livros_disponiveis):
                    print(f"{i + 1}. Título: {livro.titulo}, Autor: {livro.autor}, Ano: {livro.ano_publicacao}, Cópias Disponíveis: {livro.copias}")

            opcao = input("Digite o número do livro que deseja emprestar ('0' para sair): ")
            if opcao.isdigit():
                opcao = int(opcao)
                if opcao == 0:
                    print("Operação cancelada.")
                elif opcao > 0 and opcao <= len(livros_disponiveis):
                    livro_escolhido = livros_disponiveis[opcao - 1]
                    id_usuario = input("ID do Usuário que está Emprestando: ")
                    biblioteca.emprestar_livro(livro_escolhido.titulo, id_usuario)
                else:
                    print("Escolha inválida. Por favor, escolha um número válido.")
            else:
                print("Escolha inválida. Por favor, digite um número.")
                
        elif opcao == '5':
            nome = input("Nome do Usuário: ")
            contato = input("Contato: ")
            biblioteca.cadastrar_usuario(nome, contato)
        elif opcao == '6':
            id_usuario = input("ID do Usuário para Consulta (vazio caso queira listar todos): ")
            biblioteca.consultar_usuarios(id_usuario)
        elif opcao == '7':
            biblioteca.gerar_relatorios()
        elif opcao == '0':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")
        
        input("Pressione Enter para continuar...")
        limpar_console()

if __name__ == "__main__":
    abrirMenu()
