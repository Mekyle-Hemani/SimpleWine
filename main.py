import save
import colourprint
import time
import os

os_type = os.name

def osname():


    if (save.load_part("os") == True):
        print("passed")
    else:
        if os_type == 'posix':
            colourprint.print_colored("OS is running Linux", colourprint.GREEN)
            save.save_data("os", True)

        else:
            colourprint.print_colored("OS is not Linux based, this file will not work", colourprint.RED)
            save.save_data("os", False)
            quit()

osname()