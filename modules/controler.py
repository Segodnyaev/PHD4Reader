import deviceoperator, printer
import msvcrt

def get_confirm_to_quit():
    confirm = True
    while confirm:
        a = raw_input('Do You really want to quit? (Y/N)>>> ')
        if (a == 'Y')+(a == 'y'):
            break
        elif (a == 'N')+(a == 'n'):
            confirm = False
        else:
            print 'Not right input. Please repeat.'
    return confirm
            

class Controler():
    def __init__(self, param):
        self.param = param
        self.oper = deviceoperator.Operator(self.param)
        self.data = []
        self.first_quit = True
    def runControl(self):
        self.oper.start()
        key_stop = self.param['STOP_KEY'].lower()
        key_start = self.param['START_KEY'].lower()
        key_pause = self.param['PAUSE_KEY'].lower()
        while self.oper.isAlive():
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch.lower() == key_stop:
                    if self.oper.cur_cond:
                        self.oper.cur_cond = deviceoperator.DO_CONDITIONS.PAUSE
                    if get_confirm_to_quit():
                        if self.first_quit:
                            self.oper.munit = ''
                        self.oper.cur_cond = deviceoperator.DO_CONDITIONS.STOP
                        break
                    if self.oper.cur_cond == deviceoperator.DO_CONDITIONS.PAUSE:
                        printer.print_pause_read(self.param)
                    else: 
                        printer.print_ready(self.param)
                elif ch.lower() == key_start:
                    if self.first_quit:
                        self.first_quit = False
                    if self.oper.cur_cond != deviceoperator.DO_CONDITIONS.PROCESS:
                        self.oper.cur_cond = deviceoperator.DO_CONDITIONS.START
                elif ch.lower() == key_pause:
                    self.oper.cur_cond = deviceoperator.DO_CONDITIONS.PAUSE
                    printer.print_pause_read(self.param)
                    
        if self.oper.munit != '':
            self.data.append(self.oper.munit)
            self.data.append(self.oper.tlist)
            self.data.append(self.oper.mlist)
            self.data.append(self.oper.start_time)