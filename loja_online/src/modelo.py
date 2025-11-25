"""
Modelos de dados para a loja online.
"""

from datetime import datetime
from typing import Optional


class Produto:
    """Representa um produto na loja."""
    
    def __init__(self, nome: str, descricao: str, preco: float, estoque: int, 
                 categoria: str, id: Optional[int] = None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.categoria = categoria
        self.data_criacao = datetime.now()
        self.avaliacao_media = 0.0
        self.total_avaliacoes = 0
    
    def __repr__(self):
        return f"Produto(id={self.id}, nome='{self.nome}', preco=R${self.preco})"


class Usuario:
    """Representa um usuário da loja."""
    
    def __init__(self, nome: str, email: str, senha: str, telefone: str = "", 
                 endereco: str = "", id: Optional[int] = None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.endereco = endereco
        self.data_cadastro = datetime.now()
        self.ativo = True
    
    def __repr__(self):
        return f"Usuario(id={self.id}, nome='{self.nome}', email='{self.email}')"


class ItemCarrinho:
    """Representa um item no carrinho."""
    
    def __init__(self, produto_id: int, quantidade: int, preco_unitario: float):
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
    
    def obter_subtotal(self) -> float:
        """Retorna o subtotal do item."""
        return self.quantidade * self.preco_unitario
    
    def __repr__(self):
        return f"ItemCarrinho(produto_id={self.produto_id}, qtd={self.quantidade})"


class Pedido:
    """Representa um pedido da loja."""
    
    STATUS_PENDENTE = "Pendente"
    STATUS_PAGAMENTO_CONFIRMADO = "Pagamento Confirmado"
    STATUS_ENVIADO = "Enviado"
    STATUS_ENTREGUE = "Entregue"
    STATUS_CANCELADO = "Cancelado"
    
    def __init__(self, usuario_id: int, items: list, endereco_entrega: str, 
                 valor_frete: float = 0.0, id: Optional[int] = None):
        self.id = id
        self.usuario_id = usuario_id
        self.items = items  # Lista de ItemCarrinho
        self.endereco_entrega = endereco_entrega
        self.valor_frete = valor_frete
        self.status = self.STATUS_PENDENTE
        self.data_pedido = datetime.now()
        self.data_entrega = None
    
    def obter_subtotal(self) -> float:
        """Retorna o subtotal dos produtos."""
        return sum(item.obter_subtotal() for item in self.items)
    
    def obter_total(self) -> float:
        """Retorna o total incluindo frete."""
        return self.obter_subtotal() + self.valor_frete
    
    def __repr__(self):
        return f"Pedido(id={self.id}, usuario_id={self.usuario_id}, status='{self.status}')"


class Avaliacao:
    """Representa uma avaliação de produto."""
    
    def __init__(self, produto_id: int, usuario_id: int, nota: int, comentario: str = "", 
                 id: Optional[int] = None):
        self.id = id
        self.produto_id = produto_id
        self.usuario_id = usuario_id
        self.nota = nota  # 1 a 5
        self.comentario = comentario
        self.data_avaliacao = datetime.now()
    
    def __repr__(self):
        return f"Avaliacao(produto_id={self.produto_id}, nota={self.nota})"
