# Vibe Eletronics · Landing page

Página da Vibe Eletronics para clientes: tabela de preços de conserto com o estoque de peças ao vivo, pedido de conserto pelo WhatsApp da loja, produtos de loja, orçamento, lojas e dúvidas frequentes.

É um único arquivo (`index.html`), sem etapa de build. Pronta para GitHub Pages.

## Como atualizar

- **Lojas e telefones:** edite a lista `LOJAS` no fim do `index.html`. Os cartões e o formulário usam essa lista.
- **Categorias de produtos:** os 12 cartões da seção Produtos seguem as categorias do sistema das lojas (sem preços nem estoque). Edite direto no HTML.
- **Textos e perguntas frequentes:** direto no HTML.
- **Capa de compartilhamento (`img/og.jpg`):** gerada por `Media Kit/fontes/social.html#og-site`.

## Tabela de preços de conserto

- Os dados vêm de um app da web do Google Apps Script (`estoque-site.gs`, guardado fora deste repositório) que lê a planilha de estoque da Dashboard das Lojas: abas Frontal, Bateria e Conector de Carga.
- O script devolve só tipo, marca, modelo, cor, compatibilidade, preço e se tem a peça. A quantidade exata não sai da planilha.
- O link do script fica na constante `ESTOQUE_URL`, no fim do `index.html`.
- O preço da planilha já é o valor final do conserto (peça e mão de obra).
- Teste local com dados de exemplo: `http://localhost:8766/?estoque=.teste/estoque-exemplo.json` (a pasta `.teste` não vai para o Git).
