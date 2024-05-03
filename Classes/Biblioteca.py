import csv  # Importa a bibioteca csv para trabalhar com arquivos CSV
from Classes.Livro import Livro  # Importa a classe Livro do módulo Livro
from Classes.Usuario import Usuario  # Importa a classe Usuario do módulo Usuario
class Biblioteca:
    def __init__(self):
        self.livros = {}
        self.livros_emprestados = {}
        self.usuarios = {}

        # Carregar dados do CSV ao iniciar o programa
        self.carregar_livros_csv("Database/livros.csv")
        self.carregar_usuarios_csv("Database/usuarios.csv")
        self.carregar_livros_emprestados_csv("Database/livros_emprestados.csv")
    
    def cadastrar_livro(self, titulo, autor, ano, copias):
        id_ultimo_livro_cadastrado = self.carregar_ultimo_id_livro_cadastrado()
        proximo_id_livro = id_ultimo_livro_cadastrado + 1

        if titulo not in self.livros:
            # Cria o livro com o próximo ID sequencial
            self.livros[proximo_id_livro] = Livro(proximo_id_livro, titulo, autor, ano, copias)
        else:
            self.livros[titulo].copias += copias
        print(f"Livro '{titulo}' cadastrado com sucesso.")

        # Após cadastrar o livro, salvar os livros em um arquivo CSV
        self.salvar_livros_csv("Database/livros.csv")
    
    def cadastrar_usuario(self, nome, contato):
        # Obtém o último ID de usuário cadastrado
        ultimo_id_usuario = self.carregar_ultimo_id_usuario_cadastrado()
        # Incrementa o ID para o próximo usuário
        id_usuario = ultimo_id_usuario + 1

        # Cria um novo usuário com as informações fornecidas
        self.usuarios[id_usuario] = Usuario(nome, id_usuario, contato)
        # Imprime uma mensagem de sucesso com o nome do usuário e seu ID
        print(f"Usuário '{nome}' cadastrado com sucesso. ID: {id_usuario}")
        # Salva os usuários em um arquivo CSV após cadastrar um novo usuário
        self.salvar_usuarios_csv("Database/usuarios.csv")

    def consultar_usuarios(self, id_usuario=None):
        # Verifica se o ID do usuário foi fornecido
        if id_usuario is None or id_usuario == "":
            # Se nenhum ID for fornecido, lista todos os usuários cadastrados
            if self.usuarios:
                # Imprime a lista de todos os usuários cadastrados na biblioteca
                print("Lista de todos os usuários cadastrados na biblioteca:")
                # Itera sobre cada usuário no dicionário de usuários
                for id_usuario, usuario in self.usuarios.items():
                    # Imprime as informações do usuário
                    print(f"Informações do usuário (ID {id_usuario}):")
                    print(f"Nome: {usuario.nome}")
                    print(f"Contato: {usuario.contato}")
                    print()
            else:
                # Se não houver usuários cadastrados, imprime uma mensagem
                print("Não há usuários cadastrados na biblioteca.")
        else:
            # Se um ID de usuário foi fornecido, verifica se ele existe
            if id_usuario in self.usuarios:
                # Se o ID de usuário existe, obtém as informações do usuário correspondente
                usuario = self.usuarios[id_usuario]
                # Imprime as informações do usuário
                print(f"Informações do usuário (ID {id_usuario}):")
                print(f"Nome: {usuario.nome}")
                print(f"Contato: {usuario.contato}")
            else:
                # Se o ID de usuário não existir, imprime uma mensagem
                print(f"Usuário com ID {id_usuario} não encontrado.")

    def carregar_ultimo_id_usuario_cadastrado(self):
            # Verifica se existem usuários cadastrados para determinar o último ID
            if self.usuarios:
                # Se houver usuários cadastrados, cria uma lista dos IDs de usuários
                lista_ids_usuarios = list(self.usuarios.keys())
                # Retorna o maior ID de usuário na lista
                return max(lista_ids_usuarios)
            else:
                # Se não houver usuários cadastrados, retorna 0
                return 0 

    def carregar_ultimo_id_livro_cadastrado(self):
            # Verifica se existem livros cadastrados para determinar o último ID
            if self.livros:
                # Se houver livros cadastrados, cria uma lista dos IDs de livros
                lista_ids_livros = list(self.livros.keys())
                # Retorna o maior ID de livro na lista
                return max(lista_ids_livros)
            else:
                # Se não houver livros cadastrados, retorna 0
                return 0 

    def obter_usuario_por_id(self, id_usuario):
        # Inicializa a variável 'usuario' como None
        usuario = None
        # Converte o ID do usuário para um número inteiro
        id_usuario = int(id_usuario)
        # Itera sobre cada item no dicionário de usuários
        for i in self.usuarios:
            # Verifica se o ID do usuário atual corresponde ao ID fornecido
            if(self.usuarios[i].id_usuario == id_usuario):
                # Se encontrar o usuário correspondente, atribui-o à variável 'usuario'
                usuario = self.usuarios[i]
                # Interrompe o loop
                break
        # Retorna o usuário encontrado (ou None se não for encontrado)
        return usuario

    def emprestar_livro(self, livro_escolhido, id_usuario):
        # Inicializa a variável 'disponivel' como False
        disponivel = False
        # Inicializa o índice do livro como -1
        idxLivro = -1
        # Itera sobre cada índice no dicionário de livros
        for idx in self.livros:
            # Obtém o livro correspondente ao índice atual
            livro_encontrado = self.livros[idx]
            # Verifica se o livro atual é o mesmo que o livro escolhido e se ainda há cópias disponíveis
            if (livro_encontrado == livro_escolhido and livro_escolhido.copias > 0):
                # Se o livro estiver disponível, define 'disponivel' como True e armazena o índice do livro
                disponivel = True
                idxLivro = idx
                # Interrompe o loop
                break


        if disponivel:
            usuario = self.obter_usuario_por_id(id_usuario)
            if usuario is None:
                print(f"Usuário com ID {id_usuario} não encontrado.")
                return
            
            # Subtrair uma cópia disponível
            self.livros[idxLivro].copias -= 1
            # Adicionar livro à lista de livros emprestados pelo usuário
            if id_usuario not in self.livros_emprestados:
                self.livros_emprestados[id_usuario] = [livro_escolhido.titulo]
            else:
                self.livros_emprestados[id_usuario].append(livro_escolhido.titulo)
            print(f"Livro '{livro_escolhido.titulo}' emprestado ao usuário {usuario.nome}.")
            
            # Salvar os livros emprestados em um arquivo CSV após emprestar um livro
            self.salvar_livros_emprestados_csv("Database/livros_emprestados.csv")
        else:
            print("Livro não disponível para empréstimo.")


    def listar_detalhes_livros_emprestados(self):
        livros_emprestados = self.get_lista_livros_emprestados()
        if livros_emprestados:
            print("=====================================================================================")
            for livro_emprestado in livros_emprestados:
                print(f"ID Usuário: {livro_emprestado['idUsuario']}, Nome do Usuário: {livro_emprestado['nome_usuario']}, Título: {livro_emprestado['titulo']}, Autor: {livro_emprestado['autor']}, Ano de Publicação: {livro_emprestado['ano_publicacao']}, Cópias: {livro_emprestado['copias']}")
            print("=====================================================================================")
        else:
            print("Nenhum livro emprestado no momento.")

    
    def devolver_livro(self, titulo, id_usuario):
        if id_usuario in self.livros_emprestados and titulo in self.livros_emprestados[id_usuario]:
            idxLivro = -1

            for i in self.livros:
                if(self.livros[i].titulo == titulo):
                  idxLivro = i 
                  break
            # Incrementar uma cópia disponível
            self.livros[idxLivro].copias += 1
            # Remover o livro da lista de livros emprestados pelo usuário
            self.livros_emprestados[id_usuario].remove(titulo)

            self.salvar_livros_emprestados_csv('Database/livros_emprestados.csv')
            print(f"Livro '{titulo}' devolvido com sucesso.")
        else:
            print(f"O usuário {id_usuario} não tem este livro emprestado.")
    
    def consultar_livros(self, busca=""):
        "\nConsulta livros com base em título, autor ou ano. Se 'busca' for vazia, retorna todos os livros.\n"
        resultados = []
        if busca:
            busca = busca.lower()
            for livro in self.livros.values():
                if (busca in livro.titulo.lower() or 
                    busca in livro.autor.lower() or 
                    busca in str(livro.ano_publicacao)):
                    resultados.append(livro)
        else:
            resultados = list(self.livros.values())
        
        if resultados:
            print("=====================================================================================")
            for livro in resultados:
                print(f"--> Título: {livro.titulo}, Autor: {livro.autor}, Ano: {livro.ano_publicacao}, Cópias: {livro.copias}\n")
            print("=====================================================================================")
        else:
            print("Nenhum livro encontrado.")

    def get_lista_livros(self):
        return list(self.livros.values())
    
    def obter_livro_por_titulo(self, titulo):
        for livro in self.livros.values():
            if livro.titulo == titulo:
                return livro
        return None

    def get_lista_livros_emprestados(self):
        lista_emprestimos = []
        
        for id_usuario, livros_emprestados in self.livros_emprestados.items():
            usuario = self.obter_usuario_por_id(id_usuario)
            if usuario:
                for titulo in livros_emprestados:
                    livro = self.obter_livro_por_titulo(titulo)
                    if livro:
                        lista_emprestimos.append({
                            'idUsuario': id_usuario,
                            'nome_usuario': usuario.nome,
                            'titulo': titulo,
                            'autor': livro.autor,
                            'ano_publicacao': livro.ano_publicacao,
                            'copias': livro.copias
                        })

        return lista_emprestimos
    
    def gerar_relatorios(self):
        print("Relatório de Livros:")
        self.listar_detalhes_livros()

        print("\nRelatório de Usuários:")
        self.listar_detalhes_usuarios()

        print("\nRelatório de Livros Emprestados:")
        self.listar_detalhes_livros_emprestados()
        
    
    def listar_detalhes_livros(self):
        if self.livros:
            print("=====================================================================================")
            for titulo, livro in self.livros.items():
                print(f"Título: {livro.titulo}")
                print(f"Autor: {livro.autor}")
                print(f"Ano de Publicação: {livro.ano_publicacao}")
                print(f"Número de Cópias: {livro.copias}")
            print("=====================================================================================")
        else:
            print("Não há livros cadastrados.")
            
    def listar_detalhes_usuarios(self):
        if self.usuarios:
            print("=====================================================================================")
            for id_usuario, usuario in self.usuarios.items():
                print(f"Informações do usuário (ID {id_usuario}):")
                print(f"Nome: {usuario.nome}")
                print(f"Contato: {usuario.contato}")
                print()
            print("=====================================================================================")
        else:
            print("Não há usuários cadastrados.")

    def salvar_livros_csv(self, nome_arquivo):
        # Abrir o arquivo CSV para escrita
        with open(nome_arquivo, 'w', newline='') as arquivo_csv:
            # Definir os nomes das colunas
            colunas = ['ID', 'Titulo', 'Autor', 'Ano', 'Copias']
            # Criar o escritor CSV
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=colunas)
            # Escrever o cabeçalho
            escritor_csv.writeheader()
            # Escrever os detalhes de cada livro
            for id_livro, livro in self.livros.items():
                escritor_csv.writerow({
                    'ID': id_livro,
                    'Titulo': livro.titulo,
                    'Autor': livro.autor,
                    'Ano': livro.ano_publicacao,
                    'Copias': livro.copias
                })

    def salvar_usuarios_csv(self, nome_arquivo):
        # Abrir o arquivo CSV para escrita
        with open(nome_arquivo, 'w', newline='') as arquivo_csv:
            # Definir os nomes das colunas
            colunas = ['ID', 'Nome', 'Contato']
            # Criar o escritor CSV
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=colunas)
            # Escrever o cabeçalho
            escritor_csv.writeheader()
            # Escrever os detalhes de cada usuário
            for usuario in self.usuarios.values():
                escritor_csv.writerow({
                    'ID': usuario.id_usuario,
                    'Nome': usuario.nome,
                    'Contato': usuario.contato
                })

    def carregar_livros_csv(self, nome_arquivo):
        # Tentar abrir o arquivo CSV para leitura
        try:
            with open(nome_arquivo, 'r', newline='') as arquivo_csv:
                # Criar um leitor CSV para ler o arquivo linha por linha
                leitor_csv = csv.DictReader(arquivo_csv)
                # Iterar sobre cada linha do arquivo CSV
                for linha in leitor_csv:
                    # Extrair informações de cada linha
                    id_livro = int(linha['ID'])
                    titulo = linha['Titulo']
                    autor = linha['Autor']
                    ano = int(linha['Ano'])
                    copias = int(linha['Copias'])
                    # Adicionar o livro ao dicionário de livros da biblioteca
                    self.livros[id_livro] = Livro(id_livro, titulo, autor, ano, copias)
        # Lidar com a exceção se o arquivo não for encontrado
        except FileNotFoundError:
            # Imprimir uma mensagem informando que o arquivo não foi encontrado
            print(f"Arquivo '{nome_arquivo}' não encontrado. Nenhum livro carregado.")

    def carregar_usuarios_csv(self, nome_arquivo):
        # Tentar abrir o arquivo CSV para leitura
        try:
            with open(nome_arquivo, 'r', newline='') as arquivo_csv:
                # Criar um leitor CSV para ler o arquivo linha por linha
                leitor_csv = csv.DictReader(arquivo_csv)
                # Iterar sobre cada linha do arquivo CSV
                for linha in leitor_csv:
                    # Extrair informações de cada linha
                    id_usuario = int(linha['ID'])
                    nome = linha['Nome']
                    contato = linha['Contato']
                    # Adicionar o usuário ao dicionário de usuários da biblioteca
                    self.usuarios[id_usuario] = Usuario(nome, id_usuario, contato)
        # Lidar com a exceção se o arquivo não for encontrado
        except FileNotFoundError:
            # Imprimir uma mensagem informando que o arquivo não foi encontrado
            print(f"Arquivo '{nome_arquivo}' não encontrado. Nenhum usuário carregado.")

    def salvar_livros_emprestados_csv(self, nome_arquivo):
        # Abrir o arquivo CSV para adição
        with open(nome_arquivo, 'w', newline='') as arquivo_csv:
            # Definir os nomes das colunas
            colunas = ['ID_Usuario', 'titulo']
            # Criar o escritor CSV
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=colunas)
            # Escrever o cabeçalho
            escritor_csv.writeheader()
            # Escrever os detalhes de cada usuário e os livros emprestados
            for id_usuario, livros_emprestados in self.livros_emprestados.items():
                for id_livro in livros_emprestados:
                    escritor_csv.writerow({
                        'ID_Usuario': id_usuario,
                        'titulo': id_livro
                    })



    def carregar_livros_emprestados_csv(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'r', newline='') as arquivo_csv:
                leitor_csv = csv.DictReader(arquivo_csv)
                for linha in leitor_csv:
                    id_usuario = int(linha['ID_Usuario'])
                    id_livro = linha['titulo']
                    # Adiciona o livro emprestado ao usuário correspondente
                    if id_usuario not in self.livros_emprestados:
                        self.livros_emprestados[id_usuario] = [id_livro]
                    else:
                        self.livros_emprestados[id_usuario].append(id_livro)
        except FileNotFoundError:
            print(f"Arquivo '{nome_arquivo}' não encontrado. Nenhum livro emprestado carregado.")
