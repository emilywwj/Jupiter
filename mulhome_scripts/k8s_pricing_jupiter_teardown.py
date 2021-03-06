"""
    Tear down all Jupiter components (WAVE, CIRCE, DRUPE).
"""

__author__ = "Quynh Nguyen, Pradipta Ghosh, Pranav Sakulkar, Jason A Tran,  Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "2.0"

# from delete_all_circe import *
from delete_all_pricing_circe import *
from delete_all_profilers import *
from delete_all_waves import *
from delete_all_exec import *
from delete_all_heft import *

if __name__ == '__main__':
	# delete_all_circe()
	delete_all_pricing_circe()
	delete_all_waves()
	delete_all_heft()
	delete_all_profilers()
	delete_all_exec()
