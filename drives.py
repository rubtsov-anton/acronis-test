import subprocess as sp
import sys
import re
import tempfile
import os


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

    def get_drives(self):
        f = tempfile.NamedTemporaryFile(dir = '.',delete=False)
        f.write('list disk')
        f.close()
        try:
            s = sp.check_output(['diskpart', '/s',os.path.basename(f.name)])
        except:
            print "Some problems" 
            return []
        else:
            return re.findall('(?P<name>\S+\s+\d+)\s+\S+\s+(?P<size>[0-9.]+\s+\S{1,3})',s)
        finally:
            os.remove(f.name)
    
    def get_partitions(self,id):
        f = tempfile.NamedTemporaryFile(dir = '.',delete=False)
        f.write('select disk ')
        f.write(str(id))
        f.write('\r\nlist partition')
        f.close()
        try:
            s = sp.check_output(['diskpart', '/s',os.path.basename(f.name)])
        except:
            print "Wrong drive id" 
            return []
        else:
            return re.findall('(?P<name>\S+\s+\d+)\s+\S+\s+(?P<size>[0-9.]+\s+\S{1,3})',s)
        finally:
            os.remove(f.name)
        

if __name__ == '__main__':
    dp = windows_drive_printer()
    if len(sys.argv) == 1:
        dp.print_drives()
    else:
        dp.print_partitions(sys.argv[1])
        