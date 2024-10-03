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
    

# Modal onde ficam os filtros do dashboard
    dbc.Row([
        # == Criar um Card com uma linha, contendo informações (não gráficos) == #
            dbc.Card([
            # == Criar uma linha com os gráficos sobre o Kwid ==
                dcc.Loading(id='loading_dashboard', type = 'circle', fullscreen=True, style={'backgroundColor': 'rgba(0,0,0,0)'},
                    children=dbc.Row([
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
                            html.Div(id='mensagem_ocorrencia_salvo'),
                            dbc.Button('Salvar', id='botao_salvar_lancamento_ocorrencia', className='ms-auto', n_clicks=0, color='success'),
                    ]), 
                    ], style={'justify-content': 'center', 'background-color': '#e9e9e9'})
                )
            ])
        ])
    ])

