import panel as pn
from sier2.panel import PanelDag
from tutorial_2a import CharDistribution, Display, ExternalInput, SingleCase

pn.extension(inline=True)

if __name__ == '__main__':
    external_input = ExternalInput()
    lc = SingleCase()
    ld = CharDistribution()
    display = Display()

    dag = PanelDag(
        [
            (external_input.param.out_text, lc.param.in_text),
            (external_input.param.out_upper, lc.param.in_upper),
            (lc.param.out_text, ld.param.in_text),
            (ld.param.out_len, display.param.in_len),
            (ld.param.out_counter, display.param.in_counter),
        ],
        doc='Count character distribution',
        title='tutorial_3a',
    )

    dag.show()
