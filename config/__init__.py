import os
import sys
import config.settings

# create settings object depending on environment
APP_ENV = os.environ.get('APP_ENV', 'Development')
_current = getattr(sys.modules['config.settings'], f"{APP_ENV}Config")()

# copy attributes to the module for convenience
for atr in [fName for fName in dir(_current) if not '__' in fName]:
    # environment can override anything
    val = os.environ.get(atr, getattr(_current, atr))
    setattr(sys.modules[__name__], atr, val)