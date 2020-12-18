'''

Thu 17 Dec 2020 08:28:38 PM +06

| ____| |  \/  | |  _ \     / \    | \ | |
|  _|   | |\/| | | |_) |   / _ \   |  \| |
| |___  | |  | | |  _ <   / ___ \  | |\  |
|_____| |_|  |_| |_| \_\ /_/   \_\ |_| \_|

'''


from os import getenv,listdir,getcwd,system,mkdir,chdir,get_terminal_size
from os.path import join,isfile,isdir,exists
from config import digest_self_config
from namecall import AvailName
from argparse import ArgumentParser



class Organizer:

    CONFIG={
    
        'VIDEO':['.mp4','.mkv'],
        'AUDIO':['.mp3','.wav'],
        'TEX':['.log','.pdf','.aux','.tex','.gz','.fls','.fdb_latexmk'],
        'TEXT':['.txt','.doc'],
        'PYTHON':['.py','.pyx','.pyd','.so','.pypy'],
        'DEFAULT_VIDEO_DIRECTORY':None,
        'DEFAULT_AUDIO_DIRECTORY':None,
        'DEFAULT_TEX_DRIRECTORY':None,
        'DEFAULT_PYTHON_DIRECTORY':None,
        'DEFAULT_ALL_DIRECTORY':None,
        'DEFAULT_DESTINATION':getcwd(),
        'type':None,
        'directory_name':None,
        'INFOFILE':open('/info/info.txt').read() if exists('/info/info.txt') else None,
        'HELP_OF_TYPE':open('/info/type.txt').read() if exists('/info/type.txt') else None,
        'HELP_OF_DIRECTORY_NAME':open('/info/directory_name.txt').read() if exists('/info/directory_name.txt') else None,
        'HELP_OF_FROM':open('/info/from.txt').read() if exists('/info/from.txt') else None,
        'HELP_OF_TO':open('/info/to.txt').read() if exists('/info/to.txt') else None,

    }
    def __init__(self,run=True,**kwargs):
        digest_self_config(self,**kwargs)
        self.directory_name=AvailName(self.get_type()).get_name().capitalize() if self.directory_name is None else AvailName(self.directory_name).get_name()
        if run:
            self.main()

    def avail_type(self):#not useful upto now,maybe useful for external library use
        return ['video','audio','tex','text','python']


    def get_cli(self):
        parser=ArgumentParser(self.INFOFILE)
        if self.type==None:
            parser.add_argument('type',help=
            self.HELP_OF_TYPE 
        if self.HELP_OF_TYPE is not None else
            "Type of parsing should be specified\n",type=str)
            
        parser.add_argument('-d','--directory_name',help=
        self.HELP_OF_DIRECTORY_NAME 
        if self.HELP_OF_DIRECTORY_NAME is not None else "directory name\n",type=str)
        
        parser.add_argument('-f','--source',help=
        self.HELP_OF_FROM
        if self.HELP_OF_FROM is not None else "Source directory\n this should be a path\n",type=str)
        
        parser.add_argument('-t','--to',help=
        self.HELP_OF_TO 
        if self.HELP_OF_TO is not None else
        "Destination folder\n this also should be a path\n",type=str)
        
        return parser.parse_args()
    
    def get_main_dir_name(self):
        return self.directory_name if self.get_cli().directory_name is None else self.get_cli().directory_name

    def set_main_dir_name(self,fname):
        self.directory_name=fname
    
    def get_type(self):
        return self.get_cli().type if self.type is None else self.type
        

    def get_video_dir(self):
        return self.DEFAULT_VIDEO_DIRECTORY if self.get_cli().source is None else self.get_cli().source
    
    def get_audio_dir(self):
        return self.DEFAULT_AUDIO_DIRECTORY if self.get_cli().source is None else self.get_cli().source
    
    def get_tex_dir(self):
        return self.DEFAULT_TEX_DIRECTORY if self.get_cli().source is None else self.get_cli().source

    def get_text_dir(self):
        return self.DEFAULT_TEXT_DIRECTORY if self.get_cli().source is None else self.get_cli().source
        
    def get_python_dir(self):
        return self.DEFAULT_PYTHON_DIRECTORY if self.get_cli().source is None else self.get_cli().source
    
    def get_all_dir(self):
        return self.DEFAULT_ALL_DIRECTORY if self.get_cli().source is None else self.get_cli().source
    
    def location(self):
        return self.get_cli().to if self.get_cli().to is not None else self.DEFAULT_DESTINATION
        
    def source(self):
        return eval('self.get_{}_dir()'.format(self.get_type()))
        
    def go_source(self):
        chdir(self.DEFAULT_DESTINATION if self.source() is None else self.source())

    def go_location(self):
        chdir(self.location())

    def get_extension(self,fname):
        return fname.split('.')[-1]

    def dirs(self):
        return self.get_main_dir_name()

    def make_dir(self,fname=None):
        if not exists(self.get_main_dir_name()):
            mkdir(self.get_main_dir_name()if fname is None else fname)#for external library use 
            if not fname is None:
                self.set_main_dir_name(fname)
                
    def go_main_dir(self):
        chdir(self.location())
        chdir(self.get_main_dir_name())

    def file_type(self):
        if self.get_type() == 'video':
            return self.VIDEO
        elif self.get_type() == 'audio':
            return self.AUDIO
        elif self.get_type() == 'tex':
            return self.TEX
        elif self.get_type() == 'text':
            return self.TEXT
        elif self.get_type() =='python':
            return self.PYTHON
        elif self.get_type() =='all':
            return self.VIDEO + self.AUDIO + self.TEX + self.TEXT + self.PYTHON
        else:
            return None

    def subdirs(self):
        subdirs=[]
        if not self.file_type() is None:
            for token in self.file_type():
                subdirs.append(self.get_extension(token))
            return subdirs
        else:
            return None

    def get_path(self,fname):
        return join(self.location(),fname)

    def get_full_path(self,fname,gname):
        return join(
            self.location(),
            self.dirs(),
            self.get_extension(fname),
            gname
        )

    def make_sub_dir(self):
        if self.subdirs() is not None:
            for files in self.subdirs():
                if not exists(files):
                    mkdir(files)

    def send(self,f1,f2):
        system(f'mv {f1} {f2}')

    def move(self):
        dirs=self.dirs()
        subdirs=self.subdirs()
        for token in listdir():
            if isfile(token) and self.get_extension(token) in subdirs:
                chdir(join(self.location(),self.dirs(),self.get_extension(token)))
                new_token=AvailName(token).get_name()
                self.go_source()
                self.send(token,self.get_full_path(token,new_token))


    def main(self):
        self.go_location()
        self.make_dir()
        self.go_main_dir()
        self.make_sub_dir()
        self.go_source()
        self.move()

if __name__=='__main__':
    Organizer()
