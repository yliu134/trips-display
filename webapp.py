import dash
import dash_core_components as dcc
import dash_html_components as html
import TripsIM.TripsIM.matcher as matcher
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children=''),

    html.Div(children='''
        Match a parse with a rule.
    '''),
    dcc.Textarea(id='input-parse', value='', style={'width': '90%', 'height': '30vh'}),
    html.H3('parse'),
    html.Div(id='parsed'),
    # html.Div(html.Ul([html.Li(x) for x in
    #                   matcher.parse_rs_to_str("TripsIM/data/ruleset.txt")]), id='rule-sets'),
    html.H3('rule'),
    html.Div(id='compare'),
    html.H3('score'),
    html.Div(id='score'),
    html.H3('Candidate rules'),
    dcc.RadioItems(
        id='rule_list',
        options=[
            {'label': '!v1 wants to !theme', 'value': '0'},
            {'label': '!v1 needs to !theme', 'value': '1'},
            {'label': 'Shall x !v1?', 'value': '2'},
            {'label': 'Does !n exist?', 'value': '3'},
            {'label': 'Does !e1 know !n?', 'value': '4'},
            {'label': '(can/could/would/will) you help me do X', 'value': '5'},
            {'label': '!object is !property', 'value': '6'},
            {'label': 'Are those !f1??', 'value': '7'},
            {'label': '!x eats !y', 'value': '8'},
            {'label': 'x does !y at !time', 'value': '9'},
            {'label': 'Hello', 'value': '10'},
            {'label': 'Is that !x', 'value': '11'}
        ],
        value='0'
    )
])


@app.callback(
    Output(component_id='parsed', component_property='children'),
    [Input(component_id='rule_list', component_property='value'),
     Input(component_id='input-parse', component_property='value')]
)
def update_output_div(input_value):
    # return html.Div([html.Li(str(x.get_element_str()))
    #                  for x in matcher.load_list_set(input_value)])
    parse = matcher.load_list_set(input_value)
    lst = []
    for tnode in parse:
        temp = html.Div([html.Li(x,
                                 style={'display': 'inline-block',
                                        'padding-left': '1.5rem'})
                         for x in tnode.get_element_str()])
        lst.append(temp)
    ret = html.Div(lst)
    return ret


# @app.callback(
#     Output(component_id='rule', component_property='children'),
#     [Input(component_id='rule_list', component_property='value')]
# )
# def show_chosen_rule(input_value):
#     rule_set = matcher.parse_rule_set("TripsIM/data/ruleset.txt")
#     chosen = rule_set[int(input_value)][0]
#     return html.Ul([html.Li(x.__repr__()) for x in chosen])
#

# @app.callback(
#     Output(component_id='compare', component_property='children'),
#     [Input(component_id='rule_list', component_property='value'),
#      Input(component_id='input-parse', component_property='value')]
# )
# def compare_rule_parse(v1_rule, v2_parse):
#     rule_set = matcher.parse_rule_set("TripsIM/data/ruleset.txt")
#     rs = rule_set[int(v1_rule)][0]
#     print(rs)
#     parse = matcher.load_list_set(v2_parse)
#     result = matcher.score(rs, parse)
#     rule_score = matcher.score_wrt_map(map_=result[3], rule_set=rs)[1]
#     ret = html.Ul([html.Li("{}      "
#                            "positionals matched: {};      "
#                            "kv-pairs matched: {}; {}"
#                            .format(k.__repr__(),
#                                    str(v[0]),
#                                    str(v[1]),
#                                    str(v[2])), style={'color': 'red'})
#                    for k, v in rule_score.items()])
#     #ret = html.Ul([html.Li(k.__repr__() + ': ' + str(v)) for k, v in rule_score.items()])
#     return ret

@app.callback(
    Output(component_id='compare', component_property='children'),
    [Input(component_id='rule_list', component_property='value'),
     Input(component_id='input-parse', component_property='value')]
)
def compare_rule_parse(v1_rule, v2_parse):
    rule_set = matcher.parse_rule_set("TripsIM/data/ruleset.txt")
    rs = rule_set[int(v1_rule)][0]
    parse = matcher.load_list_set(v2_parse)
    result = matcher.score(rs, parse)
    rule_score = matcher.score_wrt_map(map_=result[3], rule_set=rs)[1]
    lst = []

    for k, v in rule_score.items():
        li = []
        for e in k.get_element_str():
            if e.split(':')[0] in v:
                a = e + ' '
                li.append([a, 'red'])
            else:
                li.append([e, 'black'])
        temp = html.Div([html.Li(x[0],
                                 style={'color': x[1],
                                        'display': 'inline-block',
                                        'padding-left': '1.5rem'})
                         for x in li])
        lst.append(temp)
    ret = html.Div(lst)
    return ret

@app.callback(
    Output(component_id='score', component_property='children'),
    [Input(component_id='rule_list', component_property='value'),
     Input(component_id='input-parse', component_property='value')]
)
def compare_rule_parse(v1_rule, v2_parse):
    rule_set = matcher.parse_rule_set("TripsIM/data/ruleset.txt")
    rs = rule_set[int(v1_rule)][0]
    parse = matcher.load_list_set(v2_parse)
    result = matcher.score(rs, parse)
    rule_score = matcher.score_wrt_map(map_=result[3], rule_set=rs)[0]
    return str(rule_score)


if __name__ == '__main__':
    app.run_server(debug=True)
