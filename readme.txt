GENERAL 

This program can be used to detect image duplicates and/or highly similar 
images in specified folders and subfolders on your computer. These images
can then be iterated through and removed if desired.

GETTING STARTED

1. Put folder 'ImageManager' next to folder(s) you want to check for duplicates
2. Enter folder in terminal
3. Install requirements ($ pip install -r requirements.txt)
4. Run main.py ($ python main.py)

HELP

• Don’t know which directories are visible for the program?
  -> enter 'ls' in the directory loader

• Stuck in an iterating function and want to get out?
  -> enter ’q’

• What does the threshold mean?
  - higher threshold -> more images that have some similarity are detected
  - lower threshold -> only highly similar images are detected
  > threshold should be between 0 and 1

• Can I undo my actions?
  > all files that are 'removed' are moved to the trash bin (~/.Trash)
    these can be retrieved from there