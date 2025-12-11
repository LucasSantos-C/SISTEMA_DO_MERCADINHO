from produto import Produto

class ItemVenda:
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade
        self.subtotal = self.calcula_subtotal()

    def calcula_subtotal(self):
        return self.quantidade * self.produto.preco
    
    def to_dict(self):
        return {
            'quantidade': self.quantidade,
            'subtotal': self.subtotal,
            'produto': self.produto.to_dict()
        }
    
    @staticmethod
    def from_dict(data: dict):
        return ItemVenda(
            produto=Produto.from_dict(data['produto']),
            quantidade=data['quantidade']
        )