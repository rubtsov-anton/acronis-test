import subprocess as sp
import sys
import re

class drive_printer:

    def print_drives(self):
        d = self.get_drives()
        for i in xrange(len(d)):
            print i, ":",d[i][0], d[i][1]
        
    def print_partitions(self,id):
        p = self.get_partitions(id)
        for i in xrange(len(p)):
            print i, ":",p[i][0], p[i][1]
        
    def get_drives(self):
        raise NotImplementedError
    
    def get_partitions(self,id):
        raise NotImplementedError
        

class linux_drive_printer(drive_printer):

    def __init__(self):
        if not sys.platform.startswith('linux'):
            raise OSError("This type of drive printer works only in Linux OS")
        
    def get_drives(self):
        try:
            s = sp.check_output(['lsblk', '-n', '-l', '-d', '-o', 'NAME,SIZE,TYPE'])
        except:
            print "Some problems" 
        else:
            return re.findall('(?P<name>\w+)\s+?(?P<size>[0-9.]+\w{0,2})\s+?disk',s)
            
    
    def get_partitions(self,id):
        d = self.get_drives()
        try:
            i = int(id)
            drive = '/dev/'+str(d[i][0])
        except:
            print "Wrong drive id"
            return []
        else:
            try:
                s = sp.check_output(['lsblk', '-l', '-n', drive, '-o', 'NAME,SIZE,TYPE'])
            except:
                print "Some problems" 
            else:
                return re.findall('(?P<name>\w+)\s+?(?P<size>[0-9.]+\w{0,2})\s+?part',s)

class windows_drive_printer(drive_printer):

    def __init__(self):
        if not sys.platform.startswith('win'):
            raise OSError("This type of drive printer works only in Windows OS")

    def get_drives():
        pass
    
    def get_partitions(id):
        pass
        

if __name__ == '__main__':
    dp = linux_drive_printer()
    if len(sys.argv) == 1:
        dp.print_drives()
    else:
        dp.print_partitions(sys.argv[1])
        