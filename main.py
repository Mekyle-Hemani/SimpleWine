import save
import colourprint
import time
import os
import sys
import subprocess

os_type = os.name

def command(command):
    process = subprocess.run(command, shell=True)
    if process.stderr:
        colourprint.print_colored(f"Error: \n{process.stderr}")
        exit()


def osname():
    if (save.load_part("os") == True):
        command("sudo apt update && sudo apt upgrade")
    else:
        if os_type == 'posix':
            colourprint.print_colored("OS is running Linux", colourprint.GREEN)

            if os.geteuid() == 0:
                colourprint.print_colored("Recieved sudo privileges", colourprint.GREEN)
            else:
                colourprint.print_colored("Attempting sudo", colourprint.GREEN)
                subprocess.call(['sudo', 'python3', *sys.argv])
                sys.exit()

            save.save_data("os", True)
        else:
            colourprint.print_colored("OS is not Linux based, this file will not work", colourprint.RED)
            save.save_data("os", False)
            quit()
osname()