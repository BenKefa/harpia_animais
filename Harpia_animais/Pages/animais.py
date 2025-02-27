# ===== Importar as bibliotecas ===== #

from dash import html, dcc, Input, Output, dash_table, State
import plotly.express as px
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from Pages.dados import *
import datetime
from datetime import date

load_figure_template('lux')
# ===== Criar o Layout do sistema - Aqui são configurados os espaços e imagens do aplicativo ===== #
layout = html.Div(children=[
    dcc.Interval(id='atualizacao_automatica', interval=300000, n_intervals=0), # Atualização automática por intervalo de tempo
    
# Cada modal está marcado com um número para facilitar a identificação, começando com m001, m002, etc. 
# No código, cada modal é chamado pelo id, por exemplo, id='modal_filtros', id='modal_confirmacao', etc. e identificado na página
# Harpia_Animais.py nos seus respectivos callbacks.
    

# Modal onde ficam os filtros do dashboard (m001)
    dbc.Row([
        dbc.Modal([
            dbc.ModalHeader(
                dbc.Row([ 
                    dbc.Col([dbc.ModalTitle('Filtros')], width=8), 
                    dbc.Col([html.Span('m001', style={'color': 'transparent'})], width=4) 
                ]),
            ),
            dbc.ModalBody(
                dbc.Row([ 
                    dbc.Card([
                        html.H5('Data de ocorrência:', style={'textAlign': 'center'}),
                            html.Div([
                                dcc.DatePickerRange(id='filtro_data', start_date_placeholder_text='Data Início', end_date_placeholder_text='Data Fim',persistence=True, display_format='DD/MM/YYYY'),
                            ]),
                        html.H5('Situação da ocorrência:', style={'textAlign': 'center'}),
                        dcc.Dropdown(ocorrencia['nomesituacao'].value_counts().index, id='dropdown_situacao_filtro', placeholder='Selecione uma situação para filtrar', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=True),
                        html.H5('Bairro:', style={'textAlign': 'center'}),
                        dcc.Dropdown(bairro['nomebairro'].value_counts().index, id='dropdown_nomebairro_filtro', placeholder='Selecione uma bairro para filtrar', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        html.H5('Situação do animal:', style={'textAlign': 'center'}),
                        dcc.Dropdown(situacaoanimal['nomesituacaoanimal'].value_counts().index, id='dropdown_nomesituacaoanimal_filtro', placeholder='Selecione uma situação do animal para filtrar', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        html.H5('Grupo de animal:', style={'textAlign': 'center'}),
                        dcc.Dropdown(grupoanimal['nomegrupoanimal'].value_counts().index, id='dropdown_nomegrupoanimal_filtro', placeholder='Selecione um grupo para filtrar', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        html.H5('Raça de animal:', style={'textAlign': 'center'}),
                        dcc.Dropdown(racaanimal['nomeracaanimal'].value_counts().index, id='dropdown_nomeracaanimal_filtro', placeholder='Selecione uma raça para filtrar', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                    ], style={'border':'none'})
                ]),
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Fechar', id='botao_fechar_modal_filtros', className='ms-auto', n_clicks=0, color='danger')
                ])
            ])
        ], id='modal_filtros', is_open=False,  centered=True, size = 'lg'),
        
        # Modal de Confirmação de salvamentos (m002)
        dbc.Modal([
            dbc.ModalHeader(
                dbc.Row([ 
                    dbc.Col([html.Span('m002', style={'color': 'transparent'})], width=1),
                    html.Div(id='mensagem_nomesituacaoanimal_alterado'),
                    html.Div(id='mensagem_nomesituacaoanimal_salvo'),
                    html.Div(id='mensagem_nomeracaanimal_alterado'),
                    html.Div(id='mensagem_nomeracaanimal_salvo'),
                    html.Div(id='mensagem_nomegrupoanimal_alterado'),
                    html.Div(id='mensagem_nomegrupoanimal_salvo'),
                ]),
                close_button=False
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Confirmar', id='botao_confirmar_modal_confirmacao', className='ms-auto', n_clicks=0, color='success')
                ])
            ])
        ], id='modal_confirmacao', is_open=False,  centered=True, keyboard=False, backdrop=True, size = 'sm'),
        
        # Modal de Confirmação de salvamentos (m011)
        dbc.Modal([
            dbc.ModalHeader(
                dbc.Row([ 
                    dbc.Col([html.Span('m011', style={'color': 'transparent'})], width=1),
                    html.Div(id='mensagem_ocorrencia_alterada'),
                    html.Div(id='mensagem_ocorrencia_salvo'),
                ]),
                close_button=False
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Confirmar', id='botao_confirmar_modal_confirmacao_ocorrencia', className='ms-auto', n_clicks=0, color='success')
                ])
            ])
        ], id='modal_confirmacao_ocorrencia', is_open=False,  centered=True, keyboard=False, backdrop=True, size = 'sm'),
        
        


        # Modal onde Lançamento de Ocorrencias (m003)
        dbc.Modal([
            dbc.ModalHeader(
                dbc.Row([ 
                    dbc.Col([dbc.ModalTitle('Lançamento de Ocorrências')], width=11), 
                    dbc.Col([html.Span('m003', style={'color': 'transparent'})], width=1) 
                ]),
            ),
            dbc.ModalBody(
                dbc.Row([
                    dbc.Card([
                        dbc.Label('Data de Ocorrência'),
                        html.Div([
                            dcc.DatePickerSingle(id='data_lancamento_ocorrencia', placeholder='Data', persistence=False, display_format='DD/MM/YYYY', date=date.today()),
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
                        
                    ], style={'border':'none'})
                ]),            
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Salvar', id='botao_salvar_lancamento_ocorrencia', className='ms-auto', n_clicks=0, color='success'),
                    dbc.Button('Fechar', id='botao_fechar_modal_lancamento_ocorrencia', className='ms-auto', n_clicks=0, color='danger')
                ])
            ])
        ], id='modal_lancamento_ocorrencia', is_open=False, scrollable=True, centered=True, size = 'lg'),
        
        # Modal onde as ocorrencias são quitadas ou excluídas (m004)
        dbc.Modal([
                dbc.ModalHeader(
                    dbc.Row([
                        dbc.Col([dbc.ModalTitle('Atendimento de ocorrencias')], width=11), 
                        dbc.Col([html.Span('m004', style={'color': 'transparent'})], width=1) 
                    ]) 
                ),
                dbc.ModalBody(
                    dbc.Row([
                            dbc.Card([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label('Situação'),
                                    dcc.Dropdown(ocorrencia['nomesituacao'].value_counts().index, id='dropdown_situacao_alteracao_ocorrencia', placeholder='Selecione uma ocorrencia para quitar ou excluir', 
                                    multi=False, optionHeight=60, maxHeight=200, persistence=True),
                                ], width=12),
                            ]),
                            
                            dbc.Row([
                                dbc.Label(' '),
                            ]),
                            
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label('Data de atendimento'),
                                    html.Div([
                                    dcc.DatePickerSingle(id='data_atendimento_ocorrencia', placeholder='Data', persistence=False, display_format='DD/MM/YYYY', date=date.today()),
                                ]),
                                ], width=4),
                            ]),
                            
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label('Ocorrência'),
                                    dcc.Dropdown(ocorrencia['nome_ocorrencia_completo'].value_counts().index, id='dropdown_alteracao_ocorrencia', placeholder='Selecione uma ocorrência para quitar ou excluir', 
                                    multi=False, optionHeight=60, maxHeight=200, persistence=False),
                                    
                                    dbc.Label('Observações'),
                                    dbc.Textarea(id='observacao_atendimento_ocorrencia'),
                                    
                                    dbc.Label('Ações tomadas'),
                                    dbc.Textarea(id='solucao_atendimento_ocorrencia'),
                                    
                                    dbc.Label('Atender ou excluir ocorrencia'),
                                    dcc.Dropdown(['Atender', 'Excluir', 'Reabrir'], id='dropdown_atender_excluir_ocorrencia', placeholder='Selecione uma ocorrencia para quitar ou excluir', 
                                    multi=False, optionHeight=60, maxHeight=200, persistence=False),
                                    
                                    
                                ], width=12),
                            ]),
                        ], style={'border':'none'})
                    ])
                ),
                dbc.ModalFooter([
                    dbc.ButtonGroup([
                        dbc.Button('Salvar', id='botao_salvar_alteracao_ocorrencia', className='ms-auto', n_clicks=0, color='success'),
                        dbc.Button('Fechar', id='botao_fechar_modal_alteracao_ocorrencia', className='ms-auto', n_clicks=0, color='danger')
                    ])
                ])
            ], id='modal_alteracao_ocorrencia', is_open=False,  scrollable=True, centered=True, size = 'lg'),
        

        
        # Modal Cadastro de Grupos (m005)
        dbc.Modal([ 
            dbc.ModalHeader(
                dbc.Row([
                    dbc.Col([dbc.ModalTitle('Cadastro de grupos')], width=11), 
                    dbc.Col([html.Span('m005', style={'color': 'transparent'})], width=1) 
                ]) 
            ),
            dbc.ModalBody(
                    dbc.Card([
                    dbc.Row([
                        dbc.Label('Nome do grupo'),
                        dbc.Input(id='cadastro_nomegrupoanimal', placeholder='Informe um grupo de animal (gato/cachorro/etc.)', persistence=False),
                        
                    ]),       
                ], style={'border':'none'})     
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Alterar', id='botao_alterar_cadastro_nomegrupoanimal', className='ms-auto', n_clicks=0, color='danger'),
                    dbc.Button('Salvar', id='botao_salvar_cadastro_nomegrupoanimal', className='ms-auto', n_clicks=0, color='success')
                ])
            ])
        ], id='modal_cadastro_nomegrupoanimal', is_open=False,  centered=True, size = 'lg'),
        
        # Modal Alteração de Grupos (m006)
        dbc.Modal([ 
            dbc.ModalHeader(
                dbc.Row([
                    dbc.Col([dbc.ModalTitle('Alteração de grupos')], width=11), 
                    dbc.Col([html.Span('m006', style={'color': 'transparent'})], width=1) 
                ])
            ),
            dbc.ModalBody(
                    dbc.Card([
                    dbc.Row([
                        dbc.Label('Grupo do animal'),
                        dcc.Dropdown(grupoanimal['nomegrupoanimal'].value_counts().index, id='dropdown_nomegrupoanimal_alteracao_grupo', placeholder='Selecione um grupo', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        dbc.Label('Novo nome do grupo'),
                        dbc.Input(id='alteracao_nomegrupoanimal', placeholder='Informe um novo nome de grupo de animal (gato/cachorro/etc.)', persistence=False),
                        dbc.Label('Atender ou excluir grupo'),
                        dcc.Dropdown(['Alterar', 'Excluir'], id='dropdown_alterar_excluir_grupo', placeholder='Selecione um grupo para alterar ou excluir', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                                    
                        
                    ]),       
                ], style={'border':'none'})     
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Salvar', id='botao_salvar_alteracao_nomegrupo_animal', className='ms-auto', n_clicks=0, color='success')
                ])
            ])
        ], id='modal_alteracao_nomegrupoanimal', is_open=False,  centered=True, size = 'lg'),

        # Modal Cadastro de Raças (m007)
        dbc.Modal([
            dbc.ModalHeader(
                dbc.Row([
                    dbc.Col([dbc.ModalTitle('Cadastro de raças')], width=10), 
                    dbc.Col([html.Span('m007', style={'color': 'transparent'})], width=2) 
                ])
            ),
            dbc.ModalBody(
                dbc.Row([
                        dbc.Card([
                        dbc.Label('Nome da raça'),
                        dbc.Input(id='cadastro_nomeracaanimal', placeholder='Informe uma raça de animal (Golden, Pastor Alemão, etc.)', persistence=False),
                        dbc.Label('Grupo do animal'),
                        dcc.Dropdown(grupoanimal['nomegrupoanimal'].value_counts().index, id='dropdown_nomegrupoanimal_cadastro_raca', placeholder='Selecione um grupo', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        
                    ], style={'border':'none'})
                ]),            
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Alterar', id='botao_alterar_cadastro_nomeracaanimal', className='ms-auto', n_clicks=0, color='danger'),
                    dbc.Button('Salvar', id='botao_salvar_cadastro_nomeracaanimal', className='ms-auto', n_clicks=0, color='success'),
                ])
            ])
        ], id='modal_cadastro_nomeracaanimal', is_open=False,  centered=True, size = 'lg'),
        
        # Modal Alteração de racas (m008)
        dbc.Modal([ 
            dbc.ModalHeader(
                dbc.Row([
                    dbc.Col([dbc.ModalTitle('Alteração de raças')], width=10), 
                    dbc.Col([html.Span('m008', style={'color': 'transparent'})], width=2) 
                ])
            ),
            dbc.ModalBody(
                    dbc.Card([
                    dbc.Row([
                        dbc.Label('Raça do animal'),
                        dcc.Dropdown(racaanimal['nomeracaanimal'].value_counts().index, id='dropdown_nomeracaanimal_alteracao_raca', placeholder='Selecione uma raça', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        dbc.Label('Novo nome da raça'),
                        dbc.Input(id='alteracao_nomeracaanimal', placeholder='Informe um novo nome da raca de animal', persistence=False),
                        dbc.Label('Atender ou excluir raca'),
                        dcc.Dropdown(['Alterar', 'Excluir'], id='dropdown_alterar_excluir_raca', placeholder='Selecione uma raca para alterar ou excluir', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                                    
                        
                    ]),       
                ], style={'border':'none'})     
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Salvar', id='botao_salvar_alteracao_nomeraca_animal', className='ms-auto', n_clicks=0, color='success')
                ])
            ])
        ], id='modal_alteracao_nomeracaanimal', is_open=False,  centered=True, size = 'lg'),
        
        # Modal Cadastro de Situações (m009)
        dbc.Modal([
            dbc.ModalHeader(
                dbc.Row([
                    dbc.Col([dbc.ModalTitle('Cadastro de situações')], width=11), 
                    dbc.Col([html.Span('m009', style={'color': 'transparent'})], width=1) 
                ])
            ),
            dbc.ModalBody(
                dbc.Row([
                        dbc.Card([
                        dbc.Label('Situação do animal'),
                        dcc.Dropdown(gruposituacao['nomegruposituacao'].value_counts().index, id='dropdown_nomegruposituacao_cadastro_situacao', placeholder='Selecione um grupo', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        dbc.Label('Nome da situação'),
                        dbc.Input(id='cadastro_nomesituacaoanimal', placeholder='Informe uma situação do animal (Machucado, Doente, com filhotes, etc.)', persistence=False),
                        
                    ], style={'border':'none'})
                ]),            
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Alterar', id='botao_alterar_cadastro_nomesituacaoanimal', className='ms-auto', n_clicks=0, color='danger'),
                    dbc.Button('Salvar', id='botao_salvar_cadastro_nomesituacaoanimal', className='ms-auto', n_clicks=0, color='success'),
                ])
            ])
        ], id='modal_cadastro_nomesituacaoanimal', is_open=False,  centered=True, size = 'lg'),
        
        # Modal Alteração de situacaos (m010)
        dbc.Modal([ 
            dbc.ModalHeader(
                dbc.Row([
                    dbc.Col([dbc.ModalTitle('Alteração de situações')], width=11), 
                    dbc.Col([html.Span('m010', style={'color': 'transparent'})], width=1) 
                ])
            ),                
            dbc.ModalBody(
                    dbc.Card([
                    dbc.Row([
                        dbc.Label('Nome da Situação'),
                        dcc.Dropdown(situacaoanimal['nomesituacaoanimal'].value_counts().index, id='dropdown_nomesituacaoanimal_alteracao_situacao', placeholder='Selecione uma raça', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                        dbc.Label('Novo nome da situação'),
                        dbc.Input(id='alteracao_nomesituacaoanimal', placeholder='Informe um novo nome da situacao de animal', persistence=False),
                        dbc.Label('Atender ou excluir situacao'),
                        dcc.Dropdown(['Alterar', 'Excluir'], id='dropdown_alterar_excluir_situacao', placeholder='Selecione uma situacao para alterar ou excluir', 
                        multi=False, optionHeight=60, maxHeight=200, persistence=False),
                                    
                        
                    ]),       
                ], style={'border':'none'})     
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                    dbc.Button('Salvar', id='botao_salvar_alteracao_nomesituacao_animal', className='ms-auto', n_clicks=0, color='success')
                ])
            ])
        ], id='modal_alteracao_nomesituacaoanimal', is_open=False,  centered=True, size = 'lg'),
        
        # Relatório de Ocorrências por bairro (m012)
        dbc.Modal([
            dbc.ModalHeader(
                dbc.Row([
                    dbc.Col([dbc.ModalTitle('Relatório de ocorrências por bairro')], width=11), 
                    dbc.Col([html.Span('m012', style={'color': 'transparent'})], width=1) 
                ]),
            ),
            dbc.ModalBody(
                dbc.Row([
                    dash_table.DataTable(
                        id='tabela_ocorrencias_por_bairro', 
                        columns = [], 
                        data = [], 
                        # Os campos abaixo são opcionais e podem ser utilizados para exportar a tabela para excel, por exemplo
                        #filter_action='native', 
                        #sort_action="native",
                        #sort_mode="multi",
                        persistence=True,
                        #export_format='xlsx',
                        #export_headers='display',  
                        style_table={'overflowX': 'auto'}, 
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white',
                            'textAlign': 'left',
                            'whiteSpace': 'normal'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(220, 220, 220)',
                            }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold',
                            'textAlign': 'left',
                            'whiteSpace': 'normal'
                        }
                    )
                ]),
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                ])
            ])
        ], id='modal_relatorio_ocorrencias_por_bairro', is_open=False,  centered=True, fullscreen=True),
            
        # Relatório de Ocorrências por grupo de animal (m013)
        dbc.Modal([
            dbc.ModalHeader(
                dbc.Row([
                    dbc.Col([dbc.ModalTitle('Relatório de ocorrências por grupo de nimal')], width=11), 
                    dbc.Col([html.Span('m013', style={'color': 'transparent'})], width=1) 
                ]),
            ),
            dbc.ModalBody(
                dbc.Row([
                    dash_table.DataTable(
                        id='tabela_ocorrencias_por_grupo_de_animal', 
                        columns = [], 
                        data = [], 
                        #filter_action='native', 
                        #sort_action="native",
                        #sort_mode="multi",
                        persistence=True,
                        #export_format='xlsx',
                        #export_headers='display',  
                        style_table={'overflowX': 'auto'}, 
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white',
                            'textAlign': 'left',
                            'whiteSpace': 'normal'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(220, 220, 220)',
                            }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold',
                            'textAlign': 'left',
                            'whiteSpace': 'normal'
                        }
                    )
                ]),
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                ])
            ])
        ], id='modal_relatorio_ocorrencias_por_grupo_de_animal', is_open=False,  centered=True, fullscreen=True),
        
        # Relatório de Ocorrências por situação do animal (m014)
        dbc.Modal([
            dbc.ModalHeader(
                dbc.Row([
                    dbc.Col([dbc.ModalTitle('Relatório de ocorrências por situação do nimal')], width=11), 
                    dbc.Col([html.Span('m014', style={'color': 'transparent'})], width=1) 
                ]),
            ),
            dbc.ModalBody(
                dbc.Row([
                    dash_table.DataTable(
                        id='tabela_ocorrencias_por_situacao_do_animal', 
                        columns = [], 
                        data = [], 
                        #filter_action='native', 
                        #sort_action="native",
                        #sort_mode="multi",
                        persistence=True,
                        #export_format='xlsx',
                        #export_headers='display',  
                        style_table={'overflowX': 'auto'}, 
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white',
                            'textAlign': 'left',
                            'whiteSpace': 'normal'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(220, 220, 220)',
                            }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold',
                            'textAlign': 'left',
                            'whiteSpace': 'normal'
                        }
                    )
                ]),
            ),
            dbc.ModalFooter([
                dbc.ButtonGroup([
                ])
            ])
        ], id='modal_relatorio_ocorrencias_por_situacao_do_animal', is_open=False,  centered=True, fullscreen=True),
            
        
        # == Dashboard == #  
        
        dbc.Col([
            dbc.Label('CONTROLE DE ANIMAIS', style={'color': 'white', 'font-weight': 'bold', 'font-size': '20px', 'margin-left': '15px'}),
            html.Br(),
            dbc.DropdownMenu(
            label=[
            html.I(className='fas fa-database', style={'margin-right': '5px'}),
            'Cadastros'
            ],
            children=[
            dbc.DropdownMenuItem('Grupos', id='botao_modal_cadastro_gruposanimais_navbar', n_clicks=0),
            dbc.DropdownMenuItem('Raças', id='botao_modal_cadastro_racasanimais_navbar', n_clicks=0),
            dbc.DropdownMenuItem('Situações', id='botao_modal_cadastro_situacaoanimais_navbar', n_clicks=0),
            ],
            className='custom-dropdown-button',
            style={'color': 'grey'}
            ),
            dbc.DropdownMenu(
            label=[
            html.I(className='fas fa-file-alt', style={'margin-right': '5px'}),
            'Relatórios'
            ],
            children=[
            dbc.DropdownMenuItem('Ocorrências por bairro', id='botao_modal_relatorio_ocorrencias_por_bairro_navbar', n_clicks=0),
            dbc.DropdownMenuItem('Ocorrências por grupo de animal', id='botao_modal_relatorio_ocorrencias_por_grupo_de_animal_navbar', n_clicks=0),
            dbc.DropdownMenuItem('Ocorrências por situação do animal', id='botao_modal_relatorio_ocorrencias_por_situacao_di_animal_navbar', n_clicks=0),
            ],
            className='custom-dropdown-button',
            style={'color': 'grey'}
            ),
            
            dbc.Button([
            html.I(className='fas fa-filter', style={'margin-right': '5px'}),
            'Filtros'
            ], id='botao_modal_filtros', color='black', style={'color': 'grey'}),
            html.Br(),
            dbc.Button([
            html.I(className='fas fa-plus-circle', style={'margin-right': '5px'}),
            'Lançar Ocorrência'
            ], id='botao_modal_lancamento_ocorrencia', color='black', style={'color': 'grey'}),
            html.Br(),
            dbc.Button([
            html.I(className='fas fa-hand-holding-medical', style={'margin-right': '5px'}),
            'Atender Ocorrência'
            ], id='botao_modal_atendimento_ocorrencia', color='black', style={'color': 'grey'}),
        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'background-color': 'black'}),
        
        # == Criar um Card com uma linha, contendo informações (não gráficos) == #
        dbc.Col([
            dbc.Card([
                dcc.Loading(
                    id='loading_dashboard', type='circle', fullscreen=True, style={'backgroundColor': 'rgba(0,0,0,0)'},
                    children=dbc.Row([
                        # Primeira linha de cards com informações
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    
                                        dbc.Col([
                                            html.I(className='fas fa-bullhorn', style={'color': '#4A4633', 'margin': '10px'})
                                        ], width='auto'),
                                        dbc.Col([
                                            dbc.Row([
                                                dbc.Label('Ocorrências relatadas', style={'textAlign': 'center', 'font-size': 'large', 'color': '#4A4633'}),
                                            ]),
                                            dbc.Row([
                                                dbc.Label(id='fig_ocorrencias_relatadas', style={'textAlign': 'center', 'font-size': 'large', 'color': '#4A4633', 'font-weight': 'bold'}),
                                            ]), 
                                        ])
                                    
                                ], style={
                                    'margin': '3px',
                                    'backgroundColor': '#Ffffff'
                                }),
                            ], md=4),
                            dbc.Col([
                                dbc.Card([
                                    dbc.Row([
                                        dbc.Col([
                                            html.I(className='fas fa-check-circle', style={'font-size': '30px', 'color': '#3B6CFF', 'margin': '10px'})
                                        ], width='auto'),
                                        dbc.Col([
                                            dbc.Row([
                                                dbc.Label('Ocorrências resolvidas', style={'textAlign': 'center', 'font-size': 'large', 'color': '#3B6CFF'}),
                                            ]),
                                            dbc.Row([
                                                dbc.Label(id='fig_ocorrencias_resolvidas', style={'textAlign': 'center', 'font-size': 'large', 'color': '#3B6CFF', 'font-weight': 'bold'}),
                                            ]), 
                                        ])
                                    ])
                                ], style={
                                    'margin': '3px',
                                    'backgroundColor': '#Ffffff'
                                }),
                            ], md=4),
                            dbc.Col([
                                dbc.Card([
                                    dbc.Row([
                                        dbc.Col([
                                            html.I(className='fas fa-clock', style={'font-size': '30px', 'color': '#802922', 'margin': '10px'})
                                        ], width='auto'),
                                        dbc.Col([
                                            dbc.Row([
                                                dbc.Label('Ocorrências pendentes', style={'textAlign': 'center', 'font-size': 'large', 'color': '#802922'}),
                                            ]),
                                            dbc.Row([
                                                dbc.Label(id='fig_ocorrencias_pendentes', style={'textAlign': 'center', 'font-size': 'large', 'color': '#802922', 'font-weight': 'bold'}),
                                            ]), 
                                        ])
                                    ])
                                ], style={
                                    'margin': '3px',
                                    'backgroundColor': '#Ffffff'
                                }),
                            ], md=4),
                        ], className='h-10', style={'justify-content': 'center', 'background-color': '#F8F8FF'}),

                        # Segunda linha com gráficos de ocorrências
                        dbc.Row([
                            dbc.Col([
                                dbc.Card(
                                    dcc.Graph(id='fig_mapa_ocorrencias', config={'displayModeBar': False, 'staticPlot': False}, style={'height': '508px'}),
                                    style={'margin': '3px', 'border-radius': '5px', 'overflow': 'hidden'}
                                ),
                            ], sm=6),
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            dcc.Graph(id='fig_ocorrencias_por_periodo', config={'displayModeBar': False, 'staticPlot': False}, style={'height': '250px'}),
                                            style={'margin': '3px', 'border-radius': '5px', 'overflow': 'hidden'}
                                        ),    
                                    ], sm=12)  
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            dcc.Graph(id='fig_ocorrencias_por_bairro', config={'displayModeBar': False, 'staticPlot': False}, style={'height': '250px'}),
                                            style={'margin': '3px', 'border-radius': '5px', 'overflow': 'hidden'}
                                        ),    
                                    ], sm=12)
                                    
                                ]),
                                
                                
                            ], sm=6),
                        ], style={'justify-content': 'center', 'background-color': '#F8F8FF'}),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Card(
                                    dcc.Graph(id='fig_ocorrencias_por_grupo', config={'displayModeBar': False, 'staticPlot': False}, style={'height': '250px'}),
                                    style={'margin': '3px', 'border-radius': '5px', 'overflow': 'hidden'}
                                ),
                            ], sm=6),
                            dbc.Col([
                                dbc.Card(
                                    dcc.Graph(id='fig_ocorrencias_por_situacao_animal', config={'displayModeBar': False, 'staticPlot': False}, style={'height': '250px'}),
                                    style={'margin': '3px', 'border-radius': '5px', 'overflow': 'hidden'}
                                ),    
                            ], sm=6)
                            
                        ]),

                        # Linha com a grade de ocorrências
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
                            ], className='h-10', style={'justify-content': 'center', 'background-color': '#F8F8FF'})
                        ]),
                    ], className='h-10', style={'justify-content': 'center', 'background-color': '#F8F8FF'})
                )
            ])
        ], xs=10, sm=10, md=10, lg=10, xl=10)
        
    ])
])
