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
layout = html.Div(children=[
    dcc.Interval(id='atualizacao_automatica', interval=300000, n_intervals=0), # Atualização automárica dos gráficos a cada 5 minutos
    

# Linha com botões de filtros e cadastros
    dbc.Row([
        dbc.Card([
            dbc.Navbar([
                dbc.Button('Filtros', id='botao_modal_filtros', n_clicks=0, color='black'),
                dbc.Button('Lançar Ocorrência', id='botao_modal_lancamento_ocorrencia', n_clicks=0, color='black'),   
                dbc.Button('Cadastrar Grupos', id='botao_modal_cadastro_gruposanimais_navbar', n_clicks=0, color='black'),
                dbc.Button('Cadastrar Raças', id='botao_modal_cadastro_racasanimais_navbar', n_clicks=0, color='black'),
                dbc.Button('Cadastrar Situações', id='botao_modal_cadastro_situacaoanimais_navbar', n_clicks=0, color='black'), 
                     
            ],
            #color='black',
            dark=True,
            className='custom-dropdown-button',
            sticky='down',
            ),
        ]),
        # Modal onde ficam os filtros do dashboard
        dbc.Modal([
            dbc.ModalHeader(
                dbc.ModalTitle('Filtros')),
            dbc.ModalBody(
                dbc.Row([
                    html.H5('Data de vencimento:', style={'textAlign': 'center'}),
                            html.Div([
                                dcc.DatePickerRange(id='filtro_data', start_date_placeholder_text='Data Início', end_date_placeholder_text='Data Fim',persistence=True, display_format='DD/MM/YYYY'),
                            ]),
                        ]),
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Fechar', id='botao_fechar_modal_filtros', className='ms-auto', n_clicks=0, color='danger')
                ])
            ])
        ], id='modal_filtros', is_open=False,  centered=True, size = 'lg'),
        
        # Modal onde Lançamento de Ocorrencias
        dbc.Modal([
            dbc.ModalHeader(
                dbc.ModalTitle('Lançamento de Ocorrências')),
            dbc.ModalBody(
                dbc.Row([
                    dbc.Label('Data de Ocorrência'),
                        html.Div([
                            dcc.DatePickerSingle(id='data_lancamento_ocorrencia', placeholder='Data de ocorrêcia', persistence=True, display_format='DD/MM/YYYY'),
                        ]),
                        dbc.Label('Bairro'),
                        dcc.Dropdown(bairro['nomebairro'].value_counts().index, id='dropdown_nomebairro_lancamento_ocorrencia', placeholder='Selecione uma bairro', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        dbc.Label('Rua'),
                        dbc.Input(id='rua_lancamento_ocorrencia', placeholder='Informe o nome da rua'),
                        dbc.Label('Grupo do animal'),
                        dcc.Dropdown(grupoanimal['nomegrupoanimal'].value_counts().index, id='dropdown_nomegrupoanimal_lancamento_ocorrencia', placeholder='Selecione um grupo', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        dbc.Label('Raça do animal'),
                        dcc.Dropdown(racaanimal['nomeracaanimal'].value_counts().index, id='dropdown_nomeracaanimal_lancamento_ocorrencia', placeholder='Selecione uma raça', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        dbc.Label('Situação do animal'),
                        dcc.Dropdown(situacaoanimal['nomesituacaoanimal'].value_counts().index, id='dropdown_nomesituacaoanimal_lancamento_ocorrencia', placeholder='Selecione uma situação do animal', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        dbc.Label('Observações'),
                        dbc.Textarea(id='observacao_lancamento_ocorrencia'),
                        html.Div(id='mensagem_ocorrencia_salvo')
                ]),            
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Salvar', id='botao_salvar_lancamento_ocorrencia', className='ms-auto', n_clicks=0, color='success'),
                    dbc.Button('Fechar', id='botao_fechar_modal_lancamento_ocorrencia', className='ms-auto', n_clicks=0, color='danger')
                ])
            ])
        ], id='modal_lancamento_ocorrencia', is_open=False,  centered=True, size = 'lg'),
        
        # Modal Cadastro de Grupos
        dbc.Modal([
            dbc.ModalHeader(
                dbc.ModalTitle('Cadastro de grupos')),
            dbc.ModalBody(
                dbc.Row([
                        dbc.Label('Nome do grupo'),
                        dbc.Input(id='cadastro_nomegrupoanimal', placeholder='Informe um grupo de animal (gato/cachorro/etc.)', persistence=False),
                        html.Div(id='mensagem_nomegrupoanimal_salvo')
                ]),            
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Salvar', id='botao_salvar_cadastro_nomegrupoanimal', className='ms-auto', n_clicks=0, color='success'),
                    dbc.Button('Fechar', id='botao_fechar_modal_nomegrupoanimal', className='ms-auto', n_clicks=0, color='danger')
                ])
            ])
        ], id='modal_cadastro_nomegrupoanimal', is_open=False,  centered=True, size = 'lg'),

        # Modal Cadastro de Raças
        dbc.Modal([
            dbc.ModalHeader(
                dbc.ModalTitle('Cadastro de raças')),
            dbc.ModalBody(
                dbc.Row([
                        dbc.Label('Nome da raça'),
                        dbc.Input(id='cadastro_nomeracaanimal', placeholder='Informe uma raça de animal (Golden, Pastor Alemão, etc.)', persistence=False),
                        dbc.Label('Grupo do animal'),
                        dcc.Dropdown(grupoanimal['nomegrupoanimal'].value_counts().index, id='dropdown_nomegrupoanimal_cadastro_raca', placeholder='Selecione um grupo', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        html.Div(id='mensagem_nomeracaanimal_salvo')
                ]),            
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Salvar', id='botao_salvar_cadastro_nomeracaanimal', className='ms-auto', n_clicks=0, color='success'),
                    dbc.Button('Fechar', id='botao_fechar_modal_nomeracaanimal', className='ms-auto', n_clicks=0, color='danger')
                ])
            ])
        ], id='modal_cadastro_nomeracaanimal', is_open=False,  centered=True, size = 'lg'),
        
        # Modal Cadastro de Situações
        dbc.Modal([
            dbc.ModalHeader(
                dbc.ModalTitle('Cadastro de situações')),
            dbc.ModalBody(
                dbc.Row([
                    dbc.Label('Grupo do animal'),
                    dcc.Dropdown(gruposituacao['nomegruposituacao'].value_counts().index, id='dropdown_nomegruposituacao_cadastro_situacao', placeholder='Selecione um grupo', 
                    multi=False, optionHeight=60, maxHeight=200, persistence=False),
                    dbc.Label('Nome da situação'),
                    dbc.Input(id='cadastro_nomesituacaoanimal', placeholder='Informe uma situação do animal (Machucado, Doente, com filhotes, etc.)', persistence=False),
                    html.Div(id='mensagem_nomesituacaoanimal_salvo')
                ]),            
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Salvar', id='botao_salvar_cadastro_nomesituacaoanimal', className='ms-auto', n_clicks=0, color='success'),
                    dbc.Button('Fechar', id='botao_fechar_modal_nomesituacaoanimal', className='ms-auto', n_clicks=0, color='danger')
                ])
            ])
        ], id='modal_cadastro_nomesituacaoanimal', is_open=False,  centered=True, size = 'lg'),
        
        # == Dashboard == #  
        # == Criar um Card com uma linha, contendo informações (não gráficos) == #
            dbc.Card([
                dcc.Loading(id='loading_dashboard', type = 'circle', fullscreen=True, style={'backgroundColor': 'rgba(0,0,0,0)'},
                    children=dbc.Row([
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    html.H5('Ocorrencias relatadas', style={'textAlign': 'center','font-size': 'medium'}),
                                    html.H5(id='fig_ocorrencias_relatadas', style={'textAlign': 'center','font-size': 'small'}),
                                ], style={'margin': '3px', 
                                            'backgroundColor': '#FF6347'}),
                            ],md=4),
                            dbc.Col([
                                dbc.Card([
                                    html.H5('Ocorrencias resolvidas', style={'textAlign': 'center','font-size': 'medium'}),
                                    html.H5(id='fig_ocorrencias_resolvidas', style={'textAlign': 'center','font-size': 'small'}),
                                ], style={'margin': '3px', 
                                            'backgroundColor': '#4682B4'}),
                            ],md=4),
                            dbc.Col([
                                dbc.Card([
                                    html.H5('Ocorrencias pendentes', style={'textAlign': 'center','font-size': 'medium'}),
                                    html.H5(id='fig_ocorrencias_pendentes', style={'textAlign': 'center','font-size': 'small'}),
                                ], style={'margin': '3px', 
                                            'backgroundColor': '#66CDAA'}),
                            ],md=4),
                            
                        ], className='h-10', style={'justify-content': 'center', 'background-color': '#e9e9e9'}),
                        
                        dbc.Row([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card(
                                        dcc.Graph(id='fig_ocorrencias_por_periodo', config={'displayModeBar': False, 'staticPlot': False}, style={'height': '250px'}),
                                        style={'margin': '3px', 'border-radius': '5px', 'overflow': 'hidden'} 
                                    ), 
                                ],sm=6, style={'padding': '0px'}),
                                dbc.Col([
                                    dbc.Card(
                                        dcc.Graph(id='fig_ocorrencias_por_raca', config={'displayModeBar': False, 'staticPlot': False}, style={'height': '250px'}),
                                        style={'margin': '3px', 'border-radius': '5px', 'overflow': 'hidden'} 
                                    ),
                                ],sm=3, style={'padding': '0px'}),
                                dbc.Col([
                                    dbc.Card(
                                        dcc.Graph(id='fig_ocorrencias_por_situacao_animal', config={'displayModeBar': False, 'staticPlot': False}, style={'height': '250px'}),
                                        style={'margin': '3px', 'border-radius': '5px', 'overflow': 'hidden'} 
                                    ),
                                ],sm=3, style={'padding': '0px'}),
                            ], style={'justify-content': 'center', 'background-color': '#e9e9e9'}),
                            
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card(
                                        dcc.Graph(id='fig_mapa_ocorrencias', config={'displayModeBar': False, 'staticPlot': False}, style={'height': '250px'}),
                                        style={'margin': '3px', 'border-radius': '5px', 'overflow': 'hidden'} 
                                    ),
                                ],sm=12, style={'padding': '0px'}),
                                
                            ], style={'justify-content': 'center', 'background-color': '#e9e9e9'}),
                        ], style={'justify-content': 'center', 'background-color': '#e9e9e9'}),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Card(
                                    dag.AgGrid(
                                        id='grid_ocorrencias',
                                        rowData=[],
                                        columnDefs=[],
                                        defaultColDef={},
                                        dashGridOptions={"enableAdvancedFilter": False, "domLayout": "autoHeight"},
                                        columnSize="responsiveSizeToFit",
                                        enableEnterpriseModules=True,  
                                    ), style={'margin': '3px', 'border-radius': '5px', 'overflow': 'hidden'} 
                                ),
                            ], style={'justify-content': 'center', 'background-color': '#e9e9e9'})
                        ]),
                    ], style={'justify-content': 'center', 'background-color': '#e9e9e9'})
                )
            ])
        ])
    ])

