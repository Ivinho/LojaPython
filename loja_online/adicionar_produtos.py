"""
Script para popular a loja com produtos de exemplo.
Execute uma única vez para adicionar produtos ao banco de dados.
"""

from src.banco_dados import BancoDados
from src.modelo import Produto

# Inicializa o banco
db = BancoDados()

# Lista de produtos para adicionar
produtos_exemplo = [
    Produto("Notebook Dell", "Notebook Dell Inspiron 15, Intel i7, 16GB RAM, SSD 512GB", 3500.00, 5, "Eletrônicos"),
    Produto("Mouse Logitech", "Mouse sem fio, 2.4GHz, bateria até 18 meses", 89.90, 20, "Periféricos"),
    Produto("Teclado Mecânico", "Teclado mecânico RGB, switches Cherry MX", 450.00, 10, "Periféricos"),
    Produto("Monitor LG 24\"", "Monitor LG 24 polegadas, Full HD, 75Hz", 899.00, 8, "Eletrônicos"),
    Produto("Headset Gamer", "Headset com microfone, som surround 7.1, RGB", 299.90, 15, "Periféricos"),
    Produto("Webcam HD", "Webcam 1080p, microfone integrado, USB", 199.00, 12, "Periféricos"),
    Produto("SSD 1TB", "SSD NVMe 1TB, velocidade até 3500MB/s", 399.90, 25, "Armazenamento"),
    Produto("RAM 16GB", "Memória RAM DDR4 16GB, 3200MHz", 259.90, 18, "Componentes"),
    Produto("Placa Mãe", "Placa Mãe B550, socket AM4, WiFi integrado", 799.00, 6, "Componentes"),
    Produto("Processador Ryzen", "AMD Ryzen 5 5600X, 6 cores, 12 threads", 1299.00, 4, "Componentes"),
    Produto("GPU RTX 3060", "NVIDIA GeForce RTX 3060, 12GB GDDR6", 2199.00, 3, "Componentes"),
    Produto("Fonte 750W", "Fonte modular 750W, 80+ Bronze, ventilador silencioso", 549.00, 10, "Componentes"),
    Produto("Gabinete RGB", "Gabinete ATX, 4 fans RGB pré-instalados, vidro temperado", 699.00, 7, "Componentes"),
    Produto("Cooler CPU", "Cooler tower, compatível com Intel e AMD, iluminação RGB", 189.90, 12, "Componentes"),
    Produto("Mousepad Grande", "Mousepad 800x300mm, base de borracha, superfície suave", 79.90, 30, "Periféricos"),
    Produto("Hub USB", "Hub USB 3.0 com 7 portas, carregamento rápido", 129.90, 16, "Periféricos"),
    Produto("Cabo HDMI 2.1", "Cabo HDMI 2.1, 4K@120Hz, blindagem dupla", 89.90, 20, "Cabos"),
    Produto("Cabo USB-C", "Cabo USB-C 2 metros, carregamento rápido 100W", 59.90, 25, "Cabos"),
    Produto("Adaptador DisplayPort", "Adaptador DisplayPort para HDMI, resolução 4K", 149.00, 8, "Cabos"),
    Produto("Ventilador RGB", "Ventilador 120mm RGB, controle remoto, silencioso", 69.90, 22, "Componentes"),
]

print("=" * 60)
print("ADICIONANDO PRODUTOS À LOJA")
print("=" * 60)

for produto in produtos_exemplo:
    produto_id = db.criar_produto(produto)
    print(f"✅ Produto adicionado: {produto.nome} (ID: {produto_id})")

print("\n" + "=" * 60)
print(f"✨ Total de {len(produtos_exemplo)} produtos adicionados com sucesso!")
print("=" * 60)
print("\nAgora você pode rodar: streamlit run app.py")
