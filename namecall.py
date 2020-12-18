'''

Sat 12 Dec 2020 11:27:46 PM +06

_____ __  __ ____      _    _   _ 
| ____|  \/  |  _ \    / \  | \ | |
|  _| | |\/| | |_) |  / _ \ |  \| |
| |___| |  | |  _ <  / ___ \| |\  |
|_____|_|  |_|_| \_\/_/   \_\_| \_|

'''
#!/usr/bin/env python
from os import listdir
from os.path import isfile,isdir
class AvailName:
    def __init__(self,file_name):
        self.file_name=file_name

    def get_extension(self):
        return self.file_name.split('.')[-1]

    def basename(self,fname):
        return fname.split('.')[0]

    def fullname(self,base,extn):
        return base+'.'+extn

    def fresh(self,fname):
        return fname.split('_')[0]
    
    def isavail(self,fname):
        return True if fname in listdir() else False

    def changer(self,i):
        if isdir(self.file_name):
            temp_base=self.file_name
            while self.isavail(temp_base):
                temp_base=self.fresh(temp_base)
                i+=1
                temp_base+='_{}'.format(i)
            self.file_name=temp_base
        elif isfile(self.file_name):
            temp_base=self.basename(self.file_name)
            while self.isavail(self.fullname(temp_base,self.get_extension())):
                temp_base=self.fresh(temp_base)
                i+=1
                temp_base+='_{}'.format(i)  
            self.file_name=self.fullname(temp_base,self.get_extension())



    def get_name(self):
        self.changer(1)
        return self.file_name




if __name__=='__main__':
    name=AvailName('videoparser.py')
    print(name.get_name())



