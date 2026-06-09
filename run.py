import sys
from core.main import main

if len(sys.argv) > 1:
    debug_arg = sys.argv[1]
    if debug_arg == "--debug":
        main(True)
    else:
        main(False)
else:
    main(False)