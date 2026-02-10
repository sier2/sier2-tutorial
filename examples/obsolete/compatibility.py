#

# Demonstrate finding blocks that have compatible outputs.
# An output is compatible with this blocks inputs by type.
#
# **** NOT WORKING YET ****
#

from sier2 import Block, Dag
import param

class ThisBlock(Block):
    """ThisBlock"""
    # Inputs.
    #
    intp = param.Integer(label='An integer')
    strp = param.Integer(label='A string')
    dfp = param.DataFrame(label='A dataframe')

class Block1(Block):
    """Block1"""
    # Outputs.
    #
    dfp = param.DataFrame(label='A dataframe')
    intp = param.Integer(label='An integer')
    strp = param.Integer(label='A string')

class Block2(Block):
    """Block2"""
    # Outputs.
    #
    dataframep = param.DataFrame(label='A dataframe')
    numberp = param.Integer(label='An integer')
    boolp = param.Boolean(label='A boolean')

class Block3(Block):
    """Block3"""
    # Outputs.
    #
    nump = param.Integer(label='An integer')
    boolp = param.Boolean(label='A boolean')

class Block4(Block):
    """Block4"""
    # Outputs.
    #
    boolp = param.Boolean(label='A boolean')

if __name__=='__main__':
    thisg = ThisBlock()

    g1 = Block1()
    g2 = Block2()
    g3 = Block3()

    from pprint import pprint
    pprint(Dag.compatible_outputs(thisg, g1))

    pprint(Dag.compatible_outputs(thisg, g2))

    pprint(Dag.compatible_outputs(thisg, g3))
