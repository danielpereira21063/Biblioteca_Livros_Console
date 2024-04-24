import csv
from Classes.Livro import Livro
from Classes.Usuario import Usuario

class Biblioteca:
    def __init__(self):
        self.livros = {}
        self.livros_emprestados = {}
        self.usuarios = {}
    
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
        ultimo_id_usuario = self.carregar_ultimo_id_usuario_cadastrado()
        id_usuario = ultimo_id_usuario + 1

        self.usuarios[id_usuario] = Usuario(nome, id_usuario, contato)
        print(f"Usuário '{nome}' cadastrado com sucesso. ID: {id_usuario}")
        self.salvar_usuarios_csv("Database/usuarios.csv")
    
    def consultar_usuarios(self, id_usuario=None):
        if id_usuario is None or id_usuario == "":
            if self.usuarios:
                print("Lista de todos os usuários cadastrados na biblioteca:")
                for id_usuario, usuario in self.usuarios.items():
                    print(f"Informações do usuário (ID {id_usuario}):")
                    print(f"Nome: {usuario.nome}")
                    print(f"Contato: {usuario.contato}")
                    print()
            else:
                print("Não há usuários cadastrados na biblioteca.")
        else:
            if id_usuario in self.usuarios:
                usuario = self.usuarios[id_usuario]
                print(f"Informações do usuário (ID {id_usuario}):")
                print(f"Nome: {usuario.nome}")
                print(f"Contato: {usuario.contato}")
            else:
                print(f"Usuário com ID {id_usuario} não encontrado.")

    def carregar_ultimo_id_usuario_cadastrado(self):
            if self.usuarios:
                lista_ids_usuarios = list(self.usuarios.keys())
                return max(lista_ids_usuarios)
            else:
                return 0 
    
    def carregar_ultimo_id_livro_cadastrado(self):
            if self.livros:
                lista_ids_livros = list(self.livros.keys())
                return max(lista_ids_livros)
            else:
                return 0 
            
    def obter_usuario_por_id(self, id_usuario):
        if id_usuario in self.usuarios:
            return self.usuarios[id_usuario]
        else:
            return None
            
    def emprestar_livro(self, titulo, id_usuario):
        if titulo in self.livros and self.livros[titulo].copias > 0:
            usuario = self.obter_usuario_por_id(id_usuario)
            if usuario is None:
                print(f"Úsuario com id {id_usuario} não encontrado")
                return
            
            # Subtrair uma cópia disponível
            self.livros[titulo].copias -= 1
            # Adicionar livro à lista de livros emprestados pelo usuário
            if id_usuario not in self.livros_emprestados:
                self.livros_emprestados[id_usuario] = [titulo]
            else:
                self.livros_emprestados[id_usuario].append(titulo)
            print(f"Livro '{titulo}' emprestado ao usuário {usuario.nome}.")
        else:
            print("Livro não disponível para empréstimo.")

    
    def devolver_livro(self, titulo, id_usuario):
        if id_usuario in self.livros_emprestados and titulo in self.livros_emprestados[id_usuario]:
            # Incrementar uma cópia disponível
            self.livros[titulo].copias += 1
            # Remover o livro da lista de livros emprestados pelo usuário
            self.livros_emprestados[id_usuario].remove(titulo)
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
            for livro in resultados:
                print(f"--> Título: {livro.titulo}, Autor: {livro.autor}, Ano: {livro.ano_publicacao}, Cópias: {livro.copias}\n")
        else:
            print("Nenhum livro encontrado.")

    def get_lista_livros(self):
        return list(self.livros.values())
    
    def get_lista_livros_emprestados(self):
        return list(self.livros_emprestados.values())
    
    def gerar_relatorios(self):
        print("Relatório de Livros:")
        self.listar_detalhes_livros()
        print("\nRelatório de Usuários:")
        self.listar_detalhes_usuarios()
    
    def listar_detalhes_livros(self):
        if self.livros:
            for titulo, livro in self.livros.items():
                print(f"Título: {livro.titulo}")
                print(f"Autor: {livro.autor}")
                print(f"Ano de Publicação: {livro.ano_publicacao}")
                print(f"Número de Cópias: {livro.copias}")
                print()
        else:
            print("Não há livros cadastrados.")
            
    def listar_detalhes_usuarios(self):
        if self.usuarios:
            for id_usuario, usuario in self.usuarios.items():
                print(f"Informações do usuário (ID {id_usuario}):")
                print(f"Nome: {usuario.nome}")
                print(f"Contato: {usuario.contato}")
                print()
        else:
            print("Não há usuários cadastrados.")

    def salvar_livros_csv(self, nome_arquivo):
        # Abrir o arquivo CSV para escrita
        with open(nome_arquivo, 'w', newline='') as arquivo_csv:
            # Definir os nomes das colunas
            colunas = ['ID', 'Título', 'Autor', 'Ano', 'Cópias']
            # Criar o escritor CSV
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=colunas)
            # Escrever o cabeçalho
            escritor_csv.writeheader()
            # Escrever os detalhes de cada livro
            for id_livro, livro in self.livros.items():
                escritor_csv.writerow({
                    'ID': id_livro,
                    'Título': livro.titulo,
                    'Autor': livro.autor,
                    'Ano': livro.ano_publicacao,
                    'Cópias': livro.copias
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
