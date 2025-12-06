import sqlite3
from datetime import datetime

class Estoque:
    def __init__(self, db_name='estoque.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_total REAL NOT NULL,
                data TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def adicionar_produto(self, nome, preco, quantidade): # O valor deve ser adicionado inteiro ex: 10, 20, 100
        self.cursor.execute('''
            INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)
        ''', (nome, preco, quantidade))
        self.conn.commit()
        print(f"Produto '{nome}' adicionado com sucesso!")

    def remover_produto(self, nome, quantidade):
        self.cursor.execute('''
            SELECT quantidade FROM produtos WHERE nome = ?
        ''', (nome,))
        resultado = self.cursor.fetchone()
        
        if resultado:
            quantidade_atual = resultado[0]
            if quantidade_atual >= quantidade:
                nova_quantidade = quantidade_atual - quantidade
                if nova_quantidade == 0:
                    self.cursor.execute('DELETE FROM produtos WHERE nome = ?', (nome,))
                    print(f"Produto '{nome}' removido do estoque, pois a quantidade chegou a zero.")
                else:
                    self.cursor.execute('''
                        UPDATE produtos SET quantidade = ? WHERE nome = ?
                    ''', (nova_quantidade, nome))
                    print(f"{quantidade} unidades de '{nome}' removidas do estoque.")
                self.conn.commit()
            else:
                print(f"Quantidade solicitada ({quantidade}) é maior que a quantidade disponível ({quantidade_atual}).")
        else:
            print(f"Produto '{nome}' não encontrado no estoque.")

    def listar_estoque(self):
        self.cursor.execute('SELECT nome, preco, quantidade FROM produtos')
        produtos = self.cursor.fetchall()
        if not produtos:
            print("O estoque está vazio.")
        else:
            print("Estoque:")
            for nome, preco, quantidade in produtos:
                print(f"{nome} - Preço: R${preco:.2f} - Quantidade: {quantidade}")

    def verificar_produto(self, nome):
        self.cursor.execute('SELECT nome, preco, quantidade FROM produtos WHERE nome = ?', (nome,))
        produto = self.cursor.fetchone()
        if produto:
            print(f"{produto[0]} - Preço: R${produto[1]:.2f} - Quantidade: {produto[2]}")
        else:
            print(f"Produto '{nome}' não encontrado no estoque.")

    def registrar_venda(self, produto, quantidade):
        self.cursor.execute('SELECT preco, quantidade FROM produtos WHERE nome = ?', (produto,))
        resultado = self.cursor.fetchone()
        
        if resultado:
            preco = resultado[0]
            quantidade_disponivel = resultado[1]
            if quantidade_disponivel >= quantidade:
                preco_total = preco * quantidade
                self.cursor.execute('INSERT INTO vendas (produto, quantidade, preco_total, data) VALUES (?, ?, ?, ?)',
                                    (produto, quantidade, preco_total, datetime.now().isoformat()))
                self.remover_produto(produto, quantidade)  # Atualiza o estoque
                self.conn.commit()
                print(f"Venda registrada: {quantidade} unidades de '{produto}' por R${preco_total:.2f}.")
            else:
                print(f"Quantidade solicitada ({quantidade}) é maior que a quantidade disponível ({quantidade_disponivel}).")
        else:
            print(f"Produto '{produto}' não encontrado no estoque.")

    def listar_vendas(self):
        self.cursor.execute('SELECT produto, quantidade, preco_total, data FROM vendas')
        vendas = self.cursor.fetchall()
        if not vendas:
            print("Nenhuma venda registrada.")
        else:
            print("Vendas Registradas:")
            for produto, quantidade, preco_total, data in vendas:
                print(f"Produto: {produto}, Quantidade: {quantidade}, Preço Total: R${preco_total:.2f}, Data: {data}")

    def fechar_conexao(self):
        self.conn.close()

def main():
    estoque = Estoque()
    lista_produtos = []  # Lista para armazenar produtos temporariamente

    while True:
        print("\nMenu:")
        print("1. Adicionar Produto ao Esto que")
        print("2. Remover Produto do Estoque")
        print("3. Listar Estoque")
        print("4. Verificar Produto")
        print("5. Registrar Venda")
        print("6. Listar Vendas")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do produto: ")
            preco = float(input("Preço do produto: "))
            quantidade = int(input("Quantidade do produto: "))
            estoque.adicionar_produto(nome, preco, quantidade)
        elif opcao == '2':
            nome = input("Nome do produto a remover: ")
            quantidade = int(input("Quantidade a remover: "))
            estoque.remover_produto(nome, quantidade)
        elif opcao == '3':
            estoque.listar_estoque()
        elif opcao == '4':
            nome = input("Nome do produto a verificar: ")
            estoque.verificar_produto(nome)
        elif opcao == '5':
            produto = input("Nome do produto a vender: ")
            quantidade = int(input("Quantidade a vender: "))
            estoque.registrar_venda(produto, quantidade)
        elif opcao == '6':
            estoque.listar_vendas()
        elif opcao == '7':
            estoque.fechar_conexao()
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()