import pandas as pd
import plotly.express as px

from utils import ddd_to_estado, meses_to_pt

# Importar leads Ingresso Gratuito
df_leads_gratuito = pd.read_csv('./csv/leads_ingresso_gratuito.csv', sep=";", decimal=',', skip_blank_lines=True)
df_leads_gratuito = df_leads_gratuito.dropna(how='all')

# Importar leads Ingresso VIP
df_leads_vip = pd.read_csv('./csv/leads_ingresso_vip.csv', sep=";", decimal=',', skip_blank_lines=True)
df_leads_vip = df_leads_vip.dropna(how='all')

print(df_leads_vip.all())

# Concatenar Planilhas de LEADS
df_concatenado = pd.concat([df_leads_vip, df_leads_gratuito], ignore_index=True)
print(df_leads_vip)
# Remover duplicatas mantendo apenas o primeiro registro
df_concatenado.drop_duplicates(subset='E-mail:', keep='first', inplace=True)


# Converter data para tipo datetime e aplicar ordenação
df_concatenado['data'] = pd.to_datetime(df_concatenado['data'])
df_concatenado = df_concatenado.sort_values('data')


# Obter Mes/Ano
df_concatenado["MesAno"] = df_concatenado['data'].apply(lambda x: str(x.year) + '-' + str(x.month))
df_concatenado["MesAno"] = df_concatenado['data'].dt.strftime('%m/%Y')

# Substituir os meses em inglês pelos correspondentes em português
df_concatenado["MesAno"] = df_concatenado["MesAno"].replace(meses_to_pt, regex=True)


# Obter DDD / Estado
# Converter para número
df_concatenado['DDD + Telefone:'] = df_concatenado["DDD + Telefone:"].str.replace(r'\D', '', regex=True)
# Obter DDD
df_concatenado['DDD'] = df_concatenado["DDD + Telefone:"].apply(lambda x: x[:2])
print(df_concatenado['DDD'].unique())

# Estado pelo DDD
df_concatenado['Estado'] = df_concatenado['DDD'].astype(int).map(ddd_to_estado)

print(df_concatenado["ia na prática PRO"].astype(str))

# Comprou IA na prática PRO (dois preços)
df_concatenado["Comprou ia na prática PRO"] = df_concatenado["ia na prática PRO"].astype(str).str.contains('Comprou', na=False).map({True: 'SIM', False: 'NÃO'})


# Salvar csv concatenado e formatado
df_concatenado.to_csv('arquivo_merged.csv', index=False, sep=';')