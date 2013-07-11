# -*- coding: utf-8 -*-
from deviceoperator import timeFormat
from printer import TMP_STRING
from time import strftime
import os

def read_config(filename='config.conf'):
    parameters = {}
    try:
        conf = open(filename)
        for line in conf:
            elements = line.rstrip().split()
            #исключаем комментарии
            if len(elements) >= 2 and '##' not in elements:
                key, value = elements[0:2]
                #обрабатываем файл вывода
                if key == 'OUTFILE':
                    p = parameters.pop('OUTPATH', '').strip('/')
                    if value == '{date+time}':
                        value = strftime('%Y%m%d%H%M%S.dat')
                    value = p + bool(p)*'/' + value
                elif key == 'OUTPATH' and parameters.has_key('OUTFILE'):
                    parameters['OUTFILE'] = value.strip('/') + parameters['OUTFILE']
                    continue                
                parameters.setdefault(key, value)
    except:
        print 'Error of reading file \'config\''
    return parameters

def print_in_file(filename, data, time_format, mode='w'):
    if data:
        d = os.path.dirname(filename)
        if d and not os.path.isdir(d):
            os.makedirs(d)
            print 'Created path: ' + d
        with open(filename, mode) as f:
            f.write('Start time: ' + data[3] + '\n')
            fileTF = timeFormat(time_format, 15)
            f.write(TMP_STRING.format('#', 'Time, [{0}]'.format(fileTF.tunit), 'Measurement, [{0}]'.format(data[0]))+'\n')
            for i in range(len(data[1])):
                f.write(TMP_STRING.format(str(i+1), fileTF.time_in_format(data[1][i]), data[2][i])+'\n')
        print 'Data wrote in file: ' + filename
    else:
        print 'Nothing to write in file '
    return True