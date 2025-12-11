class Funcionario:
    def __init__(self, nome: str, senha: str, login: int):
        self.nome = nome
        self.senha = senha
        self.login = login

    def mudar_senha(self, novasenha: str):
        self.senha = novasenha

    def to_dict(self) -> dict:
        return {
            'nome': self.nome,
            'senha': self.senha,
            'login': self.login,
            'tipo': self.__class__.__name__
        }