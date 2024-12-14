import os
import sys
import re
import time
from loguru import logger

makers = {}

class MakeConfigs:
    GCC_Path = None
    CC_Path = None
    Environment = None

class Files:
    def __init__(self,files,type=None):
        self.files = files
        self.type = type

class Command:
    def __init__(self,commmand_string,type):
        self.command = commmand_string
        self.type = type
    @logger.catch
    def run(self):
        r = 0
        if self.type == "cml":
            r = os.system(self.command)
        elif self.type == "py":
            exec(self.command)
        return r


class Maker:
    def __init__(self, workpath, name, show=True):
        self.workpath = workpath
        self.show = show
        os.chdir(workpath)
        makers[name] = self
        self.command = []
    def set_workpath(self, workpath) -> None:
        self.workpath = workpath 
        self.command.append(Command(f"os.chdir('{workpath}')"),type="py")

    @logger.catch
    def make_command(self) -> None:
        for i in self.command:
            if self.show:
                print(i)
            result = i.run()
            if result != 0:
                logger.warning(f"Make maybe error . The error code is {result}")
        logger.info("Make Done.")
    def add_command(self,command:str,files:Files|None = None) -> None:
        if files != None:
            for i in files.files:
                self.command.append(Command(command.replace("{File}", i),type="cml"))
        else:
            self.command.append(Command(command,"cml"))

def choice_file(string):
    files = []
    for file, dir, filenames in os.walk():
        for i in filenames:
            if re.match(i,string):
                files.append(i)
    return Files(files,type="choiced")


def run_maker():
    t = time.time()
    makers[sys.argv[1]].make_command()
    logger.info(f"Run time : {(time.time() - t)}s")
if __name__ == "__main__":
    f = Files(["loguru","numpy"])
    Maker(".","all").add_command("python -m pip install {File}",files=f)
    run_maker()