from datetime import datetime
from typing import List

class Relatorio:
    def __init__(self, id_relatorio: int, periodo_inicial: str, 
                 periodo_final: str, caminho_arquivo: str):
        self.id = id_relatorio
        self.periodoInicial = periodo_inicial
        self.periodoFinal = periodo_final
        self.caminhoArquivo = caminho_arquivo
        self.bd = None 
        self.vendas_periodo = []
    
    def set_base_dados(self, bd):
        self.bd = bd
    
    def gerar(self) -> str:
        if not self.bd:
            return "Erro: Base de dados não configurada"       
        try:
            dt_inicio = datetime.strptime(self.periodoInicial, "%d/%m/%Y")
            dt_fim = datetime.strptime(self.periodoFinal, "%d/%m/%Y")
            dt_fim = dt_fim.replace(hour=23, minute=59, second=59)
            
            vendas = self.bd.listar_vendas()
            
            self.vendas_periodo = []
            for venda in vendas:
                try:
                    if " " in venda.dataHora:
                        dt_venda = datetime.strptime(venda.dataHora, "%d/%m/%Y %H:%M:%S")
                    else:
                        dt_venda = datetime.strptime(venda.dataHora, "%d/%m/%Y")
                    
                    if dt_inicio <= dt_venda <= dt_fim:
                        self.vendas_periodo.append(venda)
                except:
                    continue
            
            return self._montar_conteudo()
            
        except Exception as e:
            return f"Erro ao gerar relatório: {e}"
    
    def _montar_conteudo(self) -> str:
        linhas = []
        linhas.append("=" * 70)
        linhas.append(" RELATÓRIO DE VENDAS ".center(70))
        linhas.append("=" * 70)
        linhas.append("")
        linhas.append(f"Relatório ID: {self.id}")
        linhas.append(f"Período: {self.periodoInicial} até {self.periodoFinal}")
        linhas.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
        linhas.append("")
        linhas.append("=" * 70)
        linhas.append("")
        
        if not self.vendas_periodo:
            linhas.append("Nenhuma venda registrada neste período.")
            linhas.append("")
            linhas.append("=" * 70)
            return "\n".join(linhas)
        
        valor_total = sum(v.calcular_valor_total() for v in self.vendas_periodo)
        
        linhas.append(f"Total de Vendas: {len(self.vendas_periodo)}")
        linhas.append(f"Valor Total: R$ {valor_total:,.2f}")
        linhas.append("")
        linhas.append("-" * 70)
        linhas.append("")
        
        linhas.append(f"{'ID':<6} {'DATA/HORA':<18} {'FUNCIONÁRIO':<12} {'VALOR':<12} {'PAGAMENTO':<15}")
        linhas.append("-" * 70)
        
        for venda in self.vendas_periodo:
            total = venda.calcular_valor_total()
            linhas.append(
                f"#{venda.id:<5} {venda.dataHora:<18} "
                f"ID:{venda.idFuncionario:<9} R$ {total:>8.2f}  {venda.formaPagamento:<15}"
            )
        
        linhas.append("")
        linhas.append("=" * 70)
        linhas.append(" FIM DO RELATÓRIO ".center(70))
        linhas.append("=" * 70)
        
        return "\n".join(linhas)
    
    def exportar(self) -> bool:
        try:
            conteudo = self.gerar()
            
            with open(self.caminhoArquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            
            return True
            
        except Exception as e:
            print(f"Erro ao exportar relatório: {e}")
            return False