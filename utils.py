def format_real(val):
  return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_int(val):
  return f"{val:,.0f}".replace(',', '.')


# ddds
ddd_to_estado = {
    11: "São Paulo",
    12: "São Paulo",
    13: "São Paulo",
    14: "São Paulo",
    15: "São Paulo",
    16: "São Paulo",
    17: "São Paulo",
    18: "São Paulo",
    19: "São Paulo",
    21: "Rio de Janeiro",
    22: "Rio de Janeiro",
    24: "Rio de Janeiro",
    27: "Espírito Santo",
    28: "Espírito Santo",
    31: "Minas Gerais",
    32: "Minas Gerais",
    33: "Minas Gerais",
    34: "Minas Gerais",
    35: "Minas Gerais",
    37: "Minas Gerais",
    38: "Minas Gerais",
    41: "Paraná",
    42: "Paraná",
    43: "Paraná",
    44: "Paraná",
    45: "Paraná",
    46: "Paraná",
    47: "Santa Catarina",
    48: "Santa Catarina",
    49: "Santa Catarina",
    51: "Rio Grande do Sul",
    53: "Rio Grande do Sul",
    54: "Rio Grande do Sul",
    55: "Rio Grande do Sul",
    61: "Distrito Federal/Goiás",
    62: "Goiás",
    63: "Tocantins",
    64: "Goiás",
    65: "Mato Grosso",
    66: "Mato Grosso",
    67: "Mato Grosso do Sul",
    68: "Acre",
    69: "Rondônia",
    71: "Bahia",
    73: "Bahia",
    74: "Bahia",
    75: "Bahia",
    77: "Bahia",
    79: "Sergipe",
    81: "Pernambuco",
    82: "Alagoas",
    83: "Paraíba",
    84: "Rio Grande do Norte",
    85: "Ceará",
    86: "Piauí",
    87: "Pernambuco",
    88: "Ceará",
    89: "Piauí",
    91: "Pará",
    92: "Amazonas",
    93: "Pará",
    94: "Pará",
    95: "Roraima",
    96: "Amapá",
    97: "Amazonas",
    98: "Maranhão",
    99: "Maranhão"
}


# Para converter os meses para português
meses_to_pt = {
    'Jan': 'Jan',
    'Feb': 'Fev',
    'Mar': 'Mar',
    'Apr': 'Abr',
    'May': 'Mai',
    'Jun': 'Jun',
    'Jul': 'Jul',
    'Aug': 'Ago',
    'Sep': 'Set',
    'Oct': 'Out',
    'Nov': 'Nov',
    'Dec': 'Dez'
}



# # Criando o gráfico com dois eixos y
# chart_alcance_por_dia = go.Figure()

# # Adicionando a linha para "Impressões"
# chart_alcance_por_dia.add_trace(go.Scatter(
#     x=group_by_data['DATA'], 
#     y=group_by_data['IMPRESSÃO'], 
#     name="Impressões",
#     mode='lines+markers',
#     line=dict(color="#1f77b4"),
#     yaxis="y1"  # Associa ao primeiro eixo y
# ))

# # Adicionando a linha para "Valor"
# chart_alcance_por_dia.add_trace(go.Scatter(
#     x=group_by_data['DATA'], 
#     y=group_by_data['VALOR USADO'], 
#     name="Valor (R$)",
#     mode='lines+markers',
#     line=dict(color="#7D7D7D"), 
#     yaxis="y2",  # Associa ao segundo eixo y
# ))

# # Configurando os eixos
# chart_alcance_por_dia.update_layout(
#     title="Impressões x Valor por Dia",
#     xaxis=dict(title="Data"),
#     yaxis=dict(
#         title="Impressões",
#         titlefont=dict(color="#1f77b4"),
#         tickfont=dict(color="#1f77b4")
#     ),
#     yaxis2=dict(
#         title="Valor (R$)",
#         titlefont=dict(color="#6A7B89"),
#         tickfont=dict(color="#6A7B89"),
#         anchor="x",
#         overlaying="y",
#         side="right"
#     ),    
#     legend=dict(x=0.5, y=1.1, orientation='h')
# )
