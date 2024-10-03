# ===== Importar as bibliotecas ===== #

import pandas as pd
import numpy as np
import locale
import plotly.graph_objects as go
import plotly.express as px
import sqlalchemy as sa
from datetime import date

# Definir as propriedades de datas em Português BR
locale.setlocale(locale.LC_TIME, 'pt_BR')

# Função para formatar valores numéricos em Moeda Brasileira R$
def formatar_moeda(valor):
    locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
    valor_formatado = locale.currency(valor, grouping=True, symbol='R$')
    return valor_formatado

# Função para formatar valores números em quantidades com 1 casa decimal
def formatar_quantidade(valor):
    return '{:,.2f}'.format(valor).replace(',', 'temp').replace('.', ',').replace('temp', '.')

# Função para formatar valores numéricos em percentual
def formatar_percentual(valor):
    return '{:,.0f}%'.format(valor)

# Função para formatar datas no padrão brasileiro com dia, mes e ano - d/m/a
def formatar_data(data):
    return data.strftime('%d/%m/%Y')

# Função para formatar o cpf no padrão brasileiro 000.000.000.00
def formatar_cpf(numero):
    numero_str = str(numero).zfill(11)  # Preenche com zeros à esquerda se necessário
    cpf_formatado = f'{numero_str[:3]}.{numero_str[3:6]}.{numero_str[6:9]}-{numero_str[9:]}'
    return cpf_formatado

# ===== Carregar o token do Mapbox para geração do Gráfio de Mapa ===== #
mapbox_token = 'pk.eyJ1IjoiYmVua2VmYSIsImEiOiJjbGRmemt5NjUwaXRlM3ZzMnRvbmV1NDRrIn0.OJ2myrAkytpmthW9QG4mig'

# ===== Conexão Local ===== #
engine = sa.create_engine('mysql+mysqldb://root:root@localhost/harpia_animais')

# ===== Criar os dataframes ===== #
def dados(engine, data_ini=None, data_fin=None, pessoa=None):
    query = 'SELECT * FROM ocorrencia'
    params = []
    
    #if data_ini and data_fin:
    #    query += ' WHERE dataocorrencia BETWEEN %s AND %s'
    #    params.extend([data_ini, data_fin])
    #elif data_ini:
    #    query += ' WHERE dataocorrencia >= %s'
    #    params.append(data_ini)
    #elif data_fin:
    #    query += ' WHERE dataocorrencia <= %s'
    #    params.append(data_fin)
    #
    #if pessoa:
    #    if 'WHERE' in query:
    #        query += ' AND nome_cli = %s'
    #    else:
    #        query += ' WHERE nome_cli = %s'
    #    params.append(pessoa)

    ocorrencia = pd.read_sql_query(query, engine, params=params)
    #codigo_ocorrencia_map = dict(zip(ocorrencia['nomeocorrencia'], ocorrencia['idocorrencia']))
    
    cidade = pd.read_sql_query('SELECT * from cidade', engine)
    codigo_cidade_map = dict(zip(cidade['nomecidade'], cidade['idcidade']))
    
    bairro = pd.read_sql_query('SELECT * from bairro', engine)
    codigo_bairro_map = dict(zip(bairro['nomebairro'], bairro['idbairro']))
    
    gruposituacao = pd.read_sql_query('SELECT * from gruposituacao', engine)
    codigo_gruposituacao_map = dict(zip(gruposituacao['nomegruposituacao'], gruposituacao['idgruposituacao']))
    
    situacaoanimal = pd.read_sql_query('SELECT * from situacaoanimal', engine)
    situacaoanimal = pd.merge(situacaoanimal, gruposituacao[['idgruposituacao', 'nomegruposituacao']], on = 'idgruposituacao', how='left')
    codigo_situacao_map = dict(zip(situacaoanimal['nomesituacaoanimal'], situacaoanimal['idsituacaoanimal']))


    grupoanimal = pd.read_sql_query('SELECT * from grupoanimal', engine)
    codigo_grupoanimal_map = dict(zip(grupoanimal['nomegrupoanimal'], grupoanimal['idgrupoanimal']))

    racaanimal = pd.read_sql_query('SELECT * from racaanimal', engine)
    racaanimal = pd.merge(racaanimal, grupoanimal[['idgrupoanimal', 'nomegrupoanimal']], on = 'idgrupoanimal', how='left')
    codigo_raca_animal_map = dict(zip(racaanimal['nomeracaanimal'], racaanimal['idracaanimal']))
    
    ocorrencia = pd.merge(ocorrencia, cidade[['idcidade', 'nomecidade']], on = 'idcidade', how='left')
    ocorrencia = pd.merge(ocorrencia, bairro[['idbairro', 'nomebairro', 'latitude', 'longitude']], on = 'idbairro', how='left')
    ocorrencia = pd.merge(ocorrencia, situacaoanimal[['idsituacaoanimal', 'nomesituacaoanimal']], on = 'idsituacaoanimal', how='left')
    ocorrencia = pd.merge(ocorrencia, racaanimal[['idracaanimal', 'nomeracaanimal']], on = 'idracaanimal', how='left')
    
    ocorrencia['dataocorrencia']= pd.to_datetime(ocorrencia['dataocorrencia'], dayfirst=True)
    ocorrencia['dataresolucao']= pd.to_datetime(ocorrencia['dataresolucao'], dayfirst=True)
    
    ocorrencia['latitude'] = ocorrencia['latitude'].str.replace(',', '.').astype(float)
    ocorrencia['longitude'] = ocorrencia['longitude'].str.replace(',', '.').astype(float)


    ocorrencia['mesocorrencia'] = ocorrencia['dataocorrencia'].dt.strftime('%B')
    ocorrencia['messolucao'] = ocorrencia['dataresolucao'].dt.strftime('%B')

    mesocorrencia = {'codmes_ocorrencia':[1,2,3,4,5,6,7,8,9,10,11,12],
         'mesocorrencia':['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']}
    mesocorrencia = pd.DataFrame(mesocorrencia) 
    
    mesresolucao = {'codmes_solucao':[1,2,3,4,5,6,7,8,9,10,11,12],
         'messolucao':['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']}
    mesresolucao = pd.DataFrame(mesresolucao) 
    
    ocorrencia = pd.merge(ocorrencia, mesocorrencia, on = 'mesocorrencia', how='left')
    ocorrencia = pd.merge(ocorrencia, mesresolucao, on = 'messolucao', how='left')
    
    

    #ocorrencia['dataocorrencia_formatado'] = ocorrencia['dataocorrencia']
    #ocorrencia['dataresolucao_formatado'] = ocorrencia['dataresolucao']
    #for campo in ['dataocorrencia_formatado', 'dataresolucao_formatado']:
    #    ocorrencia[campo]=ocorrencia[campo].map(formatar_data)
    
    #ocorrencia['nome_ocorrencia_completo'] = ocorrencia.apply(lambda row: f"{row['idocorrencia']} - {row['nomeocorrencia']}", axis=1)

    #codigo_conta_map=dict(zip(ocorrencia['nome_ocorrencia_completo'], ocorrencia['idocorrencia']))
    
    #colunas_organizadas = ['nome_ocorrencia_completo']
    
    #ocorrencia = ocorrencia.reindex(columns=colunas_organizadas)
    
       
    return ocorrencia, cidade, codigo_cidade_map, bairro, codigo_bairro_map, gruposituacao, codigo_gruposituacao_map, situacaoanimal, codigo_situacao_map, grupoanimal, codigo_grupoanimal_map, racaanimal, codigo_raca_animal_map
ocorrencia, cidade, codigo_cidade_map, bairro, codigo_bairro_map, gruposituacao, codigo_gruposituacao_map, situacaoanimal, codigo_situacao_map, grupoanimal, codigo_grupoanimal_map, racaanimal, codigo_raca_animal_map = dados(engine)