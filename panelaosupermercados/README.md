# Panelão Supermercados — Diretório de Ofertas

Site: https://panelaosupermercados.com.br
Página mapeada: https://panelaosupermercados.com.br/ofertas

## Resumo da pesquisa

- A seção de ofertas fica em `/ofertas` e exibe flyers com vigência ("Confira nossas ofertas em vigência").
- O diretório atual possui **6 itens** (flyers, um por cidade), com paginação de 1 página apenas
  (botão "Próxima Página" desabilitado).
- O `<meta name="sitemap" content="https://panelaosupermercados.com.br/sitemap.xml">` existe no HTML,
  mas o `/sitemap.xml` responde com uma página HTML de campanha (Ano Novo / Carro Novo) — sitemap não está funcional.

## Diretório de ofertas (flyers)

| Ordem | Cidade | Slug (cidade) | Flyer ID | URL do flyer | Páginas | Capa |
|---|---|---|---|---|---|---|
| 1 | Bauru | `bauru` | 649 | https://panelaosupermercados.com.br/site/conteudo/649-folheto-de-ofertas.html | 1–4 | /uploads/2266/oferta loja/BAURU (1).jpg |
| 2 | Agudos | `agudos` | 650 | https://panelaosupermercados.com.br/site/conteudo/650-folheto-de-ofertas.html | 1–4 | /uploads/2266/CAPAS OFERTAS/AGUDOS.jpg |
| 3 | Botucatu | `botucatu` | 651 | https://panelaosupermercados.com.br/site/conteudo/651-folheto-de-ofertas.html | 1–4 | /uploads/2266/CAPAS OFERTAS/BOTUCATU.jpg |
| 4 | Lençois Paulista | `lencois-paulista` | 652 | https://panelaosupermercados.com.br/site/conteudo/652-folheto-de-ofertas.html | 1–4 | /uploads/2266/CAPAS OFERTAS/LENCOIS.jpg |
| 5 | Jau | `jau` | 653 | https://panelaosupermercados.com.br/site/conteudo/653-folheto-de-ofertas.html | 1–4 | /uploads/2266/CAPAS OFERTAS/JAU.jpg |
| 6 | Duartina | `duartina` | 663 | https://panelaosupermercados.com.br/site/conteudo/663-folheto-de-ofertas.html | 1–4 | /uploads/2266/CAPAS OFERTAS_DUARTINA5 copy.jpg |

## Lojas (diretório relacionado)

A página `/lojas` lista unidades por cidade (agudos, bauru, botucatu, duartina, jau, lencois-paulista, sao-manuel).

## Estrutura de filtro por cidade

- Cookie: `lojaCidade`
- Slugs usados: `agudos`, `bauru`, `botucatu`, `duartina`, `jau`, `lencois-paulista`, `sao-manuel`

## Dados estruturados

- `data/ofertas.json` — dados completos dos flyers de ofertas.
