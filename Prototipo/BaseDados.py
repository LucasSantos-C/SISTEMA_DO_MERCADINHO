import json
import os
from typing import List, Optional
from datetime import datetime, timedelta
from produto import Produto
from funcionario import Funcionario
from gerente import Gerente
from reestoque import Reestoque
from venda import Venda

class BaseDeDados:
    def __init__(self, pasta_dados: str = "dados"):
        self.pasta_dados = pasta_dados
        self.arquivo_produtos = os.path.join(pasta_dados, "produtos.json")
        self.arquivo_funcionarios = os.path.join(pasta_dados, "funcionarios.json")
        self.arquivo_vendas = os.path.join(pasta_dados, "vendas.json")
        self.arquivo_reestoques = os.path.join(pasta_dados, "reestoques.json")
        
        # Criar pasta se não existir
        if not os.path.exists(pasta_dados):
            os.makedirs(pasta_dados)
        
        # Inicializar arquivos
        self._inicializar_arquivos()
    
    def _inicializar_arquivos(self):
        """Cria os arquivos JSON vazios se não existirem"""
        arquivos = [
            self.arquivo_produtos,
            self.arquivo_funcionarios,
            self.arquivo_vendas,
            self.arquivo_reestoques
        ]
        
        for arquivo in arquivos:
            if not os.path.exists(arquivo):
                with open(arquivo, 'w', encoding='utf-8') as f:
                    json.dump([], f)
    
    # ---- PRODUTOS ----
    def listar_produtos(self):
        with open(self.arquivo_produtos, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return [Produto.from_dict(p) for p in dados]
    
    def adicionar_produto(self, produto: Produto):
        produtos = self.listar_produtos()
        
        # Verificar se código já existe
        if any(p.codigo == produto.codigo for p in produtos):
            return False
        
        produtos.append(produto)
        self._salvar_produtos(produtos)
        return True
    
    def remover_produto(self, codigo: int):
        produtos = self.listar_produtos()
        produtos_filtrados = [p for p in produtos if p.codigo != codigo]
        
        if len(produtos_filtrados) < len(produtos):
            self._salvar_produtos(produtos_filtrados)
            return True
        return False
    
    def editar_produto(self, codigo: int, nome: str = None, preco: float = None, validade: str = None, estoque: int = None):           
        produtos = self.listar_produtos()
        
        for produto in produtos:
            if produto.codigo == codigo:
                # Atualizar apenas os campos fornecidos
                if nome is not None:
                    produto.nome = nome
                if preco is not None:
                    produto.preco = preco
                if validade is not None:
                    produto.validade = validade
                if estoque is not None:
                    produto.estoque = estoque
                self._salvar_produtos(produtos)
                return True
        
        return False
    
    def consultar_produto(self, codigo: int):
        produtos = self.listar_produtos()
        for produto in produtos:
            if produto.codigo == codigo:
                return produto
        return None
    
    def _salvar_produtos(self, produtos: List[Produto]):
        with open(self.arquivo_produtos, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in produtos], f, indent=2, ensure_ascii=False)
    
    def produtos_proximos_validade(self, dias: int = 30):
        produtos = self.listar_produtos()
        produtos_proximos = []
        hoje = datetime.now()
        
        for produto in produtos:
            try:
                validade = datetime.strptime(produto.validade, "%Y-%m-%d")
                dias_restantes = (validade - hoje).days
                
                if 0 <= dias_restantes <= dias:
                    produtos_proximos.append((produto, dias_restantes))
            except:
                try:
                    validade = datetime.strptime(produto.validade, "%d/%m/%Y")
                    dias_restantes = (validade - hoje).days
                    
                    if 0 <= dias_restantes <= dias:
                        produtos_proximos.append((produto, dias_restantes))
                except:
                    pass
        
        produtos_proximos.sort(key=lambda x: x[1])
        return produtos_proximos
    
    def atualizar_estoque_produto(self, codigo: int, quantidade: int, operacao: str = "adicionar"):

        produto = self.consultar_produto(codigo)
        
        if not produto:
            return False
        
        if operacao == "adicionar":
            produto.adicionar_estoque(quantidade)
        elif operacao == "remover":
            if not produto.remover_estoque(quantidade):
                return False 
        else:
            return False
        
        produtos = self.listar_produtos()
        for i, p in enumerate(produtos):
            if p.codigo == codigo:
                produtos[i] = produto
                break
        
        self._salvar_produtos(produtos)
        return True
    
    def verificar_estoque_disponivel(self, codigo: int, quantidade: int):
        produto = self.consultar_produto(codigo)
        if not produto:
            return False
        return produto.tem_estoque_disponivel(quantidade)
    
    def listar_produtos_sem_estoque(self):
        produtos = self.listar_produtos()
        return [p for p in produtos if p.estoque == 0]
    
    def listar_produtos_estoque_baixo(self, limite: int = 10):
        produtos = self.listar_produtos()
        return [p for p in produtos if 0 < p.estoque <= limite]
    
    # ---- FUNCIONÁRIOS ----
    def listar_funcionarios(self):
        with open(self.arquivo_funcionarios, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            funcionarios = []
            for f_dict in dados:
                if f_dict['tipo'] == 'Gerente':
                    func = Gerente(f_dict['nome'], f_dict['senha'], f_dict['login'])
                else:
                    func = Funcionario(f_dict['nome'], f_dict['senha'], f_dict['login'])
                funcionarios.append(func)
            return funcionarios
    
    def adicionar_funcionario(self, funcionario: Funcionario):
        funcionarios = self.listar_funcionarios()
        
        # Verificar se login já existe
        if any(f.login == funcionario.login for f in funcionarios):
            return False
        
        funcionarios.append(funcionario)
        self._salvar_funcionarios(funcionarios)
        return True
    
    def consultar_funcionario(self, login: int, senha: str):
        funcionarios = self.listar_funcionarios()
        for func in funcionarios:
            if func.login == login and func.senha == senha:
                return func
        return None
    
    def consultar_funcionario_por_login(self, login: int):
        funcionarios = self.listar_funcionarios()
        for func in funcionarios:
            if func.login == login:
                return func
        return None
    
    def editar_funcionario(self, login: int, nome: str = None, senha: str = None):
        funcionarios = self.listar_funcionarios()
        
        for func in funcionarios:
            if func.login == login:
                if nome is not None:
                    func.nome = nome
                if senha is not None:
                    func.senha = senha
                
                self._salvar_funcionarios(funcionarios)
                return True
        
        return False
    
    def remover_funcionario(self, login: int):
        funcionarios = self.listar_funcionarios()
        funcionarios_filtrados = [f for f in funcionarios if f.login != login]
        
        if len(funcionarios_filtrados) < len(funcionarios):
            self._salvar_funcionarios(funcionarios_filtrados)
            return True
        return False
    
    def _salvar_funcionarios(self, funcionarios: List[Funcionario]):
        with open(self.arquivo_funcionarios, 'w', encoding='utf-8') as f:
            json.dump([f.to_dict() for f in funcionarios], f, indent=2, ensure_ascii=False)
    
    # ---- VENDAS ----
    def listar_vendas(self):
        with open(self.arquivo_vendas, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return [Venda.from_dict(v) for v in dados]
    
    def adicionar_venda(self, venda: Venda):
        vendas = self.listar_vendas()
        vendas.append(venda)
        self._salvar_vendas(vendas)
        return True
    
    def _salvar_vendas(self, vendas: List[Venda]):
        with open(self.arquivo_vendas, 'w', encoding='utf-8') as f:
            json.dump([v.to_dict() for v in vendas], f, indent=2, ensure_ascii=False)
    
    # ---- REESTOQUES ----
    def listar_reestoques(self):
        with open(self.arquivo_reestoques, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return [Reestoque.from_dict(r) for r in dados]
    
    def adicionar_reestoque(self, reestoque: Reestoque):
        reestoques = self.listar_reestoques()
        reestoques.append(reestoque)
        self._salvar_reestoques(reestoques)
        return True
    
    def _salvar_reestoques(self, reestoques: List[Reestoque]):
        with open(self.arquivo_reestoques, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in reestoques], f, indent=2, ensure_ascii=False)