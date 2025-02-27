# ===== Importar as bibliotecas ===== #

from dash import html, dcc, Input, Output, dash_table, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template('bootstrap')

# ===== Layout da página ===== #
layout = html.Div(
    style={
        'height': '100vh',  
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center'
    },
    children=[
        dbc.Container(
            style={
                'textAlign': 'center',
                'padding': '30px',
                'border': '1px solid #ccc',
                'border-radius': '10px',
                'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)',
                'background-color': '#ffffff',
                'maxWidth': '500px'
            },
            children=[
                html.Img(
                    src='/assets/logo_index.png', 
                    style={'width': '150px', 'margin-bottom': '20px'}
                ),
                html.H1("Bem-vindo ao Harpia Dashbords!"),
                html.P("Informe seu usuário e senha para começar."),
                dbc.Label('Usuário'),
                dbc.Input(id='nome_usuario', placeholder='Digite o seu usuário aqui', persistence=False, style={'textAlign': 'center', 'width': '100%'}),
                dbc.Label('Senha'),
                dbc.Input(id='senha_usuario', placeholder='Digite a sua senha aqui', type='password', persistence=False, style={'textAlign': 'center', 'width': '100%'}),
                dbc.Button('Login', id='botao_login', className='mt-3', n_clicks=0, color='success'),
                html.Div(id='login_message', style={'margin-top': '10px', 'color': 'red'})
            ]
        )
    ]
)
