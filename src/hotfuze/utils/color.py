from enum import Enum

class Color(Enum):
  ERROR = "\033[31m"   
  """Color[RED] is reserved for ERRORS ONLY!"""

  INFO = "\033[90m"  
  """Color[GREY] is to be used for less priority text"""

  SIGNATURE = "\033[35m"
  """Color[PURPLE] is a RESERVED COLOR"""

  GREEN = "\033[32m"
  INVLAID = "\033[31;4m"
  RESET = "\033[0m"