from sier2 import Connection, Library
from sier2.panel import PanelDag

from tutorial_3b import UserInput, Invert, Display

Library.add_block(UserInput, 'tutorial_3b:UserInput')
Library.add_block(Invert, 'tutorial_3b:Translate')
Library.add_block(Display, 'tutorial_3b:Display')

def transform_dag():
    UiBlock = Library.get_block('tutorial_3b:UserInput')
    ui = UiBlock(name='User input')

    TrBlock = Library.get_block('tutorial_3b:Translate')
    tr = TrBlock(name='Transformation')

    DiBlock = Library.get_block('tutorial_3b:Display')
    di = DiBlock(name='Display output')

    dag = PanelDag(doc='Transform text', title='transform text')
    dag.connect(ui, tr, Connection('out_text', 'in_text'), Connection('out_flag', 'in_flag'))
    dag.connect(tr, di, Connection('out_text', 'in_text'))

    return dag

if __name__=='__main__':
    dag = transform_dag()
    dag.show()
