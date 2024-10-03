import dash
from dash import html, dcc, Input, Output, dash_table, State
import plotly.figure_factory as ff
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from Pages.dados import *
from Pages.dashboard import layout as dashboard_layout
from Pages.ocorrencias import layout as ocorrencias_layout
import locale


# ===== Iniciar o app ===== #
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'], suppress_callback_exceptions=True)

server=app.server

# Barra de nevegação
navbar = dbc.NavbarSimple(
    brand=html.Img(src='/assets/logo.png', height="40px"),
    color='dark',
    dark=True,
    fluid=True,  
    sticky='dow',


)


app.layout = html.Div([
    navbar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Navegação entre as páginas
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboard':
        return dashboard_layout
    if pathname == '/ocorrencias':
        return ocorrencias_layout
    else:
        return dashboard_layout
    
    
# ----------- Controle de telas do sistema ----------- #
    
# Controles sobre o Modal de Filtros do dashboard
@app.callback(
    Output('modal_filtros', 'is_open'),
    [Input('botao_modal_filtros', 'n_clicks'),
    Input('botao_fechar_modal_filtros', 'n_clicks')],
    [State('modal_filtros', 'is_open')],
)
def modal_filtros(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Controles sobre o Modal de Lançamento de ocorrências
@app.callback(
    Output('modal_lancamento_ocorrencia', 'is_open'),
    [Input('botao_modal_lancamento_ocorrencia', 'n_clicks'),
    Input('botao_fechar_modal_lancamento_ocorrencia', 'n_clicks')],
    [State('modal_lancamento_ocorrencia', 'is_open')],
)
def modal_filtros(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Controles sobre o Modal de Cadastro de Grupos
@app.callback(
    Output('modal_cadastro_nomegrupoanimal', 'is_open'),
    [Input('botao_modal_cadastro_gruposanimais_navbar', 'n_clicks'),
    Input('botao_fechar_modal_nomegrupoanimal', 'n_clicks')],
    [State('modal_cadastro_nomegrupoanimal', 'is_open')],
)
def modal_filtros(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Controles sobre o Modal de Cadastro de Raças
@app.callback(
    Output('modal_cadastro_nomeracaanimal', 'is_open'),
    [Input('botao_modal_cadastro_racasanimais_navbar', 'n_clicks'),
    Input('botao_fechar_modal_nomeracaanimal', 'n_clicks')],
    [State('modal_cadastro_nomeracaanimal', 'is_open')],
)
def modal_filtros(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Controles sobre o Modal de Cadastro de Situações
@app.callback(
    Output('modal_cadastro_nomesituacaoanimal', 'is_open'),
    [Input('botao_modal_cadastro_situacaoanimais_navbar', 'n_clicks'),
    Input('botao_fechar_modal_nomesituacaoanimal', 'n_clicks')],
    [State('modal_cadastro_nomesituacaoanimal', 'is_open')],
)
def modal_filtros(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open




### Biblioteca de funções de formatação de valores ###

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


# Salvar e interagir com banco de dados 

# Função para atualização dos dados globais
def atualizar_dados_globais():
    global ocorrencia, cidade, codigo_cidade_map, bairro, codigo_bairro_map, gruposituacao, codigo_gruposituacao_map, situacaoanimal, codigo_situacao_map, grupoanimal, codigo_grupoanimal_map, racaanimal, codigo_raca_animal_map
    ocorrencia, cidade, codigo_cidade_map, bairro, codigo_bairro_map, gruposituacao, codigo_gruposituacao_map, situacaoanimal, codigo_situacao_map, grupoanimal, codigo_grupoanimal_map, racaanimal, codigo_raca_animal_map = dados(engine)
    
#### ---- PÁGINA DE CONTROLE DE OCORRENCIAS ---- ###

# Lançamento de Ocorrência - Cadastrar nova ocorrencia
@app.callback(
    [Output('mensagem_ocorrencia_salvo', 'children'),
     Output('data_lancamento_ocorrencia', 'date'),
     Output('dropdown_nomebairro_lancamento_ocorrencia', 'value'),
     Output('rua_lancamento_ocorrencia', 'value'),
     Output('dropdown_nomegrupoanimal_lancamento_ocorrencia', 'value'),
     Output('dropdown_nomeracaanimal_lancamento_ocorrencia', 'value'),
     Output('dropdown_nomesituacaoanimal_lancamento_ocorrencia', 'value'),
     Output('observacao_lancamento_ocorrencia', 'value')],
    Input('botao_salvar_lancamento_ocorrencia', 'n_clicks'),
    [State('data_lancamento_ocorrencia', 'date'),
     State('dropdown_nomebairro_lancamento_ocorrencia', 'value'),
     State('rua_lancamento_ocorrencia', 'value'),
     State('dropdown_nomegrupoanimal_lancamento_ocorrencia', 'value'),
     State('dropdown_nomeracaanimal_lancamento_ocorrencia', 'value'),
     State('dropdown_nomesituacaoanimal_lancamento_ocorrencia', 'value'),
     State('observacao_lancamento_ocorrencia', 'value')]
)
def salvar_ocorrencia(n_clicks, dataocorrencia, idbairro, nomerua, idgrupoanimal, idracaanimal, idsituacaoanimal, observacao):
    atualizar_dados_globais()
    if n_clicks is not None and dataocorrencia is not None and idbairro is not None and idgrupoanimal is not None and idracaanimal is not None and idsituacaoanimal is not None and observacao is not None:
        try:  
            idbairro = codigo_bairro_map[idbairro]
            idgrupoanimal = codigo_grupoanimal_map[idgrupoanimal]
            idracaanimal = codigo_raca_animal_map[idracaanimal]
            idsituacaoanimal = codigo_situacao_map[idsituacaoanimal]

            nova_ocorrencia = {'idbairro': idbairro, 'nomerua': nomerua, 'idgrupoanimal': idgrupoanimal, 'idracaanimal': idracaanimal, 
                               'idsituacaoanimal': idsituacaoanimal, 'dataocorrencia': dataocorrencia, 'observacao': observacao}         

            with engine.connect() as conn:
                conn.execute(sa.text("INSERT INTO ocorrencia (idbairro, nomerua, idgrupoanimal, idracaanimal, idsituacaoanimal, dataocorrencia, observacao) VALUES (:idbairro, :nomerua, :idgrupoanimal, :idracaanimal, :idsituacaoanimal, :dataocorrencia, :observacao)"), nova_ocorrencia)
                conn.commit()
                    
            return ('Ocorrência registrada com sucesso!', None, None, '', None, None, None, '')
    
        except Exception as e:
            return (f'Erro ao salvar ocorrência! {str(e)}', None, None, '', None, None, None, '')
        
    return ('', None, None, '', None, None, None, '')

# Cadastrar novo grupo
@app.callback(
    Output('mensagem_nomegrupoanimal_salvo', 'children'),
    Output('cadastro_nomegrupoanimal', 'value'),
    Input('botao_salvar_cadastro_nomegrupoanimal', 'n_clicks'),
    State('cadastro_nomegrupoanimal', 'value'),
)
def salvar_grupo(n_clicks, nomegrupoanimal):
    if n_clicks is not None and nomegrupoanimal is not None:
        try:  
            novo_grupo = {'nomegrupoanimal': nomegrupoanimal} 

            with engine.connect() as conn:
                conn.execute(sa.text("INSERT INTO grupoanimal (nomegrupoanimal) VALUES (:nomegrupoanimal)"), novo_grupo)
                conn.commit()
                
            
                    
            return ('Novo grupo registrado com sucesso!', '')
    
        except Exception as e:
            return (f'Erro ao salvar grupo! {str(e)}', '')
        
    return ('', '')


# Cadastrar nova raça
@app.callback(
    Output('mensagem_nomeracaanimal_salvo', 'children'),
    Output('cadastro_nomeracaanimal', 'value'),
    Output('dropdown_nomegrupoanimal_cadastro_raca', 'value'),
    Input('botao_salvar_cadastro_nomeracaanimal', 'n_clicks'),
    State('cadastro_nomeracaanimal', 'value'),
    State('dropdown_nomegrupoanimal_cadastro_raca', 'value'),
    
)
def salvar_raca(n_clicks, nomeracaanimal, idgrupoanimal):
    atualizar_dados_globais()
    if n_clicks is not None and nomeracaanimal is not None and idgrupoanimal is not None:
        try:  
            idgrupoanimal = codigo_grupoanimal_map[idgrupoanimal]
            
            nova_raca = {'nomeracaanimal': nomeracaanimal, 'idgrupoanimal': idgrupoanimal}         

            with engine.connect() as conn:
                conn.execute(sa.text("INSERT INTO racaanimal (nomeracaanimal, idgrupoanimal) VALUES (:nomeracaanimal, :idgrupoanimal)"), nova_raca)
                conn.commit()
                    
            return ('Nova raça registrada com sucesso!', '', '')
    
        except Exception as e:
            return (f'Erro ao salvar raça! {str(e)}', '', '')
        
    return ('', '', '')


# Cadastrar nova situação
@app.callback(
    Output('mensagem_nomesituacaoanimal_salvo', 'children'),
    Output('dropdown_nomegruposituacao_cadastro_situacao', 'children'),
    Output('cadastro_nomesituacaoanimal', 'value'),
    Input('botao_salvar_cadastro_nomesituacaoanimal', 'n_clicks'),
    State('dropdown_nomegruposituacao_cadastro_situacao', 'value'),
    State('cadastro_nomesituacaoanimal', 'value'),
    
    
)
def salvar_situacao(n_clicks, idgruposituacao, nomesituacaoanimal):
    atualizar_dados_globais()
    if n_clicks is not None and idgruposituacao is not None and nomesituacaoanimal is not None:
        try:  
            idgruposituacao = codigo_gruposituacao_map[idgruposituacao]
            
            nova_situacao = {'idgruposituacao': idgruposituacao, 'nomesituacaoanimal': nomesituacaoanimal,}         

            with engine.connect() as conn:
                conn.execute(sa.text("INSERT INTO situacaoanimal (idgruposituacao, nomesituacaoanimal) VALUES (:idgruposituacao, :nomesituacaoanimal)"), nova_situacao)
                conn.commit()
                    
            return ('Nova situação registrada com sucesso!', '', '')
    
        except Exception as e:
            return (f'Erro ao salvar situação! {str(e)}', '', '')
        
    return ('', '', '')

# ----------- Atualizar os dropdowns conforme novos cadastros são lançados ----------- #
@app.callback(
    Output('dropdown_nomebairro_lancamento_ocorrencia', 'options'),
    Output('dropdown_nomegrupoanimal_lancamento_ocorrencia', 'options'),
    Output('dropdown_nomeracaanimal_lancamento_ocorrencia', 'options'),
    Output('dropdown_nomesituacaoanimal_lancamento_ocorrencia', 'options'),
    Output('dropdown_nomegrupoanimal_cadastro_raca', 'options'),
    Output('dropdown_nomegruposituacao_cadastro_situacao', 'options'),
    
    [Input('atualizacao_automatica', 'n_intervals'),   
     Input('botao_salvar_lancamento_ocorrencia', 'n_clicks'),
     Input('botao_salvar_cadastro_nomegrupoanimal', 'n_clicks'),
     Input('botao_salvar_cadastro_nomeracaanimal', 'n_clicks'),
     Input('botao_salvar_cadastro_nomesituacaoanimal', 'n_clicks'),
    ]
)
def atualizar_dropdowns(n_intervals, n1, n2, n3, n4):
    atualizar_dados_globais()
    
    
    dropdown_nomebairro_lancamento_ocorrencia = [{'label': nomebairro, 'value': nomebairro} for nomebairro in bairro['nomebairro'].value_counts().index]
    dropdown_nomegrupoanimal_lancamento_ocorrencia = [{'label': nomegrupoanimal, 'value': nomegrupoanimal} for nomegrupoanimal in grupoanimal['nomegrupoanimal'].value_counts().index]  
    dropdown_nomeracaanimal_lancamento_ocorrencia = [{'label': nomeracaanimal, 'value': nomeracaanimal} for nomeracaanimal in racaanimal['nomeracaanimal'].value_counts().index]
    dropdown_nomesituacaoanimal_lancamento_ocorrencia = [{'label': nomesituacaoanimal, 'value': nomesituacaoanimal} for nomesituacaoanimal in situacaoanimal['nomesituacaoanimal'].value_counts().index]
    dropdown_nomegrupoanimal_cadastro_raca = [{'label': nomegrupoanimal, 'value': nomegrupoanimal} for nomegrupoanimal in grupoanimal['nomegrupoanimal'].value_counts().index]
    dropdown_nomegruposituacao_cadastro_situacao = [{'label': nomegruposituacao, 'value': nomegruposituacao} for nomegruposituacao in gruposituacao['nomegruposituacao'].value_counts().index]

    return dropdown_nomebairro_lancamento_ocorrencia, dropdown_nomegrupoanimal_lancamento_ocorrencia, dropdown_nomeracaanimal_lancamento_ocorrencia, dropdown_nomesituacaoanimal_lancamento_ocorrencia, dropdown_nomegrupoanimal_cadastro_raca, dropdown_nomegruposituacao_cadastro_situacao


# Atualizaçao dos gráficos
@app.callback([
    Output('fig_ocorrencias_relatadas', 'children'),
    Output('fig_ocorrencias_resolvidas', 'children'),   
    Output('fig_ocorrencias_pendentes', 'children'),   
    Output('fig_ocorrencias_por_periodo', 'figure'),   
    Output('fig_ocorrencias_por_raca', 'figure'), 
    Output('fig_ocorrencias_por_situacao_animal', 'figure'), 
    Output('fig_mapa_ocorrencias', 'figure'), 
    Output('grid_ocorrencias', 'rowData'),
    Output('grid_ocorrencias', 'columnDefs'),
    ],
    [
     Input('atualizacao_automatica', 'n_intervals'),
     Input('filtro_data', 'start_date'),
     Input('filtro_data', 'end_date'),
     ])

def aplicar_filtros(n_intervals, data_ini, data_fin):
    atualizar_dados_globais()

    ocorrencia_filtrado = ocorrencia
    
    if n_intervals:
        ocorrencia_filtrado = ocorrencia
    if data_ini and data_fin:
        ocorrencia_filtrado = ocorrencia_filtrado[(ocorrencia_filtrado['dataocorrencia'] >= data_ini) & (ocorrencia_filtrado['dataocorrencia'] <= data_fin)] 
    

    #Ocorrencias por período
    ocorrencias_por_periodo =ocorrencia_filtrado.groupby(['codmes_ocorrencia', 'mesocorrencia'])['idocorrencia'].count().reset_index()
    ocorrencias_por_periodo
    
    # Ocorrencias por raça
    ocorrencias_por_raca = ocorrencia_filtrado.groupby('nomeracaanimal', as_index=False)['idocorrencia'].count()
    ocorrencias_por_raca = ocorrencias_por_raca.round()
    if len (ocorrencias_por_raca) < 5:
        ocorrencias_por_raca = ocorrencias_por_raca
    else:
        ocorrencias_por_raca5 = ocorrencias_por_raca.nlargest(5, 'idocorrencia')
        ocorrencias_por_raca_resto = ocorrencias_por_raca.loc[~ocorrencias_por_raca.index.isin(ocorrencias_por_raca5.index)]
        ocorrencias_por_raca_resto['nomeracaanimal']='OUTROS'
        ocorrencias_por_raca=pd.concat([ocorrencias_por_raca5, ocorrencias_por_raca_resto])
        ocorrencias_por_raca = ocorrencias_por_raca.groupby('nomeracaanimal', as_index=False)['valor'].sum()
        ocorrencias_por_raca = ocorrencias_por_raca.sort_values(by='idocorrencia', ascending = False)
        
    if len(ocorrencias_por_raca) == 0:
        0
    else:
        ocorrencias_por_raca
        
    # Ocorrencias situação do animal
    ocorrencias_por_situacao_animal = ocorrencia_filtrado.groupby('nomesituacaoanimal', as_index=False)['idocorrencia'].count()
    ocorrencias_por_situacao_animal = ocorrencias_por_situacao_animal.round()
    if len (ocorrencias_por_situacao_animal) < 5:
        ocorrencias_por_situacao_animal = ocorrencias_por_situacao_animal
    else:
        ocorrencias_por_situacao_animal5 = ocorrencias_por_situacao_animal.nlargest(5, 'idocorrencia')
        ocorrencias_por_situacao_animal_resto = ocorrencias_por_situacao_animal.loc[~ocorrencias_por_situacao_animal.index.isin(ocorrencias_por_situacao_animal5.index)]
        ocorrencias_por_situacao_animal_resto['nomesituacaoanimal']='OUTROS'
        ocorrencias_por_situacao_animal=pd.concat([ocorrencias_por_situacao_animal5, ocorrencias_por_situacao_animal_resto])
        ocorrencias_por_situacao_animal = ocorrencias_por_situacao_animal.groupby('nomesituacaoanimal', as_index=False)['valor'].sum()
        ocorrencias_por_situacao_animal = ocorrencias_por_situacao_animal.sort_values(by='idocorrencia', ascending = False)
        
    if len(ocorrencias_por_situacao_animal) == 0:
        0
    else:
        ocorrencias_por_situacao_animal
        

    # KPIs
    
    # Ocorrecias relatadas
    ocorrencias_relatadas=pd.DataFrame(ocorrencia_filtrado['idocorrencia']).count()
    
    # Ocorrecias resolvidas
    ocorrencias_resolvidas = ocorrencia_filtrado[(ocorrencia_filtrado['situacao']==1)]
    ocorrencias_resolvidas=pd.DataFrame(ocorrencias_resolvidas['idocorrencia']).count()
    
    # Ocorrencias pendentes
    ocorrencias_pendentes = ocorrencias_relatadas-ocorrencias_resolvidas
    

    # Mapa de ocorrencias
    mapa_ocorrencias = ocorrencia_filtrado.groupby(['nomebairro', 'latitude', 'longitude'], as_index=False)['idocorrencia'].count()
    mapa_ocorrencias.rename(columns={'idocorrencia':'Quantidade'}, inplace=True)
    
    
    # Total de registros
    

    ## Gráficos 
    # Ocorrencias por período
    fig_ocorrencias_por_periodo = go.Figure()
    fig_ocorrencias_por_periodo.add_trace(go.Scatter(x=ocorrencias_por_periodo['mesocorrencia'], y=ocorrencias_por_periodo['idocorrencia'], name='Ocorrencias por período'))
    fig_ocorrencias_por_periodo.update_layout(title='Ocorrencias por período', yaxis_title='', xaxis_title='', title_x=0.5, height=250)
    
    # Ocorrências por raça do animal
    ocorrencias_por_raca = ocorrencias_por_raca.rename(columns={'idocorrencia':'Ocorrencias','nomeracaanimal':'Raça'})
    fig_ocorrencias_por_raca = px.pie(ocorrencias_por_raca, values='Ocorrencias', names='Raça', hole=.3)
    fig_ocorrencias_por_raca.update_layout(margin=dict(l=5, r=5, t=40, b=5), title='Ocorrencias por raça', yaxis_title='', xaxis_title='', title_x=0.5, height=250)

    # Ocorrencias por situação do animal
    ocorrencias_por_situacao_animal = ocorrencias_por_situacao_animal.rename(columns={'idocorrencia':'Ocorrencias','nomesituacaoanimal':'Situação do animal'})
    fig_ocorrencias_por_situacao_animal = px.pie(ocorrencias_por_situacao_animal, values='Ocorrencias', names='Situação do animal', hole=.3)
    fig_ocorrencias_por_situacao_animal.update_layout(margin=dict(l=5, r=5, t=40, b=5), title='Ocorrencias por situação do animal', yaxis_title='', xaxis_title='', title_x=0.5, height=250)

    fig_mapa_ocorrencias = px.scatter_mapbox(mapa_ocorrencias, lat='latitude', lon='longitude', color='Quantidade', color_discrete_sequence=['blue'], size='Quantidade', title='Gastos por cidade').update_layout(yaxis_title='', xaxis_title='', title_x=0.5)

    # Grid de ocorrencias
    grid_ocorrencias = ocorrencia_filtrado[['idocorrencia', 'nomeracaanimal', 'nomesituacaoanimal', 'mesocorrencia', 'messolucao']]
    grid_ocorrencias = grid_ocorrencias.rename(columns={'idocorrencia':'ID', 'nomeracaanimal':'Raça', 'nomesituacaoanimal':'Situação do animal', 'mesocorrencia':'Mês ocorrencia', 'messolucao':'Mês solução'})
    grid_ocorrencias = grid_ocorrencias.sort_values(by='ID', ascending=False)
    rowData = grid_ocorrencias.to_dict('records')
    columnDefs = [{"field": col} for col in grid_ocorrencias.columns]
    
    return [ocorrencias_relatadas, ocorrencias_resolvidas, ocorrencias_pendentes, fig_ocorrencias_por_periodo, fig_ocorrencias_por_raca, fig_ocorrencias_por_situacao_animal, fig_mapa_ocorrencias, rowData, columnDefs   ]


# ===== Iniciar o servidor e manter o aplicativo rodando ===== #
if __name__=='__main__':
    app.run_server(host='0.0.0.0', port=8052, debug=True)    
    #app.run_server(host='0.0.0.0', port=8051, debug=True)
