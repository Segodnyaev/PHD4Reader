# -*- coding: utf-8 -*-

class PHDmessage(object):
    def __init__(self, param):
        self.measurement_units = [\
            'PPM', 'mbar1/s',\
            'cm3/s', 'cm3/min',\
            'TorrL/s', 'PaL/s',\
            'Pam3/s', 'Kg/h',\
            'g/y(R12)', 'g/y(R314)',\
            'SCF/Y']
        self.IntegerMesVol = 9 + int(param['VOLUME_INT'])
        #message component
        self.mes = [int(param['STX'], 16), int(param['ADDR'], 16),\
                    31, 34, 30, int(param['READ_COM'], 16), int(param['ETX'], 16)]
        #read message
        self.mr_MU = self.createRM(param['MEASUREMENT_UNIT'])
        self.mr_M = self.createRM(param['MEASUREMENT'])

    def create_crc(self,s):
        crc = s[1]
        for k in s[2:]:
            crc = crc^k
        return str(hex(crc))[-2:]
    
    def createRM(self, nwin):
        self.mes[2:5] = [ord(k) for k in nwin]
        crc = self.create_crc(self.mes)
        return ''.join(chr(k) for k in self.mes)+crc
    
    def decipher(self, mes, nwin):
        s = ''
        if len(mes) == self.IntegerMesVol:
            data = mes[6:-3]          
            if nwin == 'MEASUREMENT_UNIT':
                s = self.measurement_units[int(data)]
            elif nwin == 'MEASUREMENT':
                s = data
        #handling errors
        elif mes:
            s = 'Data in message not INT'
            print s, '\n', mes                
        return s