# Sistema de Pedidos para Conveniência

Este é um sistema de pedidos desenvolvido para tablets em conveniências, permitindo que clientes façam pedidos de bebidas diretamente no estabelecimento.

## Características

- Interface responsiva para tablet
- Catálogo de bebidas com categorias e filtros
- Carrinho de compras com atualização de valor em tempo real
- Sistema de finalização de pedido com geração de lista
- Painel administrativo para gerenciar produtos e pedidos

## Tecnologias Utilizadas

- Backend: Flask (Python)
- Banco de Dados: PostgreSQL
- Frontend: HTML, CSS, JavaScript

## Configuração para Deploy no Render.com

Este projeto está configurado para deploy automático no Render.com, utilizando:

- Web Service para a aplicação Flask
- Banco de dados PostgreSQL (plano gratuito)
- Variáveis de ambiente configuradas automaticamente

## Instruções para Deploy

1. Crie uma conta no [Render.com](https://render.com)
2. Conecte sua conta GitHub ao Render
3. Faça fork deste repositório para sua conta GitHub
4. No Render Dashboard, clique em "New" e selecione "Blueprint"
5. Selecione o repositório do fork e clique em "Apply"
6. O Render irá configurar automaticamente o serviço web e o banco de dados

## Acesso ao Sistema

Após o deploy, você terá acesso a:

- Interface do Cliente: `https://conveniencia-app.onrender.com`
- Painel Administrativo: `https://conveniencia-app.onrender.com/admin`

## Credenciais de Acesso ao Painel Administrativo

- Email: admin@conveniencia.com
- Senha: admin123

## Desenvolvimento Local

Para executar o sistema localmente:

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/conveniencia-app.git

# Entre no diretório
cd conveniencia-app

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python -m src.main
```

## Licença

Este projeto está licenciado sob a licença MIT.
