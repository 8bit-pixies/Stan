from IPython.core.magic import Magics, magics_class, line_magic, cell_magic, line_cell_magic
from stan.transcompile.transcompile import transcompile
import sys

@magics_class
class StanMagics(Magics):

    @cell_magic
    def stan(self, line, cell):
        py_code = transcompile(cell)
        #exec(py_code)
        return py_code

ip = get_ipython()
ip.register_magics(StanMagics)


# have a look at the github source code for ipython execution
