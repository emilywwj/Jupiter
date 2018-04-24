

import shutil
import os
import random
import time


def evaluate_random():
    """
    Copy files from folder ``sample_input`` to folder ``input`` at random intervals for evaluation 
    
    """
    file_count = len(os.listdir("sample_input/")) 
    interval = 120
    for i in range(1,file_count+1):
        n = random.randint(1,interval)
        count = 0
        while count<n:
            count = count+1
            time.sleep(1)
        src = "sample_input/%dbotnet.ipsum"%i
        dest = "input/%dbotnet.ipsum"%i
        print('---- Generate random input files')
        shutil.copyfile(src,dest)

def evaluate_interval(interval):
    """
    Copy files from folder ``sample_input`` to folder ``input`` one after another for evaluation 
    
    Args:
        interval (int): interval time to inject the sample input file
    
    """
    file_count = len(os.listdir("sample_input/"))
    src = "sample_input/1botnet.ipsum"
    dest = "input/1botnet.ipsum"
    print('---- Generate random input files')
    shutil.copyfile(src,dest)
    for i in range(2,file_count+1):
        count = 0
        while count<interval:
            count = count+1
            time.sleep(1)
        src = "sample_input/%dbotnet.ipsum"%i
        dest = "input/%dbotnet.ipsum"%i
        print('---- Generate random input files')
        shutil.copyfile(src,dest)
    print('---- Finish generating sequential input files')
    

if __name__ == '__main__':
	#evaluate_random()
    evaluate_interval(900)