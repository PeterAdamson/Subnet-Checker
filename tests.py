#!/usr/bin/env python3

import unittest
import subnet_inventory
from subprocess import check_output


# Unit Tests
class TestFormatting(unittest.TestCase):

    def test_address_format_correct(self):
        correct_format = "10.0.0.0/24"
        self.assertTrue(subnet_inventory.check_address_format(cidr_string=correct_format))

    def test_address_format_incorrect(self):
        incorrect_format = "10.0.0.0"
        self.assertFalse(subnet_inventory.check_address_format(cidr_string=incorrect_format))


# System Tests
class TestSubnetConflictChecker(unittest.TestCase):

    def test_add_subnet(self):
        out = check_output(["python3", "subnet_inventory.py", "-l"]).decode()
        self.assertIn("Displaying all subnets", out)


if __name__ == '__main__':
    unittest.main()
