## Author
- Yke Rusticus: `yke.rusticus@gmail.com`
- MSc Artificial Intelligence: University of Amsterdam
## GENERAL 

This program can be used to detect image duplicates and/or highly similar 
images in specified folders and subfolders on your computer. These images
can then be iterated through and removed if desired.
Note: This program has been developed and tested exlusively on a Mac. Some
problems may occur for systems that have their trash bin located elsewhere
than on Mac (`~/.Trash`).

## GETTING STARTED

1. Put folder `ImageManager` next to folder(s) you want to check for duplicates.
2. Enter folder in terminal.
3. Install requirements:
    <pre><code>pip install -r requirements.txt</code></pre>
4. Run main.py:
    <pre><code>python main.py</code></pre>

## HELP

### Don’t know which directories are visible for the program?
  - Enter `ls` in the directory loader.

### Stuck in an iterating function and want to get out?
  - Enter `q`.

### What does the threshold mean?
  - Higher threshold -> more images that have some similarity are detected.
  - Lower threshold -> only highly similar images are detected.
  - Threshold should be between `0` and `1`.

### Can I undo my actions?
  - All files that are 'removed' are moved to the trash bin (`~/.Trash`),
    these can be retrieved from there.
