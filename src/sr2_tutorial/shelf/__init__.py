from sier2 import Info

pkg = 'sier2_tutorial'

def blocks():
    info = [
        Info(f'{pkg}.blocks:RandomNumberBlock', 'Random number generator'),
        Info(f'{pkg}.blocks:ConstantNumberBlock', 'Constant number generator'),
        Info(f'{pkg}.blocks:AddBlock', 'Add two numbers'),

        Info(f'{pkg}.blocks:UserInput', 'A text area and flag for input.'),
        Info(f'{pkg}.blocks:Invert', 'Transform text.'),
        Info(f'{pkg}.blocks:Display', 'Display text'),

        Info(f'{pkg}.blocks:ConfigurableBlock', 'An example configurable block'),
        Info(f'{pkg}.blocks:ExampleConfig', 'An example configuration block')
    ]

    return info

def dags():
    info = [
        Info(f'{pkg}.dags:example_add_dag', 'Example adding dag'),
        Info(f'{pkg}.dags:transform_dag', 'Transformation app')
    ]

    return info
