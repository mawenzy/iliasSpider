#!/usr/bin/env python
from config import *

### Spider 1
c = Config(
    'vorname.nachname', 
    'https://ilias.uni-konstanz.de/ilias/goto_ilias_uni_crs_...', 
    '/path/to/download/folder/', 
    )
runSpider(c)

### Spider 2
# ...
