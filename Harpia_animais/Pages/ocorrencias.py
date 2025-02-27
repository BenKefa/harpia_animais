# ===== Importar as bibliotecas ===== #

from dash import html, dcc, Input, Output, dash_table, State
import plotly.express as px
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from Pages.dados import *
import datetime
from datetime import date

load_figure_template('bootstrap')

# ===== Criar o Layout do sistema - Aqui são configurados os espaços e imagens do aplicativo ===== #
layout = html.Div(style={'backgroundColor': 'white'}, children=[
    html.H2('Ocorrências', style={'textAlign': 'center', 'marginBottom': '20px', 'marginTop': '20px'}),
    html.H5('Preencha os dados abaixo e informe a situação e localização do animal.', style={'textAlign': 'center', 'marginBottom': '20px'}),

    dcc.Loading(
        id='loading_dashboard', type='circle', fullscreen=True, style={'backgroundColor': 'rgba(0,0,0,0)'},
        children=
        dbc.Row([
             # Modal de Confirmação de salvamentos (m011)
            dbc.Modal([
                dbc.ModalHeader(
                    dbc.Row([ 
                        dbc.Col([html.Span('m111', style={'color': 'transparent'})], width=1),
                        html.Div(id='mensagem_ocorrencia_salvo_01'),
                    ]),
                    close_button=False
                ),
                dbc.ModalFooter([
                    dbc.ButtonGroup([
                        dbc.Button('Cancelar', id='botao_cancelar_modal_confirmacao_ocorrencia_01', className='ms-auto', n_clicks=0, href='/pos_ocorrencia_cancelada', color='danger'),
                        dbc.Button('Continuar', id='botao_continuar_modal_confirmacao_ocorrencia_01', className='ms-auto', n_clicks=0, color='success'),
                    ])
                ])
            ], id='modal_confirmacao_ocorrencia_01', is_open=False,  centered=True, keyboard=False, backdrop=True, size = 'sm'),
        
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Data de Ocorrência'),
                                html.Div([
                                    dcc.DatePickerSingle(id='data_lancamento_ocorrencia_01', placeholder='Data', persistence=False, display_format='DD/MM/YYYY', date=date.today())
                                ]),
                                dbc.Label('Bairro'),
                                dcc.Dropdown(
                                    bairro['nomebairro'].value_counts().index, id='dropdown_nomebairro_lancamento_ocorrencia_01',
                                    placeholder='Selecione um bairro', multi=False, optionHeight=60, maxHeight=200, persistence=False,
                                    
                                ),
                                dbc.Label('Rua'),
                                dbc.Input(
                                    id='rua_lancamento_ocorrencia_01', placeholder='Informe o nome da rua',
                                    
                                ),
                                dbc.Label('Grupo do animal'),
                                dcc.Dropdown(
                                    grupoanimal['nomegrupoanimal'].value_counts().index, id='dropdown_nomegrupoanimal_lancamento_ocorrencia_01',
                                    placeholder='Selecione um grupo', multi=False, optionHeight=60, maxHeight=200, persistence=False,
                                    
                                ),
                                dbc.Label('Raça do animal'),
                                dcc.Dropdown(
                                    racaanimal['nomeracaanimal'].value_counts().index, id='dropdown_nomeracaanimal_lancamento_ocorrencia_01',
                                    placeholder='Selecione uma raça', multi=False, optionHeight=60, maxHeight=200, persistence=False,
                                    
                                ),
                                dbc.Label('Situação do animal'),
                                dcc.Dropdown(
                                    situacaoanimal['nomesituacaoanimal'].value_counts().index, id='dropdown_nomesituacaoanimal_lancamento_ocorrencia_01',
                                    placeholder='Selecione uma situação do animal', multi=False, optionHeight=60, maxHeight=200, persistence=False,
                                    
                                ),
                                dbc.Label('Observações'),
                                dbc.Textarea(
                                    id='observacao_lancamento_ocorrencia_01',
                                    
                                ),
                                html.Div([
                                    dbc.Button(
                                        'Salvar', id='botao_salvar_lancamento_ocorrencia_01', className='ms-auto', n_clicks=0, color='success'
                                    ),
                                ], style={'display': 'flex', 'justifyContent': 'flex-end', 'marginTop': '10px'}),
                            ])
                        ]),
                    ]),
                ], style={'backgroundColor': '#f2f2f2', 'borderRadius': '10px'}),
            ], sm=12, style={'paddingLeft': '30px', 'paddingRight': '30px'}),
        ], style={'justifyContent': 'center', 'backgroundColor': 'white'})
    ),
    html.H5('Harpia Dashboards', style={'textAlign': 'center', 'marginBottom': '20px'}),

])

