from sier2 import Info

pkg = 'sier2_tutorial'

def blocks():
    info = [
        Info(f'{pkg}.block.RandomNumberBlock', 'Random number generator'),
        Info(f'{pkg}.block.ConstantNumberBlock', 'Constant number generator'),
        Info(f'{pkg}.block.AddBlock', 'Add two numbers'),

        Info(f'{pkg}.panel_block.UserInput', 'A text area and flag for input.'),
        Info(f'{pkg}.panel_block.Translate', 'Translate text to English.'),
        Info(f'{pkg}.panel_block.Display', 'Display translated text.')
    ]

    return info

def dags():
    info = [
        Info(f'{pkg}.dag.example_dag', 'Example dag'),

        Info(f'{pkg}.panel_dag.translate_dag', 'Translation app')
    ]

    return info
