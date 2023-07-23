# Subnet-Checker

## Overview

This system acts as a subnet inventory that allows users to perform the following actions: 
- add a subnet
- delete a subnet
- list all subnets
- check if subnet is in inventory
- check if subnet conflicts with another subnet in the inventory.

## Prerequisites

- Ubuntu 22.04 (Installation instructions can be found here: https://ubuntu.com/tutorials/install-ubuntu-server#1-overview)
- Python 3.8 or higher (Installation instructions can be found here: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-22-04)

## Installation and basic usage
The following instructions are for installation on Ubuntu 22.04

1. Download the ZIP package of the system by navigating to the GitHub repository and clicking on the green "Code" button.  In the dropdown list, click "Download ZIP"
2. In a terminal, navigate to the directory that the ZIP file was downloaded to
3. Unzip the package with the following command:
    `unzip Subnet-Checker-main.zip`
4. navigate into the unzipped folder with the following command:
   `cd Subnet-Checker-main`
5. To run the system and see a list of available options, use the command:
   `python3 subnet_inventory.py`
   or
   `python3 subnet_inventory.py -h`
6. To run the unit and system tests, use the command:
   `python3 tests.py`

## Detailed Usage

### Add a subnet to the inventory

1. To add a subnet, use the command:
   `python3 subnet_inventory.py -a`
2. Type a suitable name for your new subnet at the following prompt and hit enter:
   `Please enter a name for your subnet:`
3. Type the address of your new subnet in CIDR format at the following prompt and hit enter:
   `Please enter your subnet in CIDR notation:`
4. If successful, the subnet has now been added to the inventory

### List all subnets in inventory

1. To see a full list of all subnets currently in the inventory, use the command:
   `python3 subnet_inventory.py -l`

### Delete a subnet from the inventory

1. To delete a subnet, use the command:
   `python3 subnet_inventory.py -d`
2. Type the name of the subnet to delete at the following prompt and hit enter:
   `Please enter the name of the subnet you would like to delete:`
3. Confirm that you want to delete the subnet by typing Y at the following prompt and hit enter:
   `Are you sure you want to delete the test subnet? This action cannot be undone. (Y/n):`
4. If successful, the subnet has been deleted from the inventory

### Check if subnet is in inventory

1. To check if a subnet is already in the inventory, use the command:
   `python3 subnet_inventory.py -q`
2. Type the address of the subnet you would like to check in CIDR format at the following prompt and hit enter:
   `Please enter the subnet you would like to check in CIDR notation:`
3. The system will tell you whether the subnet is in the inventory.

### Check if a subnet conflicts with any other subnets already in the inventory

1. To check if a subnet conflicts with any other subnets in the inventory, use the command:
   `python3 subnet_inventory -c`
2. Type the address of the subnet you would like to check in CIDR format at the following prompt and hit enter:
   `Please enter the subnet you would like to check in CIDR notation:`
3. The system will output a list of any conflicting subnets in the inventory.