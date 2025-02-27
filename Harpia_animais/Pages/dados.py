# ===== Importar as bibliotecas ===== #

import pandas as pd
import numpy as np
import locale
import sqlalchemy as sa
from datetime import date
import hashlib

# Definir as propriedades de datas em Português BR
locale.setlocale(locale.LC_TIME, 'pt_BR')

# ===== Configuração de credenciais e permissões - Foi feito diretamente no código, pode melhorar e fazer via banco de dados. 
# Observar que as senhas são criptogtrafadas, cuiar ao fazer via banco de dados. ===== #
USUARIOS_CADASTRADOS = {
    'Lucas': {
        'senha': hashlib.sha256('Mega2403'.encode()).hexdigest(),
        'permissoes': ['/animais', '/mobilidade', '/gerenciamento', '/ocorrencias']
    },
    'Econ': {
        'senha': hashlib.sha256('47257487'.encode()).hexdigest(),
        'permissoes': ['/index']
    },
    'Abraão': {
        'senha': hashlib.sha256('55291071'.encode()).hexdigest(),
        'permissoes': ['/index']
    }
}

# ===== Carregar o token do Mapbox para geração do Gráfio de Mapa ===== #
mapbox_token = 'seu código de verificação do mapbox, sempre entre aspas'

# ===== Conexão Local ===== #
engine = sa.create_engine('mysql+mysqldb://root:root@localhost/harpia_animais')

# O acesso aos dados é feito via banco de dados, aqui é feita a conexão com o banco de dados e a leitura dos dados
# para serem utilizados no sistema.

# ===== Criar os dataframes ===== #
def dados(engine, data_ini=None, data_fin=None, pessoa=None):
    query = 'SELECT * FROM ocorrencia'
    params = []
    
    ocorrencia = pd.read_sql_query(query, engine, params=params)
    
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
    
    situacao = {'situacao': [0,1],
                'nomesituacao': ['Aberto', 'Finalizado']}
    situacao = pd.DataFrame(situacao)
    
    ocorrencia = pd.merge(ocorrencia, situacao[['situacao', 'nomesituacao']], on = 'situacao', how='left')
    
    ocorrencia = pd.merge(ocorrencia, cidade[['idcidade', 'nomecidade']], on = 'idcidade', how='left')
    ocorrencia = pd.merge(ocorrencia, bairro[['idbairro', 'nomebairro', 'latitude', 'longitude']], on = 'idbairro', how='left')
    ocorrencia = pd.merge(ocorrencia, situacaoanimal[['idsituacaoanimal', 'nomesituacaoanimal']], on = 'idsituacaoanimal', how='left')
    ocorrencia = pd.merge(ocorrencia, racaanimal[['idracaanimal', 'nomeracaanimal', 'nomegrupoanimal']], on = 'idracaanimal', how='left')
    
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
    
    
    ocorrencia['nome_ocorrencia_completo'] = ocorrencia.apply(lambda row: f"{row['idocorrencia']} - {row['dataocorrencia']} - {row['nomerua']} - {row['nomebairro']} - {row['nomegrupoanimal']}", axis=1)

    codigo_ocorrencia_map=dict(zip(ocorrencia['nome_ocorrencia_completo'], ocorrencia['idocorrencia']))
    
       
    return ocorrencia, codigo_ocorrencia_map, cidade, codigo_cidade_map, bairro, codigo_bairro_map, gruposituacao, codigo_gruposituacao_map, situacaoanimal, codigo_situacao_map, grupoanimal, codigo_grupoanimal_map, racaanimal, codigo_raca_animal_map
ocorrencia, codigo_ocorrencia_map, cidade, codigo_cidade_map, bairro, codigo_bairro_map, gruposituacao, codigo_gruposituacao_map, situacaoanimal, codigo_situacao_map, grupoanimal, codigo_grupoanimal_map, racaanimal, codigo_raca_animal_map = dados(engine)