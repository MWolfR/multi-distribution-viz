import dash
from grouper import DistributionGrouper
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from dash.dash import no_update


def read_dfs(lst_dfs):
    import pandas
    dfs = [pandas.read_pickle(_fn) for _fn in lst_dfs]
    data = pandas.concat(dfs, axis=0)
    return data


def make_parameter_dropdown(grp_obj):
    opt_dict = [dict([('label', v), ('value', v)]) for v in grp_obj._parameters]
    return dcc.Dropdown(
            options=opt_dict,
            value=grp_obj._column_used_for_lookup,
            id="parameter-dropdown")


def make_filter_dropdowns(grp_obj):
    filters = []
    for filter_cat, filter_vals in grp_obj._filter_possible_values.items():
        opt_dict = [dict([('label', v), ('value', v)]) for v in filter_vals]
        filters.append(dcc.Dropdown(
            options=opt_dict,
            value=[],
            multi=True,
            id=filter_cat
        )
        )
    return filters


def make_grouper_dropdown(grp_obj):
    opt_dict = [dict([('label', v), ('value', v)]) for v in grp_obj._filter_categories]
    return dcc.Dropdown(
        options=opt_dict,
        value="target",  # TODO: not hard coded
        id="grouper-dropdown")


def make_layout(parameter_dropdown, filter_dropdowns, grouper_dropdown):
    col_width = 400  # TODO: not hard coded
    lo_rows = [html.Tr([html.Th("Parameter", scope="col", style={"width": col_width}),
                        html.Th("Group by", scope="col", style={"width": col_width})
                        ]),
               html.Tr([html.Td(parameter_dropdown), html.Td(grouper_dropdown)]),
               html.Tr([html.Td(html.Div([html.Label(_dd.id), _dd])) for _dd in filter_dropdowns[:2]]),
               html.Tr([html.Td(html.Div([html.Label(_dd.id), _dd])) for _dd in filter_dropdowns[2:]])  # TODO: not hard coded
               ]
    return html.Table(lo_rows)


def main(lst_dbs, return_app=False):
    main_payload = read_dfs(lst_dbs)
    initial_parameter = main_payload.columns[0]  # TODO: not hard coded
    grp_obj = DistributionGrouper(main_payload, initial_parameter)

    parameter_dropdown = make_parameter_dropdown(grp_obj)
    filter_dropdowns = make_filter_dropdowns(grp_obj)
    grouper_dropdown = make_grouper_dropdown(grp_obj)
    fig = grp_obj.make_empty()

    inputs = [Input(parameter_dropdown.id, 'value'), Input(grouper_dropdown.id, 'value')] +\
        [Input(_fltr_cat, 'value') for _fltr_cat in grp_obj._filter_categories]

    app = dash.Dash(__name__)

    controls_layout = make_layout(parameter_dropdown, filter_dropdowns, grouper_dropdown)
    app.layout = html.Div([
        controls_layout,
        dcc.Graph(id='main-graph', figure=fig)
    ], style={'width': 900})
    server = app.server

    @app.callback(
        Output('main-graph', 'figure'),
        inputs
    )
    def master_callback(parameter, group_by, *args):
        return grp_obj.make_figure(parameter, args, group_by)

    if return_app:
        return app
    return server


if __name__ == "__main__":
    import sys
    main(sys.argv[1:], return_app=True).run_server(debug=False, use_reloader=True)


