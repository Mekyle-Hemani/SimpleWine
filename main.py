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
        colourprint.print_colored("OS has been previously verified", colourprint.GREEN)
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
            command("sudo apt-get update")
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
        colourprint.print_colored("Ubuntu has been previously verified", colourprint.GREEN)
        return True
    else:
        colourprint.print_colored("Installing Ubuntu desktop...", colourprint.ORANGE)
        process = subprocess.run("sudo apt install ubuntu-desktop", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.returncode == 0:
            save.save_data(True, "ubuntu_desktop")
            colourprint.print_colored("Ubuntu installed successfully", colourprint.GREEN)
        else:
            colourprint.print_colored(f"Error installing Ubuntu: \n{process.stderr.decode()}", colourprint.RED)
            return False
        return True
    
def lightdm():
    if save.load_part("lightdm") == True:
        colourprint.print_colored("Lightdm has been previously verified", colourprint.GREEN)
        return True
    else:
        colourprint.print_colored("Installing lightdm...", colourprint.ORANGE)
        process = subprocess.run("sudo apt install lightdm", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.returncode == 0:
            save.save_data(True, "lightdm")
            colourprint.print_colored("Lightdm installed successfully", colourprint.GREEN)
            #command("sudo reboot")
        else:
            colourprint.print_colored(f"Error installing lightdm: \n{process.stderr.decode()}", colourprint.RED)
            return False
        return True
    
def defualt_display():
    if save.load_part("defualt_display") == True:
        colourprint.print_colored("Defualt display has been previously verified", colourprint.GREEN)
        return True
    else:
        colourprint.print_colored("Installing defualt display...", colourprint.ORANGE)
        process = subprocess.run("sudo systemctl set-default multi-user.target", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.returncode == 0:
            save.save_data(True, "defualt_display")
            colourprint.print_colored("Defualt display installed successfully", colourprint.GREEN)
            #command("sudo reboot")
        else:
            colourprint.print_colored(f"Error installing defualt display: \n{process.stderr.decode()}", colourprint.RED)
            return False
        return True

def command_create():
    if save.load_part("command_create") == True:
        return True
    else:
        colourprint.print_colored("reating gui command display...", colourprint.ORANGE)
        subprocess.run("echo -e '#!/bin/bash\nsudo systemctl start lightdm' | sudo tee /usr/local/bin/start-gui", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run("sudo chmod +x /usr/local/bin/start-gui", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        save.save_data(True, "command_create")
        return True


if osname() == True:
    print(save.load_data())
    time.sleep(5)
    if install_ubuntu_desktop() == False:
        colourprint.print_colored("Failed installation... Fixing dependency", colourprint.YELLOW)
        time.sleep(2)
        command("sudo dpkg --configure -a")
    time.sleep(2)
    if lightdm() == False:
        quit()
    if defualt_display() == False:
        quit()
    if command_create() == False:
        quit()
    command("sudo reboot")

