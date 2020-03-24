#
# Author: Yke Rusticus
# Date  : 21 March 2020
#

import os
import matplotlib.pyplot as plt

class UserMenu():
    def __init__(self, imageManager):
        self.options = ["Load directory", "Find duplicates", 
                        "Manage duplicates", "Manage unopened files", "Exit"]  
        self.suboptions = ["List", "Iterate", "Exit"]  
        self.loadoptions = ["Load from disk", "Re-process"]
        self.imageManager = imageManager
        self.directory, self.threshold = None, None
        self.deleted, self.ignore = set(), set()
        
    def print_stats(self, clear=True):
        if clear:
            os.system("clear")
        print(f"\n| Directory loaded : {self.directory}")
        print(f"| Number of images : {self.imageManager.num_images}")
        print(f"| Unable to open   : {self.imageManager.num_unopened}")
        print(f"| Duplicates       : {self.imageManager.num_duplicates}")
        
    def show(self, clear=False):
        if clear:
            os.system("clear")
        print("\n> Select one of the following\n")
        for i, option in enumerate(self.options):
            print(f"  [{i+1}] {option}")
            
    def submenu(self, selection, clear=False):
        if clear:
            os.system("clear")
        self.print_stats()
        print(f"\n> Select how you would like to manage your {selection}\n")
        for i, option in enumerate(self.suboptions):
            print(f"  [{i+1}] {option}")
            
    def loadmenu(self):
        print()
        for i, option in enumerate(self.loadoptions):
            print(f"  [{i+1}] {option}")

    def get_choice(self, allow="general"):
        print() if allow=="general" or allow=="load" or allow=="subchoice" else ""
        while True:
            try:
                if allow == "general":
                    self.choice = int(input(">> "))
                    if self.choice > 0 and self.choice <= len(self.options):
                        return self.choice
                elif allow == "directory":
                    self.directory = input(">> ")
                    if not self.directory == "":
                        if os.path.exists(self.directory) or self.directory == "q" or self.directory == "ls":
                            return self.directory
                        elif os.path.exists("../"+self.directory):
                            self.directory = "../"+self.directory
                            return self.directory
                elif allow == "threshold":
                    self.threshold = input(">> ")
                    if self.threshold == "q" or self.threshold == "" or (float(self.threshold) >= 0 and float(self.threshold) <= 1):
                        return self.threshold
                elif allow == "subchoice":
                    self.subchoice = int(input(">> "))
                    if self.subchoice > 0 and self.subchoice <= len(self.suboptions):
                        return self.subchoice
                elif allow == "load":
                    self.loadchoice = int(input(">> "))
                    if self.loadchoice > 0 and self.loadchoice <= len(self.loadoptions):
                        return self.loadchoice
            except:
                pass  
        
    def execute1(self, clear=False, wait=True):
        if clear:
            os.system("clear")
        loaddata = False
        print("\n> Choose directory")
        while self.get_choice("directory") != "q":
            if self.directory == "ls":
                print("\n> Choose any of the following directories, or their subdirectories\n")
                for visible in os.listdir(".."):
                    if os.path.isdir("../"+visible) and visible[0] != ".":
                        print("  "+visible)
                print()
            else:
                if self.imageManager.data_on_disk(self.directory):
                    self.loadmenu()
                    if self.get_choice("load") == 1:
                        loaddata = True
                self.imageManager.load(self.directory, loaddata)
                if wait:
                    input("\n>> ENTER")
                self.print_stats()
                self.execute2()
                return
        if self.directory == "q":
            self.directory = None
            self.imageManager.reset()
        
            
    def execute2(self, clear=False, wait=True):
        if clear:
            os.system("clear")
        if self.directory is not None:
            print(f"\n> Select duplicate threshold (ENTER = {self.imageManager.threshold})")
            if self.get_choice("threshold") != "q":
                if self.threshold != "":
                    self.imageManager.threshold = float(self.threshold)
                self.imageManager.find_duplicates()
                if wait:
                    input("\n>> ENTER")
        else:
            print("\n> Load directory first")
            self.execute1()
        
    def execute3(self, clear=False):
        self.submenu("duplicates")
        while self.get_choice("subchoice") != len(self.suboptions):
            if self.subchoice == 1:
                os.system("clear")
                self.print_stats()
                print("\n> The following pairs are duplicates")
                self.imageManager.print_duplicates()
                input("\n>> ENTER")
            else:
                for fname1, fname2 in list(self.imageManager.duplicates):
                    if fname1 not in self.deleted and fname2 not in self.deleted and\
                                                (fname1, fname2) not in self.ignore:
                        os.system("clear")
                        self.print_stats()
                        print("\n> Delete [A/B] (ENTER = ignore)")
                        print("\n  [A] "+fname1+"\n  [B] "+fname2)
                        self.imageManager.show_pair(fname1, fname2)
                        delete = input(">> ")
                        plt.close()
                        if (delete == "A" or delete == "a") or (delete == "B" or delete == "b"):
                            fremove = fname1 if (delete == "A" or delete == "a") else fname2
                            self.imageManager.remove(fremove)
                            self.imageManager.trash(fremove)
                            self.deleted.add(fremove)
                        elif delete == "q":
                            break
                        else:
                            self.ignore.add((fname1, fname2))
                self.imageManager.write(self.directory)
            self.submenu("duplicates", clear=True)
        
    def execute4(self):
        self.submenu("unopened files")
        while self.get_choice("subchoice") != len(self.suboptions):
            if self.subchoice == 1:
                os.system("clear")
                self.print_stats()
                print("\n> The following files could not be opened\n")
                self.imageManager.print_unopened()
                input("\n>> ENTER")
            else:
                for fname in list(self.imageManager.unopened):
                    os.system("clear")
                    self.print_stats()
                    print("\n> Delete [y/n] (ENTER = ignore)\n")
                    delete = input("  "+fname+"\r") 
                    if delete == "y":
                        self.imageManager.unopened.remove(fname)
                        self.imageManager.trash(fname)
                    elif delete == "q":
                        break
                self.imageManager.write(self.directory)      
            self.submenu("unopened files")
        
           
    def execute(self):
        self.print_stats()
        exec("self.execute"+str(self.choice)+"()")
            