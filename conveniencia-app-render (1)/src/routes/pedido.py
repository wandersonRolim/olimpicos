from src.models import db
from flask import Blueprint, jsonify, request
from src.models.pedido import Pedido, ItemPedido
from src.models.produto import Produto

pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    """Cria um novo pedido"""
    dados = request.json
    
    novo_pedido = Pedido(
        observacoes=dados.get('observacoes', '')
    )
    
    # Adiciona os itens ao pedido
    valor_total = 0
    for item in dados.get('itens', []):
        produto = Produto.query.get_or_404(item['produto_id'])
        preco_unitario = produto.preco
        subtotal = preco_unitario * item['quantidade']
        
        novo_item = ItemPedido(
            produto_id=item['produto_id'],
            quantidade=item['quantidade'],
            preco_unitario=preco_unitario,
            subtotal=subtotal
        )
        
        novo_pedido.itens.append(novo_item)
        valor_total += subtotal
    
    novo_pedido.valor_total = valor_total
    
    db.session.add(novo_pedido)
    db.session.commit()
    
    return jsonify(novo_pedido.to_dict()), 201

@pedido_bp.route('/pedidos/<int:pedido_id>', methods=['GET'])
def obter_pedido(pedido_id):
    """Obtém detalhes de um pedido específico"""
    pedido = Pedido.query.get_or_404(pedido_id)
    return jsonify(pedido.to_dict())

@pedido_bp.route('/pedidos/lista', methods=['GET'])
def listar_pedidos():
    """Lista todos os pedidos"""
    pedidos = Pedido.query.order_by(Pedido.data_hora.desc()).all()
    return jsonify([pedido.to_dict() for pedido in pedidos])

@pedido_bp.route('/pedidos/<int:pedido_id>/status', methods=['PUT'])
def atualizar_status_pedido(pedido_id):
    """Atualiza o status de um pedido"""
    pedido = Pedido.query.get_or_404(pedido_id)
    dados = request.json
    
    pedido.status = dados.get('status', pedido.status)
    db.session.commit()
    
    return jsonify(pedido.to_dict())
