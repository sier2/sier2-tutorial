import holoviews as hv
import panel as pn
import json
from pathlib import Path
import tempfile

from sier2 import Dag, Connection
from sier2.panel import PanelDag

from _panel_widgets import QueryWidget, BarchartWidget

NTHREADS = 2
DOC = """Generate barcharts

This dag contains an input block that takes a number and generates a `pandas` dataframe containing random numbers in the range 1 .. number.

The dataframe is then passed to *two* instances of a **barchart** block, one displaying the dataframe, the other displaying the "inverse" of the dataframe.
"""

QUERY_DOC = """Generate random numbers with maximum specified by the slider."""
CHART_DOC = """This bar chart visualises the data from the previous block."""
CHARTI_DOC = """This chart is the same as the previous one, except the bars are inverted."""

hv.extension('bokeh', inline=True)
pn.extension('floatpanel', nthreads=NTHREADS, loading_spinner='bar', inline=True)
# hv.renderer('bokeh').theme = 'dark_minimal'

def main():
    # Build a dag.
    #
    q = QueryWidget(name='Run a query', continue_label='Draw chart', block_doc=QUERY_DOC)
    b = BarchartWidget(name='Results bars', block_doc=CHART_DOC)
    bi = BarchartWidget(inverted=True, name='Results bars (inverted)', block_doc=CHARTI_DOC)

    dag = PanelDag(doc=DOC, site='Example', title='Bars')
    dag.connect(q, b,
        Connection('out_df', 'in_df'),
        Connection('out_max_height', 'in_max_height')
    )
    dag.connect(q, bi,
        Connection('out_df', 'in_df'),
        Connection('out_max_height', 'in_max_height')
    )

    title = 'Random weighted barcharts'

    # Dump the dag and add panel information.
    #
    dump = dag.dump()
    # dump['panel'] = {
    #     'title': title
    # }

    # Save the dump.
    #
    p = Path(tempfile.gettempdir()) / 'dag.json'
    print(f'Saving dag to {p} ...')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(dump, f, indent=2)

    dag.show()

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

if __name__=='__main__':
    main()
