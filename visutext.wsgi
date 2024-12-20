#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/visutext/VisuTextAI/") 

from app import app as application 
application.secret_key = 'assd#sdd411s@das2Dyrsdatrasas2WasfdfvDeQLfdg'
