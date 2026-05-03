"""
Script para gerar PDFs de amostra com conteúdo educacional sobre investimentos.
Rode uma vez para criar os PDFs em agents/rag_agent/pdfs/.
Dependência: pip install fpdf2
"""

import os
from fpdf import FPDF

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "pdfs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_pdf(filename: str, title: str, sections: list[tuple[str, str]]):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(8)

    for heading, body in sections:
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, heading, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, body.strip())
        pdf.ln(6)

    path = os.path.join(OUTPUT_DIR, filename)
    pdf.output(path)
    print(f"  Criado: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# PDF 1: Renda Fixa
# ─────────────────────────────────────────────────────────────────────────────
RENDA_FIXA = [
    ("O que e Renda Fixa", """
Renda fixa e uma categoria de investimentos em que as regras de remuneracao sao definidas
no momento da aplicacao. O investidor sabe, no ato da compra, qual sera a forma de
remuneracao do titulo: prefixada (taxa fixa), pos-fixada (atrelada a um indicador como
CDI ou Selic) ou hibrida (parte fixa + indicador de inflacao como IPCA).

Diferente da renda variavel, onde o retorno e incerto, na renda fixa o investidor empresta
dinheiro a um emissor (governo, banco ou empresa) e recebe juros por isso. E o investimento
mais indicado para quem esta comecando, para reserva de emergencia e para objetivos de
curto e medio prazo.
"""),
    ("Tesouro Direto", """
O Tesouro Direto e um programa do Governo Federal criado em 2002 para democratizar o acesso
a titulos publicos. E considerado o investimento mais seguro do Brasil, pois e garantido
pelo Tesouro Nacional.

Tipos de titulos disponiveis:

1. Tesouro Selic (LFT): pos-fixado, acompanha a taxa Selic. Ideal para reserva de emergencia
   por ter liquidez diaria e baixa volatilidade. Rendimento aproximado: 100% da Selic.

2. Tesouro IPCA+ (NTN-B Principal): hibrido, paga IPCA + uma taxa fixa (ex: IPCA + 6% a.a.).
   Protege contra inflacao. Indicado para aposentadoria e objetivos de longo prazo.
   Atencao: tem marcacao a mercado e pode ter rentabilidade negativa se vendido antes do
   vencimento em cenario de alta de juros.

3. Tesouro Prefixado (LTN): taxa definida na compra (ex: 12% a.a.). Bom quando se espera
   queda futura de juros. Risco: se os juros subirem, o titulo perde valor de mercado.

4. Tesouro RendA+: lancado em 2023, voltado para aposentadoria complementar. Paga renda
   mensal por 20 anos apos o vencimento.

Investimento minimo: aproximadamente R$30. Liquidez: D+1 para Tesouro Selic, marcacao a
mercado para os demais. Custos: taxa de custodia da B3 de 0,20% a.a. (isento ate R$10 mil
para Tesouro Selic).
"""),
    ("CDB - Certificado de Deposito Bancario", """
CDB e um titulo emitido por bancos para captar recursos. Ao investir em um CDB, voce esta
emprestando dinheiro ao banco, que devolve com juros.

Tipos de remuneracao:
- Pos-fixado: rende um percentual do CDI (ex: 110% do CDI)
- Prefixado: taxa fixa definida na compra (ex: 13% a.a.)
- Hibrido: IPCA + spread (ex: IPCA + 7%)

Cobertura do FGC: sim, ate R$250 mil por CPF por instituicao (limite global de R$1 milhao
a cada 4 anos). Isso significa que, mesmo se o banco quebrar, voce recebe ate esse limite.

Tributacao: Imposto de Renda regressivo sobre o rendimento:
- Ate 180 dias: 22,5%
- De 181 a 360 dias: 20%
- De 361 a 720 dias: 17,5%
- Acima de 720 dias: 15%

Dica: bancos menores geralmente pagam taxas maiores para atrair investidores, compensando
o maior risco de credito (mitigado pelo FGC).
"""),
    ("LCI e LCA - Letras de Credito", """
LCI (Letra de Credito Imobiliario) e LCA (Letra de Credito do Agronegocio) sao titulos
emitidos por bancos para financiar os setores imobiliario e do agronegocio, respectivamente.

Principal vantagem: ISENCAO de Imposto de Renda para pessoa fisica. Isso faz com que um
LCI/LCA que paga 85% do CDI possa render mais que um CDB de 100% do CDI apos IR.

Comparacao pratica (considerando CDI a 13,75% a.a.):
- CDB 100% CDI: rendimento liquido apos IR (15%) = 11,69% a.a.
- LCI 85% CDI: rendimento liquido (isento) = 11,69% a.a.
- Ou seja: LCI 85% CDI equivale a CDB 100% CDI para investimentos acima de 720 dias.

Cobertura do FGC: sim, mesmas regras do CDB.
Carencia minima: geralmente 90 dias (nao tem liquidez diaria).
Investimento minimo: varia, geralmente a partir de R$1.000 a R$5.000.
"""),
    ("Debentures", """
Debentures sao titulos de divida emitidos por empresas (sociedades anonimas) para financiar
projetos, expansoes ou reestruturar dividas. O investidor empresta dinheiro a empresa e
recebe juros.

Tipos:
- Debentures comuns: tributadas normalmente (tabela regressiva de IR)
- Debentures incentivadas (Lei 12.431): isentas de IR para pessoa fisica. Financiam
  projetos de infraestrutura (rodovias, energia, saneamento).

Riscos:
- Credito: a empresa pode nao pagar (default). Nao tem cobertura do FGC.
- Liquidez: mercado secundario menos liquido que titulos publicos
- Mercado: variacao de preco conforme juros e risco do emissor

Rating de credito: agencias como S&P, Moody's e Fitch avaliam o risco. AAA e o melhor;
abaixo de BBB e considerado grau especulativo.

Rentabilidade tipica: CDI + spread (ex: CDI + 2% a.a.) ou IPCA + spread.
"""),
    ("CRI e CRA", """
CRI (Certificado de Recebiveis Imobiliarios) e CRA (Certificado de Recebiveis do
Agronegocio) sao titulos de renda fixa emitidos por securitizadoras, lastreados em
recebiveis dos setores imobiliario e do agronegocio.

Vantagens:
- Isentos de IR para pessoa fisica
- Geralmente pagam taxas superiores a LCI/LCA
- Diversificacao de risco de credito

Desvantagens:
- NAO tem cobertura do FGC
- Menor liquidez
- Risco de credito do lastro (inadimplencia dos recebiveis)
- Investimento minimo mais alto

Indicado para: investidores com mais experiencia que buscam rentabilidade superior em
renda fixa e aceitam menor liquidez e maior risco de credito.
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# PDF 2: Renda Variavel
# ─────────────────────────────────────────────────────────────────────────────
RENDA_VARIAVEL = [
    ("O que e Renda Variavel", """
Renda variavel e a classe de investimentos cujo retorno nao pode ser determinado no
momento da aplicacao. O preco dos ativos flutua conforme oferta e demanda, resultados
das empresas, cenario macroeconomico e expectativas do mercado.

Historicamente, a renda variavel oferece retornos superiores a renda fixa no longo prazo,
mas com maior volatilidade. O Ibovespa, principal indice da bolsa brasileira, teve
retorno medio de aproximadamente 13% a.a. nos ultimos 20 anos (nominal), mas com anos
de -40% e anos de +80%.

Regra pratica: so invista em renda variavel dinheiro que voce nao vai precisar nos
proximos 5 anos, no minimo.
"""),
    ("Acoes - Conceitos Basicos", """
Acoes sao fracoes do capital social de uma empresa. Ao comprar uma acao, voce se torna
socio daquela empresa, com direito a parte dos lucros e participacao nas decisoes (em
assembleias).

Tipos de acoes:
- ON (Ordinarias - sufixo 3): dao direito a voto em assembleias. Ex: PETR3, VALE3
- PN (Preferenciais - sufixo 4): preferencia no recebimento de dividendos. Ex: PETR4, ITUB4
- Units (sufixo 11): pacotes combinando ON e PN. Ex: TAEE11, SANB11

Formas de ganhar com acoes:
1. Valorizacao: comprar barato e vender mais caro
2. Dividendos: parte do lucro distribuida aos acionistas (isento de IR)
3. JCP (Juros sobre Capital Proprio): similar a dividendos, mas com IR de 15%

Custos operacionais:
- Corretagem: muitas corretoras zeraram para acoes
- Emolumentos B3: ~0,03% por operacao
- IR: 15% sobre lucro em operacoes normais (swing trade), 20% em day trade
- Isencao: vendas ate R$20 mil/mes sao isentas de IR (swing trade)
"""),
    ("Como funciona a Bolsa de Valores (B3)", """
A B3 (Brasil, Bolsa, Balcao) e a unica bolsa de valores do Brasil e uma das maiores do
mundo em valor de mercado. Ela funciona como um ambiente organizado para negociacao de
ativos financeiros.

Horario de funcionamento (horario de Brasilia):
- Pre-abertura: 9:45 - 10:00
- Pregao regular: 10:00 - 17:55
- Call de fechamento: 17:55 - 18:00
- After market: 18:30 - 18:45

Indices principais:
- Ibovespa (IBOV): indice das acoes mais negociadas, referencia do mercado brasileiro
- IBrX-100: 100 acoes mais negociadas
- IFIX: indice de fundos imobiliarios
- SMLL: indice de small caps

Para investir: abra conta em uma corretora, transfira recursos, e envie ordens de compra
pelo home broker ou aplicativo. A liquidacao ocorre em D+2 (dois dias uteis apos a compra).
"""),
    ("Dividendos e Proventos", """
Dividendos sao a parcela do lucro liquido de uma empresa distribuida aos acionistas.
No Brasil, empresas listadas sao obrigadas a distribuir no minimo 25% do lucro liquido
(conforme estatuto).

Tipos de proventos:
1. Dividendos: distribuicao de lucro, isenta de IR para o acionista
2. JCP (Juros sobre Capital Proprio): tributado em 15% na fonte
3. Bonificacao: distribuicao de novas acoes proporcionais
4. Desdobramento (split): divide acoes sem alterar valor total
5. Grupamento (inplit): agrupa acoes

Indicador-chave - Dividend Yield (DY):
DY = (Dividendos pagos nos ultimos 12 meses / Preco atual da acao) x 100

Exemplo: acao a R$50 que pagou R$4 em dividendos = DY de 8%

Empresas boas pagadoras de dividendos no Brasil: utilities (energia, saneamento),
bancos, telecomunicacoes. Caracteristicas: negocios maduros, previdencia de receita,
baixa necessidade de reinvestimento.

Data-com e data-ex: para receber dividendos, voce precisa ter a acao ate a data-com.
Na data-ex, a acao ja negocia sem direito ao provento anunciado.
"""),
    ("BDRs - Brazilian Depositary Receipts", """
BDRs sao certificados que representam acoes de empresas estrangeiras, negociados na B3.
Permitem investir em empresas como Apple, Google, Amazon, Tesla sem precisar abrir conta
no exterior.

Como funcionam: uma instituicao depositaria compra as acoes no exterior e emite
certificados correspondentes no Brasil. O BDR acompanha o preco da acao original +
variacao cambial (dolar).

Tipos:
- BDR Nao Patrocinado (maioria): emitido por instituicao sem participacao da empresa
- BDR Patrocinado Nivel I, II e III: com participacao da empresa emissora

Custos e tributacao:
- Negociados como acoes na B3
- IR: 15% sobre ganho de capital (sem isencao de R$20 mil/mes)
- Dividendos: tributados conforme regras do pais de origem

Exemplos populares: AAPL34 (Apple), GOGL34 (Google), AMZO34 (Amazon), TSLA34 (Tesla),
MSFT34 (Microsoft), NVDC34 (NVIDIA).
"""),
    ("IPO e Follow-on", """
IPO (Initial Public Offering) e a oferta publica inicial de acoes - quando uma empresa
abre capital e passa a ser negociada em bolsa pela primeira vez.

Etapas de um IPO:
1. Preparacao: auditoria, governanca, contratacao de bancos coordenadores
2. Registro na CVM: documentacao e prospecto
3. Roadshow: apresentacao a investidores institucionais
4. Bookbuilding: definicao do preco por demanda
5. Inicio de negociacao na B3

Follow-on: oferta subsequente de acoes por empresa ja listada (primaria: novas acoes;
secundaria: acoes de acionistas existentes).

Riscos do IPO para o investidor:
- Assimetria de informacao (empresa conhece mais sobre si mesma)
- Lock-up period: restricao de venda para insiders (90-180 dias)
- Possivel precificacao otimista
- Liquidez incerta nos primeiros dias

Dica: historicamente, a media dos IPOs no Brasil nao supera o Ibovespa nos primeiros
12 meses. Avalie com cuidado.
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# PDF 3: Fundos Imobiliarios
# ─────────────────────────────────────────────────────────────────────────────
FIIS = [
    ("O que sao Fundos Imobiliarios (FIIs)", """
Fundos de Investimento Imobiliario (FIIs) sao fundos que investem em ativos do setor
imobiliario e sao negociados em bolsa como acoes. Cada cota representa uma fracao do
patrimonio do fundo.

Regulamentacao: instrucao CVM 472/2008. Devem distribuir no minimo 95% dos rendimentos
semestrais aos cotistas.

Vantagens:
- Renda passiva mensal (a maioria distribui mensalmente)
- Isencao de IR sobre rendimentos para pessoa fisica (condicoes abaixo)
- Diversificacao imobiliaria com pouco capital (cotas a partir de ~R$10)
- Liquidez superior a imoveis fisicos
- Gestao profissional

Condicoes para isencao de IR nos rendimentos:
1. O fundo deve ter no minimo 50 cotistas
2. As cotas devem ser negociadas exclusivamente em bolsa
3. O investidor nao pode deter mais de 10% das cotas do fundo

Atencao: ganho de capital na venda de cotas e tributado em 20% (sem isencao).
"""),
    ("Tipos de FIIs", """
1. FIIs de Tijolo: investem em imoveis fisicos
   - Lajes corporativas: escritorios comerciais. Ex: HGRE11, BRCR11
   - Shoppings: centros comerciais. Ex: XPML11, VISC11
   - Logistica/Industrial: galpoes e centros de distribuicao. Ex: HGLG11, XPLG11
   - Hospitais/Educacionais: Ex: NSLU11
   - Agencias bancarias: Ex: BBPO11
   - Hibridos: multiplos segmentos

2. FIIs de Papel: investem em titulos imobiliarios
   - CRIs (Certificados de Recebiveis Imobiliarios)
   - LCIs (Letras de Credito Imobiliario)
   - Outros titulos de renda fixa imobiliaria
   - Ex: KNCR11, KNIP11, MXRF11

3. FIIs de Fundos (FOFs): investem em cotas de outros FIIs
   - Diversificacao automatica
   - Gestao ativa de carteira de FIIs
   - Ex: BCFF11, KFOF11

4. FIIs de Desenvolvimento: investem em construcao de imoveis
   - Maior risco (obra, venda)
   - Potencial de retorno superior
"""),
    ("Indicadores para Analise de FIIs", """
1. Dividend Yield (DY): rendimento distribuido / preco da cota
   - DY mensal tipico: 0,6% a 1,0%
   - DY anual tipico: 8% a 12%
   - Cuidado: DY muito alto pode indicar risco elevado

2. P/VP (Preco sobre Valor Patrimonial):
   - P/VP = 1,0: cota negociada pelo valor patrimonial
   - P/VP < 1,0: cota com desconto (pode ser oportunidade ou problema)
   - P/VP > 1,0: cota com premio (mercado vê valor adicional)

3. Vacancia:
   - Vacancia fisica: % de area vaga
   - Vacancia financeira: % de receita nao realizada
   - Quanto menor, melhor (indica imoveis ocupados)

4. Cap Rate (Taxa de Capitalizacao):
   - NOI (receita liquida operacional) / Valor do imovel
   - Mede a rentabilidade do imovel em si

5. ABL (Area Bruta Locavel): tamanho total disponivel para locacao
   - Quanto maior e mais diversificada, menor o risco de concentracao

6. Liquidez: volume medio diario de negociacao
   - Fundos com mais de R$1 milhao/dia sao considerados liquidos
"""),
    ("Riscos dos FIIs", """
1. Risco de vacancia: imoveis desocupados reduzem rendimentos
   - Mitigacao: fundos com multiplos imoveis e inquilinos

2. Risco de inadimplencia: inquilinos nao pagam aluguel
   - Mitigacao: contratos com garantias, inquilinos de qualidade

3. Risco de mercado: cotas podem se desvalorizar
   - FIIs sao negociados em bolsa e sofrem volatilidade
   - Em ciclos de alta de juros, FIIs tendem a cair

4. Risco de credito (FIIs de papel): default dos CRIs
   - Mitigacao: diversificacao de devedores e LTV adequado

5. Risco de concentracao: poucos imoveis ou inquilinos
   - Prefira fundos com multiplos ativos e contratos

6. Risco de gestao: decisoes ruins do gestor
   - Avalie track record e alinhamento de interesses

7. Risco regulatorio: mudancas na legislacao tributaria
   - Ja houve tentativas de tributar rendimentos de FIIs

Dica: em cenarios de Selic alta, FIIs de papel (CDI+) tendem a performar melhor;
em cenarios de Selic baixa, FIIs de tijolo se beneficiam da valorizacao dos imoveis.
"""),
    ("Como montar uma carteira de FIIs", """
Estrategia de diversificacao por segmento:
- 30-40% em logistica/industrial (contratos longos, demanda crescente)
- 20-30% em papel/CRIs (renda atrelada a CDI ou IPCA)
- 15-25% em lajes corporativas ou shoppings (ciclo economico)
- 10-15% em FOFs (diversificacao adicional)

Criterios de selecao:
1. Liquidez minima: R$500 mil/dia de volume medio
2. Numero de cotistas: acima de 500 (garante isencao de IR)
3. Vacancia: abaixo da media do segmento
4. P/VP: preferencialmente entre 0,9 e 1,1
5. Historico de distribuicao: consistencia nos ultimos 12 meses
6. Qualidade dos imoveis: localizacao, idade, estado de conservacao
7. Contratos: prazo medio, tipo (tipico vs atipico), reajuste

Reinvestimento: usar os rendimentos mensais para comprar mais cotas gera efeito
de juros compostos ao longo do tempo (estrategia de bola de neve).
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# PDF 4: ETFs
# ─────────────────────────────────────────────────────────────────────────────
ETFS = [
    ("O que sao ETFs", """
ETFs (Exchange Traded Funds) sao fundos de investimento que replicam a composicao e
rentabilidade de um indice de referencia (benchmark). Sao negociados em bolsa como acoes.

Funcionamento: o gestor do ETF compra todos os ativos do indice na mesma proporcao,
permitindo que o investidor, com uma unica compra, tenha exposicao a dezenas ou centenas
de ativos.

Vantagens:
- Diversificacao instantanea com um unico ativo
- Taxas de administracao muito baixas (0,20% a 0,60% a.a.)
- Transparencia: composicao do indice e publica
- Liquidez: negociados em bolsa no horario normal
- Acessibilidade: cotas a partir de poucos reais

Desvantagens:
- Nao ha isencao de IR para vendas ate R$20 mil/mes (como ha para acoes)
- Dividendos sao reinvestidos automaticamente (nao voce recebe em conta)
- Tracking error: pequena diferenca entre ETF e indice
- Menos controle sobre composicao individual
"""),
    ("Principais ETFs no Brasil", """
ETFs de Renda Variavel Brasil:
- BOVA11: replica o Ibovespa (~90 acoes). Taxa: 0,10%. Mais liquido do mercado.
- BOVV11: tambem replica Ibovespa. Taxa: 0,10%. Alternativa ao BOVA11.
- SMAL11: replica o indice Small Cap (empresas menores). Taxa: 0,50%.
- DIVO11: replica o IDIV (acoes boas pagadoras de dividendos). Taxa: 0,50%.
- FIND11: replica indice financeiro. Taxa: 0,50%.

ETFs Internacionais (negociados na B3):
- IVVB11: replica S&P 500 (500 maiores empresas dos EUA). Taxa: 0,23%.
- NASD11: replica Nasdaq-100 (tecnologia). Taxa: 0,30%.
- EURP11: replica indice europeu. Taxa: 0,30%.
- XINA11: replica indice chines. Taxa: 0,30%.
- ACWI11: replica indice global (mercados desenvolvidos + emergentes). Taxa: 0,30%.

ETFs de Renda Fixa:
- IMAB11: replica IMA-B (titulos IPCA+). Taxa: 0,25%.
- IRFM11: replica IRF-M (titulos prefixados). Taxa: 0,20%.
- B5P211: replica IMA-B 5+ (IPCA+ com vencimento acima de 5 anos). Taxa: 0,20%.

ETFs de Criptoativos:
- HASH11: replica indice de criptomoedas (Bitcoin, Ethereum, etc.). Taxa: 0,30%.
- BITH11: 100% Bitcoin. Taxa: 0,70%.
- ETHE11: 100% Ethereum. Taxa: 0,70%.
"""),
    ("ETFs vs Fundos de Investimento", """
Comparacao detalhada:

Taxas:
- ETF: 0,10% a 0,60% a.a. (muito baixas)
- Fundo ativo: 1,0% a 3,0% a.a. + taxa de performance

Gestao:
- ETF: passiva (replica indice, sem decisoes do gestor)
- Fundo: ativa (gestor tenta superar o benchmark)

Tributacao:
- ETF de renda variavel: 15% sobre ganho na venda (sem come-cotas)
- Fundo de acoes: 15% sobre ganho no resgate (sem come-cotas)
- ETF de renda fixa: tabela regressiva de IR (sem come-cotas a partir de 2024)
- Fundo de renda fixa: tabela regressiva + come-cotas semestral

Liquidez:
- ETF: venda em bolsa a qualquer momento, liquidacao em D+2
- Fundo: resgate conforme regulamento (D+0 a D+30 ou mais)

Performance historica: estudos mostram que, no longo prazo, a maioria dos fundos ativos
nao supera seus benchmarks apos taxas. ETFs garantem o retorno do indice menos taxas.

Quando escolher ETF: investidor de longo prazo, custos baixos, simplicidade.
Quando escolher fundo ativo: quando ha um gestor com track record comprovado e
estrategia diferenciada.
"""),
    ("Estrategias com ETFs", """
1. Buy and Hold passivo:
   - Comprar ETFs diversificados e manter por anos
   - Exemplo: 60% BOVA11 + 30% IVVB11 + 10% IMAB11
   - Rebalancear anualmente

2. Dollar Cost Averaging (DCA):
   - Investir valor fixo todo mes, independente do preco
   - Reduz impacto da volatilidade e timing de mercado
   - Ideal para quem recebe salario mensal

3. Core-Satellite:
   - Core (70-80%): ETFs de indice amplo para a base da carteira
   - Satellite (20-30%): ETFs tematicos ou acoes individuais para potencial extra

4. Asset Allocation por perfil:
   - Conservador: 70% IMAB11 + 20% BOVA11 + 10% IVVB11
   - Moderado: 40% IMAB11 + 35% BOVA11 + 25% IVVB11
   - Arrojado: 15% IMAB11 + 45% BOVA11 + 30% IVVB11 + 10% SMAL11

5. Exposicao internacional:
   - IVVB11 + NASD11 + EURP11 + XINA11 para diversificacao global
   - Protecao cambial natural (ativos em dolar)
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# PDF 5: Fundos de Investimento
# ─────────────────────────────────────────────────────────────────────────────
FUNDOS = [
    ("O que sao Fundos de Investimento", """
Fundos de investimento sao veiculos coletivos de aplicacao financeira. Diversos investidores
(cotistas) juntam seus recursos, que sao geridos por um profissional (gestor) conforme uma
estrategia definida no regulamento do fundo.

Estrutura de um fundo:
- Gestor: toma as decisoes de investimento
- Administrador: responsavel legal e operacional
- Custodiante: guarda os ativos
- Distribuidor: vende as cotas (corretoras, bancos)
- Auditor: verifica as demonstracoes financeiras

Custos:
- Taxa de administracao: cobrada anualmente sobre o patrimonio (ex: 2% a.a.)
- Taxa de performance: cobrada sobre rendimento que excede o benchmark (ex: 20% do que
  exceder o CDI). Cobranca por linha d'agua.
- Come-cotas: antecipacao semestral de IR (maio e novembro) para fundos de renda fixa
  e multimercado. Aliquota de 15% (longo prazo) ou 20% (curto prazo).
"""),
    ("Classificacao ANBIMA de Fundos", """
A ANBIMA classifica os fundos por nivel de risco e estrategia:

1. Renda Fixa:
   - Simples: investe em titulos publicos e operacoes compromissadas
   - Indexados: acompanha um indice (CDI, IPCA)
   - Credito privado: investe em debentures, CRIs, CRAs (maior risco e retorno)

2. Multimercado:
   - Macro: aposta em cenarios macroeconomicos (juros, cambio, bolsa)
   - Long & Short: comprado e vendido em acoes simultaneamente
   - Quantitativo: usa algoritmos e modelos matematicos
   - Livre: sem restricao de estrategia

3. Acoes:
   - Indexados: replica indices (similar a ETFs mas com resgate, nao bolsa)
   - Ativos: gestor busca superar benchmark
   - Especificos: setoriais, small caps, dividendos

4. Cambial:
   - Investe em ativos atrelados a moedas estrangeiras
   - Hedge cambial ou especulacao

Resolucao CVM 175 (2023): nova regulamentacao que modernizou a industria de fundos,
permitindo classes de cotas, responsabilidade limitada e mais transparencia.
"""),
    ("Como avaliar um Fundo de Investimento", """
Indicadores quantitativos:

1. Rentabilidade: retorno historico (12 meses, 24 meses, desde inicio)
   - Compare SEMPRE com o benchmark (CDI, Ibovespa, etc.)
   - Retorno passado nao garante retorno futuro

2. Volatilidade: desvio padrao dos retornos
   - Mede o risco/oscilacao do fundo
   - Fundos de renda fixa: volatilidade baixa (0,1-2% a.a.)
   - Multimercados: volatilidade media (3-10% a.a.)
   - Fundos de acoes: volatilidade alta (15-30% a.a.)

3. Sharpe Ratio: (retorno do fundo - CDI) / volatilidade
   - Mede retorno ajustado ao risco
   - Quanto maior, melhor (acima de 0,5 e bom; acima de 1,0 e excelente)

4. Drawdown maximo: maior queda do pico ao vale
   - Mostra o pior cenario historico

5. Patrimonio liquido: tamanho do fundo
   - Muito pequeno (<R$50M): risco de fechamento
   - Muito grande (>R$10B): pode ter dificuldade de gerar alfa

Indicadores qualitativos:
- Track record do gestor (minimo 3-5 anos)
- Consistencia de estrategia
- Alinhamento de interesses (gestor investe no proprio fundo?)
- Transparencia na comunicacao com cotistas
"""),
    ("Tributacao de Fundos", """
Fundos de Renda Fixa e Multimercado:
- Come-cotas: antecipacao semestral (maio/novembro)
  - Longo prazo (prazo medio > 365 dias): 15%
  - Curto prazo (prazo medio <= 365 dias): 20%
- No resgate: complemento ate a aliquota final (tabela regressiva)
  - Ate 180 dias: 22,5%
  - 181-360 dias: 20%
  - 361-720 dias: 17,5%
  - Acima de 720 dias: 15%

Fundos de Acoes:
- NAO tem come-cotas
- Aliquota fixa de 15% sobre ganho no resgate
- Independente do prazo de aplicacao

IOF: incide sobre resgates em menos de 30 dias (tabela regressiva de 96% a 0%)

Importante: o come-cotas reduz o efeito dos juros compostos ao longo do tempo,
pois antecipa o pagamento do imposto. ETFs nao tem come-cotas, sendo mais eficientes
tributariamente para o longo prazo.
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# PDF 6: Gestao de Carteira e Diversificacao
# ─────────────────────────────────────────────────────────────────────────────
GESTAO_CARTEIRA = [
    ("Teoria Moderna do Portfolio (Markowitz)", """
A Teoria Moderna do Portfolio, desenvolvida por Harry Markowitz em 1952 (Premio Nobel de
Economia em 1990), demonstra que e possivel construir carteiras que maximizam o retorno
esperado para um dado nivel de risco, ou minimizam o risco para um dado retorno esperado.

Conceitos fundamentais:
- Retorno esperado: media ponderada dos retornos esperados de cada ativo
- Risco (volatilidade): medido pelo desvio padrao dos retornos
- Correlacao: como os ativos se movem em relacao uns aos outros
  - Correlacao +1: movem juntos (nao diversifica)
  - Correlacao 0: independentes (boa diversificacao)
  - Correlacao -1: movem em direcoes opostas (diversificacao perfeita)

Fronteira eficiente: conjunto de carteiras otimas que oferecem o maior retorno possivel
para cada nivel de risco. Qualquer carteira abaixo da fronteira e subotima.

Na pratica, para o investidor brasileiro:
- Acoes brasileiras e americanas tem correlacao moderada (~0,5-0,7)
- Renda fixa e acoes tem correlacao baixa ou negativa
- Ouro e dolar servem como hedge em momentos de crise
"""),
    ("Alocacao de Ativos por Perfil", """
A alocacao de ativos e a decisao mais importante do investidor - estudos mostram que
ela explica mais de 90% da variacao de retorno de uma carteira no longo prazo.

Perfil Conservador (preservacao de capital):
- 70% Renda Fixa (Tesouro Selic, CDBs, LCIs/LCAs)
- 15% Renda Fixa de medio prazo (Tesouro IPCA+, debentures)
- 10% FIIs
- 5% Renda Variavel (ETFs diversificados)
- Retorno esperado: CDI + 0,5% a 1% a.a.

Perfil Moderado (crescimento com protecao):
- 40% Renda Fixa (Tesouro IPCA+, CDBs, debentures)
- 25% Renda Variavel Brasil (acoes/ETFs)
- 15% FIIs
- 15% Renda Variavel Internacional (IVVB11, BDRs)
- 5% Alternativos (cripto, ouro)
- Retorno esperado: CDI + 2% a 4% a.a.

Perfil Arrojado (crescimento agressivo):
- 20% Renda Fixa (Tesouro IPCA+ longo, debentures incentivadas)
- 35% Renda Variavel Brasil (acoes, small caps)
- 10% FIIs
- 25% Renda Variavel Internacional
- 10% Alternativos (cripto, ouro, private equity)
- Retorno esperado: CDI + 5% a 8% a.a. (com maior volatilidade)
"""),
    ("Rebalanceamento de Carteira", """
Rebalanceamento e o processo de reajustar a carteira para manter a alocacao-alvo definida.
Com o tempo, ativos que valorizam mais passam a representar uma fatia maior, alterando o
perfil de risco da carteira.

Exemplo pratico:
- Alocacao-alvo: 60% RF + 40% RV
- Apos valorizacao da bolsa: 50% RF + 50% RV
- Rebalanceamento: vender parte de RV e comprar RF (ou aportar em RF)

Estrategias de rebalanceamento:

1. Por calendario: rebalancear em datas fixas (trimestral, semestral, anual)
   - Vantagem: simples, disciplinado
   - Desvantagem: pode rebalancear desnecessariamente

2. Por banda (threshold): rebalancear quando desvio excede um limite (ex: 5%)
   - Vantagem: mais eficiente, menos custos
   - Desvantagem: requer monitoramento constante

3. Por aporte: usar novos aportes para comprar o que esta abaixo da meta
   - Vantagem: sem custos de venda, sem gatilho de IR
   - Desvantagem: funciona melhor com aportes relevantes

Beneficio comprovado: rebalancear sistematicamente tende a melhorar o retorno ajustado
ao risco, pois voce vende caro e compra barato de forma mecanica.
"""),
    ("Financas Comportamentais", """
Financas comportamentais estuda os vieses psicologicos que afetam decisoes de investimento.
Conhece-los ajuda a evitar erros comuns:

1. Aversao a perda: sentimos a dor de perder 2x mais que o prazer de ganhar
   - Efeito: vender acoes vencedoras cedo e segurar perdedoras (efeito disposicao)
   - Solucao: definir stop loss e take profit antes de investir

2. Efeito manada (herd behavior): seguir a maioria sem analise propria
   - Efeito: comprar na euforia (topo) e vender no panico (fundo)
   - Solucao: ter uma estrategia definida e seguir independente do mercado

3. Vies de confirmacao: buscar informacoes que confirmam nossas crencas
   - Efeito: ignorar sinais negativos sobre investimentos que ja temos
   - Solucao: buscar ativamente opinioes contrarias

4. Ancoragem: fixar em um numero de referencia (preco de compra)
   - Efeito: nao vender porque "esta abaixo do que paguei"
   - Solucao: avaliar o ativo pelo valor presente, nao pelo preco de entrada

5. Excesso de confianca: acreditar que sabemos mais do que realmente sabemos
   - Efeito: concentrar carteira, operar demais (overtrading)
   - Solucao: diversificar e reduzir frequencia de operacoes

6. FOMO (Fear of Missing Out): medo de ficar de fora
   - Efeito: entrar em investimentos hypados sem analise
   - Solucao: lembrar que sempre havera novas oportunidades
"""),
    ("Investimento de Longo Prazo - Juros Compostos", """
Albert Einstein supostamente chamou os juros compostos de 'oitava maravilha do mundo'.
O efeito exponencial do reinvestimento e o maior aliado do investidor de longo prazo.

Simulacao pratica (aporte mensal de R$1.000):
- Em 10 anos a 10% a.a.: R$204.845 (R$120.000 investidos, R$84.845 de juros)
- Em 20 anos a 10% a.a.: R$759.369 (R$240.000 investidos, R$519.369 de juros)
- Em 30 anos a 10% a.a.: R$2.279.325 (R$360.000 investidos, R$1.919.325 de juros)

Observe: nos ultimos 10 anos, os juros geraram mais que nos primeiros 20 anos combinados.
Isso e o efeito exponencial em acao.

Regra dos 72: divida 72 pela taxa anual para saber em quantos anos o capital dobra.
- 72 / 10% = 7,2 anos para dobrar
- 72 / 12% = 6 anos para dobrar
- 72 / 6% = 12 anos para dobrar

Licoes praticas:
1. Comece o mais cedo possivel (tempo > valor do aporte)
2. Reinvista dividendos e rendimentos sempre
3. Nao interrompa os aportes em momentos de crise
4. O custo de esperar 5 anos para comecar pode ser centenas de milhares de reais
5. Consistencia supera timing de mercado
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# PDF 7: Analise Fundamentalista
# ─────────────────────────────────────────────────────────────────────────────
ANALISE_FUNDAMENTALISTA = [
    ("O que e Analise Fundamentalista", """
Analise fundamentalista e o metodo de avaliacao de ativos que examina os fundamentos
economicos e financeiros de uma empresa para determinar seu valor intrinseco. Se o preco
de mercado esta abaixo do valor intrinseco, a acao esta 'barata' (oportunidade de compra).

Pilares da analise:
1. Analise macroeconomica: PIB, inflacao, juros, cambio, politica fiscal
2. Analise setorial: dinamica do setor, concorrencia, barreiras de entrada
3. Analise da empresa: demonstracoes financeiras, governanca, vantagens competitivas

Demonstracoes financeiras essenciais:
- DRE (Demonstracao de Resultado): receita, custos, lucro
- Balanco Patrimonial: ativos, passivos, patrimonio liquido
- Fluxo de Caixa: geracao real de caixa da empresa
- DVA (Demonstracao de Valor Adicionado): como a riqueza e distribuida

Escolas de analise:
- Value Investing (Benjamin Graham, Warren Buffett): comprar empresas abaixo do valor
- Growth Investing: focar em empresas com alto crescimento de lucros
- Quality Investing: empresas com alta rentabilidade e vantagens competitivas
- GARP (Growth at Reasonable Price): crescimento a preco justo
"""),
    ("Indicadores de Valuation", """
1. P/L (Preco/Lucro):
   - Quantos anos de lucro atual pagam o preco da acao
   - P/L = Preco da acao / Lucro por acao (LPA)
   - Ibovespa historico: 10-15x. Abaixo de 10 pode ser barato; acima de 20 pode ser caro
   - Cuidado: P/L negativo (empresa com prejuizo) nao faz sentido

2. P/VP (Preco/Valor Patrimonial):
   - Relacao entre preco de mercado e valor contabil
   - P/VP = Preco da acao / Valor patrimonial por acao
   - Abaixo de 1: pode estar barata (ou com problemas)
   - Bancos: P/VP tipico entre 1,0 e 2,0

3. EV/EBITDA (Enterprise Value / EBITDA):
   - Valor da firma inteira / geração de caixa operacional
   - Mais completo que P/L pois inclui divida e exclui efeitos contabeis
   - Quanto menor, mais barata a empresa esta

4. Dividend Yield:
   - Dividendos pagos / Preco da acao
   - Acima de 6% a.a. e considerado bom no Brasil
   - Muito alto (>12%) pode indicar queda no preco por problemas

5. PSR (Price to Sales Ratio):
   - Preco / Receita Liquida por acao
   - Util para empresas sem lucro (startups, tech)
   - Quanto menor, mais barata
"""),
    ("Indicadores de Rentabilidade", """
1. ROE (Return on Equity - Retorno sobre Patrimonio):
   - ROE = Lucro Liquido / Patrimonio Liquido
   - Mede eficiencia da empresa em gerar retorno para o acionista
   - Acima de 15% e bom; acima de 20% e excelente
   - Cuidado: ROE muito alto com divida elevada pode ser artificialmente inflado

2. ROIC (Return on Invested Capital):
   - ROIC = NOPAT / Capital Investido
   - Mais robusto que ROE pois considera toda a estrutura de capital
   - Empresa boa: ROIC consistentemente acima do WACC (custo de capital)

3. Margem Liquida:
   - Margem = Lucro Liquido / Receita Liquida
   - Quanto sobra de lucro apos todos os custos
   - Varia muito por setor: tech (20-40%), varejo (2-5%), bancos (15-25%)

4. Margem EBITDA:
   - EBITDA / Receita Liquida
   - Mede eficiencia operacional antes de juros, impostos e depreciacao
   - Boa para comparar empresas do mesmo setor

5. CAGR (Taxa de Crescimento Anual Composta):
   - Taxa media de crescimento ao longo de um periodo
   - Usar para avaliar crescimento de receita e lucro
   - Empresa de crescimento: CAGR de lucro > 15% a.a.
"""),
    ("Indicadores de Endividamento e Saude Financeira", """
1. Divida Liquida / EBITDA:
   - Quantos anos de geracao de caixa operacional para pagar a divida
   - Abaixo de 2x: saudavel
   - 2x a 3x: atencao
   - Acima de 3x: risco elevado

2. Divida Liquida / Patrimonio Liquido:
   - Proporcao de divida em relacao ao capital proprio
   - Acima de 1,0: empresa mais alavancada (mais endividada que capitalizada)

3. Indice de Cobertura de Juros:
   - EBIT / Despesas Financeiras
   - Capacidade de pagar juros com o lucro operacional
   - Abaixo de 2x e preocupante

4. Liquidez Corrente:
   - Ativo Circulante / Passivo Circulante
   - Capacidade de pagar dividas de curto prazo
   - Ideal: acima de 1,5

5. Payout Ratio:
   - Dividendos pagos / Lucro Liquido
   - Porcentagem do lucro distribuida como dividendo
   - Acima de 80%: pode ser insustentavel (empresa nao reinveste)
   - Abaixo de 30%: empresa retendo lucro para crescer

Capital de Giro: ativo circulante - passivo circulante
   - Positivo: empresa tem folga financeira
   - Negativo: pode indicar problemas de liquidez (exceto varejo, que opera com CG negativo)
"""),
    ("Vantagens Competitivas (Moats)", """
Warren Buffett popularizou o conceito de 'moat' (fosso): vantagens competitivas duraiveis
que protegem a empresa da concorrencia, permitindo retornos acima da media por longos
periodos.

Tipos de moats:

1. Efeito de rede: produto fica mais valioso com mais usuarios
   - Exemplos: Visa/Mastercard, B3 (unica bolsa), redes sociais
   - Mais forte: quanto mais gente usa, mais dificil substituir

2. Custo de troca (switching costs): dificuldade/custo de mudar para concorrente
   - Exemplos: sistemas ERP (TOTVS), bancos (conta salario), software empresarial

3. Escala: custos fixos diluidos por volume impossibilitam concorrentes menores
   - Exemplos: Ambev (distribuicao), grandes bancos (custo de funding)

4. Marca e reputacao: permite cobrar premium ou ter preferencia do consumidor
   - Exemplos: Itau (confianca), WEG (qualidade), Natura (marca)

5. Patentes e regulacao: protecao legal contra concorrencia
   - Exemplos: farmaceuticas, concessoes de energia/rodovias

6. Localizacao: vantagem geografica dificil de replicar
   - Exemplos: shoppings em localizacoes premium, portos, mineradoras

Como identificar: empresa com moat tem ROE consistentemente alto (>15%) por muitos anos
e consegue repassar precos sem perder clientes.
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# PDF 8: Planejamento Financeiro
# ─────────────────────────────────────────────────────────────────────────────
PLANEJAMENTO = [
    ("Reserva de Emergencia", """
A reserva de emergencia e o primeiro passo de qualquer planejamento financeiro. E um
montante guardado para cobrir imprevistos sem precisar se endividar ou resgatar
investimentos de longo prazo em momento ruim.

Quanto guardar:
- CLT (empregado formal): 6 meses de gastos mensais
- PJ/Autonomo/Empreendedor: 12 meses de gastos mensais
- Aposentado: 12 meses de gastos mensais

Onde investir a reserva:
- Tesouro Selic: liquidez D+1, seguro, rende 100% da Selic
- CDB com liquidez diaria de banco grande: 100% CDI, FGC
- Fundo de renda fixa simples (DI): liquidez D+0

Onde NAO colocar a reserva:
- Poupanca (rende menos)
- CDB sem liquidez (carencia)
- Renda variavel (pode estar em baixa quando voce precisar)
- Tesouro IPCA+ ou Prefixado (volatilidade antes do vencimento)

Regra de ouro: a reserva nao e para render, e para estar DISPONIVEL. Priorize liquidez
e seguranca sobre rentabilidade.

Dica: mantenha a reserva em instituicao diferente da conta corrente do dia a dia para
evitar a tentacao de gastar.
"""),
    ("Organizacao do Orcamento", """
Metodos populares de orcamento:

1. Regra 50-30-20:
   - 50% para necessidades (moradia, alimentacao, transporte, saude)
   - 30% para desejos (lazer, compras, streaming, restaurantes)
   - 20% para prioridades financeiras (investimentos, dividas)

2. Metodo dos envelopes (adaptado ao digital):
   - Separar dinheiro em categorias no inicio do mes
   - Quando acabar o envelope, nao gasta mais naquela categoria
   - Apps como Organizze, Mobills ajudam na versao digital

3. Orcamento base zero:
   - Toda receita deve ter uma destinacao (ate o ultimo centavo)
   - Forca decisoes conscientes sobre cada gasto
   - Mais trabalhoso, mas mais eficaz

Dicas praticas:
- Automatize investimentos (debito automatico no dia do pagamento)
- Pague-se primeiro (investir antes de gastar)
- Revise gastos fixos anualmente (plano de celular, seguro, assinaturas)
- Evite parcelamento como habito (cria bola de neve)
- Distinga gastos necessarios de gastos emocionais
"""),
    ("Planejamento por Objetivos", """
Investimentos devem estar atrelados a objetivos concretos com prazo definido:

Curto prazo (ate 2 anos):
- Exemplos: viagem, troca de celular, curso
- Onde investir: Tesouro Selic, CDB liquidez diaria, LCI/LCA curta
- Prioridade: liquidez e seguranca

Medio prazo (2 a 5 anos):
- Exemplos: entrada de imovel, carro, intercambio, casamento
- Onde investir: Tesouro IPCA+ com vencimento proximo, CDB prefixado, LCI/LCA
- Prioridade: protecao contra inflacao + previsibilidade

Longo prazo (5+ anos):
- Exemplos: aposentadoria, independencia financeira, faculdade dos filhos
- Onde investir: acoes, ETFs, FIIs, Tesouro IPCA+ longo, fundos multimercado
- Prioridade: crescimento real (acima da inflacao)

Independencia financeira:
- Patrimonio necessario = gastos mensais x 12 / taxa de retirada segura (4%)
- Exemplo: gastos de R$10.000/mes -> patrimonio necessario: R$3.000.000
- Regra dos 4%: retirar ate 4% ao ano do patrimonio preserva o capital por 30+ anos
  (baseado no estudo Trinity, adaptado: no Brasil, 3,5% e mais conservador dado juros
  reais mais altos historicamente)
"""),
    ("Erros Comuns de Investidores Iniciantes", """
1. Nao ter reserva de emergencia antes de investir
   - Resultado: precisa resgatar no pior momento

2. Seguir dicas de influenciadores sem entender
   - Resultado: comprar ativos inadequados ao seu perfil

3. Olhar rentabilidade passada como garantia
   - "Rentabilidade passada nao e garantia de rentabilidade futura"
   - O fundo que rendeu 30% pode perder 20% no proximo ano

4. Nao considerar taxas e impostos
   - Fundo com 2% de taxa precisa render 2% a mais so para empatar

5. Concentrar demais em um unico ativo
   - "All in" em uma acao: risco de perda total
   - Diversificacao e gratuita e reduz risco

6. Operar demais (overtrading)
   - Mais operacoes = mais custos + mais IR + mais erros emocionais
   - Buy and hold tende a superar trading ativo para maioria das pessoas

7. Nao ter paciencia com juros compostos
   - Trocar de estrategia a cada 3 meses impede o efeito exponencial
   - Consistencia > otimizacao constante

8. Ignorar a inflacao
   - Rendimento nominal de 10% com inflacao de 5% = ganho real de ~5%
   - Poder de compra e o que importa, nao o numero na conta

9. Misturar dinheiro de curto e longo prazo
   - Usar reserva de emergencia para "aproveitar oportunidades"
   - Cada objetivo deve ter seu proprio veiculo

10. Nao reinvestir dividendos e rendimentos
    - Quebra o efeito de juros compostos
    - Automatize o reinvestimento sempre que possivel
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# PDF 9: Tributacao de Investimentos
# ─────────────────────────────────────────────────────────────────────────────
TRIBUTACAO = [
    ("Visao Geral da Tributacao de Investimentos no Brasil", """
A tributacao de investimentos no Brasil segue regras diferentes conforme a classe de ativo.
Compreender a tributacao e essencial para calcular o retorno liquido real e comparar
investimentos de forma justa.

Orgao responsavel: Receita Federal do Brasil (RFB)
Obrigacao: declarar todos os investimentos na DIRPF (Declaracao de Imposto de Renda)
Prazo: ate o ultimo dia util de abril (ref. ano anterior)

Tipos de tributacao:
1. Tabela regressiva: aliquota diminui com o tempo (renda fixa)
2. Aliquota fixa: mesma aliquota independente do prazo (acoes, FIIs)
3. Isencao: nao ha cobranca de imposto (LCI, LCA, rendimentos de FIIs, dividendos)

Responsabilidade de recolhimento:
- Retido na fonte: banco/corretora desconta automaticamente (CDB, fundos, JCP)
- DARF: investidor calcula e paga ate o ultimo dia util do mes seguinte (acoes, FIIs, cripto)

Compensacao de prejuizos: perdas em bolsa podem ser compensadas com ganhos futuros
na mesma categoria (acoes com acoes, FIIs com FIIs, day trade com day trade).
"""),
    ("Tributacao de Renda Fixa", """
Tabela regressiva de IR (aplicavel a CDB, Tesouro Direto, debentures comuns, fundos RF):

| Prazo de aplicacao     | Aliquota |
|------------------------|----------|
| Ate 180 dias           | 22,5%    |
| De 181 a 360 dias      | 20,0%    |
| De 361 a 720 dias      | 17,5%    |
| Acima de 720 dias      | 15,0%    |

IOF (Imposto sobre Operacoes Financeiras):
- Incide sobre resgates em menos de 30 dias
- Aliquota regressiva: 96% no dia 1, 0% no dia 30
- Apos 30 dias: nao ha IOF

Investimentos ISENTOS de IR para pessoa fisica:
- LCI e LCA (Letras de Credito Imobiliario e do Agronegocio)
- CRI e CRA (Certificados de Recebiveis)
- Debentures incentivadas (infraestrutura - Lei 12.431)
- Poupanca

Come-cotas (fundos de renda fixa e multimercado):
- Antecipacao semestral: ultimo dia util de maio e novembro
- Fundo curto prazo: 20% sobre rendimento acumulado
- Fundo longo prazo: 15% sobre rendimento acumulado
- No resgate: cobra-se a diferenca ate a aliquota final

Atencao: a base de calculo e sempre o RENDIMENTO, nunca o valor principal.
"""),
    ("Tributacao de Renda Variavel", """
Acoes (operacoes normais - swing trade):
- Aliquota: 15% sobre o ganho liquido
- Isencao: vendas totais ate R$20.000 no mes sao isentas de IR
- IRRF (dedo-duro): 0,005% sobre o valor da venda (serve como sinal para a Receita)
- DARF: investidor deve calcular e recolher ate o ultimo dia util do mes seguinte
- Codigo DARF: 6015

Acoes (day trade):
- Aliquota: 20% sobre o ganho liquido
- NAO ha isencao de R$20 mil
- IRRF: 1% sobre o lucro
- Codigo DARF: 6015
- Compensacao: prejuizo de day trade so compensa ganho de day trade

Fundos Imobiliarios (FIIs):
- Rendimentos mensais: ISENTOS para PF (condicoes: fundo com 50+ cotistas, negociado
  em bolsa, investidor com menos de 10% das cotas)
- Ganho de capital (venda de cotas): 20% sem isencao de R$20 mil
- DARF: investidor recolhe. Codigo: 6015
- Compensacao: prejuizo em FII so compensa ganho em FII

BDRs:
- Aliquota: 15% sobre ganho (swing), 20% (day trade)
- NAO ha isencao de R$20 mil/mes (diferente de acoes)
- Dividendos: tributados conforme pais de origem (retencao na fonte la fora)

ETFs de renda variavel:
- Aliquota: 15% sobre ganho de capital
- NAO ha isencao de R$20 mil/mes
"""),
    ("Tributacao de Criptoativos", """
A Receita Federal equipara criptoativos a ativos financeiros desde 2019 (IN RFB 1888/2019).

Tributacao sobre ganho de capital:
- Vendas ate R$35.000 no mes: ISENTAS de IR
- Vendas acima de R$35.000 no mes: aliquota progressiva:
  - Ate R$5 milhoes: 15%
  - De R$5M a R$10M: 17,5%
  - De R$10M a R$30M: 20%
  - Acima de R$30M: 22,5%

Obrigacoes acessorias:
- Exchanges nacionais: informam a Receita automaticamente (operacoes acima de R$30 mil/mes)
- Exchanges estrangeiras: investidor deve informar operacoes acima de R$30 mil/mes
  via declaracao mensal (programa disponivel no site da Receita)

Na declaracao anual (DIRPF):
- Declarar na ficha "Bens e Direitos" - grupo 08 (Criptoativos)
- Codigos: 01 (Bitcoin), 02 (altcoins), 03 (stablecoins), 10 (NFTs), 99 (outros)
- Informar quantidade e custo de aquisicao

Dica: manter planilha atualizada de todas as operacoes com data, quantidade, preco
de compra e venda. Apps como Koinly e CoinTracker ajudam a calcular automaticamente.
"""),
    ("Como Declarar Investimentos no IR", """
Na Declaracao Anual de Imposto de Renda (DIRPF), investimentos aparecem em varias fichas:

Ficha "Bens e Direitos":
- Grupo 01 - Bens imoveis
- Grupo 03 - Participacoes societarias (acoes)
- Grupo 04 - Aplicacoes e investimentos (RF, fundos, cripto)
- Grupo 07 - Fundos (FIIs, ETFs)
- Grupo 08 - Criptoativos
- Informar: CNPJ da instituicao, saldo em 31/12

Ficha "Rendimentos Isentos e Nao Tributaveis":
- Dividendos de acoes
- Rendimentos de FIIs (para PF)
- Rendimentos de LCI, LCA, CRI, CRA
- Ganhos de capital isentos (vendas de acoes ate R$20mil/mes)

Ficha "Rendimentos Sujeitos a Tributacao Exclusiva":
- Rendimentos de aplicacoes financeiras (CDB, Tesouro, fundos)
- JCP recebido
- Informar rendimento bruto e IR retido na fonte

Ficha "Renda Variavel":
- Operacoes em bolsa mes a mes
- Informar ganhos, perdas e IR pago (DARFs)
- Compensar prejuizos acumulados

Informe de Rendimentos: documento enviado pelas corretoras/bancos todo ano (ate fim
de fevereiro) com todos os dados necessarios para a declaracao.
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# PDF 10: Criptoativos e Ativos Digitais
# ─────────────────────────────────────────────────────────────────────────────
CRIPTO = [
    ("O que sao Criptoativos", """
Criptoativos sao ativos digitais que utilizam criptografia e tecnologia blockchain para
garantir seguranca, transparencia e descentralizacao. Diferente de moedas tradicionais,
nao dependem de um banco central ou governo para funcionar.

Blockchain: livro-razao distribuido onde todas as transacoes sao registradas de forma
imutavel e transparente. Cada bloco contem transacoes e e ligado ao anterior por um
hash criptografico.

Principais criptoativos por capitalizacao de mercado:
1. Bitcoin (BTC): primeira e maior criptomoeda. Criada em 2009 por Satoshi Nakamoto.
   Supply maximo: 21 milhoes de unidades. Considerado 'ouro digital'.
2. Ethereum (ETH): plataforma de contratos inteligentes (smart contracts). Base para
   DeFi, NFTs e milhares de tokens.
3. Stablecoins: atreladas a moedas fiat (USDT, USDC atrelados ao dolar; BRZ ao real).
   Usadas para trading e transferencias sem volatilidade.

Riscos especificos:
- Volatilidade extrema (quedas de 50-80% sao historicamente comuns)
- Risco regulatorio (paises podem restringir ou proibir)
- Risco de custodia (perda de chaves privadas = perda total)
- Golpes e fraudes (projetos falsos, rug pulls, esquemas ponzi)
- Risco tecnologico (bugs em smart contracts, hacks)
"""),
    ("Bitcoin - Reserva de Valor Digital", """
O Bitcoin foi criado em 2009 como resposta a crise financeira de 2008. Seu whitepaper
propoe um sistema de pagamento eletronico peer-to-peer sem intermediarios.

Caracteristicas fundamentais:
- Supply fixo: maximo de 21 milhoes de BTC (escasso como ouro)
- Halving: a cada ~4 anos, a emissao de novos BTC cai pela metade
  - 2012: 50 -> 25 BTC/bloco
  - 2016: 25 -> 12,5 BTC/bloco
  - 2020: 12,5 -> 6,25 BTC/bloco
  - 2024: 6,25 -> 3,125 BTC/bloco
- Mineracao: Proof of Work (PoW) - computadores resolvem problemas matematicos
- Descentralizacao: milhares de nos ao redor do mundo validam transacoes

Tese de investimento:
- 'Ouro digital': reserva de valor contra inflacao e desvalorizacao de moedas fiat
- Adocao institucional crescente (ETFs spot aprovados nos EUA em 2024)
- Escassez programada (supply fixo + demanda crescente)
- Hedge geopolitico (funciona sem governo)

Criticas e riscos:
- Consumo energetico elevado (PoW)
- Volatilidade alta para reserva de valor
- Sem fluxo de caixa (nao gera dividendos/juros)
- Risco regulatorio persistente
"""),
    ("DeFi - Financas Descentralizadas", """
DeFi (Decentralized Finance) e o ecossistema de servicos financeiros construidos em
blockchain, sem intermediarios tradicionais (bancos, corretoras). Funciona principalmente
na rede Ethereum e outras blockchains programaveis.

Principais aplicacoes:

1. Exchanges descentralizadas (DEXs):
   - Uniswap, Curve, PancakeSwap
   - Negociacao de tokens sem intermediario (AMM - Automated Market Maker)

2. Lending/Borrowing (emprestimos):
   - Aave, Compound
   - Depositar cripto como garantia e tomar emprestimo
   - Ou emprestar cripto e receber juros

3. Yield Farming / Liquidity Mining:
   - Fornecer liquidez a protocolos e receber recompensas
   - Retornos variam: 5% a 100%+ a.a. (maior retorno = maior risco)

4. Staking:
   - Travar tokens para ajudar a validar transacoes (Proof of Stake)
   - Ethereum staking: ~4-5% a.a. em ETH

Riscos do DeFi:
- Smart contract risk: bugs no codigo podem ser explorados
- Impermanent loss: perda ao fornecer liquidez se precos divergem
- Rug pulls: criadores do protocolo fogem com os fundos
- Risco de liquidacao: se garantia cai abaixo do minimo
- Complexidade: curva de aprendizado alta, erros custam caro
"""),
    ("Como investir em Cripto no Brasil", """
Formas de exposicao a criptoativos:

1. Exchanges centralizadas (CEXs):
   - Mercado Bitcoin, Foxbit, Binance, Coinbase
   - Vantagem: facilidade de uso, liquidez, suporte
   - Desvantagem: custodia centralizada (nao sao suas chaves)
   - KYC obrigatorio (verificacao de identidade)

2. ETFs de cripto na B3:
   - HASH11: indice de criptomoedas (mais diversificado)
   - BITH11: 100% Bitcoin
   - ETHE11: 100% Ethereum
   - Vantagem: comprar via corretora normal, sem se preocupar com custódia
   - Desvantagem: taxa de administracao, horario da bolsa

3. Fundos de criptoativos:
   - Hashdex, QR Asset, Vitreo oferecem fundos
   - Gestao profissional, diversificacao
   - Taxas: 0,5% a 2% a.a.

4. Self-custody (carteiras proprias):
   - Hardware wallets: Ledger, Trezor (mais seguro)
   - Software wallets: MetaMask, Trust Wallet
   - 'Not your keys, not your coins'
   - Responsabilidade total pela seguranca

Alocacao sugerida em carteira diversificada:
- Conservador: 0-2% do patrimonio em cripto
- Moderado: 2-5% do patrimonio
- Arrojado: 5-10% do patrimonio
- Nunca mais que voce pode perder totalmente
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# Geracao dos PDFs
# ─────────────────────────────────────────────────────────────────────────────
PDFS = [
    ("guia_renda_fixa.pdf", "Guia Completo de Renda Fixa", RENDA_FIXA),
    ("guia_renda_variavel.pdf", "Guia de Renda Variavel e Acoes", RENDA_VARIAVEL),
    ("guia_fiis.pdf", "Guia de Fundos Imobiliarios (FIIs)", FIIS),
    ("guia_etfs.pdf", "Guia de ETFs - Fundos de Indice", ETFS),
    ("guia_fundos_investimento.pdf", "Guia de Fundos de Investimento", FUNDOS),
    ("guia_gestao_carteira.pdf", "Gestao de Carteira e Diversificacao", GESTAO_CARTEIRA),
    ("guia_analise_fundamentalista.pdf", "Analise Fundamentalista de Acoes", ANALISE_FUNDAMENTALISTA),
    ("guia_planejamento_financeiro.pdf", "Planejamento Financeiro Pessoal", PLANEJAMENTO),
    ("guia_tributacao_investimentos.pdf", "Tributacao de Investimentos no Brasil", TRIBUTACAO),
    ("guia_criptoativos.pdf", "Criptoativos e Ativos Digitais", CRIPTO),
]


if __name__ == "__main__":
    print("Gerando PDFs de amostra...")
    for filename, title, sections in PDFS:
        create_pdf(filename, title, sections)
    print(f"\n{len(PDFS)} PDFs criados em {OUTPUT_DIR}/")
    print("Proximo passo: python agents/rag_agent/build_index.py")
