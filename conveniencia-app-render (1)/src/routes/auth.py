from src.models import db
from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Autenticação de usuário"""
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario or not check_password_hash(usuario.senha, senha):
        return jsonify({'erro': 'Credenciais inválidas'}), 401
    
    session['usuario_id'] = usuario.id
    session['usuario_tipo'] = usuario.tipo
    
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo': usuario.tipo
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Encerra a sessão do usuário"""
    session.clear()
    return jsonify({'mensagem': 'Logout realizado com sucesso'})

@auth_bp.route('/admin/usuarios', methods=['POST'])
def criar_usuario():
    """Cria um novo usuário (apenas administradores)"""
    dados = request.json
    
    # Verifica se o email já está em uso
    if Usuario.query.filter_by(email=dados['email']).first():
        return jsonify({'erro': 'Email já cadastrado'}), 400
    
    novo_usuario = Usuario(
        nome=dados['nome'],
        email=dados['email'],
        senha=generate_password_hash(dados['senha']),
        tipo=dados.get('tipo', 'funcionario')
    )
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify(novo_usuario.to_dict()), 201

@auth_bp.route('/admin/usuarios', methods=['GET'])
def listar_usuarios():
    """Lista todos os usuários (apenas administradores)"""
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios])
