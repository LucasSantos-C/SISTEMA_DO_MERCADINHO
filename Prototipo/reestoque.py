from produto import Produto

class Reestoque:
    def __init__(self, id: int, data: str, quantidade: int, produto: Produto):
        self.id = id
        self.data = data
        self.quantidade = quantidade
        self.produto = produto 

    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'data': self.data,
            'quantidade': self.quantidade,
            'produto': self.produto.to_dict()
        }
    
    @staticmethod
    def from_dict(data: dict):
        return Reestoque(
            id=data['id'], 
            data=data['data'],
            quantidade=data['quantidade'],
            produto=Produto.from_dict(data['produto'])
        )