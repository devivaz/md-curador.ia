import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from leads_data import df_concatenado as df_leads
from gestao_trafego_data import df_concatenado as df_trafego
import utils

# Configurações da página
st.set_page_config(
    layout='wide',
    page_title="Gestão de tráfego CuradorI.A",
    page_icon=":bar_chart:",
    menu_items={
        "About": "Author: https://www.linkedin.com/in/lucaseso",
    })

# Importar CSS
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


# Sidebar

# logo
st.sidebar.image("./img/logo_lumere_branco.png", use_column_width=True)

st.sidebar.header("Aplicar filtros:")


# Declarar filtros
mes_ano_filter = st.sidebar.multiselect(
    "Mês", 
    options=df_leads['MesAno'].unique(),
    placeholder="Todos selecionados")

origem_filter = st.sidebar.multiselect(
    "Origem", 
    options=df_leads['origem'].dropna().unique(),
    placeholder="Todos selecionados")

estado_filter = st.sidebar.multiselect(
    "Estado",
    options=df_leads['Estado'].unique(),
    placeholder="Todos selecionados")

# Filtros dos totais
df_leads_selection = df_leads
df_trafego_selection = df_trafego

# Filtro condicional para MesAno
if mes_ano_filter:
    df_leads_selection = df_leads_selection[df_leads_selection['MesAno'].isin(mes_ano_filter)]
    df_trafego_selection = df_trafego_selection[df_trafego_selection['MesAno'].isin(mes_ano_filter)]

# Filtro condicional para origem
if origem_filter:
    df_leads_selection = df_leads_selection[df_leads_selection['origem'].isin(origem_filter)]
    df_trafego_selection = df_trafego_selection[df_trafego_selection['Plataforma'].isin(origem_filter)]

# Filtro condicional para estado
if estado_filter:
    df_leads_selection = df_leads_selection[df_leads_selection['Estado'].isin(estado_filter)]



# Calcular período das campanhas
min_date = df_trafego['DATA'].min().strftime('%d/%m/%y')
max_date = df_trafego['DATA'].max().strftime('%d/%m/%y')

# st.title(":bar_chart: Dashboard Gestão de tráfego curador.IA")
st.subheader(":bar_chart: Dashboard Gestão de tráfego curador.IA")
st.markdown(f"###### Período {min_date} até {max_date}")


# Calcular valores baseado na seleção dos filtros

# Investimento total
VALOR_INVESTIMENTO = df_trafego_selection['VALOR USADO'].astype(float).sum()

# Total de Leads e Custo por LEAD
total_leads = len(df_leads_selection)
total_leads_trafego = df_trafego_selection['LEADS'].astype(int).sum()
# print('LEADS', total_leads)
# print('LEADS TRAFEGO', total_leads_trafego)
cpl = VALOR_INVESTIMENTO / total_leads if total_leads > 0 else 0



# Contratos
contratos_ia_pratica_pro = df_leads_selection[df_leads_selection["Comprou ia na prática PRO"] == 'SIM']
contratos_vip = df_leads_selection[df_leads_selection["ingresso VIP"] == 'Comprou']
count_contratos_ia_pratica_pro = len(contratos_ia_pratica_pro)
count_contratos_vip = len(contratos_vip)
count_vendas = count_contratos_ia_pratica_pro + count_contratos_vip

taxa_conversao = count_vendas / total_leads * 100 if total_leads > 0 else 0

cac = VALOR_INVESTIMENTO / count_vendas if count_vendas > 0 else 0


# Calcular valores de venda
df_venda_por_produto = pd.DataFrame({
    'Produto': [
        'VIP R$ 37,00',
        'IA na prática PRO R$ 97,00',
        'IA na prática PRO R$ 197,00'
    ],
    'Quantidade': [
        count_contratos_vip,
        len(df_leads_selection[df_leads_selection['ia na prática PRO'] == 'Comprou R$97']),
        len(df_leads_selection[df_leads_selection['ia na prática PRO'] == 'Comprou R$197'])
    ]
})

df_venda_por_produto['Valor Total'] = [
    df_venda_por_produto['Quantidade'][0] * 37,
    df_venda_por_produto['Quantidade'][1] * 97,
    df_venda_por_produto['Quantidade'][2] * 197
]

# Valor Total de vendas
valor_total_venda = df_venda_por_produto['Valor Total'].sum()


if origem_filter == [] or 'GoogleAds' in origem_filter or 'MetaAds' in origem_filter: 
    # Total de Click e Custo por Click
    total_clicks = df_trafego_selection['CLIQUES'].astype(int).sum()
    # cpc = VALOR_INVESTIMENTO / total_clicks

    # Total de impressões e Taxa de clicks
    total_impressoes = df_trafego_selection['IMPRESSÃO'].astype(int).sum()
    # ctr = total_clicks / total_impressoes * 100

    # Alcance
    total_alcance = df_trafego_selection['ALCANCE'].dropna().astype(int).sum()

    # ROAS
    print('total_vendas', valor_total_venda)
    print('VALOR_INVESTIMENTO', VALOR_INVESTIMENTO)
    roas = valor_total_venda / VALOR_INVESTIMENTO
else: 
    total_clicks = 0
    total_impressoes = 0
    roas = 0

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    st.metric("Investimento", f"R$ {utils.format_real(VALOR_INVESTIMENTO)}")
with col2:
    # st.metric("Impressões", utils.format_int(total_impressoes))
    st.metric("Leads", utils.format_int(total_leads))
with col3:
    st.metric("Custo por Lead (CPL)", f"R$ {utils.format_real(cpl)}")
with col4:
    st.metric("Vendas", utils.format_int(count_vendas))
with col5:
    st.metric("Taxa de Conversão", f"{utils.format_int(taxa_conversao)}%")
with col6:
    st.metric("CAC", f"R$ {utils.format_real(cac)}")
with col7:
    st.metric("ROAS", f"{utils.format_real(roas)}")


st.markdown("---")


st.markdown(
    f"<h4 style='text-align: center;'>Total em vendas: R$ {utils.format_real(valor_total_venda)}</h4>",
    unsafe_allow_html=True
)
# st.dataframe(df_selection)
#total_df_selection.


# Gráfico LEADS por ORIGEM
leads_por_origem = (
    df_leads_selection.groupby('origem').size().sort_values(ascending=True).reset_index(name='Leads')
)
leads_por_origem.columns = ['Origem', 'Leads']

chart_leads_por_origem = px.pie(
    leads_por_origem,
    values='Leads',
    names=leads_por_origem['Origem'],
    title="Leads por Origem",
    template="plotly_white",
    color_discrete_sequence=['#ff7f0e', '#1f77b4', '#2ca02c', '#d62728', '#946700'],
)

# Tamanho da fonte dentro da seção
chart_leads_por_origem.update_traces(textfont_size=13)

chart_leads_por_origem.update_layout(legend=dict(
    font=dict(
        size=14  # Tamanho da fonte da legenda
    )
))




# Gráfico Pizza Valor de venda de produtos

# chart_valor_venda_por_produto = px.bar(
#     df_chart_valor_venda.sort_values('Quantidade'),
#     y='Produto',
#     x=['Quantidade', 'ValorTotal'],
#     orientation='h',
#     title="Valor de Venda",
#     # color_discrete_sequence=["#0083B8"] * len(df_chart_valor_venda),
#     template="plotly_white"
# )

df_venda_por_produto['Valor Total Formatado'] = df_venda_por_produto['Valor Total'].apply(lambda x: f"R$ {utils.format_real(x)}")

chart_valor_venda_por_produto = px.bar(
    df_venda_por_produto.sort_values('Quantidade', ascending=False),
    y='Quantidade',
    x='Produto',
    title='Quantidade de Vendas por Produto',
    orientation='v',
    color='Produto',
    color_discrete_map={
        "VIP R$ 37,00": "#003D6C", 
        "IA na prática PRO R$ 97,00": "#005B9A", 
        "IA na prática PRO R$ 197,00": "#0083B8"
    },
    text='Valor Total Formatado',
)

chart_valor_venda_por_produto.update_traces(
    texttemplate='%{text}',
    textposition='inside',
    textfont=dict(size=16)  # Tamanho da fonte dos textos nas barras
)

chart_valor_venda_por_produto.update_layout(legend=dict(
    font=dict(
        size=14  # Tamanho da fonte da legenda
    )
))

total_clientes = len(df_leads_selection[df_leads_selection["É Cliente"] == 'SIM'])

etapas = ['Cliques', 'Leads', 'Clientes']
valores = [
    total_clicks, #df_trafego_selection['CLIQUES'].sum(),
    total_leads,  #df_trafego_selection['LEADS'].sum(),
    total_clientes,
]

cor_roxa_suave = "#A78BBF"

# # Criar gráfico de funil
chart_funil_vendas = go.Figure(go.Funnel(
    y=etapas,
    x=valores,
    textinfo="value",
    marker=dict(color=cor_roxa_suave))
)

# Atualizar o layout do gráfico
chart_funil_vendas.update_layout(
    title="Funil de Vendas",
    funnelmode="stack",
    font=dict(size=14)  # Tamanho da fonte dos textos nas barras
)


# Gráfico LEADS por Estado
leads_por_estado = (
    df_leads_selection.groupby('Estado').size().sort_values(ascending=False).reset_index(name='Leads')
)

leads_por_estado_top10 = leads_por_estado.sort_values(by="Leads", ascending=False).head(10)

chart_leads_por_estado = px.bar(
    leads_por_estado_top10.sort_values(by="Leads", ascending=True),
    x='Leads',
    y='Estado',
    orientation="h",
    title="Top 10 Estados",
    color_discrete_sequence=(["#0083B8"] * len(leads_por_estado_top10)) if len(leads_por_estado_top10) > 0 else ["#0083B8"],
    template="plotly_white",
)


left_col, right_col = st.columns(2)
# left_col, middle_col, right_col = st.columns(3)

with left_col:
    st.plotly_chart(chart_leads_por_origem)
with right_col:
    st.plotly_chart(chart_valor_venda_por_produto)

# with right_col:
left_col, right_col = st.columns(2)
with left_col:
    st.plotly_chart(chart_leads_por_estado)
with right_col:
    st.plotly_chart(chart_funil_vendas)


# Gráfico Impressão por dia
group_by_data = df_trafego_selection.groupby('DATA').agg({
    'IMPRESSÃO': 'sum',
    'CLIQUES': 'sum',
    'LEADS': 'sum'
}).reset_index().sort_values('DATA')

print(group_by_data)

chart_impressao_por_dia = px.line(
    group_by_data, 
    x='DATA', 
    y='IMPRESSÃO',
    title='Impressões por dia',
    labels={'value': 'Quantidade', 'variable': 'Métrica'},
    markers=True
)

# left_col, right_col = st.columns(2)

# with left_col:
#     st.plotly_chart(chart_impressao_por_dia)
# with right_col:
#     st.plotly_chart(chart_leads_por_estado)
path_img_curador_ia = 'img/logo_curador_ia_branca.png'


st.markdown("###")


st.image(path_img_curador_ia, width=376)