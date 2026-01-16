from sier2 import Connection
from sier2.panel import PanelDag

from ..blocks import UserInput, Invert, Display

DAG_DOC = '''
A demonstration dag that "translates" text into other text.
'''

def transform_dag():
    ui = UserInput(name='User input')
    tr = Invert(name='Transform')
    di = Display(name='Display output')

    dag = PanelDag(doc=DAG_DOC, site='Transform', title='Transform text')
    dag.connect(ui, tr, Connection('out_text', 'in_text'), Connection('out_flag', 'in_flag'))
    dag.connect(tr, di, Connection('out_text', 'in_text'))

    return dag
