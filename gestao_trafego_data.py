import pandas as pd
import plotly.express as px

from utils import ddd_to_estado, meses_to_pt

# Importar Controle de tráfego MetaADS
df_metaads = pd.read_csv('./csv/gestao_trafego_metaads.csv', sep=",", decimal=',', skip_blank_lines=True)
df_metaads = df_metaads.dropna(how='all')
df_metaads['Plataforma'] = 'MetaAds'

# Importar Controle de tráfego MetaADS
df_google_ads = pd.read_csv('./csv/gestao_trafego_googleads.csv', sep=",", decimal=',', skip_blank_lines=True)
df_google_ads = df_google_ads.dropna(how='all')
df_google_ads['Plataforma'] = 'GoogleAds'

# Concatenar Planilhas de LEADS
df_concatenado = pd.concat(
  [df_google_ads, df_metaads], 
  ignore_index=True)


# Converter data para tipo datetime e aplicar ordenação
df_concatenado['DATA'] = pd.to_datetime(df_concatenado['DATA'])
df_concatenado = df_concatenado.sort_values('DATA')

# Obter Mes/Ano
df_concatenado["MesAno"] = df_concatenado['DATA'].apply(lambda x: str(x.year) + '-' + str(x.month))
df_concatenado["MesAno"] = df_concatenado['DATA'].dt.strftime('%m/%Y')

# Substituir os meses em inglês pelos correspondentes em português
df_concatenado["MesAno"] = df_concatenado["MesAno"].replace(meses_to_pt, regex=True)
