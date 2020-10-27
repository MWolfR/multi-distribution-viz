import numpy
from data_structures import ConditionCollection
import plotly.graph_objects as go


class DistributionGrouper(object):

    def __init__(self, payload, initial_column):
        self._payload = payload
        self._parameters = list(payload.columns)
        self._data = None
        self._filter_categories = None
        self._filter_possible_values = None
        self._height = 500  # TODO: not hard coded
        tmp = self.activate_column(initial_column)
        self._column_used_for_lookup = initial_column
        self._filter_categories = tmp.conditions()
        self._filter_possible_values = dict([(_cat, tmp.labels_of(_cat))
                                             for _cat in self._filter_categories])

    def activate_column(self, col_name):
        coll = ConditionCollection.from_pandas(self._payload[col_name])
        return coll

    def values_across(self, parameter, category, **kwargs):
        assert category in self._filter_categories
        filtered = self.activate_column(parameter).filter(**kwargs)
        if len(filtered.contents):
            return [(val, numpy.hstack(filtered.get(**dict([(category, val)]))))
                    for val in filtered.labels_of(category)]
        return []

    def violins_for(self, parameter, lst_filter_values, main_category, comparator=None):
        fltr_dict = dict([(category, values)
                          for category, values in zip(self._filter_categories,
                                                      lst_filter_values)
                          if len(values)])
        if comparator is not None:
            fltr_dict[comparator[0]] = comparator[1][0]  # TODO: Overrides specified filter. Is that desired?
            values = self.values_across(parameter, main_category, **fltr_dict)
            violins = [go.Violin(x0=k, y=v, name=comparator[1][0],
                                 side='negative', line={"color": 'blue'},
                                 scalegroup=k, showlegend=(k == values[0][0]),
                                 meanline_visible=True, legendgroup=comparator[1][0])
                       for k, v in values]
            fltr_dict[comparator[0]] = comparator[1][-1]
            values = self.values_across(parameter, main_category, **fltr_dict)
            violins = violins + [go.Violin(x0=k, y=v, name=comparator[1][-1],
                                           side='positive', line={"color": "orange"},
                                           scalegroup=k, showlegend=(k == values[0][0]),
                                           meanline_visible=True, legendgroup=comparator[1][-1])
                                 for k, v in values]
        else:
            values = self.values_across(parameter, main_category, **fltr_dict)
            violins = [go.Violin(x0=k, y=v, name=k, meanline_visible=True) for k, v in values]
        return violins

    def make_empty(self):
        fwgt = go.FigureWidget(data=[])
        fwgt.layout.height = self._height
        return fwgt

    def make_figure(self, parameter, lst_filter_values, main_category, comparator=None):
        fwgt = go.FigureWidget(data=self.violins_for(parameter, lst_filter_values, main_category,
                                                     comparator=comparator),
                               layout=go.Layout())
        fwgt.layout.height = self._height
        return fwgt



