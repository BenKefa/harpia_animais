# ===== Importar as bibliotecas ===== #


### Essa página é responsável por gerenciar os cadastros de empresas e usuários do sistema, não está funcional, 
# pode ignorar no projeto ou continuar para cadastrar usuários, empresas, 
# prestadores de serviços, etc. diretamente por aqui. ###

from dash import html, dcc, Input, Output, dash_table, State
import plotly.express as px
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from Pages.dados import *
import datetime
from datetime import date

load_figure_template('bootstrap')
layout = html.Div(children=[
    dcc.Interval(id='atualizacao_automatica', interval=300000, n_intervals=0),

# Modal onde ficam os filtros do dashboard
    dbc.Row([
        dbc.Card([   
                dbc.Navbar([
                    dbc.DropdownMenu(
                                    label='Cadastros',
                                    children=[
                                        dbc.DropdownMenuItem('Empresas', id='botao_modal_cadastro_empresas_navbar', n_clicks=0),
                                        dbc.DropdownMenuItem('Usuários', id='botao_modal_cadastro_usuarios_navbar', n_clicks=0),
                                    ], className='custom-dropdown-button'),
                    html.Div(id='resultado_botao_atualizar')      
                ],
                color='black',
                dark=True,
                className='custom-navbar',
                sticky='down',
                    )
            ]),
            
            # Cadastro de empresas - Modal onde ficam os cadastros de empresas
            dbc.Modal([
                    dbc.ModalHeader(
                        dbc.ModalTitle('Cadastro de empresas')),
                    dbc.ModalBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Nome'),
                                dbc.Input(id='nome_empresa', placeholder='Informe o nome da empresa', persistence=False),
                        html.Div(id='mensagem_empresa_salvo')
                            ], width=12  ),
                        ]),
                    ]),
                    dbc.ModalFooter([
                        dbc.ButtonGroup([
                            dbc.Button('Empresas', id='botao_empresas_cadastro_empresas', className='ms-auto', n_clicks=0, color='primary'),
                        ]),
                        dbc.ButtonGroup([
                            dbc.Button('Salvar', id='botao_salvar_cadastro_empresas', className='ms-auto', n_clicks=0, color='success'),
                            dbc.Button('Fechar', id='botao_fechar_modal_cadastro_empresas', className='ms-auto', n_clicks=0, color='danger')
                        ])
                    ])
                ], id='modal_cadastro_empresas', is_open=False,  centered=True, size = 'lg'),
            
            # Alteração cadastro de empresas - Modal onde alteramos os cadastros de empresas
            dbc.Modal([
                    dbc.ModalHeader(
                        dbc.ModalTitle('Alteração cadastro de empresas')),
                    dbc.ModalBody([
                        dbc.Label('Alterar empresa'),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Nome'),
                                dbc.Input(id='alteracao_nome_empresa', placeholder='Informe o nome da empresa', persistence=False),
                                                       
                            ], width=12),
                            
                        dbc.Label('Alterar ou excluir empresa'),
                                dbc.Checklist(
                                options=[{"label": 'Excluir', "value": 1}],
                                value=[0],
                                id='swich_alterar_excluir_empresa',
                                switch=True),
                        html.Div(id='mensagem_empresa_alterado')
                        ]),
                    ]),
                    dbc.ModalFooter([
                        dbc.ButtonGroup([
                            dbc.Button('Salvar', id='botao_alterar_cadastro_empresas', className='ms-auto', n_clicks=0, color='success'),
                            dbc.Button('Fechar', id='botao_fechar_modal_alteracao_empresas', className='ms-auto', n_clicks=0, color='danger')
                        ])
                    ])
                ], id='modal_alteracao_empresas', is_open=False,  centered=True, size = 'lg'),
            
            # Cadastro de empresas - Modal onde ficam os cadastros de usuários
            dbc.Modal([
                    dbc.ModalHeader(
                        dbc.ModalTitle('Cadastro de usuários')),
                    dbc.ModalBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Nome'),
                                dbc.Input(id='nome_usuario', placeholder='Informe o nome do usuario', persistence=False),
                                dbc.Label('Senha'),
                                dbc.Input(id='nome_usuario', placeholder='Informe uma senhapara o usuario', persistence=False),
                                dbc.Label('Permissões'),
                                dbc.Input(id='permissoes_usuario', placeholder='Informe as permissõa do usuario', persistence=False),
                        html.Div(id='mensagem_usuario_salvo')
                            ], width=12  ),
                        ]),
                    ]),
                    dbc.ModalFooter([
                        dbc.ButtonGroup([
                            dbc.Button('Usuários', id='botao_usuarios_cadastro_usuarios', className='ms-auto', n_clicks=0, color='primary'),
                        ]),
                        dbc.ButtonGroup([
                            dbc.Button('Salvar', id='botao_salvar_cadastro_usuarios', className='ms-auto', n_clicks=0, color='success'),
                            dbc.Button('Fechar', id='botao_fechar_modal_cadastro_usuarios', className='ms-auto', n_clicks=0, color='danger')
                        ])
                    ])
                ], id='modal_cadastro_usuarios', is_open=False,  centered=True, size = 'lg'),
            
            # Alteração cadastro de usuários - Modal onde alteramos os cadastros de usuários
            dbc.Modal([
                    dbc.ModalHeader(
                        dbc.ModalTitle('Alteração cadastro de usuários')),
                    dbc.ModalBody([
                        dbc.Label('Alterar usuário'),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Nome'),
                                dbc.Input(id='alteracao_nome_usuario', placeholder='Informe o nome do usuario', persistence=False),
                                                       
                            ], width=12),
                            
                        dbc.Label('Alterar ou excluir usuario'),
                                dbc.Checklist(
                                options=[{"label": 'Excluir', "value": 1}],
                                value=[0],
                                id='swich_alterar_excluir_usuario',
                                switch=True),
                        html.Div(id='mensagem_usuario_alterado')
                        ]),
                    ]),
                    dbc.ModalFooter([
                        dbc.ButtonGroup([
                            dbc.Button('Salvar', id='botao_alterar_cadastro_usuarios', className='ms-auto', n_clicks=0, color='success'),
                            dbc.Button('Fechar', id='botao_fechar_modal_alteracao_usuarios', className='ms-auto', n_clicks=0, color='danger')
                        ])
                    ])
                ], id='modal_alteracao_usuarios', is_open=False,  centered=True, size = 'lg'),
    ])
])
       
     
            
