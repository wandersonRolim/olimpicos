from src.models import db
from datetime import datetime
from src.models.produto import Produto

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='pendente')  # pendente, em_andamento, concluido
    valor_total = db.Column(db.Float, nullable=False, default=0.0)
    observacoes = db.Column(db.Text, nullable=True)
    
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'data_hora': self.data_hora.strftime('%Y-%m-%d %H:%M:%S') if self.data_hora else None,
            'status': self.status,
            'valor_total': self.valor_total,
            'observacoes': self.observacoes,
            'itens': [item.to_dict() for item in self.itens]
        }

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    produto = db.relationship('Produto', backref='itens_pedido', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'produto_id': self.produto_id,
            'produto_nome': self.produto.nome if self.produto else None,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal
        }
