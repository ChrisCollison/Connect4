from collections import namedtuple
from enum import Enum

Offset = namedtuple('Offsets', ['row', 'column'])

class Axis(Enum):
  HORZ = Offset(row=0, column=1)
  VERT = Offset(row=1, column=0)
  DIAG_FWD = Offset(row=1, column=1)
  DIAG_BWD = Offset(row=1, column=-1)