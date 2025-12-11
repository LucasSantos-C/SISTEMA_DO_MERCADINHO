from datetime import datetime
import os

from BaseDados import BaseDeDados
from produto import Produto
from funcionario import Funcionario
from gerente import Gerente
from itemvenda import ItemVenda
from venda import Venda
from reestoque import Reestoque
from controlador import ControladorVenda


# ========== CLASSE DE CORES ==========
class Cores:
    """Classe para gerenciar cores no terminal - Tema: Vermelho, Azul Escuro e Branco"""
    
    # Cores do tema
    VERMELHO = '\033[91m'      # Vermelho brilhante
    AZUL_ESCURO = '\033[34m'   # Azul escuro
    BRANCO = '\033[97m'        # Branco brilhante
    
    # Estilos
    NEGRITO = '\033[1m'
    RESET = '\033[0m'          # Reseta todas as cores
    
    @staticmethod
    def vermelho(texto):
        return f"{Cores.VERMELHO}{texto}{Cores.RESET}"
    
    @staticmethod
    def azul_escuro(texto):
        return f"{Cores.AZUL_ESCURO}{texto}{Cores.RESET}"
    
    @staticmethod
    def branco(texto):
        return f"{Cores.BRANCO}{texto}{Cores.RESET}"
    
    @staticmethod
    def titulo(texto):
        return f"{Cores.AZUL_ESCURO}{Cores.NEGRITO}{texto}{Cores.RESET}"
    
    @staticmethod
    def erro(texto):
        return f"{Cores.VERMELHO}{Cores.NEGRITO}{texto}{Cores.RESET}"
    
    @staticmethod
    def sucesso(texto):
        return f"{Cores.AZUL_ESCURO}{texto}{Cores.RESET}"


class InterfaceUsuario:  
    def __init__(self):
        self.limpar_tela()
        print(Cores.azul_escuro(" Inicializando sistema..."))
        self.bd = BaseDeDados()
        self.funcionario_logado = None
        self._inicializar_dados_exemplo()
        print(Cores.azul_escuro(" Sistema pronto!\n"))
    
    def _inicializar_dados_exemplo(self):
        funcionarios = self.bd.listar_funcionarios()
        if not funcionarios:
            gerente = Gerente("Gerente Admin", "admin123", 100)
            self.bd.adicionar_funcionario(gerente)
      
            func = Funcionario("Funcionario Padrão", "func123", 101)
            self.bd.adicionar_funcionario(func)
            print(Cores.branco(" Gerente padrão criado (Login: 100, Senha: admin123)"))        
            print(Cores.branco(" Funcionário padrão criado (Login: 101, Senha: func123)"))        
        
        produtos = self.bd.listar_produtos()
        if not produtos:
            produtos_exemplo = [
                Produto(1538, "Arroz Camil 5kg", 25.90, "2025-12-31", 12),
                Produto(8716, "Feijão Saboroso 1kg", 8.50, "2025-12-15", 9),
                Produto(7541, "Óleo Soya 900ml", 7.20, "2026-01-15", 7),
            ]
            for p in produtos_exemplo:
                self.bd.adicionar_produto(p)
            print(Cores.branco(" Produtos de exemplo criados"))
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pausar(self):
        input(Cores.azul_escuro("\n[Pressione ENTER para continuar]"))

    def executar(self):
        print(Cores.azul_escuro("="*60))
        print(Cores.titulo(" BEM-VINDO AO SISTEMA SILVA & LIRA ".center(60)))
        print(Cores.azul_escuro("="*60))
        self.pausar()
        
        while True:
            try:
                if not self.funcionario_logado:
                    self.tela_login()
                else:
                    if isinstance(self.funcionario_logado, Gerente):
                        self.menu_gerente()
                    else:
                        self.menu_funcionario()
            except KeyboardInterrupt:
                print(Cores.vermelho("\nSistema interrompido pelo usuário!"))
                break
            except Exception as e:
                print(Cores.erro(f"\nERRO INESPERADO: {e}"))
                import traceback
                traceback.print_exc()
                self.pausar()
    
    def tela_login(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("="*60))
        print(Cores.titulo(" LOGIN ".center(60)))
        print(Cores.azul_escuro("="*60))
        
        try:
            login = int(input(Cores.branco("\n Login: ")))
            senha = input(Cores.branco(" Senha: "))
            
            func = self.bd.consultar_funcionario(login, senha)
            
            if func:
                self.funcionario_logado = func
                tipo = "GERENTE" if isinstance(func, Gerente) else "FUNCIONÁRIO"
                print(Cores.sucesso(f"\n Bem-vindo(a), {func.nome}! ({tipo})"))
                self.pausar()
            else:
                print(Cores.erro("\n Login ou senha incorretos!"))
                self.pausar()
         
        except ValueError:
            print(Cores.erro("\n Login deve ser um número inteiro!"))
            self.pausar()

    def mostrar_proximos_validade(self):
        proximos = self.bd.produtos_proximos_validade(7) 
        
        if proximos:
            print("\n" + Cores.vermelho("=" *60))
            print(Cores.vermelho(f" ALERTA: {len(proximos)} PRODUTO(S) PRÓXIMO(S) DO VENCIMENTO ".center(60)))
            print(Cores.vermelho("="*60))
            
            for produto, dias_restantes in proximos:
                if dias_restantes == 0:
                    print(Cores.vermelho(f" {produto.nome}: {produto.codigo} - VENCE HOJE!"))
                else:
                    print(Cores.vermelho(f" {produto.nome}: {produto.codigo} - Vence em {dias_restantes} dia(s)"))
            
            print(Cores.vermelho("="*60 + "\n"))

    def menu_funcionario(self):
        while True:
            self.limpar_tela()
            print("\n" + Cores.azul_escuro("="*60))
            print(Cores.titulo(f" MENU FUNCIONÁRIO - {self.funcionario_logado.nome} ".center(60)))
            print(Cores.azul_escuro("="*60))
            print(Cores.branco("\n1. Realizar Vendas"))
            print(Cores.branco("2. Exibir Produtos"))
            print(Cores.branco("3. Registrar Reestoque"))
            print(Cores.branco("4. Alterar Senha "))
            print(Cores.vermelho("0. Logout"))
            self.mostrar_proximos_validade()
            
            opcao = input(Cores.azul_escuro("\n> Escolha: "))

            if opcao == "1":
                self.realizar_vendas()
            elif opcao == "2":
                self.listar_produtos()
            elif opcao == "3":
                self.registrar_reestoque()
                self.pausar()
            elif opcao == "4":
                self.alterar_senha()
                self.pausar()
            elif opcao == "0":
                self.funcionario_logado = None
                print(Cores.sucesso("\n Logout realizado!"))
                self.pausar()
                break
            else:
                print(Cores.erro("\n Opção inválida!"))
                self.pausar()
    
    def menu_gerente(self):
        while True:
            self.limpar_tela()
            print("\n" + Cores.azul_escuro("="*60))
            print(Cores.titulo(f" MENU GERENTE - {self.funcionario_logado.nome} ".center(60)))
            print(Cores.azul_escuro("="*60))
            print(Cores.branco("\n1. Realizar Vendas"))
            print(Cores.branco("2. Gerenciar Produtos"))
            print(Cores.branco("3. Exibir Produtos"))
            print(Cores.branco("4. Gerenciar Funcionários"))
            print(Cores.branco("5. Registrar Reestoque"))
            print(Cores.branco("6. Gerar Relatórios"))
            print(Cores.branco("7. Alterar Senha"))
            print(Cores.vermelho("0. Logout"))

            self.mostrar_proximos_validade()
            opcao = input(Cores.azul_escuro("\n> Digite a opção desejada: "))
            
            if opcao == "1":
                self.realizar_vendas()
            elif opcao == "2":
                self.menu_produtos()
            elif opcao == "3":
                self.listar_produtos()
            elif opcao == "4":
                self.menu_gerenciar_funcionarios()
            elif opcao == "5":
                self.registrar_reestoque()
            elif opcao == "6":
                self.gerar_relatorio()
            elif opcao == "7":
                self.alterar_senha()
            elif opcao == "0":
                self.funcionario_logado = None
                print(Cores.sucesso("\n Logout realizado!"))
                self.pausar()
                break
            else:
                print(Cores.erro("\n Opção inválida!"))
                self.pausar()

    # --- FUNÇÕES DE PRODUTOS ---

    def menu_produtos(self):
        while True:
            self.limpar_tela()
            print("\n" + Cores.azul_escuro("-"*60))
            print(Cores.titulo(" GERENCIAR PRODUTOS ".center(60)))
            print(Cores.azul_escuro("-"*60))
            print(Cores.branco("\n1. Adicionar Produto"))
            print(Cores.branco("2. Editar Produto"))
            print(Cores.branco("3. Remover Produto"))
            print(Cores.vermelho("0. Voltar"))
            
            opcao = input(Cores.azul_escuro("\n> Escolha: "))
            
            if opcao == "1":
                self.adicionar_produto()
            elif opcao == "2":
                self.editar_produto()
            elif opcao == "3":
                self.remover_produto()
            elif opcao == "0":
                break
            else:
                print(Cores.erro("\n Opção inválida!"))
                self.pausar()
    
    def adicionar_produto(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("-"*60))
        print(Cores.titulo(" ADICIONAR NOVO PRODUTO ".center(60)))
        print(Cores.azul_escuro("-" * 60))
        try:
            codigo = int(input(Cores.branco("\nCódigo do Produto: ")))
            if self.bd.consultar_produto(codigo):
                print(Cores.erro("\n Já existe um produto com este código."))
                self.pausar()
                return
            
            nome = input(Cores.branco("Nome do Produto: "))
            preco = float(input(Cores.branco("Preço (R$): ")).replace(',', '.'))
            validade = input(Cores.branco("Validade (AAAA-MM-DD): "))
            estoque = int(input(Cores.branco("Quantidade em Estoque: "))) 
            
            if estoque < 0:
                print(Cores.erro("\n Estoque não pode ser negativo!"))
                self.pausar()
                return
            
            novo_produto = Produto(codigo, nome, preco, validade, estoque)  
            self.bd.adicionar_produto(novo_produto)
            print(Cores.sucesso(f"\n Produto '{nome}' adicionado com sucesso!"))
            print(Cores.branco(f"   Estoque inicial: {estoque} unidades"))
            
        except ValueError:
            print(Cores.erro("\n Erro de formato! Código, preço e estoque devem ser números."))
        except Exception as e:
            print(Cores.erro(f"\n Ocorreu um erro: {e}"))
        self.pausar()

    def editar_produto(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("-"*60))
        print(Cores.titulo(" EDITAR PRODUTO ".center(60)))
        print(Cores.azul_escuro("-" * 60))
        try:
            codigo = int(input(Cores.branco("\nCódigo do Produto para editar: ")))
            produto_existente = self.bd.consultar_produto(codigo)
            
            if not produto_existente:
                print(Cores.erro(f"\n Produto com código {codigo} não encontrado."))
                self.pausar()
                return
            
            print(Cores.branco(f"\nProduto atual: {produto_existente.nome}"))
            print(Cores.branco(f"Preço: R$ {produto_existente.preco:.2f}"))
            print(Cores.branco(f"Validade: {produto_existente.validade}"))
            print(Cores.branco(f"Estoque: {produto_existente.estoque} unidades"))
            
            novo_nome = input(Cores.azul_escuro("\nNovo nome (Deixe vazio para manter): ")) or None
            novo_preco_str = input(Cores.azul_escuro("Novo preço (R$) (Deixe vazio para manter): "))
            nova_validade = input(Cores.azul_escuro("Nova validade (AAAA-MM-DD) (Deixe vazio para manter): ")) or None
            novo_estoque_str = input(Cores.azul_escuro("Novo estoque (Deixe vazio para manter): "))
            
            novo_preco = None
            if novo_preco_str:
                novo_preco = float(novo_preco_str.replace(',', '.'))
            
            novo_estoque = None
            if novo_estoque_str:
                novo_estoque = int(novo_estoque_str)
                if novo_estoque < 0:
                    print(Cores.erro("\n Estoque não pode ser negativo!"))
                    self.pausar()
                    return
            
            if self.bd.editar_produto(codigo, novo_nome, novo_preco, nova_validade, novo_estoque):
                print(Cores.sucesso(f"\n Produto {codigo} atualizado com sucesso!"))
            else:
                print(Cores.branco("\n Nenhuma alteração realizada."))

        except ValueError:
            print(Cores.erro("\n Erro de formato! Código, preço ou estoque inválido."))
        except Exception as e:
            print(Cores.erro(f"\n Ocorreu um erro: {e}"))
        self.pausar()

    def remover_produto(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("-"*60))
        print(Cores.titulo(" REMOVER PRODUTO ".center(60)))
        print(Cores.azul_escuro("-" * 60))
        try:
            codigo = int(input(Cores.branco("\nCódigo do Produto para remover: ")))
            
            if self.bd.remover_produto(codigo):
                print(Cores.sucesso(f"\n Produto com código {codigo} removido com sucesso!"))
            else:
                print(Cores.erro(f"\n Produto com código {codigo} não encontrado."))
            
        except ValueError:
            print(Cores.erro("\n Erro de formato! Código deve ser um número inteiro."))
        except Exception as e:
            print(Cores.erro(f"\n Ocorreu um erro: {e}"))
        self.pausar()

    def listar_produtos(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("="*60))
        print(Cores.titulo(" PRODUTOS CADASTRADOS ".center(60)))
        print(Cores.azul_escuro("="*60))
        
        produtos = self.bd.listar_produtos()
        
        if not produtos:
            print(Cores.branco("\n Nenhum produto cadastrado."))
        else:
            print(Cores.branco(f"\nTotal: {len(produtos)} produtos\n"))
            print(Cores.azul_escuro(f"{'CÓDIGO':<8} {'NOME':<30} {'PREÇO':<10} {'ESTOQUE':<10} {'VALIDADE':<12}"))
            print(Cores.azul_escuro("-" * 80))
            for p in produtos:
                estoque_str = f"{p.estoque} un"
                if p.estoque == 0:
                    estoque_str = Cores.vermelho(" SEM ESTOQUE")
                elif p.estoque <= 5:
                    estoque_str = Cores.vermelho(f" {p.estoque} un")
                else:
                    estoque_str = f" {p.estoque} un"
                
                print(Cores.branco(f"{p.codigo:<8} {p.nome:<30} R$ {p.preco:>6.2f}") + f"  {estoque_str:<10} " + Cores.branco(f"{p.validade:<12}"))
            print(Cores.azul_escuro("-" * 80))
            
            sem_estoque = [p for p in produtos if p.estoque == 0]
            estoque_baixo = [p for p in produtos if 0 < p.estoque <= 5]
            
            if sem_estoque:
                print(Cores.vermelho(f"\n {len(sem_estoque)} produto(s) SEM ESTOQUE"))
            if estoque_baixo:
                print(Cores.vermelho(f" {len(estoque_baixo)} produto(s) com ESTOQUE BAIXO (<=5)"))
        
        self.pausar()

    def registrar_reestoque(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("-"*60))
        print(Cores.titulo(" REGISTRAR REESTOQUE ".center(60)))
        print(Cores.azul_escuro("-" * 60))
        
        try:
            codigo = int(input(Cores.branco("\nCódigo do Produto: ")))
            produto = self.bd.consultar_produto(codigo)
            
            if not produto:
                print(Cores.erro(f"\n Produto com código {codigo} não encontrado."))
                self.pausar()
                return
            
            print(Cores.branco(f"\nProduto: {produto.nome}"))
            print(Cores.branco(f"Estoque atual: {produto.estoque} unidades"))
            
            quantidade = int(input(Cores.branco("\nQuantidade a adicionar ao estoque: ")))
            
            if quantidade <= 0:
                print(Cores.erro("\n A quantidade deve ser maior que zero."))
                self.pausar()
                return
            
            estoque_anterior = produto.estoque
            
            if self.bd.atualizar_estoque_produto(codigo, quantidade, "adicionar"):
                reestoques = self.bd.listar_reestoques()
                proximo_id = len(reestoques) + 1
                
                produto_atualizado = self.bd.consultar_produto(codigo)
                
                novo_reestoque = Reestoque(
                    id=proximo_id,
                    data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    quantidade=quantidade,
                    produto=produto_atualizado  
                )
                
                self.bd.adicionar_reestoque(novo_reestoque)
                
                print(Cores.sucesso(f"\n Reestoque registrado com sucesso!"))
                print(Cores.branco(f"   Produto: {produto_atualizado.nome}"))
                print(Cores.branco(f"   Quantidade adicionada: {quantidade} unidades"))
                print(Cores.branco(f"   Estoque anterior: {estoque_anterior} unidades"))
                print(Cores.branco(f"   Estoque atual: {produto_atualizado.estoque} unidades")) 
            else:
                print(Cores.erro("\n Erro ao atualizar estoque."))
            
        except ValueError:
            print(Cores.erro("\n Erro de formato! Código e quantidade devem ser números inteiros."))
        except Exception as e:
            print(Cores.erro(f"\n Ocorreu um erro: {e}"))
        
        self.pausar()

    # --- FUNÇÃO DE VENDAS ---

    def realizar_vendas(self):
        ctrl = ControladorVenda(self.funcionario_logado.login, self.bd)
        ctrl.abrir_caixa()
        venda_atual = Venda(
            id_venda=-1, 
            data_hora="", 
            forma_pagamento="", 
            valor_recebido=0.0, 
            troco=0.0, 
            id_funcionario=self.funcionario_logado.login
        )

        while True:
            self.limpar_tela()
            print("\n" + Cores.azul_escuro("="*60))
            print(Cores.titulo(" REGISTRAR VENDA ".center(60)))
            print(Cores.azul_escuro("="*60))
            
            total = venda_atual.calcular_valor_total()
            print(Cores.branco(f"\nTOTAL PARCIAL: R$ {total:.2f}"))

            print(Cores.branco("\n1. Adicionar Item"))
            print(Cores.branco("2. Fechar Venda"))
            print(Cores.vermelho("0. Cancelar Venda"))
            
            opcao = input(Cores.azul_escuro("\n> Escolha: "))
            
            if opcao == "1":
                self.adicionar_item_venda(ctrl, venda_atual)
            
            elif opcao == "2":
                if not venda_atual.itens:
                    print(Cores.erro("\n Adicione itens antes de fechar a venda!"))
                    self.pausar()
                    continue
                
                self.finalizar_registro_venda(ctrl, venda_atual)
                break

            elif opcao == "0":
                print(Cores.vermelho("\nVenda cancelada."))
                self.pausar()
                break
            
            else:
                print(Cores.erro("\n Opção inválida!"))
                self.pausar()
                
        ctrl.fechar_caixa()

    def adicionar_item_venda(self, ctrl: ControladorVenda, venda_atual: Venda):
        self.limpar_tela()
        try:
            codigo = int(input(Cores.branco("\nCódigo do Produto: ")))
            produto = self.bd.consultar_produto(codigo)
            
            if not produto:
                print(Cores.erro(f"\n Produto com código {codigo} não encontrado."))
                return
            
            print(Cores.branco(f"\nProduto: {produto.nome}"))
            print(Cores.branco(f"Preço unitário: R$ {produto.preco:.2f}"))
            print(Cores.branco(f"Estoque disponível: {produto.estoque} unidades"))
            
            if produto.estoque == 0:
                print(Cores.erro("\n Produto SEM ESTOQUE! Não é possível adicionar à venda."))
                self.pausar()
                return

            quantidade = int(input(Cores.branco(f"\nQuantidade desejada: ")))
            
            if quantidade <= 0:
                print(Cores.erro("\n A quantidade deve ser maior que zero."))
                self.pausar()
                return
            
            if quantidade > produto.estoque:
                print(Cores.erro(f"\n Estoque insuficiente!"))
                print(Cores.branco(f"   Disponível: {produto.estoque} unidades"))
                print(Cores.branco(f"   Solicitado: {quantidade} unidades"))
                print(Cores.vermelho(f"   Faltam: {quantidade - produto.estoque} unidades"))
                self.pausar()
                return
            
            ctrl.adicionar_produto(venda_atual, produto, quantidade)
            
            item_adicionado = venda_atual.itens[-1]
            print(Cores.sucesso(f"\n Adicionado: {item_adicionado.quantidade} x {produto.nome}"))
            print(Cores.branco(f"   Subtotal: R$ {item_adicionado.subtotal:.2f}"))
            print(Cores.branco(f"   Estoque após venda: {produto.estoque - quantidade} unidades"))

        except ValueError:
            print(Cores.erro("\n Erro de formato! Código e quantidade devem ser números inteiros."))
        except Exception as e:
            print(Cores.erro(f"\n Ocorreu um erro ao adicionar item: {e}"))
        
        self.pausar()

    def finalizar_registro_venda(self, ctrl: ControladorVenda, venda_atual: Venda):
        self.limpar_tela()
        total_a_pagar = venda_atual.calcular_valor_total()
        print("\n" + Cores.azul_escuro("-"*60))
        print(Cores.titulo(f" TOTAL DA VENDA: R$ {total_a_pagar:.2f} ".center(60)))
        print(Cores.azul_escuro("-" * 60))
        
        try:
            print(Cores.branco("\nFormas de pagamento disponíveis:"))
            print(Cores.branco("1. Dinheiro"))
            print(Cores.branco("2. Cartão de Débito"))
            print(Cores.branco("3. Cartão de Crédito"))
            print(Cores.branco("4. PIX"))
            print(Cores.branco("5. Vale/Ticket"))
            
            forma_pagamento = input(Cores.azul_escuro("\nEscolha a forma de pagamento: ")).strip().lower()
            
            if forma_pagamento in ["1", "dinheiro"]:
                while True:
                    valor_recebido = float(input(Cores.branco("Valor Recebido (R$): ")).replace(',', '.'))
                    
                    if valor_recebido < total_a_pagar:
                        print(Cores.erro(f"\nValor insuficiente! Falta: R$ {total_a_pagar - valor_recebido:.2f}"))
                        continuar = input(Cores.azul_escuro("Tentar novamente? (s/n): ")).lower()
                        if continuar != 's':
                            print(Cores.vermelho("\n Venda cancelada."))
                            self.pausar()
                            return
                    else:
                        break
                
                venda_finalizada = ctrl.finalizar_venda(valor_recebido, "Dinheiro")
                venda_finalizada.itens = venda_atual.itens
                venda_finalizada.calcular_troco()
                
                print(Cores.sucesso(f"\n Troco: R$ {venda_finalizada.troco:.2f}"))
            
            else:
                formas = {
                    "2": "Cartão de Débito",
                    "cartão de débito": "Cartão de Débito",
                    "cartao de debito": "Cartão de Débito",
                    "debito": "Cartão de Débito",
                    "3": "Cartão de Crédito",
                    "cartão de crédito": "Cartão de Crédito",
                    "cartao de credito": "Cartão de Crédito",
                    "credito": "Cartão de Crédito",
                    "4": "PIX",
                    "pix": "PIX",
                    "PIX": "PIX",
                    "5": "Vale/Ticket",
                    "vale": "Vale/Ticket",
                    "VALE": "Vale/Ticket",
                    "TICKET": "Vale/Ticket",
                    "ticket": "Vale/Ticket"
                }
                
                forma_nome = formas.get(forma_pagamento, "Outros")
                
                venda_finalizada = ctrl.finalizar_venda(total_a_pagar, forma_nome)
                venda_finalizada.itens = venda_atual.itens
                venda_finalizada.troco = 0.0
                
                print(Cores.sucesso(f"\n Pagamento via {forma_nome} confirmado."))
            
            print(Cores.azul_escuro("\n Atualizando estoque..."))
            estoque_atualizado = True
            
            for item in venda_finalizada.itens:
                sucesso = self.bd.atualizar_estoque_produto(
                    item.produto.codigo,
                    item.quantidade,
                    "remover"
                )
                
                if not sucesso:
                    print(Cores.erro(f" Erro ao atualizar estoque do produto {item.produto.nome}"))
                    estoque_atualizado = False
                    break
            
            if not estoque_atualizado:
                print(Cores.erro("\n Erro ao atualizar estoque. Venda NÃO foi registrada."))
                self.pausar()
                return
            
            print(Cores.sucesso(" Estoque atualizado com sucesso!"))
            
            if self.bd.adicionar_venda(venda_finalizada):
                print(Cores.sucesso(f"\n Venda #{venda_finalizada.id} registrada com sucesso!"))
                print(Cores.branco(f"   Total: R$ {total_a_pagar:.2f}"))
                print(Cores.branco(f"   Forma: {venda_finalizada.formaPagamento}"))
                print(Cores.branco(f"   Data: {venda_finalizada.dataHora}"))
            else:
                print(Cores.erro("  \n Erro ao salvar a venda no banco de dados."))

        except ValueError:
            print(Cores.erro("\nErro de formato! Valor deve ser um número."))
        except Exception as e:
            print(Cores.erro(f"\nOcorreu um erro ao finalizar a venda: {e}"))
        
        self.pausar()

    def gerar_relatorio(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("-"*60))
        print(Cores.titulo(" GERAR RELATÓRIO DE VENDAS ".center(60)))
        print(Cores.azul_escuro("-" * 60))
        
        try:
            print(Cores.branco("\nFormato de data: DD/MM/YYYY"))
            print(Cores.branco("Exemplo: 01/12/2024\n"))
            
            data_inicio = input(Cores.branco("Data de Início: "))
            data_fim = input(Cores.branco("Data Final: "))
            
            try:
                datetime.strptime(data_inicio, "%d/%m/%Y")
                datetime.strptime(data_fim, "%d/%m/%Y")
            except ValueError:
                print(Cores.erro("\n Formato de data inválido! Use DD/MM/YYYY"))
                self.pausar()
                return
            
            print(Cores.azul_escuro("\n Gerando relatório..."))
            
            di = data_inicio.replace("/", "-")
            df = data_fim.replace("/", "-")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"relatorio_{di}_ate_{df}_{timestamp}.txt"
            
            import os
            id_relatorio = len([f for f in os.listdir('.') if f.startswith('relatorio_')]) + 1
            
            from relatorio import Relatorio
            relatorio = Relatorio(id_relatorio, data_inicio, data_fim, nome_arquivo)
            relatorio.set_base_dados(self.bd)
            
            conteudo = relatorio.gerar()
            
            self.limpar_tela()
            print(conteudo)
            
            print("\n" + Cores.azul_escuro("-"*60))
            exportar = input(Cores.azul_escuro("\nDeseja exportar para arquivo TXT? (s/n): ")).lower()
            
            if exportar == 's':
                if relatorio.exportar():
                    print(Cores.sucesso(f"\n Relatório exportado com sucesso!"))
                    print(Cores.branco(f"   Arquivo: {nome_arquivo}"))
                else:
                    print(Cores.erro(f"\n Erro ao exportar relatório!"))
            
        except Exception as e:
            print(Cores.erro(f"\n Ocorreu um erro: {e}"))
        
        self.pausar()

    #------ Funções de gerenciar Funcionarios-------

    def menu_gerenciar_funcionarios(self):
        while True:
            self.limpar_tela()
            print("\n" + Cores.azul_escuro("-"*60))
            print(Cores.titulo(" GERENCIAR FUNCIONÁRIOS ".center(60)))
            print(Cores.azul_escuro("-"*60))
            print(Cores.branco("\n1. Adicionar Funcionário"))
            print(Cores.branco("2. Editar Funcionário"))
            print(Cores.branco("3. Remover Funcionário"))
            print(Cores.branco("4. Listar Funcionários"))
            print(Cores.vermelho("0. Voltar"))
            
            opcao = input(Cores.azul_escuro("\n> Escolha: "))
            
            if opcao == "1":
                self.adicionar_funcionario()
            elif opcao == "2":
                self.editar_funcionario()
            elif opcao == "3":
                self.remover_funcionario()
            elif opcao == "4":
                self.listar_funcionarios()
            elif opcao == "0":
                break
            else:
                print(Cores.erro("\n Opção inválida!"))
                self.pausar()

    def adicionar_funcionario(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("-"*60))
        print(Cores.titulo(" ADICIONAR NOVO FUNCIONÁRIO ".center(60)))
        print(Cores.azul_escuro("-" * 60))
        try:
            nome = input(Cores.branco("\nNome do Funcionário: "))
            senha = input(Cores.branco("Senha: "))
            login = int(input(Cores.branco("Login (Número Inteiro): ")))
            
            if self.bd.consultar_funcionario_por_login(login):
                print(Cores.erro("\n Já existe um funcionário com este login."))
                self.pausar()
                return
            
            if self.funcionario_logado.criar_funcionario(self.bd, nome, login, senha):
                print(Cores.sucesso(f"\n Funcionário '{nome}' adicionado com sucesso!"))
            else:
                print(Cores.erro("\n Erro ao adicionar funcionário."))
            
        except ValueError:
            print(Cores.erro("\n Erro de formato! Login deve ser um número inteiro."))
        except Exception as e:
            print(Cores.erro(f"\n Ocorreu um erro: {e}"))
        self.pausar()

    def editar_funcionario(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("-"*60))
        print(Cores.titulo(" EDITAR FUNCIONÁRIO ".center(60)))
        print(Cores.azul_escuro("-" * 60))
        try:
            login = int(input(Cores.branco("\nLogin do Funcionário para editar: ")))
            funcionario_existente = self.bd.consultar_funcionario_por_login(login)
            
            if not funcionario_existente:
                print(Cores.erro(f"\n Funcionário com login {login} não encontrado."))
                self.pausar()
                return
            
            print(Cores.branco(f"\nFuncionário atual: {funcionario_existente.nome}"))
            
            novo_nome = input(Cores.azul_escuro("Novo nome (Deixe vazio para manter): ")) or None
            nova_senha = input(Cores.azul_escuro("Nova senha (Deixe vazio para manter): ")) or None

            if self.funcionario_logado.editar_funcionario(self.bd, login, novo_nome, nova_senha):
                print(Cores.sucesso(f"\nFuncionário {login} atualizado com sucesso!"))
            else:
                print(Cores.branco("\nNenhuma alteração realizada."))

        except ValueError:
            print(Cores.erro("\nErro de formato! Login inválido."))
        except Exception as e:
            print(Cores.erro(f"\nOcorreu um erro: {e}"))
        self.pausar()

    def remover_funcionario(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("-"*60))
        print(Cores.titulo(" REMOVER FUNCIONÁRIO ".center(60)))
        print(Cores.azul_escuro("-" * 60))
        try:
            login = int(input(Cores.branco("\nLogin do Funcionário para remover: ")))
            
            if self.funcionario_logado.remover_funcionario(self.bd, login):
                print(Cores.sucesso(f"\n Funcionário com login {login} removido com sucesso!"))
            else:
                print(Cores.erro(f"\n Funcionário com login {login} não encontrado."))
            
        except ValueError:
            print(Cores.erro("\n Erro de formato! Login deve ser um número inteiro."))
        except Exception as e:
            print(Cores.erro(f"\n Ocorreu um erro: {e}"))
        self.pausar()

    def listar_funcionarios(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("="*60))
        print(Cores.titulo(" FUNCIONÁRIOS CADASTRADOS ".center(60)))
        print(Cores.azul_escuro("="*60))
        
        funcionarios = self.bd.listar_funcionarios()
        
        if not funcionarios:
            print(Cores.branco("\n Nenhum funcionário cadastrado."))
        else:
            print(Cores.branco(f"\nTotal: {len(funcionarios)} funcionários\n"))
            print(Cores.azul_escuro(f"{'LOGIN':<8} {'NOME':<40} {'TIPO':<15}"))
            print(Cores.azul_escuro("-" * 70))
            for f in funcionarios:
                tipo = "Gerente" if isinstance(f, Gerente) else "Funcionário"
                print(Cores.branco(f"{f.login:<8} {f.nome:<40} {tipo:<15}"))
            print(Cores.azul_escuro("-" * 70))
        
        self.pausar()

    def alterar_senha(self):
        self.limpar_tela()
        print("\n" + Cores.azul_escuro("-"*60))
        print(Cores.titulo(" ALTERAR SENHA ".center(60)))
        print(Cores.azul_escuro("-" * 60))
        
        try:
            senha_atual = input(Cores.branco("\nSenha Atual: "))
            
            if senha_atual != self.funcionario_logado.senha:
                print(Cores.erro("\n Senha atual incorreta!"))
                self.pausar()
                return
            
            nova_senha = input(Cores.branco("Nova Senha: "))
            confirma_senha = input(Cores.branco("Confirme a Nova Senha: "))
            
            if nova_senha != confirma_senha:
                print(Cores.erro("\n As senhas não coincidem!"))
                self.pausar()
                return
            
            self.funcionario_logado.mudar_senha(nova_senha)
            self.bd.editar_funcionario(self.funcionario_logado.login, senha=nova_senha)
            
            print(Cores.sucesso("\n Senha alterada com sucesso!"))
            
        except Exception as e:
            print(Cores.erro(f"\n Ocorreu um erro: {e}"))
        
        self.pausar()


if __name__ == "__main__":
    try:
        sistema = InterfaceUsuario()
        sistema.executar()
        
    except KeyboardInterrupt:
        print(Cores.vermelho("\nSistema interrompido!"))
        print(Cores.branco("Até logo!"))
        
    except Exception as e:
        print(Cores.erro(f"\n\nERRO CRÍTICO: {e}"))
        import traceback
        traceback.print_exc()
        input(Cores.azul_escuro("\n[Pressione ENTER para sair]"))