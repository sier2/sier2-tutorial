from tutorial_2a import ExternalInput, SingleCase, CharDistribution, Display
from sr2 import Connection, Connections
from sr2.panel import PanelDag

import panel as pn

pn.extension(inline=True)

if __name__=='__main__':
    external_input = ExternalInput()
    lc = SingleCase()
    ld = CharDistribution()
    display = Display()

    dag = PanelDag(doc='Count character distribution', title='tutorial_1a')
    dag.connect(external_input, lc, Connection('out_text', 'in_text'), Connection('out_upper', 'in_upper'))
    dag.connect(lc, ld, Connection('out_text', 'in_text'))

    # Use ``Connections`` for a more succint mapping.
    #
    dag.connect(ld, display, Connections({
        'out_len': 'in_len',
        'out_counter': 'in_counter'})
    )

    dag.show()
