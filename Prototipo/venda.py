from typing import List, Dict, Optional
from itemvenda import ItemVenda

class Venda:
    def __init__(self, id_venda: int, data_hora: str, forma_pagamento: str, 
                 valor_recebido: float, troco: float, id_funcionario: int):
        self.id = id_venda
        self.dataHora = data_hora
        self.formaPagamento = forma_pagamento
        self.valorRecebido = valor_recebido
        self.troco = troco
        self.idFuncionario = id_funcionario
        self.itens: List[ItemVenda] = []
    
    def calcular_valor_total(self):
        return sum(item.subtotal for item in self.itens)
    
    def calcular_troco(self) -> float:
        self.troco = self.valorRecebido - self.calcular_valor_total()
        return self.troco
    
    def to_dict(self):
        return {
            'id': self.id,
            'dataHora': self.dataHora,
            'formaPagamento': self.formaPagamento,
            'valorRecebido': self.valorRecebido,
            'troco': self.troco,
            'idFuncionario': self.idFuncionario,
            'itens': [item.to_dict() for item in self.itens]
        }
    
    @staticmethod
    def from_dict(dado: dict):
        venda = Venda(
            id_venda=dado['id'],
            data_hora=dado['dataHora'],
            forma_pagamento=dado['formaPagamento'],
            valor_recebido=dado['valorRecebido'],
            troco=dado['troco'],
            id_funcionario=dado['idFuncionario']
        )
        venda.itens = [ItemVenda.from_dict(item) for item in dado['itens']]
        return venda