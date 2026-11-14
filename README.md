# Vibe Eletronics · Landing page

Página da Vibe Eletronics para clientes: busca de produtos com preço e carrinho que envia o pré-pedido pelo WhatsApp da loja, assistência técnica, orçamento, lojas e dúvidas frequentes.

Página `index.html` + catálogo `catalogo.json`, sem etapa de build. Pronta para GitHub Pages.

## Como atualizar

- **Lojas e telefones:** edite a lista `LOJAS` no fim do `index.html`. Os cartões e o formulário usam essa lista.
- **Categorias de produtos:** os 12 cartões da seção Produtos seguem as categorias do sistema das lojas (sem preços nem estoque). Edite direto no HTML.
- **Textos e perguntas frequentes:** direto no HTML.
- **Capa de compartilhamento (`img/og.jpg`):** gerada por `Media Kit/fontes/social.html#og-site`.

## Catálogo de produtos (busca e carrinho)

- `catalogo.json` é gerado a partir do catálogo do sistema das lojas:

  ```
  python ferramentas/exportar_catalogo.py
  ```

- Só saem código, nome, categoria e preço de venda. Custo, estoque, fornecedor e dados fiscais não entram.
- Ficam fora: peças de conserto, tabacaria, itens inativos, preços abaixo de R$ 1 e os nomes listados em `NOMES_FORA` no script.
- Mudou preço no ERP? Atualize o `catalogo-hiper.js`, rode o script e publique. O site mostra a data do catálogo.
- O carrinho fica salvo só no navegador do cliente. O pedido vai pelo WhatsApp da loja escolhida, que confirma disponibilidade e valor.
