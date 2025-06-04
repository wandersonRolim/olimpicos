import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, session
from src.models import db
from src.models.usuario import Usuario
from src.models.produto import Produto
from src.models.pedido import Pedido, ItemPedido
from src.routes.produto import produto_bp
from src.routes.pedido import pedido_bp
from src.routes.auth import auth_bp
from werkzeug.security import generate_password_hash

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Registrando blueprints
app.register_blueprint(produto_bp, url_prefix='/api')
app.register_blueprint(pedido_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')

# Configuração do banco de dados
# Verifica se existe DATABASE_URL (usado pelo Render) ou usa configuração local
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    # Configuração local para desenvolvimento
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Inicialização do banco de dados e dados de exemplo
def inicializar_banco():
    with app.app_context():
        db.create_all()
        
        # Verifica se já existem dados
        if Usuario.query.count() == 0:
            # Cria usuário administrador padrão
            admin = Usuario(
                nome='Administrador',
                email='admin@conveniencia.com',
                senha=generate_password_hash('admin123'),
                tipo='admin'
            )
            db.session.add(admin)
            
            # Cria alguns produtos de exemplo
            produtos = [
                Produto(nome='Água Mineral 500ml', descricao='Água mineral sem gás', preco=2.50, categoria='Água', imagem_url='/static/img/agua.jpg', estoque=50),
                Produto(nome='Refrigerante Cola 350ml', descricao='Refrigerante sabor cola', preco=4.50, categoria='Refrigerante', imagem_url='/static/img/refrigerante_cola.jpg', estoque=40),
                Produto(nome='Refrigerante Guaraná 350ml', descricao='Refrigerante sabor guaraná', preco=4.00, categoria='Refrigerante', imagem_url='/static/img/refrigerante_guarana.jpg', estoque=40),
                Produto(nome='Suco de Laranja 300ml', descricao='Suco natural de laranja', preco=6.00, categoria='Suco', imagem_url='/static/img/suco_laranja.jpg', estoque=20),
                Produto(nome='Cerveja Pilsen 350ml', descricao='Cerveja tipo pilsen', preco=5.50, categoria='Alcoólica', imagem_url='/static/img/cerveja.jpg', estoque=30),
                Produto(nome='Energético 250ml', descricao='Bebida energética', preco=8.00, categoria='Energético', imagem_url='/static/img/energetico.jpg', estoque=25),
                Produto(nome='Água de Coco 300ml', descricao='Água de coco natural', preco=7.00, categoria='Água', imagem_url='/static/img/agua_coco.jpg', estoque=15),
                Produto(nome='Chá Gelado 350ml', descricao='Chá gelado sabor limão', preco=5.00, categoria='Chá', imagem_url='/static/img/cha_gelado.jpg', estoque=20)
            ]
            
            for produto in produtos:
                db.session.add(produto)
                
            db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/admin', defaults={'path': ''})
@app.route('/admin/<path:path>')
def serve_admin(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    admin_path = os.path.join(static_folder_path, 'admin.html')
    if os.path.exists(admin_path):
        return send_from_directory(static_folder_path, 'admin.html')
    else:
        return "admin.html not found", 404

# Inicialização do banco de dados na inicialização da aplicação
with app.app_context():
    inicializar_banco()

# Para o Render, precisamos expor a aplicação para ser importada
# O Render usa gunicorn para servir a aplicação
if __name__ == '__main__':
    # Quando rodando localmente
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
