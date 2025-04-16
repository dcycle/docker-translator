"""Apply translations to text."""
# pylint: disable=E0401
import utilities
from importlib import util, machinery

PROCESS = utilities.env('PREPROCESS', 'mock').split(';')
TARGETLANG = utilities.env('TARGETLANG', 'fr')
SOURCEFILE = utilities.env('SOURCEFILE')
DESTFILE = utilities.env('DESTFILE')

result = utilities.readFile(SOURCEFILE)

for processor in PROCESS:
    processor = utilities.import_module(processor)
    result = processor.processs(result)
