from pathlib import Path

import holoviews as hv
import panel as pn
from _panel_widgets import BarchartWidget, QueryWidget
from sier2 import Connection
from sier2.panel import PanelDag

NTHREADS = 2
DOC = """Generate barcharts

This dag contains an input block that takes a number and generates a `pandas` dataframe containing random numbers in the range 1 .. number.

The dataframe is then passed to *two* instances of a **barchart** block, one displaying the dataframe, the other displaying the "inverse" of the dataframe.

This app can be started with "python bars.py" or "python -m panel serve bars.py".
"""

QUERY_DOC = """Generate random numbers with maximum specified by the slider."""
CHART_DOC = """This bar chart visualises the data from the previous block."""
CHARTI_DOC = """This chart is the same as the previous one, except the bars are inverted."""

hv.extension('bokeh', inline=True)
pn.extension('floatpanel', nthreads=NTHREADS, loading_spinner='bar', inline=True)


def build_dag():
    # Build a dag.
    #
    q = QueryWidget(name='Run a query', continue_label='Draw chart', doc=QUERY_DOC)
    b = BarchartWidget(name='Results bars', doc=CHART_DOC)
    bi = BarchartWidget(inverted=True, name='Results bars (inverted)', doc=CHARTI_DOC)

    title = 'Random weighted barcharts'

    logo_path = Path(__file__).parent / 'py.svg'

    dag = PanelDag(
        doc=DOC,
        site='Example',
        title=title,
        logo=str(logo_path),
        author={'name': 'Arthur Author', 'email': 'arthur.author@example.com'},
    )
    dag.connect(q, b, Connection('out_df', 'in_df'), Connection('out_max_height', 'in_max_height'))
    dag.connect(q, bi, Connection('out_df', 'in_df'), Connection('out_max_height', 'in_max_height'))

    # # Dump the dag and add panel information.
    # #
    # dump = dag.dump()

    # # Save the dump.
    # #
    # p = Path(tempfile.gettempdir()) / 'dag.json'
    # print(f'Saving dag to {p} ...')
    # with open(p, 'w', encoding='utf-8') as f:
    #     json.dump(dump, f, indent=2)

    # dag.show()

    # # Build a panel app.
    # #
    # template = pn.template.MaterialTemplate(
    #     title=title,
    #     theme='dark',
    #     site='PoC ',
    #     sidebar=pn.Column('## Blocks'),
    #     collapsed_sidebar=True
    # )
    # template.main.objects = [pn.Column(q, b, bi)]
    # template.sidebar.objects = [pn.panel(dag.hv_graph().opts(invert_yaxis=True, xaxis=None, yaxis=None))]
    # template.show(threaded=False)

    return dag


dag = build_dag()
print(f'{__name__=}')

if __name__ == '__main__':
    dag.show()
else:
    dag.servable()
