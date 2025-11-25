"""
Banco de dados SQLite para a loja online.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional
from src.modelo import Produto, Usuario, ItemCarrinho, Pedido, Avaliacao


class BancoDados:
    """Gerencia conexão e operações com banco de dados SQLite."""
    
    def __init__(self, caminho_db: str = "dados/loja.db"):
        self.caminho_db = caminho_db
        os.makedirs(os.path.dirname(caminho_db), exist_ok=True)
        self.criar_tabelas()
    
    def obter_conexao(self) -> sqlite3.Connection:
        """Retorna conexão com o banco."""
        conexao = sqlite3.connect(self.caminho_db)
        conexao.row_factory = sqlite3.Row
        return conexao
    
    def criar_tabelas(self):
        """Cria as tabelas do banco de dados."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        # Tabela de Produtos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco REAL NOT NULL,
                estoque INTEGER DEFAULT 0,
                categoria TEXT NOT NULL,
                avaliacao_media REAL DEFAULT 0,
                total_avaliacoes INTEGER DEFAULT 0,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de Usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                telefone TEXT,
                endereco TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ativo BOOLEAN DEFAULT 1
            )
        ''')
        
        # Tabela de Pedidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                endereco_entrega TEXT NOT NULL,
                valor_subtotal REAL NOT NULL,
                valor_frete REAL DEFAULT 0,
                valor_total REAL NOT NULL,
                status TEXT DEFAULT 'Pendente',
                data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_entrega TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Tabela de Itens do Pedido
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        ''')
        
        # Tabela de Avaliações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS avaliacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                nota INTEGER NOT NULL,
                comentario TEXT,
                data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produto_id) REFERENCES produtos (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        conexao.commit()
        conexao.close()
    
    # ===== OPERAÇÕES COM PRODUTOS =====
    
    def criar_produto(self, produto: Produto) -> int:
        """Cria um novo produto."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('''
            INSERT INTO produtos (nome, descricao, preco, estoque, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (produto.nome, produto.descricao, produto.preco, produto.estoque, produto.categoria))
        
        conexao.commit()
        produto_id = cursor.lastrowid
        conexao.close()
        
        return produto_id
    
    def obter_produto(self, produto_id: int) -> Optional[Produto]:
        """Obtém um produto pelo ID."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
        linha = cursor.fetchone()
        conexao.close()
        
        if linha:
            return Produto(
                id=linha['id'],
                nome=linha['nome'],
                descricao=linha['descricao'],
                preco=linha['preco'],
                estoque=linha['estoque'],
                categoria=linha['categoria']
            )
        return None
    
    def obter_todos_produtos(self) -> List[Produto]:
        """Obtém todos os produtos."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT * FROM produtos ORDER BY nome')
        linhas = cursor.fetchall()
        conexao.close()
        
        produtos = []
        for linha in linhas:
            produto = Produto(
                id=linha['id'],
                nome=linha['nome'],
                descricao=linha['descricao'],
                preco=linha['preco'],
                estoque=linha['estoque'],
                categoria=linha['categoria']
            )
            produto.avaliacao_media = linha['avaliacao_media']
            produto.total_avaliacoes = linha['total_avaliacoes']
            produtos.append(produto)
        
        return produtos
    
    def obter_produtos_por_categoria(self, categoria: str) -> List[Produto]:
        """Obtém produtos de uma categoria específica."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT * FROM produtos WHERE categoria = ? ORDER BY nome', (categoria,))
        linhas = cursor.fetchall()
        conexao.close()
        
        produtos = []
        for linha in linhas:
            produto = Produto(
                id=linha['id'],
                nome=linha['nome'],
                descricao=linha['descricao'],
                preco=linha['preco'],
                estoque=linha['estoque'],
                categoria=linha['categoria']
            )
            produtos.append(produto)
        
        return produtos
    
    def buscar_produtos(self, termo: str) -> List[Produto]:
        """Busca produtos por nome ou descrição."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        termo_busca = f"%{termo}%"
        cursor.execute('''
            SELECT * FROM produtos 
            WHERE nome LIKE ? OR descricao LIKE ? 
            ORDER BY nome
        ''', (termo_busca, termo_busca))
        linhas = cursor.fetchall()
        conexao.close()
        
        produtos = []
        for linha in linhas:
            produto = Produto(
                id=linha['id'],
                nome=linha['nome'],
                descricao=linha['descricao'],
                preco=linha['preco'],
                estoque=linha['estoque'],
                categoria=linha['categoria']
            )
            produtos.append(produto)
        
        return produtos
    
    def atualizar_estoque(self, produto_id: int, quantidade: int) -> bool:
        """Atualiza o estoque de um produto."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('''
            UPDATE produtos SET estoque = estoque - ? WHERE id = ?
        ''', (quantidade, produto_id))
        
        conexao.commit()
        sucesso = cursor.rowcount > 0
        conexao.close()
        
        return sucesso
    
    # ===== OPERAÇÕES COM USUÁRIOS =====
    
    def criar_usuario(self, usuario: Usuario) -> int:
        """Cria um novo usuário."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO usuarios (nome, email, senha, telefone, endereco, ativo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (usuario.nome, usuario.email, usuario.senha, usuario.telefone, 
                  usuario.endereco, usuario.ativo))
            
            conexao.commit()
            usuario_id = cursor.lastrowid
            return usuario_id
        except sqlite3.IntegrityError:
            return -1  # Email já existe
        finally:
            conexao.close()
    
    def obter_usuario(self, usuario_id: int) -> Optional[Usuario]:
        """Obtém um usuário pelo ID."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
        linha = cursor.fetchone()
        conexao.close()
        
        if linha:
            return Usuario(
                id=linha['id'],
                nome=linha['nome'],
                email=linha['email'],
                senha=linha['senha'],
                telefone=linha['telefone'],
                endereco=linha['endereco']
            )
        return None
    
    def verificar_login(self, email: str, senha: str) -> Optional[int]:
        """Verifica se o login está correto. Retorna o ID do usuário ou None."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT id FROM usuarios WHERE email = ? AND senha = ? AND ativo = 1', 
                      (email, senha))
        linha = cursor.fetchone()
        conexao.close()
        
        return linha['id'] if linha else None
    
    # ===== OPERAÇÕES COM PEDIDOS =====
    
    def criar_pedido(self, pedido: Pedido) -> int:
        """Cria um novo pedido."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        subtotal = pedido.obter_subtotal()
        total = pedido.obter_total()
        
        cursor.execute('''
            INSERT INTO pedidos (usuario_id, endereco_entrega, valor_subtotal, valor_frete, valor_total, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (pedido.usuario_id, pedido.endereco_entrega, subtotal, pedido.valor_frete, total, pedido.status))
        
        pedido_id = cursor.lastrowid
        
        # Insere os itens do pedido
        for item in pedido.items:
            cursor.execute('''
                INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
            ''', (pedido_id, item.produto_id, item.quantidade, item.preco_unitario))
        
        conexao.commit()
        conexao.close()
        
        return pedido_id
    
    def obter_pedidos_usuario(self, usuario_id: int) -> List[dict]:
        """Obtém todos os pedidos de um usuário."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT * FROM pedidos WHERE usuario_id = ? ORDER BY data_pedido DESC
        ''', (usuario_id,))
        linhas = cursor.fetchall()
        conexao.close()
        
        return [dict(linha) for linha in linhas]
    
    # ===== OPERAÇÕES COM AVALIAÇÕES =====
    
    def criar_avaliacao(self, avaliacao: Avaliacao) -> int:
        """Cria uma nova avaliação."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('''
            INSERT INTO avaliacoes (produto_id, usuario_id, nota, comentario)
            VALUES (?, ?, ?, ?)
        ''', (avaliacao.produto_id, avaliacao.usuario_id, avaliacao.nota, avaliacao.comentario))
        
        conexao.commit()
        avaliacao_id = cursor.lastrowid
        
        # Atualiza a avaliação média do produto
        self._atualizar_avaliacao_produto(avaliacao.produto_id)
        
        conexao.close()
        return avaliacao_id
    
    def obter_avaliacoes_produto(self, produto_id: int) -> List[dict]:
        """Obtém todas as avaliações de um produto."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT a.*, u.nome FROM avaliacoes a
            JOIN usuarios u ON a.usuario_id = u.id
            WHERE a.produto_id = ? ORDER BY a.data_avaliacao DESC
        ''', (produto_id,))
        linhas = cursor.fetchall()
        conexao.close()
        
        return [dict(linha) for linha in linhas]
    
    def _atualizar_avaliacao_produto(self, produto_id: int):
        """Atualiza a avaliação média de um produto."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT AVG(nota) as media, COUNT(*) as total FROM avaliacoes WHERE produto_id = ?
        ''', (produto_id,))
        resultado = cursor.fetchone()
        
        media = resultado['media'] if resultado['media'] else 0
        total = resultado['total'] if resultado['total'] else 0
        
        cursor.execute('''
            UPDATE produtos SET avaliacao_media = ?, total_avaliacoes = ? WHERE id = ?
        ''', (round(media, 2), total, produto_id))
        
        conexao.commit()
        conexao.close()
    
    def obter_categorias(self) -> List[str]:
        """Obtém todas as categorias de produtos."""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT DISTINCT categoria FROM produtos ORDER BY categoria')
        linhas = cursor.fetchall()
        conexao.close()
        
        return [linha['categoria'] for linha in linhas]
