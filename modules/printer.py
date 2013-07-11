# -*- coding: utf-8 -*-
LINE = '-'*70
TMP_STRING = '{0:>5} {1:>19} {2:>26}'

def print_initparameters(param):
    print 'Initial parameters:\n    Number of measurements: '+param['NM']+\
        '\n    Reading time: '+param['READINGTIME']+' s'+\
        '\n    Measurement interval: '+param['DT']+' s'
    
def print_controlkeys(param):
    print 'Control keys: \"{0}\"-STOP; \"{1}\"-PAUSE'.format(param['STOP_KEY'], param['PAUSE_KEY'])
    
def print_pause_read(param):
    print 'Reading device paused\nTo resume reading use key \"{0}\", to stop reading - \"{1}\"'\
    	.format(param['START_KEY'], param['STOP_KEY'])

def print_ready(param):
    print 'Connection is right\nTo start read device press key: \"{0}\", or'\
            ' \"{1} - to quit\" >>>'.format(param['START_KEY'], param['STOP_KEY'])
    
def print_start_time(t):
    print 'Start time: ' + t

def print_head(tunit,munit):
    print LINE + '\n' + TMP_STRING.format('#', 'Time, [{0}]'.format(tunit), 'Measurement, [{0}]'.format(munit)) + '\n' + LINE

def print_stopreason(i, t, maxi, maxt):
    print 'Reading stoped on {0} iterations (max iterations: {1}) at {2} s (max reading time: {3} s)'\
			.format(i, maxi, t, maxt)

def print_row(n, t, a):
    print TMP_STRING.format(n, t, a)
    
def print_not_connection():
    print 'Some problem in connection to device\nCheck the physical connection'+\
    ' and number of port in config.conf file\nAnd restart the PHD4Reader'
    