from pprint import pprint
import sys

pprint(sys.path)

import services.connections

print(locals())

# services.connections.cursor_command("SELECT version();")
