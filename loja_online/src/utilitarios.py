"""
Funções utilitárias para a loja online.
"""

import streamlit as st
from src.modelo import Produto


def formatar_moeda(valor: float) -> str:
    """Formata um valor como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')


def calcular_frete(valor_pedido: float) -> float:
    """Calcula o valor do frete baseado no valor do pedido."""
    if valor_pedido >= 100:
        return 0.0  # Frete grátis
    elif valor_pedido >= 50:
        return 10.0
    else:
        return 15.0


def gerar_carrinho_padrao():
    """Gera um carrinho padrão na sessão."""
    if 'carrinho' not in st.session_state:
        st.session_state.carrinho = {}
    if 'usuario_id' not in st.session_state:
        st.session_state.usuario_id = None
    if 'usuario_nome' not in st.session_state:
        st.session_state.usuario_nome = None


def adicionar_ao_carrinho(produto_id: int, quantidade: int, preco: float):
    """Adiciona um item ao carrinho."""
    gerar_carrinho_padrao()
    
    if produto_id in st.session_state.carrinho:
        st.session_state.carrinho[produto_id]['quantidade'] += quantidade
    else:
        st.session_state.carrinho[produto_id] = {
            'quantidade': quantidade,
            'preco_unitario': preco
        }


def remover_do_carrinho(produto_id: int):
    """Remove um item do carrinho."""
    if produto_id in st.session_state.carrinho:
        del st.session_state.carrinho[produto_id]


def obter_total_carrinho() -> float:
    """Calcula o total do carrinho."""
    gerar_carrinho_padrao()
    total = 0
    
    for item in st.session_state.carrinho.values():
        total += item['quantidade'] * item['preco_unitario']
    
    return total


def obter_quantidade_carrinho() -> int:
    """Retorna a quantidade de itens no carrinho."""
    gerar_carrinho_padrao()
    return sum(item['quantidade'] for item in st.session_state.carrinho.values())


def limpar_carrinho():
    """Limpa o carrinho."""
    st.session_state.carrinho = {}


def efetuou_login() -> bool:
    """Verifica se o usuário está logado."""
    return st.session_state.usuario_id is not None


def fazer_logout():
    """Remove o login do usuário."""
    st.session_state.usuario_id = None
    st.session_state.usuario_nome = None
    limpar_carrinho()
