from funcionario import Funcionario
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from BaseDados import BaseDeDados

class Gerente(Funcionario):
    def __init__(self, nome: str, senha: str, login: int):
        super().__init__(nome, senha, login)
    
    def criar_funcionario(self, bd: 'BaseDeDados', nome: str, login: int, senha: str) -> bool:
        novo_func = Funcionario(nome, senha, login)
        return bd.adicionar_funcionario(novo_func)
    
    def editar_funcionario(self, bd: 'BaseDeDados', login: int, nome: str = None, senha: str = None) -> bool:
        return bd.editar_funcionario(login, nome, senha)
    
    def remover_funcionario(self, bd: 'BaseDeDados', login: int) -> bool:
        return bd.remover_funcionario(login)