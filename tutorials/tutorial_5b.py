from sier2 import Connection, Library
from sier2.panel import PanelDag

print('Loading ui ...')
UiBlock = Library.get_block('sier2_tutorial.blocks:UserInput')
ui = UiBlock(name='User input')

print('Loading text transformation ...')
TrBlock = Library.get_block('sier2_tutorial.blocks:Invert')
tr = TrBlock(name='Translation')

print('Loading display ...')
DiBlock = Library.get_block('sier2_tutorial.blocks:Display')
di = DiBlock(name='Display output')

dag = PanelDag(doc='Trasnformation', title='transform text')
dag.connect(ui, tr, Connection('out_text', 'in_text'), Connection('out_flag', 'in_flag'))
dag.connect(tr, di, Connection('out_text', 'in_text'))

dag.show()
