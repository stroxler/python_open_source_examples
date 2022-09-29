print("Running subpackage1 module scope")
from . import subpackage0
x = subpackage0.x
print("Finishing subpackage1 module scope")
