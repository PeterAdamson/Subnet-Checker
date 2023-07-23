#!/usr/bin/env python3

"""
This script acts as an inventory system for subnets and can perform the following actions:
    - Add a subnet
    - Delete a subnet
    - Get all subnets
    - Check if a given subnet is in the system
    - Check if a given subnet conflicts with any in the system

Usage: python3 subnet_inventory.py [arguments]
"""

import argparse
import ipaddress
import re
import sys
from pathlib import Path

# TODO: A flat file is not the ideal solution for this system, a database would be a better solution
INVENTORY_PATH = "/subnet_inventory/inventory"
reserved_subnets = ["192.168.14.128/25"]


class Subnet:
    """Subnet object that holds the following class variables:
    name: String, the given name of the subnet
    cidr_string: String, the subnet address in CIDR format"""

    def __init__(self, name=None, cidr_string=None):
        self.name = name
        self.cidr_string = cidr_string


def add_subnet(subnet_object=None):
    """Adds a new subnet to inventory

    Args:
        subnet_object: Instance of Subnet representing the subnet to add to inventory

    Returns:
        Void

    Raises:
        None
    """
    # first check if conflict with a reserved subnet
    for reserved in reserved_subnets:
        if subnets_conflict(ipaddress.ip_network(subnet_object.cidr_string, strict=False),
                            ipaddress.ip_network(reserved, strict=False)):
            print("Subnet is reserved or conflicts with a reserved subnet and cannot be added")
            return

    conflicting_subnets = check_inventory_for_conflicts(cidr=ipaddress.ip_network(subnet_object.cidr_string,
                                                                                  strict=False))

    if conflicting_subnets:
        while True:
            verify = input("This subnet conflicts with one or more subnets already in the inventory. Are you sure you "
                           "wish to add it? (Y/n): ")
            if verify == "Y":
                break
            elif verify == "n":
                print("Did not add subnet to inventory")
                return
            else:
                print("Please select Y or n")

    to_add = "{name} {address}\n".format(name=subnet_object.name,
                                         address=subnet_object.cidr_string)

    with open(INVENTORY_PATH, "a+") as f:
        f.write(to_add)

    print("Subnet added to inventory: {subnet}".format(subnet=to_add))


def check_subnet_by_address(cidr_string=None):
    """Checks for existence of a given subnet in the inventory using the CIDR address

    Args:
        cidr_string: String representing the subnet to check if present in inventory

    Returns:
        Boolean:
            True if CIDR address is in inventory
            False otherwise

    Raises:
        FileNotFoundError if inventory has not yet been created
    """
    try:
        with open(INVENTORY_PATH, "r") as f:
            inventory = f.readlines()
    except FileNotFoundError:
        return False

    for inventory_address in inventory:
        if inventory_address.rsplit(' ', 1)[1].strip() == cidr_string:
            return True

    return False


def check_subnet_by_name(name_to_check=None):
    """Checks for existence of a given subnet in the inventory using the given subnet name

     Args:
         name_to_check: String representing the name of the subnet to check if present in inventory

     Returns:
         Boolean:
             True if name is in inventory
             False otherwise

     Raises:
         FileNotFoundError if inventory has not yet been created
     """
    try:
        with open(INVENTORY_PATH, "r") as f:
            inventory = f.readlines()
    except FileNotFoundError:
        return False

    for inventory_address in inventory:
        if inventory_address.rsplit(' ', 1)[0] == name_to_check:
            return True

    return False


def subnets_conflict(cidr1=None, cidr2=None):
    """Checks whether two subnets overlap

    Args:
        cidr1: ipaddress.ip_network object representing the first subnet to compare
        cidr2: ipaddress.ip_network object representing the second subnet to compare

    Returns:
        Boolean:
            True if cidr1 is partly or wholly contained in cidr2 or cidr2 is wholly contained in cidr1.
            False otherwise

    Raises:
        None
    """
    return cidr1.overlaps(cidr2)


def check_inventory_for_conflicts(cidr=None):
    """Checks the inventory for all subnet conflicts

    Args:
        cidr: ipaddress.ip_network object representing the subnet to check for conflicts against

    Returns:
        conflict_list: list of Subnet objects that conflict in the inventory

    Raises:
        None
    """
    with open(INVENTORY_PATH, "r") as f:
        inventory = f.readlines()

    conflict_list = []
    for inventory_address in inventory:
        cidr_string_to_compare = inventory_address.rsplit(' ', 1)[1].strip()
        if subnets_conflict(cidr, ipaddress.ip_network(cidr_string_to_compare, strict=False)):
            conflict_list.append(Subnet(name=inventory_address.rsplit(' ', 1)[0],
                                        cidr_string=cidr_string_to_compare))

    return conflict_list


def names_conflict(chosen_name=None):
    """Checks whether a chosen name is already used

    Args:
        chosen_name: String representing the name to be used for a subnet

    Returns:
        Boolean:
            True if name is already used
            False otherwise

    Raises:
        None
    """
    with open(INVENTORY_PATH, "r") as f:
        inventory = f.readlines()

    for inventory_address in inventory:
        if chosen_name == inventory_address.rsplit(' ', 1)[0]:
            return True

    return False


def check_address_format(cidr_string=None):
    """Verifies that a given address is in proper CIDR format

    Args:
        cidr_string: String representing the address to be used for a subnet

    Returns:
        Boolean:
            True if address is in CIDR format
            False otherwise

    Raises:
        None
    """
    cidr_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}"
    if re.search(cidr_pattern, cidr_string):
        return True
    return False


def display_inventory():
    """Displays the full contents of the inventory to the user

    Args:
        None

    Returns:
        Void

    Raises:
        None
    """
    with open(INVENTORY_PATH, 'r') as f:
        inventory = f.readlines()

    print("Subnet Name - Subnet Address")
    for line in inventory:
        split_line = line.rsplit(' ', 1)
        print("{name} - {address}".format(name=split_line[0],
                                          address=split_line[1].strip()))


def delete_subnet(delete_name=None):
    """Deletes a subnet from the inventory using the given name of the subnet

    Args:
        delete_name: String representing the name of the subnet to delete

    Returns:
        Void

    Raises:
        None
    """
    with open(INVENTORY_PATH, "r+") as f:
        inventory = f.readlines()
        f.seek(0)
        for inventory_address in inventory:
            inventory_name = inventory_address.rsplit(' ', 1)[0]
            if inventory_name != delete_name:
                f.write(inventory_address)
        f.truncate()
    # TODO: Should display the deleted address in addition to the name to the user
    print("{name} subnet removed from inventory".format(name=delete_name))


def setup_parser():
    """Setup for command line interface arguments

    Args:
        None

    Returns:
        argparse.ArgumentParser: parser object with command line arguments configured

    Raises:
        None
    """
    parser = argparse.ArgumentParser(description="Inventory system to track subnet usage.  All subnets must be in "
                                                 "CIDR notation, e.g. 10.0.0.0/8")
    exclusive_parser = parser.add_mutually_exclusive_group()
    exclusive_parser.add_argument("-a", "--add",
                                  help="Add new subnet to inventory",
                                  action="store_true", )
    exclusive_parser.add_argument("-d", "--delete",
                                  help="Delete subnet from inventory",
                                  action="store_true", )
    exclusive_parser.add_argument("-c", "--conflict",
                                  help="Check if subnet conflicts with any subnets already in inventory",
                                  action="store_true", )
    exclusive_parser.add_argument("-q", "--query",
                                  help="Check if a subnet already exists in inventory",
                                  action="store_true", )
    exclusive_parser.add_argument("-l", "--list",
                                  help="List all subnets in inventory",
                                  action="store_true", )
    return parser


# TODO: This user interface only prompts the user once and exits.  It may be preferable to the user to be able
#  to perform multiple actions without exiting the program each time
if __name__ == '__main__':
    args = setup_parser()

    # show help message if no arguments supplied
    if len(sys.argv) == 1:
        args.print_help(sys.stderr)
        sys.exit(1)

    args = setup_parser().parse_args()

    subnet = Subnet()
    # TODO: Lots of prompt reuse between arguments, would be better to break this out user prompts to a dedicated method
    #  that could be used for all arguments
    if args.add:
        print("Adding a new subnet")
        while True:
            user_subnet_name = input("Please enter a name for your subnet: ")
            if not names_conflict(chosen_name=user_subnet_name):
                subnet.name = user_subnet_name
                break
            print("ERROR: Name already in use.  Please use a different name.")

        while True:
            cidr_addr_string = input("Please enter your subnet in CIDR notation: ")
            # TODO: if nest, there is probably a cleaner way to do this
            if check_address_format(cidr_string=cidr_addr_string):
                if not check_subnet_by_address(cidr_string=cidr_addr_string):
                    subnet.cidr_string = cidr_addr_string
                    break
                else:
                    print("Subnet already in inventory.")
            else:
                print("ERROR: Address is not in CIDR format.  Addresses must be in CIDR format, e.g. 10.0.0.0/8")

        add_subnet(subnet_object=subnet)
    elif args.query:
        print("Checking for subnet in inventory")
        cidr_addr_string = input("Please enter the subnet you would like to check in CIDR notation: ")
        # TODO: it would be better if this output also told the user the name of the subnet from the inventory.  It
        #  may improve the user experience to also add in the CIDR format checking here as well even though we are
        #  not affecting the inventory here.
        if check_subnet_by_address(cidr_string=cidr_addr_string):
            print("Subnet exists in inventory")
        else:
            print("Subnet does not exist in inventory")
    elif args.conflict:
        print("Checking for subnet conflicts")
        cidr_addr_string = input("Please enter the subnet you would like to check in CIDR notation: ")
        if check_address_format(cidr_string=cidr_addr_string):
            conflicts = check_inventory_for_conflicts(cidr=ipaddress.ip_network(cidr_addr_string, strict=False))
            if not conflicts:
                print("No conflicting subnets in inventory")
            else:
                print("The following subnet conflicts were found: ")
                for conflict in conflicts:
                    print("Conflicting subnet: {name} {address}".format(name=conflict.name,
                                                                        address=conflict.cidr_string))
        else:
            print("ERROR: Address is not in CIDR format.  Addresses must be in CIDR format, e.g. 10.0.0.0/8")
    elif args.list:
        print("Displaying all subnets")
        display_inventory()
    elif args.delete:
        print("Deleting subnet")
        subnet_name = input("Please enter the name of the subnet you would like to delete: ")
        if check_subnet_by_name(name_to_check=subnet_name):
            # Ensure the user really wants to delete the subnet
            while True:
                confirm = input("Are you sure you want to delete the {name} subnet? This action cannot be undone. "
                                "(Y/n): ".format(name=subnet_name))
                if confirm == "Y":
                    delete_subnet(subnet_name)
                    break
                elif confirm == "n":
                    print("Subnet not deleted")
                    break
                else:
                    print("Please select Y or n")

        else:
            print("No subnet with that name found in inventory")
