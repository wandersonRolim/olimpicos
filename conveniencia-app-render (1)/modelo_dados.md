# Modelo de Dados para o Sistema de Pedidos

## Tabela: Produtos
- id: Identificador único do produto
- nome: Nome do produto
- descricao: Descrição detalhada do produto
- preco: Preço unitário
- categoria: Categoria do produto (ex: refrigerante, água, suco, etc.)
- imagem_url: Caminho para a imagem do produto
- estoque: Quantidade disponível em estoque
- disponivel: Booleano indicando se o produto está disponível para venda
- data_cadastro: Data de cadastro do produto

## Tabela: Pedidos
- id: Identificador único do pedido
- data_hora: Data e hora da criação do pedido
- status: Status do pedido (pendente, em andamento, concluído)
- valor_total: Valor total do pedido
- observacoes: Observações adicionais do cliente

## Tabela: ItensPedido
- id: Identificador único do item
- pedido_id: Referência ao pedido
- produto_id: Referência ao produto
- quantidade: Quantidade do produto
- preco_unitario: Preço unitário no momento da compra
- subtotal: Preço total do item (quantidade * preço_unitário)

## Tabela: Usuarios
- id: Identificador único do usuário
- nome: Nome do usuário
- email: Email do usuário (usado para login)
- senha: Senha criptografada
- tipo: Tipo de usuário (admin, funcionário)
- data_cadastro: Data de cadastro do usuário
