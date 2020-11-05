import unittest

from prime import is_prime

class Tests(unittest.TestCase):

    def test_1(self):
        """ Check that 1 is not a prime number. """
        self.assertFalse(is_prime(1))
    
    def test_2(self):
        """ Check that 2 is a prime number. """
        self.assertTrue(is_prime(2))
    
    def test_8(self):
        """ Check that 8 is not a prime number. """
        self.assertFalse(is_prime(8))
    
    def test_11(self):
        """ Check that 11 is a prime number. """
        self.assertTrue(is_prime(11))
    
    def test_25(self):
        """ Check that 25 is not a prime number. """
        self.assertFalse(is_prime(25))
    
    def test_28(self):
        """ Check that 28 is not a prime number. """
        self.assertFalse(is_prime(28))
    
if __name__ == "__main__":
    unittest.main()