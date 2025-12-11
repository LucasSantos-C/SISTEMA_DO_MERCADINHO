from typing import List
from datetime import datetime
from BaseDados import BaseDeDados
from produto import Produto
from itemvenda import ItemVenda
from venda import Venda

class ControladorVenda:
    def __init__(self, id_funcionario: int, bd: BaseDeDados):
        self.idFuncionario = id_funcionario
        self.bd = bd
    
    def abrir_caixa(self):
        print(f"\n{'='*50}")
        print("CAIXA ABERTO")
        print(f"{'='*50}")
        return True

    def fechar_caixa(self):
        print(f"\n{'='*50}")
        print("CAIXA FECHADO")
        print(f"{'='*50}")
        return True
    
    def adicionar_produto(self, venda: Venda, produto: Produto, quantidade: int):
        item = ItemVenda(produto, quantidade) 
        venda.itens.append(item)
    
    def finalizar_venda(self, valor_recebido: float, forma_pagamento: str):

        vendas = self.bd.listar_vendas()
        proximo_id = len(vendas) + 1
        
        venda = Venda(
            id_venda=proximo_id,
            data_hora=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            forma_pagamento=forma_pagamento,
            valor_recebido=valor_recebido,
            troco=0,
            id_funcionario=self.idFuncionario
        ) 
        return venda