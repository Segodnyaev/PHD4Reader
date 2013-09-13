# -*- coding: utf-8 -*-
#всякие приблуды с кодировками
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from modules import filemanager, controler
#from modules import literead
param = filemanager.read_config()

controler = controler.Controler(param)
controler.runControl()
filemanager.print_in_file(param['OUTFILE'], controler.data, param['FILE_TIMEFORMAT'])
raw_input('For exit press \"Enter\"')
#literead.letgo(param)