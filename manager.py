#
# Author: Yke Rusticus
# Date  : 21 March 2020
#

import os 
import cv2
import numpy as np
import pickle as pkl
import time
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
matplotlib.rcParams['toolbar'] = 'None'

class ImageManager():
    
    def __init__(self):
        self.reset()
        self.threshold = 0.2
        self.ignore = {"mov","MOV","mp4","MP4"}
        self.datadir = "Processed"
        self.csfont = {'fontname':'monospace'}
            
    @property
    def num_images(self):
        return len(self.imgdic)
    
    @property
    def num_duplicates(self):
        return len(self.duplicates)
    
    @property
    def num_unopened(self):
        return len(self.unopened)
    
    def reset(self):
        self.unopened, self.duplicates, self.imgdic = [], [], {}
    
    def resize(self, img, height=16, width=16):
        return cv2.resize(img, (height, width), interpolation=cv2.INTER_AREA)

    def intensity_diff(self, img):
        diff_row = np.diff(img.flatten()) > 0
        diff_col = np.diff(img.flatten("F")) > 0
        return np.concatenate((diff_row, diff_col))
        
    def get_fnames(self, directory):
        subdirs = []
        fnames = os.listdir(directory)   
        for fname in np.array(fnames):
            if fname[0] == '.':
                fnames.remove(fname)
            elif '.' not in fname[-5:]:
                fnames.remove(fname)
                subdirs.append(fname)
        return fnames, subdirs
        
    def process_imgs(self, directory):
        opened = 0
        fnames, subdirs = self.get_fnames(directory)
        for fname in fnames:
            impath = directory+'/'+fname
            try:  
                #open and process the image
                img = cv2.imread(impath, cv2.IMREAD_GRAYSCALE).astype(float)
                self.imgdic[impath] = self.intensity_diff(self.resize(img))
                opened += 1
                print("  {:<10} {}\r".format(str(opened)+'/'+str(len(fnames)), directory), end='')
            except:  
                #unable to open or process
                if fname[-3:] not in self.ignore:
                    self.unopened.append(impath)  
        print()
        for subdir in subdirs:
            try:
                self.process_imgs(directory+'/'+subdir)
            except:
                pass
            
    def get_diffscores(self):
        imgs = [self.imgdic[f] for f in self.fnames]
        if len(imgs) > 0:
            self.diffscores = pairwise_distances(imgs, metric="hamming")
        else:
            self.diffscores = np.array([[]])
        
    def get_path(self, directory):
        return self.datadir+'/'+''.join([char if char!='/' else':' for char in directory])+".pkl"
    
    def data_on_disk(self, directory):
        path = self.get_path(directory)
        return os.path.exists(path)
    
    def load(self, directory, loaddata=True):
        self.reset()
        path = self.get_path(directory) 
        if not os.path.exists(self.datadir):
            os.mkdir(self.datadir)
        if not os.path.exists(path) or not loaddata:
            print("\n> Processing data")
            self.process_imgs(directory)
            self.fnames = [*self.imgdic]
            self.get_diffscores()
            self.write(directory)
            
        else:
            print("\n> Loading data from disk")
            with open(path, "rb") as f:
                loaded = pkl.load(f)     
                self.imgdic = loaded["imgdic"] 
                self.unopened = loaded["unopened"]
                self.diffscores = loaded["diffscores"]
                self.fnames = [*self.imgdic]
        print(f"> Found {len(self.fnames)} images")
                
    def write(self, directory):
        path = self.get_path(directory)
        with open(path, "wb") as f:   
                pkl.dump({"imgdic": self.imgdic, 
                          "unopened": self.unopened, 
                          "diffscores": self.diffscores}, f)
     
    #https://stackoverflow.com/questions/7449585/how-do-you-set-
    # the-absolute-position-of-figure-windows-with-matplotlib
    def move_figure(self, f, x, y):
        """Move figure's upper left corner to pixel (x, y)"""
        backend = matplotlib.get_backend()
        if backend == 'TkAgg':
            f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
        elif backend == 'WXAgg':
            f.canvas.manager.window.SetPosition((x, y))
        else:
            # This works for QT and GTK
            # You can also use window.setGeometry
            f.canvas.manager.window.move(x, y)
                
    def show_pair(self, fname1, fname2):
        img1 = plt.imread(fname1)
        img2 = plt.imread(fname2)
        f = plt.figure(facecolor="black")
        plt.subplot(1,2,1)
        plt.title("[A] in '"+fname1.split("/")[-2]+"'", **self.csfont, color="white", )
        plt.imshow(img1)
        plt.axis("off")
        plt.subplot(1,2,2)
        plt.title("[B] in '"+fname2.split("/")[-2]+"'", **self.csfont, color="white" )
        plt.imshow(img2)
        plt.axis("off")
        # self.move_figure(f, 0, 0)
        plt.show(block=False)
    
    def remove(self, fname):
        indexf = self.fnames.index(fname)
        #need to recalculate diffscores if this changes order
        del self.imgdic[fname]
        self.fnames.remove(fname)
        self.diffscores = np.delete(self.diffscores, indexf, axis=0)
        self.diffscores = np.delete(self.diffscores, indexf, axis=1)
        N = len(self.duplicates)
        for i, (fname1, fname2) in enumerate(reversed(self.duplicates)):
            if fname1 == fname or fname2 == fname:
                del self.duplicates[N-i-1]
        
    def trash(self, fname):
        if os.path.exists(fname):
            os.rename(fname, os.path.expanduser("~/.Trash/"+fname.split("/")[-1]))
        else:
            print("\n> ERROR: "+fname+" ALREADY REMOVED")
            input("\n>> ENTER")
                    
    def print_unopened(self):
        for fname in self.unopened:
            time.sleep(0.03)
            print(f"  {fname}")
    
    def print_duplicates(self):
        for fname1, fname2 in self.duplicates:
            time.sleep(0.03)
            print("\n  "+fname1+"\n  "+fname2)
                
    def find_duplicates(self, print_results=False):
        self.duplicates = []
        duplicates = self.diffscores < self.threshold
        duplicates[np.triu_indices(len(self.fnames))] = False
        for i, j in np.argwhere(duplicates):
            self.duplicates.append((self.fnames[i], self.fnames[j]))
        print(f"> Found {len(self.duplicates)} duplicates")
        if print_results:
            self.print_duplicates()
        
    
    
                
    
                 