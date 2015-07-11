import os
import sys
dir_name_path = os.path.join(os.path.dirname(__file__), os.path.pardir)
print "MARK: dir", dir_name_path
sys.path.append(os.path.abspath(dir_name_path))
