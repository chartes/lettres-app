import unittest
import os

os.chdir('..')

loader = unittest.TestLoader()
start_dir = 'tests'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)

if __name__ == "__main__":
    unittest.main()
