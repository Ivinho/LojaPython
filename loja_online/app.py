"""
Aplicação principal - Loja Online com Streamlit
"""

import streamlit as st
from src.banco_dados import BancoDados
from src.utilitarios import (
    formatar_moeda, calcular_frete, gerar_carrinho_padrao,
    adicionar_ao_carrinho, remover_do_carrinho, obter_total_carrinho,
    obter_quantidade_carrinho, limpar_carrinho, efetuou_login, fazer_logout
)
from src.modelo import Usuario, Pedido, ItemCarrinho, Avaliacao

# Configuração da página
st.set_page_config(
    page_title="Loja Online",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa o banco de dados
db = BancoDados()

# Inicializa a sessão
gerar_carrinho_padrao()

# CSS customizado
st.markdown("""
    <style>
    .produto-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .preco {
        font-size: 24px;
        color: #00cc00;
        font-weight: bold;
    }
    .botao-comprar {
        background-color: #ff6b6b;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====

st.sidebar.title("🛍️ Loja Online")

# Menu principal
menu = st.sidebar.radio("Navegação", 
    ["🏠 Home", "🛒 Carrinho", "📦 Meus Pedidos", "👤 Conta"],
    key="menu_principal"
)

# Status de login no sidebar
if efetuou_login():
    st.sidebar.success(f"✅ Logado como: **{st.session_state.usuario_nome}**")
    if st.sidebar.button("🚪 Sair"):
        fazer_logout()
        st.rerun()
else:
    st.sidebar.warning("⚠️ Você não está logado")
    st.sidebar.info("👉 Clique em '👤 Conta' no menu para fazer login")

# ===== PÁGINAS =====

if menu == "🏠 Home":
    # Banner principal
    st.title("🛍️ Bem-vindo à Loja Online!")
    st.write("Encontre os melhores produtos com preços incríveis!")
    
    # Abas de navegação
    tab1, tab2, tab3 = st.tabs(["🔍 Todos os Produtos", "📂 Por Categoria", "🔎 Buscar"])
    
    with tab1:
        st.subheader("Todos os Produtos")
        
        # Filtro de preço
        col1, col2 = st.columns(2)
        with col1:
            preco_min = st.slider("Preço Mínimo (R$)", 0, 1000, 0, key="preco_min_tab1")
        with col2:
            preco_max = st.slider("Preço Máximo (R$)", 0, 1000, 1000, key="preco_max_tab1")
        
        produtos = db.obter_todos_produtos()
        produtos_filtrados = [p for p in produtos if preco_min <= p.preco <= preco_max]
        
        if not produtos_filtrados:
            st.warning("Nenhum produto encontrado nessa faixa de preço.")
        else:
            # Exibe produtos em grid
            cols = st.columns(3)
            for idx, produto in enumerate(produtos_filtrados):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="produto-card">
                        <h4>{produto.nome}</h4>
                        <p>{produto.descricao[:50]}...</p>
                        <p class="preco">{formatar_moeda(produto.preco)}</p>
                        <p>Estoque: {produto.estoque}</p>
                        <p>⭐ {produto.avaliacao_media:.1f} ({produto.total_avaliacoes} avaliações)</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🛒 Adicionar", key=f"add_{produto.id}", use_container_width=True):
                        if produto.estoque > 0:
                            adicionar_ao_carrinho(produto.id, 1, produto.preco)
                            st.success(f"✅ {produto.nome} adicionado ao carrinho!")
                        else:
                            st.error("❌ Produto sem estoque!")
    
    with tab2:
        st.subheader("Produtos por Categoria")
        
        categorias = db.obter_categorias()
        
        if not categorias:
            st.info("Nenhuma categoria disponível ainda.")
        else:
            categoria_selecionada = st.selectbox("Escolha uma categoria:", categorias)
            
            produtos = db.obter_produtos_por_categoria(categoria_selecionada)
            
            if not produtos:
                st.warning("Nenhum produto nessa categoria.")
            else:
                cols = st.columns(3)
                for idx, produto in enumerate(produtos):
                    with cols[idx % 3]:
                        st.markdown(f"""
                        <div class="produto-card">
                            <h4>{produto.nome}</h4>
                            <p class="preco">{formatar_moeda(produto.preco)}</p>
                            <p>Estoque: {produto.estoque}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("🛒 Adicionar", key=f"add_cat_{produto.id}"):
                            if produto.estoque > 0:
                                adicionar_ao_carrinho(produto.id, 1, produto.preco)
                                st.success(f"✅ {produto.nome} adicionado!")
                            else:
                                st.error("❌ Sem estoque!")
    
    with tab3:
        st.subheader("Buscar Produtos")
        
        termo = st.text_input("Digite o nome ou descrição do produto:")
        
        if termo:
            produtos = db.buscar_produtos(termo)
            
            if not produtos:
                st.warning(f"Nenhum produto encontrado para '{termo}'")
            else:
                st.write(f"Encontrados {len(produtos)} produto(s)")
                
                cols = st.columns(2)
                for idx, produto in enumerate(produtos):
                    with cols[idx % 2]:
                        st.markdown(f"""
                        <div class="produto-card">
                            <h4>{produto.nome}</h4>
                            <p>{produto.descricao}</p>
                            <p class="preco">{formatar_moeda(produto.preco)}</p>
                            <p>Estoque: {produto.estoque}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("🛒 Adicionar", key=f"add_bus_{produto.id}"):
                            if produto.estoque > 0:
                                adicionar_ao_carrinho(produto.id, 1, produto.preco)
                                st.success(f"✅ Adicionado!")
                            else:
                                st.error("❌ Sem estoque!")

elif menu == "🛒 Carrinho":
    st.title("🛒 Seu Carrinho")
    
    gerar_carrinho_padrao()
    
    if not st.session_state.carrinho:
        st.info("Seu carrinho está vazio! 😢")
    else:
        # Tabela do carrinho
        st.subheader("Itens do Carrinho")
        
        carrinho_data = []
        for produto_id, item in st.session_state.carrinho.items():
            produto = db.obter_produto(produto_id)
            if produto:
                carrinho_data.append({
                    "Produto": produto.nome,
                    "Preço": formatar_moeda(item['preco_unitario']),
                    "Quantidade": item['quantidade'],
                    "Subtotal": formatar_moeda(item['quantidade'] * item['preco_unitario'])
                })
        
        st.table(carrinho_data)
        
        # Resumo do carrinho
        st.markdown("---")
        
        subtotal = obter_total_carrinho()
        frete = calcular_frete(subtotal)
        total = subtotal + frete
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Subtotal", formatar_moeda(subtotal))
        with col2:
            st.metric("Frete", formatar_moeda(frete))
        with col3:
            st.metric("Total", formatar_moeda(total))
        
        # Botões
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Limpar Carrinho", use_container_width=True):
                limpar_carrinho()
                st.rerun()
        
        with col2:
            if st.button("💳 Finalizar Compra", type="primary", use_container_width=True):
                if not efetuou_login():
                    st.session_state.mostrar_login_carrinho = True
                    st.rerun()
                else:
                    st.session_state.em_checkout = True
                    st.rerun()
        
        # Mostrar formulário de login se clicou em Finalizar sem estar logado
        if st.session_state.get("mostrar_login_carrinho", False):
            st.markdown("---")
            st.warning("⚠️ Você precisa estar logado para fazer uma compra!")
            
            st.subheader("🔑 Faça Login para Continuar")
            with st.form("login_form_carrinho"):
                email = st.text_input("📧 Email:", placeholder="seu@email.com")
                senha = st.text_input("🔐 Senha:", type="password", placeholder="Digite sua senha")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✅ Entrar", use_container_width=True):
                        if not email or not senha:
                            st.error("❌ Preencha o email e a senha!")
                        else:
                            usuario_id = db.verificar_login(email, senha)
                            if usuario_id:
                                usuario = db.obter_usuario(usuario_id)
                                st.session_state.usuario_id = usuario_id
                                st.session_state.usuario_nome = usuario.nome
                                st.session_state.mostrar_login_carrinho = False
                                st.success("✅ Login efetuado com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Email ou senha incorretos!")
                
                with col2:
                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                        st.session_state.mostrar_login_carrinho = False
                        st.rerun()

# ===== PÁGINA DE CHECKOUT =====

if st.session_state.get("em_checkout", False):
    st.title("💳 Finalizar Compra")
    
    gerar_carrinho_padrao()
    
    st.markdown("---")
    
    # Resumo dos itens
    st.subheader("📦 Resumo do Pedido")
    
    carrinho_data = []
    for produto_id, item in st.session_state.carrinho.items():
        produto = db.obter_produto(produto_id)
        if produto:
            carrinho_data.append({
                "Produto": produto.nome,
                "Preço Unitário": formatar_moeda(item['preco_unitario']),
                "Quantidade": item['quantidade'],
                "Subtotal": formatar_moeda(item['quantidade'] * item['preco_unitario'])
            })
    
    st.table(carrinho_data)
    
    st.markdown("---")
    
    # Cálculos
    st.subheader("💰 Valores")
    
    subtotal = obter_total_carrinho()
    frete = calcular_frete(subtotal)
    total = subtotal + frete
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Subtotal", formatar_moeda(subtotal))
    with col2:
        st.metric("Frete", formatar_moeda(frete))
    with col3:
        st.metric("Total", formatar_moeda(total))
    with col4:
        st.metric("Status", "Pendente")
    
    st.markdown("---")
    
    # Dados de entrega
    st.subheader("📍 Dados para Entrega")
    
    usuario = db.obter_usuario(st.session_state.usuario_id)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Comprador:** {usuario.nome}")
    with col2:
        st.write(f"**Telefone:** {usuario.telefone or 'Não informado'}")
    
    endereco_padrao = usuario.endereco or ""
    
    endereco_entrega = st.text_area(
        "Endereço de Entrega:",
        value=endereco_padrao,
        height=80,
        placeholder="Rua, número, bairro, cidade - Estado, CEP"
    )
    
    st.markdown("---")
    
    # Botões
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔙 Voltar ao Carrinho", use_container_width=True):
            st.session_state.em_checkout = False
            st.rerun()
    
    with col2:
        if st.button("❌ Cancelar Compra", use_container_width=True):
            st.session_state.em_checkout = False
            limpar_carrinho()
            st.rerun()
    
    with col3:
        if not endereco_entrega.strip():
            st.button("✅ Confirmar Pedido", disabled=True, use_container_width=True)
        else:
            if st.button("✅ Confirmar Pedido", type="primary", use_container_width=True):
                # Criar pedido
                items_pedido = []
                for produto_id, item in st.session_state.carrinho.items():
                    items_pedido.append(ItemCarrinho(
                        produto_id=produto_id,
                        quantidade=item['quantidade'],
                        preco_unitario=item['preco_unitario']
                    ))
                
                pedido = Pedido(
                    usuario_id=st.session_state.usuario_id,
                    items=items_pedido,
                    endereco_entrega=endereco_entrega,
                    valor_frete=frete
                )
                
                # Atualizar status do pedido
                pedido.status = "Pagamento Confirmado"
                
                # Salvar no banco
                pedido_id = db.criar_pedido(pedido)
                
                # Atualizar estoque
                for produto_id, item in st.session_state.carrinho.items():
                    db.atualizar_estoque(produto_id, item['quantidade'])
                
                # Guardar dados para exibição
                valor_total = pedido.obter_total()
                valor_frete = pedido.valor_frete
                nome_comprador = usuario.nome
                
                # Limpar carrinho
                limpar_carrinho()
                st.session_state.em_checkout = False
                
                st.success(f"✅ Pedido #{pedido_id} realizado com sucesso!")
                st.balloons()
                
                st.info(f"""
                    ### 🎉 Compra Finalizada!
                    
                    **Número do Pedido:** #{pedido_id}  
                    **Comprador:** {nome_comprador}  
                    **Valor Total:** {formatar_moeda(valor_total)}  
                    **Frete:** {formatar_moeda(valor_frete)}  
                    **Endereço de Entrega:** {endereco_entrega}  
                    **Status:** 📋 Pagamento Confirmado
                    
                    Você pode acompanhar seu pedido na seção "📦 Meus Pedidos".
                """)
                
                st.write("")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🏠 Voltar à Home", use_container_width=True):
                        st.session_state.em_checkout = False
                        st.rerun()
                
                with col2:
                    if st.button("📦 Ver Meus Pedidos", use_container_width=True):
                        st.session_state.menu_principal = "📦 Meus Pedidos"
                        st.session_state.em_checkout = False
                        st.rerun()

elif menu == "📦 Meus Pedidos":
    st.title("📦 Meus Pedidos")
    
    if not efetuou_login():
        st.info("📋 Acesse sua conta para ver seus pedidos")
        
        st.subheader("Faça Login")
        with st.form("login_form_pedidos"):
            email = st.text_input("📧 Email:", placeholder="seu@email.com")
            senha = st.text_input("🔐 Senha:", type="password", placeholder="Digite sua senha")
            
            if st.form_submit_button("🔑 Entrar", use_container_width=True):
                if not email or not senha:
                    st.error("❌ Preencha o email e a senha!")
                else:
                    usuario_id = db.verificar_login(email, senha)
                    if usuario_id:
                        usuario = db.obter_usuario(usuario_id)
                        st.session_state.usuario_id = usuario_id
                        st.session_state.usuario_nome = usuario.nome
                        st.success("✅ Login efetuado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Email ou senha incorretos!")
    else:
        pedidos = db.obter_pedidos_usuario(st.session_state.usuario_id)
        
        if not pedidos:
            st.info("Você ainda não fez nenhum pedido.")
        else:
            for pedido in pedidos:
                with st.expander(f"Pedido #{pedido['id']} - {pedido['status']} - {formatar_moeda(pedido['valor_total'])}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Data:** {pedido['data_pedido']}")
                    with col2:
                        st.write(f"**Status:** {pedido['status']}")
                    with col3:
                        st.write(f"**Total:** {formatar_moeda(pedido['valor_total'])}")
                    
                    st.write(f"**Endereço de Entrega:** {pedido['endereco_entrega']}")

elif menu == "👤 Conta":
    st.title("👤 Minha Conta")
    
    if not efetuou_login():
        # CSS customizado para o login
        st.markdown("""
            <style>
            .login-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px;
                border-radius: 15px;
                color: white;
                text-align: center;
                margin-bottom: 30px;
            }
            .login-container h2 {
                margin: 0;
                font-size: 28px;
                font-weight: bold;
            }
            .login-container p {
                margin: 10px 0 0 0;
                opacity: 0.9;
            }
            </style>
            <div class="login-container">
                <h2>🔐 Acesso à Sua Conta</h2>
                <p>Faça login ou crie uma nova conta para continuar</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Tabs de login e cadastro
        tab1, tab2 = st.tabs(["🔑 Entrar", "📝 Criar Conta"])
        
        with tab1:
            st.subheader("Bem-vindo de volta!")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                with st.form("login_form_conta"):
                    st.markdown("#### Insira seus dados")
                    email = st.text_input("📧 Email", placeholder="seu@email.com", label_visibility="collapsed")
                    senha = st.text_input("🔐 Senha", type="password", placeholder="Digite sua senha", label_visibility="collapsed")
                    
                    st.write("")
                    if st.form_submit_button("🔑 Entrar", use_container_width=True, type="primary"):
                        if not email or not senha:
                            st.error("❌ Preencha o email e a senha!")
                        else:
                            usuario_id = db.verificar_login(email, senha)
                            if usuario_id:
                                usuario = db.obter_usuario(usuario_id)
                                st.session_state.usuario_id = usuario_id
                                st.session_state.usuario_nome = usuario.nome
                                st.success("✅ Login efetuado com sucesso!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("❌ Email ou senha incorretos!")
        
        with tab2:
            st.subheader("Crie sua conta agora!")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                with st.form("cadastro_form"):
                    st.markdown("#### Informações Pessoais")
                    nome = st.text_input("👤 Nome Completo", placeholder="Seu nome aqui", label_visibility="collapsed")
                    email = st.text_input("📧 Email", placeholder="seu@email.com", label_visibility="collapsed")
                    telefone = st.text_input("📱 Telefone", placeholder="(11) 99999-9999", label_visibility="collapsed")
                    
                    st.markdown("#### Endereço")
                    endereco = st.text_area("📍 Endereço", placeholder="Rua, número, bairro, cidade - Estado", height=70, label_visibility="collapsed")
                    
                    st.markdown("#### Segurança")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        senha = st.text_input("🔐 Senha", type="password", placeholder="Mínimo 6 caracteres", label_visibility="collapsed")
                    with col_b:
                        confirmar_senha = st.text_input("🔐 Confirmar", type="password", label_visibility="collapsed")
                    
                    st.write("")
                    if st.form_submit_button("✅ Criar Conta", use_container_width=True, type="primary"):
                        if not nome or not email or not senha:
                            st.error("❌ Preencha os campos obrigatórios!")
                        elif len(senha) < 6:
                            st.error("❌ A senha deve ter no mínimo 6 caracteres!")
                        elif senha != confirmar_senha:
                            st.error("❌ As senhas não coincidem!")
                        else:
                            usuario = Usuario(
                                nome=nome,
                                email=email,
                                senha=senha,
                                telefone=telefone,
                                endereco=endereco
                            )
                            usuario_id = db.criar_usuario(usuario)
                            
                            if usuario_id > 0:
                                st.success("✅ Conta criada com sucesso! Agora faça login.")
                                st.balloons()
                            else:
                                st.error("❌ Este email já está registrado!")
    
    else:
        st.success(f"✅ Logado como: **{st.session_state.usuario_nome}**")
        
        usuario = db.obter_usuario(st.session_state.usuario_id)
        
        st.subheader("Informações da Conta")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Nome:** {usuario.nome}")
            st.write(f"**Email:** {usuario.email}")
        
        with col2:
            st.write(f"**Telefone:** {usuario.telefone or 'Não informado'}")
            st.write(f"**Endereço:** {usuario.endereco or 'Não informado'}")
        
        if st.button("🚪 Fazer Logout"):
            fazer_logout()
            st.success("✅ Você foi desconectado!")
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center'>"
    "<p>© 2025 Loja Online - Desenvolvido com Python + Streamlit 🚀</p>"
    "</div>",
    unsafe_allow_html=True
)
