import threading
import serial
from printer import *
from PHDmessage import *
from collections import namedtuple
from time import clock, sleep, strftime, localtime, time

namtup = namedtuple('namtup', ['START', 'PROCESS', 'PAUSE', 'STOP'])
DO_CONDITIONS = namtup(1,2,3,4)
port_timeout = 7

# translate float seconds to string format
class timeFormat():
    def __init__(self, formater, fieldwidth= 14):
        self.fieldwidth = fieldwidth
        a = formater.split('.')
        self.tunit = a[0]
        self.dig = int(a[-1])
        if self.tunit == 's':
            self.f = True
            self.fs = '{0:>{2}.{1}f}'
        else:
            self.f = False
            self.fs = '{0:0>2}:{1:0>{2}.{3}f}'

    def time_in_format(self, t):
        a = float(t)
        if self.f:
            s = self.fs.format(a, min(self.dig, self.fieldwidth-len(str(int(a)))-1), self.fieldwidth)
        else:
            m = int(a/60)
            sec = float(a - m*60)
            s = self.fs.format(m, sec, min(3+self.dig, self.fieldwidth), min(self.dig, self.fieldwidth-3))
        return s

class Operator(threading.Thread):
    def __init__(self, param):
        threading.Thread.__init__(self)
        self.cur_cond = 0
        self.param = param
        self.devport = DevicePort(param)
        self.munit = ''
        self.start_time = 0
        # container for read measurement
        self.mlist = []
        # container for time of read measurement
        self.tlist = []
        # parameters of output time on screen
        self.scrTF = timeFormat(param['SCR_TIMEFORMAT'], 14)
    
    def run(self):
        print_initparameters(self.param) 
        if self.connect():
            # write message about ready
            print_ready(self.param)
            # create PHDmessage object
            phdmessage = PHDmessage(self.param)
            # read measurement unit
            self.devport.write(phdmessage.mr_MU)
            answer = ''
            st = time()
            while len(answer) != phdmessage.IntegerMesVol and time()-st <= port_timeout: 
                c = self.devport.read()
                if c:
                    answer += c
#                answer = self.devport.read(phdmessage.IntegerMesVol)
            self.munit = phdmessage.decipher(answer, 'MEASUREMENT_UNIT') 
            i = 0
            printerstep = int(self.param['HEADER_STEP'])
            DT = float(self.param['DT'])
            while self.cur_cond != DO_CONDITIONS.STOP:
                if self.cur_cond == DO_CONDITIONS.PROCESS:
                    if i:
                        # check on max iteration or max reading time
                        if i == self.param['NM'] or self.tlist[-1] >= self.param['READINGTIME']:
                            self.cur_cond = DO_CONDITIONS.STOP
                            print_stopreason(i, self.tlist[-1], self.param['NM'], self.param['READINGTIME'])
                            break
                        else:
                            # delay of reading
                            delaytime = DT -(clock()-self.tlist[-1])
                            if delaytime > 0:
                                sleep(delaytime)
                    i += 1
                    self.devport.write(phdmessage.mr_M)
                    answer = ''
                    st = time()
                    while len(answer) != phdmessage.IntegerMesVol: 
                        c = self.devport.read()
                        if c:
                            answer += c
                        if time()-st >= port_timeout:
                            self.cur_cond = DO_CONDITIONS.STOP
                            print_not_connection()
                            break
                    # write to list read measurement and appropriate time
                    if self.cur_cond == DO_CONDITIONS.PROCESS:
                        self.mlist.append(phdmessage.decipher(answer, 'MEASUREMENT'))
                        self.tlist.append(clock())
                        # print read data in console
                        print_row(i, self.scrTF.time_in_format(self.tlist[-1]), self.mlist[-1])
                    else:
                        i -= 1
                        # every 10 value print control keys and table head
                    if i%printerstep == 0:
                        print LINE
                        print_controlkeys(self.param)
                        print_head(self.scrTF.tunit, self.munit)
                elif self.cur_cond == DO_CONDITIONS.PAUSE:
                    # if pause, nothing to do
                    pass
                elif self.cur_cond == DO_CONDITIONS.START:
                    # safe a time of start
                    print_controlkeys(self.param)
                    self.start_time = strftime('%d.%m.%Y %H:%M:%S', localtime())
                    if not i:
                        print_start_time(self.start_time)
                    print_head(self.scrTF.tunit, self.munit)
                    self.cur_cond = DO_CONDITIONS.PROCESS
            self.disconnect()

    def connect(self):
        try:
            self.devport.open()
            status = True
        except:
            print_not_connection()
            status = False
        return status
    
    def disconnect(self):
        try:
            self.devport.close()
        except:
            pass
        
class DevicePort(serial.Serial):
    def __init__(self, param):
        super(DevicePort, self).__init__()
        self.port = int(param['PORT'])
        self.baudrate = int(param['BAUDRATE'])
        self.timeout = float(param['TIMEOUT'])