import dash
from dash import html, dcc, Input, Output, dash_table, State
import plotly.figure_factory as ff
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from Pages.dados import *
from Pages.login import layout as login_layout
from Pages.gerenciamento import layout as gerenciamento_layout
from Pages.animais import layout as animais_layout
from Pages.ocorrencias import layout as ocorrencias_layout
from Pages.pos_ocorrencia import layout as pos_ocorrencia_layout
from Pages.pos_ocorrencia_cancelada import layout as pos_ocorrencia_cancelada_layout

import locale
from dash.dash import no_update



# ===== Iniciar o app ===== #
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'], suppress_callback_exceptions=True)

app.title = 'Harpia Dashboards'
app._favicon = ("logo_index.ico") 

server=app.server

# ===== Navbar Dinâmico ===== #
def gerar_navbar(usuario):
    permissoes = USUARIOS_CADASTRADOS.get(usuario, {}).get('permissoes', [])
    navbar_children = [
        dbc.NavItem(dbc.NavLink([html.I(className='fas fa-paw'), ' Animais'], href='/animais')) if '/animais' in permissoes else None,
        dbc.NavItem(dbc.NavLink([html.I(className='fas fa-map-signs'), ' Mobilidade'], href='/mobilidade')) if '/mobilidade' in permissoes else None,
        dbc.NavItem(dbc.NavLink([html.I(className='fas fa-exclamation-triangle'), ' Ocorrências'], href='/ocorrencias')) if '/ocorrencias' in permissoes else None,
        dbc.NavItem(dbc.NavLink([html.I(className='fas fa-cog'), ' Gerenciamento'], href='/gerenciamento')) if '/gerenciamento' in permissoes else None,
        dbc.NavItem(dbc.NavLink([html.I(className='fas fa-sign-out-alt'), ' Sair'], href='/logout', id='logout-link')),
    ]
    return dbc.NavbarSimple(
        children=[child for child in navbar_children if child is not None],
        brand=html.Img(src='/assets/logo.png', height='40px'),
        color='black',
        dark=True,
        fluid=True,
        sticky='top',
    )

# ===== Layout do App ===== #
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='session_user', storage_type='session')
])

# ===== Callback para limpar sessão ao clicar em 'Sair' ===== #
@app.callback(
    Output('session_user', 'data'),
    Input('logout-link', 'n_clicks')
)
def logout(n_clicks):
    if n_clicks:
        return None
    return dash.no_update

# ===== Função de Verificação de Credenciais ===== #
def verificar_credenciais(usuario, senha):
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    return USUARIOS_CADASTRADOS.get(usuario, {}).get('senha') == senha_hash

# ===== Callbacks ===== #
# Navegação entre páginas e controle de acesso
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'), 
     Input('session_user', 'data')]
)
def display_page(pathname, session_user):
    permissoes = USUARIOS_CADASTRADOS.get(session_user, {}).get('permissoes', [])
    
    if pathname == '/logout':
        return login_layout

    # Páginas que não precisam de senha
    non_auth_pages = {
        '/ocorrencias': ocorrencias_layout,
        '/pos_ocorrencia': pos_ocorrencia_layout,
        '/pos_ocorrencia_cancelada': pos_ocorrencia_cancelada_layout
    }

    if pathname in non_auth_pages:
        return html.Div([non_auth_pages[pathname]])
    
    # Páginas que precisam de autenticação
    if session_user is None:
        return login_layout
    
    if pathname == '/animais' and '/animais' in permissoes:
        return html.Div([gerar_navbar(session_user), animais_layout])
    elif pathname == '/gerenciamento' and '/gerenciamento' in permissoes:
        return html.Div([gerar_navbar(session_user), gerenciamento_layout])
    
    return login_layout



# Login com redirecionamento para index_layout
@app.callback(
    [Output('session_user', 'data', allow_duplicate=True), 
     Output('login_message', 'children'), 
     Output('url', 'pathname')],
    [Input('botao_login', 'n_clicks')],
    [State('nome_usuario', 'value'), 
     State('senha_usuario', 'value')],
    prevent_initial_call=True
)
def fazer_login(n_clicks, nome_usuario, senha_usuario):
    if n_clicks > 0:
        if nome_usuario and senha_usuario and verificar_credenciais(nome_usuario, senha_usuario):
            return nome_usuario, '', '/animais'
        else:
            return None, 'Usuário ou senha incorretos', no_update
    return no_update, '', no_update
    
# ----------- Controle de telas do sistema ----------- #
    
# Controles sobre o Modal de Filtros do dashboard (m001)
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


# Controles sobre o Modal de Confirmação dos cadastros (m002)
@app.callback(
    Output('modal_confirmacao', 'is_open'),
    [Input('botao_salvar_cadastro_nomegrupoanimal', 'n_clicks'),
     Input('botao_salvar_alteracao_nomegrupo_animal', 'n_clicks'),
     Input('botao_salvar_cadastro_nomeracaanimal', 'n_clicks'),
     Input('botao_salvar_alteracao_nomeraca_animal', 'n_clicks'),
     Input('botao_salvar_cadastro_nomesituacaoanimal', 'n_clicks'),
     Input('botao_salvar_alteracao_nomesituacao_animal', 'n_clicks'),
     Input('botao_confirmar_modal_confirmacao', 'n_clicks'),     
    ],
    [State('modal_confirmacao', 'is_open')],
)
def modal_confirmacao(n1, n2, n3, n4, n5, n6, n7, is_open):
    if n1 or n2 or n3 or n4 or n5 or n6 or n7:
        return not is_open
    return is_open



# Callback para limpar o conteúdo do cabeçalho quando o modal de confirmação de cadastros é fechado
@app.callback(
    [Output('mensagem_nomesituacaoanimal_alterado', 'children', allow_duplicate=True),
     Output('mensagem_nomesituacaoanimal_salvo', 'children', allow_duplicate=True),
     Output('mensagem_nomeracaanimal_alterado', 'children', allow_duplicate=True),
     Output('mensagem_nomeracaanimal_salvo', 'children', allow_duplicate=True),
     Output('mensagem_nomegrupoanimal_alterado', 'children', allow_duplicate=True),
     Output('mensagem_nomegrupoanimal_salvo', 'children', allow_duplicate=True)],
    [Input('modal_confirmacao', 'is_open')],
    prevent_initial_call=True
)
def clear_modal_header(is_open):
    if not is_open:
        return '', '', '', '', '', ''
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Controles sobre o Modal de Confirmação das ocorrências (m011)
@app.callback(
    Output('modal_confirmacao_ocorrencia', 'is_open'),
    [Input('botao_salvar_lancamento_ocorrencia', 'n_clicks'),
     Input('botao_salvar_alteracao_ocorrencia', 'n_clicks'),
     Input('botao_confirmar_modal_confirmacao_ocorrencia', 'n_clicks'),     
    ],
    [State('modal_confirmacao_ocorrencia', 'is_open')],
)
def modal_confirmacao_ocorrencia(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open



# Callback para limpar o conteúdo do cabeçalho quando o modal de confirmação de ocorrencias é fechado (m011)
@app.callback(
    [Output('mensagem_ocorrencia_alterada', 'children', allow_duplicate=True),
     Output('mensagem_ocorrencia_salvo', 'children', allow_duplicate=True)],
    [Input('modal_confirmacao', 'is_open')],
    prevent_initial_call=True
)
def clear_modal_header(is_open):
    if not is_open:
        return '', ''
    return dash.no_update, dash.no_update

# Controles sobre o Modal de Confirmação das ocorrências (m111)
@app.callback(
    Output('modal_confirmacao_ocorrencia_01', 'is_open'),
    [Input('botao_salvar_lancamento_ocorrencia_01', 'n_clicks'),
     Input('botao_continuar_modal_confirmacao_ocorrencia_01', 'n_clicks'),   
    ],
    [State('modal_confirmacao_ocorrencia_01', 'is_open')],
)
def modal_confirmacao_ocorrencia_01(n1, n2, is_open):
    if n1 or n2:
        return not is_open 
    return is_open



# Callback para limpar o conteúdo do cabeçalho quando o modal de confirmação de ocorrencias é fechado (m111)
@app.callback(
    Output('mensagem_ocorrencia_salvo_01', 'children', allow_duplicate=True),
    Output('botao_cancelar_modal_confirmacao_ocorrencia_01', 'hidden'),
    Output('botao_continuar_modal_confirmacao_ocorrencia_01', 'hidden'),
    Input('modal_confirmacao_ocorrencia_01', 'is_open'),
    prevent_initial_call=True
)
def clear_modal_header(is_open):
    if not is_open:
        return '', True, True
    else:
        return dash.no_update, False, False 





# Controles sobre o Modal de Lançamento de ocorrências (m003)
@app.callback(
    Output('modal_lancamento_ocorrencia', 'is_open'),
    [Input('botao_modal_lancamento_ocorrencia', 'n_clicks'),
    Input('botao_fechar_modal_lancamento_ocorrencia', 'n_clicks')],
    [State('modal_lancamento_ocorrencia', 'is_open')],
)
def modal_lancamento_ocorrencia(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Controles sobre o Modal de Atendimento de ocorrências (m004)
@app.callback(
    Output('modal_alteracao_ocorrencia', 'is_open'),
    [Input('botao_modal_atendimento_ocorrencia', 'n_clicks'),
    Input('botao_fechar_modal_alteracao_ocorrencia', 'n_clicks')],
    [State('modal_alteracao_ocorrencia', 'is_open')],
)
def modal_alteracao_ocorrencia(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Controles sobre o Modal de Cadastro de Grupos (m005)
@app.callback(
    Output('modal_cadastro_nomegrupoanimal', 'is_open'),
    Input('botao_modal_cadastro_gruposanimais_navbar', 'n_clicks'),
    State('modal_cadastro_nomegrupoanimal', 'is_open'),
)
def modal_cadastro_nomegrupoanimal(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Controles sobre o Modal de Alteração de Grupos (m006)
@app.callback(
    Output('modal_alteracao_nomegrupoanimal', 'is_open'),
    Input('botao_alterar_cadastro_nomegrupoanimal', 'n_clicks'),
    State('modal_alteracao_nomegrupoanimal', 'is_open'),
)
def modal_alteracao_nomegrupoanimal(n1, is_open):
    if n1:
        return not is_open
    return is_open
 

# Controles sobre o Modal de Cadastro de Raças (m007)
@app.callback(
    Output('modal_cadastro_nomeracaanimal', 'is_open'),
    [Input('botao_modal_cadastro_racasanimais_navbar', 'n_clicks')],
    [State('modal_cadastro_nomeracaanimal', 'is_open')],
)
def modal_cadastro_nomeracaanimal(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Controles sobre o Modal de Alteração de racas (m008)
@app.callback(
    Output('modal_alteracao_nomeracaanimal', 'is_open'),
    Input('botao_alterar_cadastro_nomeracaanimal', 'n_clicks'),
    State('modal_alteracao_nomeracaanimal', 'is_open'),
)
def modal_alteracao_nomeracaanimal(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Controles sobre o Modal de Cadastro de Situações (m009)
@app.callback(
    Output('modal_cadastro_nomesituacaoanimal', 'is_open'),
    [Input('botao_modal_cadastro_situacaoanimais_navbar', 'n_clicks'),],
    [State('modal_cadastro_nomesituacaoanimal', 'is_open')],
)
def modal_cadastro_nomesituacaoanimal(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Controles sobre o Modal de Alteração de Situações (m010)
@app.callback(
    Output('modal_alteracao_nomesituacaoanimal', 'is_open'),
    [Input('botao_alterar_cadastro_nomesituacaoanimal', 'n_clicks'),],
    [State('modal_alteracao_nomesituacaoanimal', 'is_open')],
)
def modal_alteracao_nomesituacaoanimal(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Controles sobre o Modal Relatório de Ocorrências por bairro (m012)
@app.callback(
    Output('modal_relatorio_ocorrencias_por_bairro', 'is_open'),
    [Input('botao_modal_relatorio_ocorrencias_por_bairro_navbar', 'n_clicks'),],
    [State('modal_relatorio_ocorrencias_por_bairro', 'is_open')],
)
def modal_relatorio_ocorrencias_por_bairro(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Controles sobre o Modal Relatório de Ocorrências por grupo de animal (m013)
@app.callback(
    Output('modal_relatorio_ocorrencias_por_grupo_de_animal', 'is_open'),
    [Input('botao_modal_relatorio_ocorrencias_por_grupo_de_animal_navbar', 'n_clicks'),],
    [State('modal_relatorio_ocorrencias_por_grupo_de_animal', 'is_open')],
)
def modal_relatorio_ocorrencias_por_grupo_de_animal(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Controles sobre o Modal Relatório de Ocorrências por situação do animal (m014)
@app.callback(
    Output('modal_relatorio_ocorrencias_por_situacao_do_animal', 'is_open'),
    [Input('botao_modal_relatorio_ocorrencias_por_situacao_di_animal_navbar', 'n_clicks'),],
    [State('modal_relatorio_ocorrencias_por_situacao_do_animal', 'is_open')],
)
def modal_relatorio_ocorrencias_por_situacao_do_animal(n1, is_open):
    if n1:
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

# Função para atualizar os mapeamentos após uma inserção
def atualizar_mapeamentos(engine):
    return dados(engine)

# Função para atualização dos dados globais
def atualizar_dados_globais():
    global ocorrencia, codigo_ocorrencia_map, cidade, codigo_cidade_map, bairro, codigo_bairro_map, gruposituacao, codigo_gruposituacao_map, situacaoanimal, codigo_situacao_map, grupoanimal, codigo_grupoanimal_map, racaanimal, codigo_raca_animal_map
    ocorrencia, codigo_ocorrencia_map, cidade, codigo_cidade_map, bairro, codigo_bairro_map, gruposituacao, codigo_gruposituacao_map, situacaoanimal, codigo_situacao_map, grupoanimal, codigo_grupoanimal_map, racaanimal, codigo_raca_animal_map = dados(engine)
    
#### ---- PÁGINA DE LANÇAMENTO DE ocorrencias ---- ###

# Lançamento de Ocorrência - Cadastrar nova ocorrencia - Tela de ocorrencias
@app.callback(
    [Output('mensagem_ocorrencia_salvo_01', 'children'),
     Output('data_lancamento_ocorrencia_01', 'date'),
     Output('dropdown_nomebairro_lancamento_ocorrencia_01', 'value'),
     Output('rua_lancamento_ocorrencia_01', 'value'),
     Output('dropdown_nomegrupoanimal_lancamento_ocorrencia_01', 'value'),
     Output('dropdown_nomeracaanimal_lancamento_ocorrencia_01', 'value'),
     Output('dropdown_nomesituacaoanimal_lancamento_ocorrencia_01', 'value'),
     Output('observacao_lancamento_ocorrencia_01', 'value'),
     ],
    Input('botao_salvar_lancamento_ocorrencia_01', 'n_clicks'),
    [State('data_lancamento_ocorrencia_01', 'date'),
     State('dropdown_nomebairro_lancamento_ocorrencia_01', 'value'),
     State('rua_lancamento_ocorrencia_01', 'value'),
     State('dropdown_nomegrupoanimal_lancamento_ocorrencia_01', 'value'),
     State('dropdown_nomeracaanimal_lancamento_ocorrencia_01', 'value'),
     State('dropdown_nomesituacaoanimal_lancamento_ocorrencia_01', 'value'),
     State('observacao_lancamento_ocorrencia_01', 'value')]
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
            return (f'Erro ao salvar cadastro de ocorrência! Verifique se todos os campos estão preenchidos e tente novamente.! {str(e)}', None, None, '', None, None, None, '')
        
    return ('Erro ao salvar cadastro de ocorrência! Verifique se todos os campos estão preenchidos e tente novamente.', no_update, no_update, no_update, no_update, no_update, no_update, no_update)


#### ---- PÁGINA DE CONTROLE DE ocorrencias ---- ###


# Lançamento de Ocorrência - Cadastrar nova ocorrencia - Tela de gestão (m003)
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
            return (f'Erro ao salvar cadastro de ocorrência! Verifique se todos os campos estão preenchidos e tente novamente.! {str(e)}', None, None, '', None, None, None, '')
        
    return ('Erro ao salvar cadastro de ocorrência! Verifique se todos os campos estão preenchidos e tente novamente.', no_update, no_update, no_update, no_update, no_update, no_update, no_update)

# Atendimento de ocorrencias - Callback para preencher os campos ao selecionar uma ocorrência (m004)
@app.callback(
    Output('observacao_atendimento_ocorrencia', 'value'),
    Output('solucao_atendimento_ocorrencia', 'value'),
    
    Input('dropdown_alteracao_ocorrencia', 'value')
)
def preencher_campos_ocorrencia_selecionada(ocorrencia_selecionada):
    if ocorrencia_selecionada:
        observacao_ocorrencia = ocorrencia.loc[ocorrencia['nome_ocorrencia_completo'] == ocorrencia_selecionada, 'observacao'].iloc[0]
        solucao_ocorrencia = ocorrencia.loc[ocorrencia['nome_ocorrencia_completo'] == ocorrencia_selecionada, 'solucao'].iloc[0]
        return observacao_ocorrencia, solucao_ocorrencia
    return '', ''

# Atendimento de ocorrencias - Atender ou excluir ocorrencia (m004)
@app.callback(
    [Output('mensagem_ocorrencia_alterada', 'children'),
     Output('dropdown_alteracao_ocorrencia', 'value')],
    Input('botao_salvar_alteracao_ocorrencia', 'n_clicks'),
    State('data_atendimento_ocorrencia', 'date'),
    State('observacao_atendimento_ocorrencia', 'value'),
    State('solucao_atendimento_ocorrencia', 'value'),
    State('dropdown_alteracao_ocorrencia', 'value'),
    State('dropdown_atender_excluir_ocorrencia', 'value'),
)
def quitar_ou_excluir_ocorrencia(n_clicks, data_atendimento, observacao_ocorrencia, solucao_ocorrencia, ocorrencia_selecionada, alterar_excluir):
    atualizar_dados_globais()
    
    if not n_clicks:
        return '', no_update
    
    codigo_ocorrencia_map = dict(zip(ocorrencia['nome_ocorrencia_completo'], ocorrencia['idocorrencia']))

    if ocorrencia_selecionada and data_atendimento is not None:
        try:
            cod_ocorrencia_selecionada = codigo_ocorrencia_map.get(ocorrencia_selecionada)
            if cod_ocorrencia_selecionada is not None:
                with engine.connect() as conn:
                    if alterar_excluir == 'Excluir':
                        try:
                            conn.execute(sa.text("DELETE FROM ocorrencia WHERE idocorrencia= :idocorrencia"), {'idocorrencia': cod_ocorrencia_selecionada})
                            conn.commit()
                            atualizar_dados_globais()
                            return f'Ocorrencia "{ocorrencia_selecionada}" excluída com sucesso!', None
                        except Exception as e:
                            return f'Erro ao excluir ocorrencia! {str(e)}', no_update
                        
                    elif alterar_excluir == 'Atender':
                        try:
                            conn.execute(sa.text("UPDATE ocorrencia SET situacao = 1, dataresolucao = :dataresolucao, observacao = :observacao, solucao = :solucao WHERE idocorrencia= :idocorrencia"), 
                                         {'idocorrencia': cod_ocorrencia_selecionada, 'dataresolucao': data_atendimento, 'observacao': observacao_ocorrencia, 'solucao': solucao_ocorrencia})
                            conn.commit()
                            atualizar_dados_globais()
                            return f'Ocorrencia "{ocorrencia_selecionada}" atendida com sucesso!', None
                        except Exception as e:
                            return f'Erro ao atender ocorrencia! {str(e)}', no_update
                        
                    elif alterar_excluir == 'Reabrir':
                        try:
                            conn.execute(sa.text("UPDATE ocorrencia SET situacao = 0, observacao = :observacao, solucao = :solucao WHERE idocorrencia= :idocorrencia"), 
                                         {'idocorrencia': cod_ocorrencia_selecionada, 'observacao': observacao_ocorrencia, 'solucao': solucao_ocorrencia})
                            conn.commit()
                            atualizar_dados_globais()
                            return f'Ocorrencia "{ocorrencia_selecionada}" reaberta com sucesso!', None
                        except Exception as e:
                            return f'Erro ao reabrir ocorrencia! {str(e)}', no_update
        except Exception as e:
            return f'Erro ao atender ocorrencia! Verifique se todos os campos estão preenchidos e tente novamente. {str(e)}', no_update

    return 'Erro ao atender ocorrencia! Verifique se todos os campos estão preenchidos e tente novamente.', no_update


# Cadastrar novo grupo (m005)
@app.callback(
    Output('mensagem_nomegrupoanimal_salvo', 'children'),
    Output('cadastro_nomegrupoanimal', 'value'),
    Input('botao_salvar_cadastro_nomegrupoanimal', 'n_clicks'),
    State('cadastro_nomegrupoanimal', 'value'),
)
def salvar_grupo(n_clicks, nomegrupoanimal):
    if n_clicks is not None and nomegrupoanimal:
        try:  
            novo_grupo = {'nomegrupoanimal': nomegrupoanimal} 

            with engine.connect() as conn:
                conn.execute(sa.text("INSERT INTO grupoanimal (nomegrupoanimal) VALUES (:nomegrupoanimal)"), novo_grupo)
                conn.commit()
                
            
                    
            return ('Novo grupo registrado com sucesso!', '')
    
        except Exception as e:
            return (f'Erro ao salvar grupo! {str(e)}', '')
        
    return ('Erro ao salvar cadastro de grupo! Verifique se todos os campos estão preenchidos e tente novamente.', '')

# Cadastrar novo grupo - Callback para preencher os campos ao selecionar um grupo (m006)
@app.callback(
    Output('alteracao_nomegrupoanimal', 'value'),    
    Input('dropdown_nomegrupoanimal_alteracao_grupo', 'value')
)
def preencher_campos_grupo_selecionado(grupo_selecionado):
    if grupo_selecionado:
        nome_grupo_animal = grupoanimal.loc[grupoanimal['nomegrupoanimal'] == grupo_selecionado, 'nomegrupoanimal'].iloc[0]
        return nome_grupo_animal
    return ''

# Cadastrar novo grupo - Alterar ou excluir grupo (m006)
@app.callback(
    [Output('mensagem_nomegrupoanimal_alterado', 'children'),
     Output('dropdown_nomegrupoanimal_alteracao_grupo', 'value')],
    Input('botao_salvar_alteracao_nomegrupo_animal', 'n_clicks'),
    State('dropdown_nomegrupoanimal_alteracao_grupo', 'value'),
    State('alteracao_nomegrupoanimal', 'value'),
    State('dropdown_alterar_excluir_grupo', 'value')
)
def alterar_ou_excluir_grupo_animais(n_clicks, grupo_selecionado, nomegrupoanimal, alterar_excluir):
    atualizar_dados_globais()

    if not n_clicks:
        return '', no_update

    codigo_grupoanimal_map = dict(zip(grupoanimal['nomegrupoanimal'], grupoanimal['idgrupoanimal']))

    if grupo_selecionado is not None:
        try:
            cod_grupo_selecionado = codigo_grupoanimal_map.get(grupo_selecionado)
            if cod_grupo_selecionado is not None:
                with engine.connect() as conn:
                    if alterar_excluir == 'Excluir':
                        try:
                            conn.execute(sa.text("DELETE FROM grupoanimal WHERE idgrupoanimal= :idgrupoanimal"), {'idgrupoanimal': cod_grupo_selecionado})
                            conn.commit()
                            atualizar_dados_globais()
                            return f'Grupo de animal "{grupo_selecionado}" excluído com sucesso!', None
                        except Exception as e:
                            return f'Erro ao excluir grupo de animal! {str(e)}', no_update
                        
                    elif alterar_excluir == 'Alterar':
                        try:
                            conn.execute(sa.text("UPDATE grupoanimal SET nomegrupoanimal = :nomegrupoanimal WHERE idgrupoanimal= :idgrupoanimal"), 
                                         {'idgrupoanimal': cod_grupo_selecionado, 'nomegrupoanimal': nomegrupoanimal})
                            conn.commit()
                            atualizar_dados_globais()
                            return f'Grupo de animal "{grupo_selecionado}" alterado com sucesso!', None
                        except Exception as e:
                            return f'Erro ao alterar grupo de animal! {str(e)}', no_update
                        
        except Exception as e:
            return f'Erro ao alterar grupo de animal! {str(e)}', no_update

    return 'Erro ao salvar cadastro de grupo! Verifique se todos os campos estão preenchidos e tente novamente.', no_update

# Cadastrar nova raça (m007)
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
    if n_clicks is not None and nomeracaanimal and idgrupoanimal is not None:
        try:  
            idgrupoanimal = codigo_grupoanimal_map[idgrupoanimal]
            
            nova_raca = {'nomeracaanimal': nomeracaanimal, 'idgrupoanimal': idgrupoanimal}         

            with engine.connect() as conn:
                conn.execute(sa.text("INSERT INTO racaanimal (nomeracaanimal, idgrupoanimal) VALUES (:nomeracaanimal, :idgrupoanimal)"), nova_raca)
                conn.commit()
                    
            return ('Nova raça registrada com sucesso!', '', '')
    
        except Exception as e:
            return (f'Erro ao salvar raça! {str(e)}', '', '')
        
    return ('Erro ao salvar cadastro de raça! Verifique se todos os campos estão preenchidos e tente novamente.', '', '')

# Cadastrar nova raca - Callback para preencher os campos ao selecionar uma raca (m008)
@app.callback(
    Output('alteracao_nomeracaanimal', 'value'),    
    Input('dropdown_nomeracaanimal_alteracao_raca', 'value')
)
def preencher_campos_raca_selecionado(raca_selecionado):
    if raca_selecionado:
        nome_raca_animal = racaanimal.loc[racaanimal['nomeracaanimal'] == raca_selecionado, 'nomeracaanimal'].iloc[0]
        return nome_raca_animal
    return ''

# Cadastrar nova raca - Alterar ou excluir raça (m008)
@app.callback(
    [Output('mensagem_nomeracaanimal_alterado', 'children'),
     Output('dropdown_nomeracaanimal_alteracao_raca', 'value')],
    Input('botao_salvar_alteracao_nomeraca_animal', 'n_clicks'),
    State('dropdown_nomeracaanimal_alteracao_raca', 'value'),
    State('alteracao_nomeracaanimal', 'value'),
    State('dropdown_alterar_excluir_raca', 'value')
)
def quitar_ou_excluir_raca_animais(n_clicks, raca_selecionada, nomeracaanimal, alterar_excluir):
    atualizar_dados_globais()

    if not n_clicks:
        return '', no_update

    codigo_racaanimal_map = dict(zip(racaanimal['nomeracaanimal'], racaanimal['idracaanimal']))

    if raca_selecionada:
        try:
            cod_raca_selecionada = codigo_racaanimal_map.get(raca_selecionada)
            if cod_raca_selecionada is not None:
                with engine.connect() as conn:
                    if alterar_excluir == 'Excluir':
                        try:
                            conn.execute(sa.text("DELETE FROM racaanimal WHERE idracaanimal= :idracaanimal"), {'idracaanimal': cod_raca_selecionada})
                            conn.commit()
                            atualizar_dados_globais()
                            return f'Cadastro de raça de animal "{raca_selecionada}" excluído com sucesso!', None
                        except Exception as e:
                            return f'Erro ao salvar cadastro de raça! Verifique se todos os campos estão preenchidos e tente novamente. {str(e)}', no_update
                        
                    elif alterar_excluir == 'Alterar':
                        try:
                            conn.execute(sa.text("UPDATE racaanimal SET nomeracaanimal = :nomeracaanimal WHERE idracaanimal= :idracaanimal"), 
                                         {'idracaanimal': cod_raca_selecionada, 'nomeracaanimal': nomeracaanimal})
                            conn.commit()
                            atualizar_dados_globais()
                            return f'Cadastro de raça de animal "{raca_selecionada}" alterada com sucesso!', None
                        except Exception as e:
                            return f'Erro ao alterar raca de animal! {str(e)}', no_update
                        
        except Exception as e:
            return f'Erro ao salvar cadastro de raça! Verifique se todos os campos estão preenchidos e tente novamente. {str(e)}', no_update

    return 'Erro ao salvar cadastro de raça! Verifique se todos os campos estão preenchidos e tente novamente.', no_update



# Cadastrar nova situação (m009)
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
    if n_clicks is not None and idgruposituacao is not None and nomesituacaoanimal:
        try:  
            idgruposituacao = codigo_gruposituacao_map[idgruposituacao]
            
            nova_situacao = {'idgruposituacao': idgruposituacao, 'nomesituacaoanimal': nomesituacaoanimal,}         

            with engine.connect() as conn:
                conn.execute(sa.text("INSERT INTO situacaoanimal (idgruposituacao, nomesituacaoanimal) VALUES (:idgruposituacao, :nomesituacaoanimal)"), nova_situacao)
                conn.commit()
                    
            return ('Nova situação registrada com sucesso!', '', '')
    
        except Exception as e:
            return (f'Erro ao salvar situação! {str(e)}', '', '')
        
    return ('Erro ao salvar cadastro de situação do animal! Verifique se todos os campos estão preenchidos e tente novamente.', '', '')

# Cadastrar nova situacao - Callback para preencher os campos ao selecionar uma situacao (m010)
@app.callback(
    Output('alteracao_nomesituacaoanimal', 'value'),    
    Input('dropdown_nomesituacaoanimal_alteracao_situacao', 'value')
)
def preencher_campos_situacao_selecionado(situacao_selecionado):
    if situacao_selecionado:
        nome_situacao_animal = situacaoanimal.loc[situacaoanimal['nomesituacaoanimal'] == situacao_selecionado, 'nomesituacaoanimal'].iloc[0]
        return nome_situacao_animal
    return ''

# Cadastrar nova situacao - Alterar ou excluir situação (m010)
@app.callback(
    [Output('mensagem_nomesituacaoanimal_alterado', 'children'),
     Output('dropdown_nomesituacaoanimal_alteracao_situacao', 'value')],
    Input('botao_salvar_alteracao_nomesituacao_animal', 'n_clicks'),
    State('dropdown_nomesituacaoanimal_alteracao_situacao', 'value'),
    State('alteracao_nomesituacaoanimal', 'value'),
    State('dropdown_alterar_excluir_situacao', 'value')
)
def quitar_ou_excluir_situacao_animais(n_clicks, situacao_selecionada, nomesituacaoanimal, alterar_excluir):
    atualizar_dados_globais()

    if not n_clicks:
        return '', no_update

    codigo_situacaoanimal_map = dict(zip(situacaoanimal['nomesituacaoanimal'], situacaoanimal['idsituacaoanimal']))

    if situacao_selecionada is not None:
        try:
            cod_situacao_selecionada = codigo_situacaoanimal_map.get(situacao_selecionada)
            if cod_situacao_selecionada is not None:
                with engine.connect() as conn:
                    if alterar_excluir == 'Excluir':
                        try:
                            conn.execute(sa.text("DELETE FROM situacaoanimal WHERE idsituacaoanimal= :idsituacaoanimal"), {'idsituacaoanimal': cod_situacao_selecionada})
                            conn.commit()
                            atualizar_dados_globais()
                            return f'situacao de animal "{situacao_selecionada}" excluído com sucesso!', None
                        except Exception as e:
                            return f'Erro ao excluir situacao de animal! {str(e)}', no_update
                        
                    elif alterar_excluir == 'Alterar':
                        try:
                            conn.execute(sa.text("UPDATE situacaoanimal SET nomesituacaoanimal = :nomesituacaoanimal WHERE idsituacaoanimal= :idsituacaoanimal"), 
                                         {'idsituacaoanimal': cod_situacao_selecionada, 'nomesituacaoanimal': nomesituacaoanimal})
                            conn.commit()
                            atualizar_dados_globais()
                            return f'situacao de animal "{situacao_selecionada}" alterada com sucesso!', None
                        except Exception as e:
                            return f'Erro ao alterar situacao de animal! {str(e)}', no_update
                        
        except Exception as e:
            return f'Erro ao salvar cadastro de situação do animal! Verifique se todos os campos estão preenchidos e tente novamente. {str(e)}', no_update

    return 'Erro ao salvar cadastro de situação do animal! Verifique se todos os campos estão preenchidos e tente novamente.', no_update

# ----------- Atualizar novos cadastros ----------- #
@app.callback(
    Output('dropdown_nomebairro_lancamento_ocorrencia', 'options'),
    
    Output('dropdown_nomegrupoanimal_lancamento_ocorrencia', 'options'),
    Output('dropdown_nomegrupoanimal_alteracao_grupo', 'options'),
    Output('dropdown_nomegrupoanimal_filtro', 'options'),
    Output('dropdown_nomegrupoanimal_cadastro_raca', 'options'),

    Output('dropdown_nomeracaanimal_lancamento_ocorrencia', 'options'),
    Output('dropdown_nomeracaanimal_alteracao_raca', 'options'),
    Output('dropdown_nomeracaanimal_filtro', 'options'),
    
    Output('dropdown_nomesituacaoanimal_lancamento_ocorrencia', 'options'),
    Output('dropdown_nomesituacaoanimal_alteracao_situacao', 'options'),
    Output('dropdown_nomesituacaoanimal_filtro', 'options'),

    Output('dropdown_nomegruposituacao_cadastro_situacao', 'options'),
    Output('dropdown_alteracao_ocorrencia', 'options'),
    
    [Input('atualizacao_automatica', 'n_intervals'),   
     Input('botao_confirmar_modal_confirmacao', 'n_clicks'),
     Input('dropdown_situacao_alteracao_ocorrencia', 'value'),
    ]
    
    
)
def atualizar_dropdowns(n_intervals, n1, situacao_selecionada):
    atualizar_dados_globais()
    
    ocorrencia_filtrada = ocorrencia
    
    dropdown_nomebairro_lancamento_ocorrencia = [{'label': nomebairro, 'value': nomebairro} for nomebairro in bairro['nomebairro'].value_counts().index]
    
    dropdown_nomegrupoanimal_lancamento_ocorrencia = [{'label': nomegrupoanimal, 'value': nomegrupoanimal} for nomegrupoanimal in grupoanimal['nomegrupoanimal'].value_counts().index]  
    dropdown_nomegrupoanimal_alteracao_grupo = [{'label': nomegrupoanimal, 'value': nomegrupoanimal} for nomegrupoanimal in grupoanimal['nomegrupoanimal'].value_counts().index]  
    dropdown_nomegrupoanimal_filtro = [{'label': nomegrupoanimal, 'value': nomegrupoanimal} for nomegrupoanimal in grupoanimal['nomegrupoanimal'].value_counts().index]  
    dropdown_nomegrupoanimal_cadastro_raca = [{'label': nomegrupoanimal, 'value': nomegrupoanimal} for nomegrupoanimal in grupoanimal['nomegrupoanimal'].value_counts().index]
    
    dropdown_nomeracaanimal_lancamento_ocorrencia = [{'label': nomeracaanimal, 'value': nomeracaanimal} for nomeracaanimal in racaanimal['nomeracaanimal'].value_counts().index]
    dropdown_nomeracaanimal_alteracao_raca = [{'label': nomeracaanimal, 'value': nomeracaanimal} for nomeracaanimal in racaanimal['nomeracaanimal'].value_counts().index]
    dropdown_nomeracaanimal_filtro = [{'label': nomeracaanimal, 'value': nomeracaanimal} for nomeracaanimal in racaanimal['nomeracaanimal'].value_counts().index]

    dropdown_nomesituacaoanimal_lancamento_ocorrencia = [{'label': nomesituacaoanimal, 'value': nomesituacaoanimal} for nomesituacaoanimal in situacaoanimal['nomesituacaoanimal'].value_counts().index]
    dropdown_nomesituacaoanimal_alteracao_situacao = [{'label': nomesituacaoanimal, 'value': nomesituacaoanimal} for nomesituacaoanimal in situacaoanimal['nomesituacaoanimal'].value_counts().index]
    dropdown_nomesituacaoanimal_filtro = [{'label': nomesituacaoanimal, 'value': nomesituacaoanimal} for nomesituacaoanimal in situacaoanimal['nomesituacaoanimal'].value_counts().index]

    
    dropdown_nomegruposituacao_cadastro_situacao = [{'label': nomegruposituacao, 'value': nomegruposituacao} for nomegruposituacao in gruposituacao['nomegruposituacao'].value_counts().index]


    # Aplica filtros de pessoa e situação ao DataFrame de contas
    if situacao_selecionada:
        ocorrencia_filtrada = ocorrencia_filtrada[ocorrencia_filtrada['nomesituacao'] == situacao_selecionada]

    dropdown_alteracao_ocorrencia = [{'label': ocorrencia_filtrada, 'value': ocorrencia_filtrada} for ocorrencia_filtrada in ocorrencia_filtrada['nome_ocorrencia_completo']]
    
    
    return dropdown_nomebairro_lancamento_ocorrencia, dropdown_nomegrupoanimal_lancamento_ocorrencia, dropdown_nomegrupoanimal_alteracao_grupo, dropdown_nomegrupoanimal_filtro, dropdown_nomegrupoanimal_cadastro_raca, dropdown_nomeracaanimal_lancamento_ocorrencia, dropdown_nomeracaanimal_alteracao_raca,dropdown_nomeracaanimal_filtro, dropdown_nomesituacaoanimal_lancamento_ocorrencia, dropdown_nomesituacaoanimal_alteracao_situacao, dropdown_nomesituacaoanimal_filtro, dropdown_nomegruposituacao_cadastro_situacao, dropdown_alteracao_ocorrencia


# Atualizaçao dos gráficos de vendas (m001)
@app.callback([
    
    # Figures
    Output('fig_ocorrencias_relatadas', 'children'),
    Output('fig_ocorrencias_resolvidas', 'children'),   
    Output('fig_ocorrencias_pendentes', 'children'),   
    Output('fig_ocorrencias_por_periodo', 'figure'),   
    Output('fig_ocorrencias_por_grupo', 'figure'), 
    Output('fig_ocorrencias_por_situacao_animal', 'figure'), 
    Output('fig_mapa_ocorrencias', 'figure'), 
    Output('fig_ocorrencias_por_bairro', 'figure'), 
    Output('grid_ocorrencias', 'rowData'),
    Output('grid_ocorrencias', 'columnDefs'),
    Output('tabela_ocorrencias_por_bairro', 'data'),
    Output('tabela_ocorrencias_por_bairro', 'columns'),
    Output('tabela_ocorrencias_por_grupo_de_animal', 'data'),
    Output('tabela_ocorrencias_por_grupo_de_animal', 'columns'),
    Output('tabela_ocorrencias_por_situacao_do_animal', 'data'),
    Output('tabela_ocorrencias_por_situacao_do_animal', 'columns'),

    ],
    [
     Input('atualizacao_automatica', 'n_intervals'),
     Input('filtro_data', 'start_date'),
     Input('filtro_data', 'end_date'), 
     Input('dropdown_situacao_filtro', 'value'),
     Input('dropdown_nomebairro_filtro', 'value'),
     Input('dropdown_nomesituacaoanimal_filtro', 'value'),
     Input('dropdown_nomegrupoanimal_filtro', 'value'),
     Input('dropdown_nomeracaanimal_filtro', 'value'),
     Input('modal_confirmacao_ocorrencia', 'is_open'),  
     ])

def aplicar_filtros(n_intervals, data_ini, data_fin, situacao_ocorrencia, bairro_ocorrencia, situacao_animal_ocorrencia, grupo_animal_ocorrencia, raca_animal_ocorrencia , is_open):

    atualizar_dados_globais()
    ocorrencia_filtrado = ocorrencia
    
    if n_intervals:
        ocorrencia_filtrado = ocorrencia
    if data_ini and data_fin:
        ocorrencia_filtrado = ocorrencia_filtrado[(ocorrencia_filtrado['dataocorrencia'] >= data_ini) & (ocorrencia_filtrado['dataocorrencia'] <= data_fin)] 
    if situacao_ocorrencia:
        ocorrencia_filtrado = ocorrencia_filtrado[ocorrencia_filtrado['nomesituacao'] == situacao_ocorrencia]
    if bairro_ocorrencia:
        ocorrencia_filtrado = ocorrencia_filtrado[ocorrencia_filtrado['nomebairro'] == bairro_ocorrencia]
    if situacao_animal_ocorrencia:
        ocorrencia_filtrado = ocorrencia_filtrado[ocorrencia_filtrado['nomesituacaoanimal'] == situacao_animal_ocorrencia]
    if grupo_animal_ocorrencia:
        ocorrencia_filtrado = ocorrencia_filtrado[ocorrencia_filtrado['nomegrupoanimal'] == grupo_animal_ocorrencia]
    if raca_animal_ocorrencia:
        ocorrencia_filtrado = ocorrencia_filtrado[ocorrencia_filtrado['nomeracaanimal'] == raca_animal_ocorrencia]
        
    #Ocorrencias por período
    ocorrencias_por_periodo =ocorrencia_filtrado.groupby(['codmes_ocorrencia', 'mesocorrencia'])['idocorrencia'].count().reset_index()
    ocorrencias_por_periodo
    
    # Ocorrencias finalizadas por período
    ocorrencia_finalizado = ocorrencia_filtrado[(ocorrencia_filtrado['situacao'] == 1)]	
    ocorrencia_finalizado =ocorrencia_finalizado.groupby(['codmes_solucao', 'messolucao'])['idocorrencia'].count().reset_index()
    
    #Ocorrencias por bairro
    ocorrencias_por_bairro =ocorrencia_filtrado.groupby(['nomebairro'])['idocorrencia'].count().reset_index().sort_values(by='idocorrencia',ascending=False)
    
    # Ocorrencias por raça
    ocorrencias_por_grupo = ocorrencia_filtrado.groupby('nomegrupoanimal', as_index=False)['idocorrencia'].count()
    ocorrencias_por_grupo = ocorrencias_por_grupo.round()
    if len (ocorrencias_por_grupo) < 5:
        ocorrencias_por_grupo = ocorrencias_por_grupo
    else:
        ocorrencias_por_grupo5 = ocorrencias_por_grupo.nlargest(5, 'idocorrencia')
        ocorrencias_por_grupo_resto = ocorrencias_por_grupo.loc[~ocorrencias_por_grupo.index.isin(ocorrencias_por_grupo5.index)]
        ocorrencias_por_grupo_resto['nomegrupoanimal']='OUTROS'
        ocorrencias_por_grupo=pd.concat([ocorrencias_por_grupo5, ocorrencias_por_grupo_resto])
        ocorrencias_por_grupo = ocorrencias_por_grupo.groupby('nomegrupoanimal', as_index=False)['idocorrencia'].sum()
        ocorrencias_por_grupo = ocorrencias_por_grupo.sort_values(by='idocorrencia', ascending = False)
        
    if len(ocorrencias_por_grupo) == 0:
        0
    else:
        ocorrencias_por_grupo
        
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
        ocorrencias_por_situacao_animal = ocorrencias_por_situacao_animal.groupby('nomesituacaoanimal', as_index=False)['idocorrencia'].sum()
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
    fig_ocorrencias_por_periodo.add_trace(go.Scatter(x=ocorrencias_por_periodo['mesocorrencia'], y=ocorrencias_por_periodo['idocorrencia'], name='Ocorrencias relatadas', line=dict(color='#4A4633')))
    fig_ocorrencias_por_periodo.add_trace(go.Scatter(x=ocorrencia_finalizado['messolucao'], y=ocorrencia_finalizado['idocorrencia'], name='Ocorrencias resolvidas', line=dict(color='#3B6CFF')))
    fig_ocorrencias_por_periodo.update_layout(margin=dict(l=5, r=5, t=40, b=5), title='Ocorrencias por período', yaxis_title='', xaxis_title='', title_x=0.5, height=250)
    
    # Ocorrências por raça do animal
    ocorrencias_por_grupo = ocorrencias_por_grupo.rename(columns={'idocorrencia':'Ocorrencias','nomegrupoanimal':'Animal'})
    fig_ocorrencias_por_grupo = px.pie(ocorrencias_por_grupo, values='Ocorrencias', names='Animal', hole=.5)
    fig_ocorrencias_por_grupo.update_layout(margin=dict(l=5, r=5, t=40, b=5), title='Ocorrencias por Grupo', yaxis_title='', xaxis_title='', title_x=0.5, height=250)

    # Ocorrencias por situação do animal
    ocorrencias_por_situacao_animal = ocorrencias_por_situacao_animal.rename(columns={'idocorrencia':'Ocorrencias','nomesituacaoanimal':'Situação do animal'})
    fig_ocorrencias_por_situacao_animal = px.pie(ocorrencias_por_situacao_animal, values='Ocorrencias', names='Situação do animal', hole=.5)
    fig_ocorrencias_por_situacao_animal.update_layout(margin=dict(l=5, r=5, t=40, b=5), title='Ocorrencias por Situação', yaxis_title='', xaxis_title='', title_x=0.5, height=250)

    fig_mapa_ocorrencias = px.scatter_mapbox(mapa_ocorrencias, lat='latitude', lon='longitude', color='Quantidade', color_discrete_sequence=['#004040'], size='Quantidade', title='Ocorrências por Localização').update_layout(mapbox_style="open-street-map", yaxis_title='', xaxis_title='', title_x=0.5, height=500, margin={'l': 0, 'r': 0, 't': 0, 'b': 0}, mapbox_zoom=12)

    # Ocorrencias por bairro
    ocorrencias_por_bairro = ocorrencias_por_bairro.rename(columns={'idocorrencia':'Ocorrencias','nomebairro':'Bairro'})
    fig_ocorrencias_por_bairro = px.bar(ocorrencias_por_bairro, x='Bairro', y='Ocorrencias', title='Ocorrencias por Bairro')
    fig_ocorrencias_por_bairro.update_layout(margin=dict(l=5, r=5, t=40, b=5), title='Ocorrencias por bairro', yaxis_title='', xaxis_title='', title_x=0.5, height=250)

    # Grid de ocorrencias
    grid_ocorrencias = ocorrencia_filtrado[['idocorrencia',  'nomesituacao', 'mesocorrencia', 'nomegrupoanimal', 'nomesituacaoanimal', 'observacao']]
    grid_ocorrencias = grid_ocorrencias.rename(columns={'idocorrencia':'ID', 'nomesituacao':'Situação' ,'nomegrupoanimal':'Animal',  'mesocorrencia':'Mês ocorrencia', 'nomesituacaoanimal':'Situação do animal', 'observacao':'Observação'})
    grid_ocorrencias = grid_ocorrencias.sort_values(by='ID', ascending=False)
    rowData = grid_ocorrencias.to_dict('records')
    columnDefs = [{"field": col} for col in grid_ocorrencias.columns]
    
    # Relatório de ocorrências por bairro
    tabela_ocorrencias_por_bairro = ocorrencia_filtrado[['idocorrencia', 'dataocorrencia', 'nomesituacao', 'dataresolucao', 'nomebairro', 'nomerua', 'observacao', 'solucao']]
    tabela_ocorrencias_por_bairro = tabela_ocorrencias_por_bairro.rename(columns={'idocorrencia':'Código', 'dataocorrencia':'Data', 'nomesituacao': 'Situação', 'dataresolucao': 'Data Resolução' , 'nomebairro':'Bairro', 'nomerua':'Rua', 'observacao':'Observação', 'solucao':'Solução'})
    for campo in ['Data', 'Data Resolução']:
        tabela_ocorrencias_por_bairro[campo] = tabela_ocorrencias_por_bairro[campo].apply(lambda x: formatar_data(x) if pd.notnull(x) else x)
    tabela_ocorrencias_por_bairro = tabela_ocorrencias_por_bairro.sort_values(by ='Código', ascending = False)
    columns = [{"name": col, "id": col} for col in tabela_ocorrencias_por_bairro.columns]
    data = tabela_ocorrencias_por_bairro.to_dict('records')
    
    # Relatório de ocorrências por grupo de animal (m013)
    tabela_ocorrencias_por_grupo_de_animal = ocorrencia_filtrado[['idocorrencia', 'nomegrupoanimal', 'dataocorrencia', 'nomesituacao', 'dataresolucao', 'observacao', 'solucao']]
    tabela_ocorrencias_por_grupo_de_animal = tabela_ocorrencias_por_grupo_de_animal.rename(columns={'idocorrencia':'Código', 'nomegrupoanimal':'Grupo de Animal', 'dataocorrencia':'Data', 'nomesituacao': 'Situação', 'dataresolucao': 'Data Resolução' , 'observacao':'Observação', 'solucao':'Solução'})
    for campo in ['Data', 'Data Resolução']:
        tabela_ocorrencias_por_grupo_de_animal[campo] = tabela_ocorrencias_por_grupo_de_animal[campo].apply(lambda x: formatar_data(x) if pd.notnull(x) else x)
    tabela_ocorrencias_por_grupo_de_animal = tabela_ocorrencias_por_grupo_de_animal.sort_values(by ='Código', ascending = False)
    columns01 = [{"name": col, "id": col} for col in tabela_ocorrencias_por_grupo_de_animal.columns]
    data01 = tabela_ocorrencias_por_grupo_de_animal.to_dict('records')
    
    # Relatório de ocorrências por situação do animal (m014)
    tabela_ocorrencias_por_situacao_do_animal = ocorrencia_filtrado[['idocorrencia', 'nomesituacaoanimal', 'dataocorrencia', 'nomesituacao', 'dataresolucao', 'observacao', 'solucao']]
    tabela_ocorrencias_por_situacao_do_animal = tabela_ocorrencias_por_situacao_do_animal.rename(columns={'idocorrencia':'Código', 'nomesituacaoanimal':'Situação do Animal', 'dataocorrencia':'Data', 'nomesituacao': 'Situação', 'dataresolucao': 'Data Resolução' , 'observacao':'Observação', 'solucao':'Solução'})
    for campo in ['Data', 'Data Resolução']:
        tabela_ocorrencias_por_situacao_do_animal[campo] = tabela_ocorrencias_por_situacao_do_animal[campo].apply(lambda x: formatar_data(x) if pd.notnull(x) else x)
    tabela_ocorrencias_por_situacao_do_animal = tabela_ocorrencias_por_situacao_do_animal.sort_values(by ='Código', ascending = False)
    columns02 = [{"name": col, "id": col} for col in tabela_ocorrencias_por_situacao_do_animal.columns]
    data02 = tabela_ocorrencias_por_situacao_do_animal.to_dict('records')

        
    return [ocorrencias_relatadas, ocorrencias_resolvidas, ocorrencias_pendentes, fig_ocorrencias_por_periodo, fig_ocorrencias_por_grupo, fig_ocorrencias_por_situacao_animal, fig_mapa_ocorrencias, fig_ocorrencias_por_bairro, rowData, columnDefs, data, columns, data01, columns01, data02, columns02]


# ===== Iniciar o servidor e manter o aplicativo rodando ===== #
if __name__=='__main__':
    app.run_server(host='0.0.0.0', port=8052, debug=True)    
