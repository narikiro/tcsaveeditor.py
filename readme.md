
## tcsaveeditor.py
A save editing python script for the game [Turing Complete](https://store.steampowered.com/app/1444480/Turing_Complete/).

### Requirements
- Python 3
- [python-snappy](https://pypi.org/project/python-snappy/) (for save compression/decompression)

### Use
Download the source from github, create a python file and import `tcsaveditor`. Below is an example program that loads a file, adds an And gate at `(0, 0)`, then saves the file:
```python
from tcsaveeditor import *

circuit_file = '/path/to/your/circuit.data'

save = TCSave().from_file(circuit_file)
save.components.append(TCComponent(ComponentKind.And, TCPoint(0, 0)))
save.save(circuit_file)
```
Check out `TCComponent` to see the rest of the parameters available when creating a component. Certain components (like customs, programs, counters, constants, etc.) use the remaining parameters for their configuration.

Note that you can also run `print()` against the different save objects to get some basic information about them (try `print(save)`).

Also built-in is functionality for creating teleport wires:
```python
save.create_teleport_wire(TCPoint(0, 0), TCPoint(2, 0))
```
which creates a teleport wire between the points `(0, 0)` and `(2, 0)`. Check out `create_teleport_wire()` to see the remaining parameters available for wires.

#### Notes
- If the schematic you are editing is currently open in-game, you will need to switch to a different schematic and reload that schematic to see any changes.
- Right now the wire body data is read as-is, rather than converted to a collection of points. Most applications right now involve using teleport wires anyway, so this shouldn\'t be a problem.
