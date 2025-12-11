class Produto:
    def __init__(self, codigo: int, nome: str, preco: float, validade: str, estoque: int = 0):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.validade = validade
        self.estoque = estoque

    def adicionar_estoque(self, quantidade: int):
        if quantidade > 0:
            self.estoque += quantidade
            return True
        return False
    
    def remover_estoque(self, quantidade: int):
        if quantidade > 0 and self.estoque >= quantidade:
            self.estoque -= quantidade
            return True
        return False
    
    def tem_estoque_disponivel(self, quantidade: int):
        return self.estoque >= quantidade

    def to_dict(self):
        return {
            'codigo': self.codigo,
            'nome': self.nome,
            'preco': self.preco,
            'validade': self.validade,
            'estoque': self.estoque  # NOVO
        }
    
    @staticmethod
    def from_dict(data: dict):
        return Produto(
            codigo=data['codigo'],
            nome=data['nome'],
            preco=data['preco'],
            validade=data['validade'],
            estoque=data.get('estoque', 0)
        )