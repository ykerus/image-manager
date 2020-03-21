#
# Author: Yke Rusticus
# Date  : 21 March 2020
#

from navigator import UserMenu
from manager import ImageManager
      
def main():
    menu = UserMenu(ImageManager())
    
    menu.print_stats()
    menu.execute1()
    menu.print_stats()
    menu.show()
    
    while menu.get_choice() != len(menu.options):
        menu.execute() 
        menu.print_stats()
        menu.show()
    
if __name__ == "__main__":
    main()