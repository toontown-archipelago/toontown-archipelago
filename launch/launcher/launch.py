"""
This file is a hack to make the Nuitka build work.
In theory, we should be able to use the multidist mode, but results are mixed on Windows.
As we can't use multidist, we'd have to build the game 3 times (client, AI, UD).
So this file is a single entrypoint, so we only build once.
"""
import os

match os.environ.get("SERVICE_TO_RUN", None):
    case "CLIENT":
        from toontown.launcher import TTOffQuickStartLauncher
    case "AI":
        from toontown.ai import AIStart
    case "UD":
        from toontown.uberdog import UDStart
    case _:
        print("Unknown service type!")
