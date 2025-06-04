from src.models import db
from flask import Blueprint, jsonify, request
from src.models.produto import Produto

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    """Lista todos os produtos disponíveis"""
    produtos = Produto.query.filter_by(disponivel=True).all()
    return jsonify([produto.to_dict() for produto in produtos])

@produto_bp.route('/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    """Obtém detalhes de um produto específico"""
    produto = Produto.query.get_or_404(produto_id)
    return jsonify(produto.to_dict())

@produto_bp.route('/produtos/categorias', methods=['GET'])
def listar_categorias():
    """Lista todas as categorias de produtos"""
    categorias = db.session.query(Produto.categoria).distinct().all()
    return jsonify([categoria[0] for categoria in categorias])

@produto_bp.route('/produtos/categoria/<categoria>', methods=['GET'])
def listar_por_categoria(categoria):
    """Lista produtos por categoria"""
    produtos = Produto.query.filter_by(categoria=categoria, disponivel=True).all()
    return jsonify([produto.to_dict() for produto in produtos])

# Rotas administrativas
@produto_bp.route('/admin/produtos', methods=['POST'])
def adicionar_produto():
    """Adiciona um novo produto"""
    dados = request.json
    
    novo_produto = Produto(
        nome=dados['nome'],
        descricao=dados.get('descricao', ''),
        preco=dados['preco'],
        categoria=dados['categoria'],
        imagem_url=dados.get('imagem_url', ''),
        estoque=dados.get('estoque', 0),
        disponivel=dados.get('disponivel', True)
    )
    
    db.session.add(novo_produto)
    db.session.commit()
    
    return jsonify(novo_produto.to_dict()), 201

@produto_bp.route('/admin/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    """Atualiza um produto existente"""
    produto = Produto.query.get_or_404(produto_id)
    dados = request.json
    
    produto.nome = dados.get('nome', produto.nome)
    produto.descricao = dados.get('descricao', produto.descricao)
    produto.preco = dados.get('preco', produto.preco)
    produto.categoria = dados.get('categoria', produto.categoria)
    produto.imagem_url = dados.get('imagem_url', produto.imagem_url)
    produto.estoque = dados.get('estoque', produto.estoque)
    produto.disponivel = dados.get('disponivel', produto.disponivel)
    
    db.session.commit()
    
    return jsonify(produto.to_dict())

@produto_bp.route('/admin/produtos/<int:produto_id>', methods=['DELETE'])
def remover_produto(produto_id):
    """Remove um produto"""
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    
    return jsonify({'mensagem': 'Produto removido com sucesso'})
