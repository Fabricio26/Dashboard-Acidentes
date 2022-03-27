import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd


df = pd.read_excel("Estatistica acidentes.xlsx")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

valor_decresente = df.sort_values("VALOR DIAS PERDIDOS R$")

opcoes =  list(df['Ano'].unique())


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#00CED1",
   
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Img(id="logo", src=app.get_asset_url("logo-social.png"), height=50),
        html.Hr(),
        html.H4(
            "ESTATÍSTICAS DE ACIDENTE", className="lead", style={"color": "#0000CD"}
        ),
        dbc.Nav(
            [
                dbc.NavLink("IRA", href="/", id="ph", active="exact"),
                dbc.NavLink("IAG", href="/page-1", id="p1", active="exact"),                
                dbc.NavLink("TAXA DE GRAVIDADE", href="/page-2", id="p2", active="exact"),
                dbc.NavLink("TAXA DE FREQUÊNCIA", href="/page-3", id="p3", active="exact"),
                dbc.NavLink("CUSTO", href="/page-4", id="p4", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    html.P("ANO DE EXIBIÇÃO", style={"padding-left": "19rem", "margin-top": "40px", "color": "#00CED1" }),
    dbc.Row([
        dcc.Dropdown(
            opcoes,
            value="2016", 
            id="lista_ano",
            style={
                "margin-left": "9.5rem",
                'width': "35%",
                'textAlign': 'center',
                'color': '#00FFFF'                    
            } 
        ),
        dbc.Card([
            dbc.CardBody([
                html.Span("ACUMULADO IRA %:", id="textodacaixa", style={"color": "#00CED1"}),
                html.H3(style={"color": "#0000CD"}, id="acumulado"),
                                      
            ], style={"background": "#FFFAFA"}
            )   
        ], style={"margin-left": "21rem", 'width': "20%", "background-color": "#00CED1"})
    ]),
    dcc.Location(id="url"),
    sidebar,
    content,
    ]
)

@app.callback(
    Output("textodacaixa", "children"),
    Output('acumulado', "children"),
    Input("url", "pathname"),
    Input("lista_ano", "value")     
)

def render_page_content(pathname, value):
    if pathname == "/":
        return f"ACUMULADO IRA %:", df.loc[df["Ano"] == value]["IRA %"].sum()
    elif pathname == "/page-1":
        return f"ACUMULADO IAG:", df.loc[df["Ano"] == value]["IAG"].sum()
    elif pathname == "/page-2":
        return f"ACUMULADO GRAVIDADE:", df.loc[df["Ano"] == value]["TAXA DE GRAVIDADE"].sum()
    elif pathname == "/page-3":
        return f"ACUMULADO FREQUÊNCIA:", df.loc[df["Ano"] == 
        value]["TAXA DE FREQUÊNCIA TOTAL DOS ACIDENTES"].sum()
    elif pathname == "/page-4":
        return f"ACUMULADO CUSTO R$:", df.loc[df["Ano"] == value]["VALOR DIAS PERDIDOS R$"].sum()

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
    [Input("lista_ano", "value")]  
)
def render_page_content(pathname, value):    
    if pathname == "/":            
        return [                         
                html.H1('Taxa de IRA',
                        style={
                            'textAlign':'center',
                            'color':'#FFFAFA'
                        }),                
                dcc.Loading(id="loading-1", type="default",
                children=[dcc.Graph(id='IRA',
                         figure=px.bar(df.loc[df["Ano"]==value, :], barmode='group', x='Mês',
                         y='IRA %'))])
                ]
    elif pathname == "/page-1":
        return [          
                html.H1('Taxa de IAG',
                        style={
                            'textAlign':'center',
                            'color':'#FFFAFA'
                        }),                    
                dcc.Loading(id="loading-2", type="default",
                children=[dcc.Graph(id='IAG',
                         figure=px.bar(df.loc[df["Ano"]==value, :], barmode='group', x='Mês',
                         y='IAG'))])
                ]
    elif pathname == "/page-2":
        return [
                html.H1('Taxa de Gravidade',
                        style={
                            'textAlign':'center',
                            'color':'#FFFAFA'
                        }),                   
                dcc.Loading(id="loading-3", type="default",
                children=[dcc.Graph(id='gravidade',
                         figure=px.bar(df.loc[df["Ano"]==value, :], barmode='group', x='Mês',
                         y='TAXA DE GRAVIDADE'))])
                ]
    elif pathname == "/page-3":
        return [
                html.H1('Taxa de Frequência',
                        style={
                            'textAlign':'center',
                            'color':'#FFFAFA'
                        }),                   
                dcc.Loading(id="loading-4", type="default",
                children=[dcc.Graph(id='frequecia',
                         figure=px.bar(df.loc[df["Ano"]==value, :], barmode='group', x='Mês',
                         y='TAXA DE FREQUÊNCIA TOTAL DOS ACIDENTES'))])
                ]
    elif pathname == "/page-4":
        return [
                html.H1('Custo Por Dias Perdidos',
                        style={
                            'textAlign':'center',
                            'color':'#FFFAFA'
                        }),                   
                dcc.Loading(id="loading-5", type="default",
                children=[dcc.Graph(id='custo',
                         figure=px.bar(valor_decresente.loc[valor_decresente["Ano"]==value, :], 
                         x='VALOR DIAS PERDIDOS R$',
                         y='Mês', orientation='h',))])
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised...")
        ]
    )


if __name__=='__main__':
    app.run_server(debug=True, port=3000)
