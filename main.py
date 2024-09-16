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
        colourprint.print_colored(f"Error: \n{process.stderr}", colourprint.RED)
        quit()


def osname():
    if (save.load_part("os") == True):
        return True
    else:
        if os_type == 'posix':
            colourprint.print_colored("OS is running Linux", colourprint.GREEN)

            if os.geteuid() == 0:
                colourprint.print_colored("Recieved sudo privileges", colourprint.GREEN)
            else:
                colourprint.print_colored("Attempting sudo", colourprint.GREEN)
                subprocess.call(['sudo', 'python3', *sys.argv])
                sys.exit()

            save.save_data(True, "os")
            command("sudo apt update && sudo apt upgrade")
            colourprint.print_colored("Updating...", colourprint.ORANGE)
            command("sudo reboot")
            return True
        else:
            colourprint.print_colored("OS is not Linux based, this file will not work", colourprint.RED)
            save.save_data(False, "os")
            quit()

def install_ubuntu_desktop():
    if save.load_part("ubuntu_desktop") == True:
        return True
    else:
        command("sudo apt install ubuntu-desktop")
        save.save_data(True,"ubuntu_desktop")
        return True

if osname() == True:
    install_ubuntu_desktop()
    colourprint.print_colored("Ubuntu installed", colourprint.GREEN)