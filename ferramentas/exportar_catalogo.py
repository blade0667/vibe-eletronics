"""Gera o catalogo.json público da landing page a partir do catálogo do sistema das lojas.

Uso (na pasta "Landing Page"):
    python ferramentas/exportar_catalogo.py

Lê:   ../Vibe SaaS - PDV & Fiscal/catalogo-hiper.js   (catálogo mestre dos PDVs)
Gera: catalogo.json                                    (só código, nome, categoria e preço de venda)

Custo, estoque, fornecedor e dados fiscais NUNCA saem daqui.
Alterações de preço feitas no ERP depois do catalogo-hiper.js (patches "subdiff" no Supabase)
não entram: atualize o catalogo-hiper.js e rode este script de novo.
"""
import datetime
import json
import pathlib
import re
import sys
import unicodedata

AQUI = pathlib.Path(__file__).resolve().parent.parent
FONTE = AQUI.parent / "Vibe SaaS - PDV & Fiscal" / "catalogo-hiper.js"
SAIDA = AQUI / "catalogo.json"

# Ordem e nomes iguais aos cartões da seção Produtos.
CATEGORIAS = [
    ("peliculas", "Películas"),
    ("capas_cases", "Capas & Cases"),
    ("audio_fones", "Áudio & Fones"),
    ("fontes_carregadores", "Fontes & Carregadores"),
    ("cabos_adaptadores", "Cabos & Adaptadores"),
    ("celulares_tablets", "Celulares & Tablets"),
    ("informatica_tv", "Informática & TV"),
    ("pilhas_baterias", "Pilhas & Baterias"),
    ("acessorios_geral", "Acessórios & Geral"),
    ("oculos_otica", "Óculos & Ótica"),
    ("games_brinquedos", "Games & Brinquedos"),
    ("praia_termicos", "Praia & Térmicos"),
]
# Fora do site: peças usadas no conserto e tabacaria.
CATEGORIAS_FORA = {"manutencao_pecas", "tabacaria_outros"}
PRECO_MINIMO = 1.00  # abaixo disso são cadastros provisórios (R$ 0,01)
# Itens que não são produto de prateleira, ou peças de conserto cadastradas em Acessórios.
NOMES_FORA = re.compile(
    r"^(produto padr[aã]o|conta google|celular usado"
    r"|placa de carga|camera traseira|conector de carga"
    r"|lente (iphone|moto|samsung|lg|xiaomi|redmi))\b"
    r"|regi[aã]o manguinhos",  # capas com preço diferente por bairro
    re.IGNORECASE,
)


def ler_catalogo() -> list[dict]:
    texto = FONTE.read_text(encoding="utf-8")
    achado = re.search(r"^window\.CATALOGO_HIPER_REAL = (.*?);\s*$", texto, re.M | re.S)
    if not achado:
        sys.exit(f"Não achei CATALOGO_HIPER_REAL em {FONTE}")
    return json.loads(achado.group(1))


def chave(nome: str) -> str:
    sem_acento = unicodedata.normalize("NFD", nome).encode("ascii", "ignore").decode()
    return " ".join(sem_acento.lower().split())


def main() -> None:
    indice = {slug: i for i, (slug, _) in enumerate(CATEGORIAS)}
    vistos: dict[str, list] = {}
    fora = {"inativo": 0, "categoria": 0, "preco": 0, "nome": 0, "repetido": 0}

    for p in ler_catalogo():
        nome = " ".join(str(p.get("nome", "")).split())
        slug = p.get("categoria_slug")
        preco = float(p.get("preco") or 0)
        if not p.get("ativo"):
            fora["inativo"] += 1; continue
        if slug in CATEGORIAS_FORA:
            fora["categoria"] += 1; continue
        if preco < PRECO_MINIMO:
            fora["preco"] += 1; continue
        if NOMES_FORA.search(nome):
            fora["nome"] += 1; continue
        if nome.lower().startswith("celular "):  # aparelhos cadastrados em outra categoria
            slug = "celulares_tablets"
        if slug not in indice:
            slug = "acessorios_geral"
        k = chave(nome)
        if k in vistos:  # mesmo nome cadastrado duas vezes: fica o de maior preço, para não prometer menos
            fora["repetido"] += 1
            if preco > vistos[k][3]:
                vistos[k] = [str(p["codigo"]), nome, indice[slug], round(preco, 2)]
            continue
        vistos[k] = [str(p["codigo"]), nome, indice[slug], round(preco, 2)]

    produtos = sorted(vistos.values(), key=lambda r: (r[2], chave(r[1])))
    data = datetime.date.fromtimestamp(FONTE.stat().st_mtime).isoformat()
    saida = {
        "atualizado": data,
        "categorias": [nome for _, nome in CATEGORIAS],
        "campos": ["codigo", "nome", "categoria", "preco"],
        "produtos": produtos,
    }
    SAIDA.write_text(json.dumps(saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    por_cat = [sum(1 for r in produtos if r[2] == i) for i in range(len(CATEGORIAS))]
    print(f"{len(produtos)} produtos no site (catálogo de {data}) -> {SAIDA.name}, {SAIDA.stat().st_size / 1024:.0f} KB")
    print("por categoria:", ", ".join(f"{n} {c}" for (_, n), c in zip(CATEGORIAS, por_cat)))
    print("fora do site:", fora)


if __name__ == "__main__":
    main()
