#!/usr/bin/env python
import shutil
import sys, os
import glob

def run(args):
    if len(args) < 3:
        print "\nUsage: batch_rename <out> <in 1> <in 2>, ..."
        print "\nExample: batch_rename results/model_{0}.pdb Run_1/*.pdb Run_2/*.pdb\n"
        sys.exit()
        
    out_mask = args[0]
    
    path_to = os.path.split(out_mask)[0]
    if not os.path.exists(path_to):
        os.makedirs(path_to)

    global_ind = 0
    for mask in args[1:]:
        file_list = glob.glob(mask)
        file_list.sort()
        
        for in_file_name in file_list: 
            out_file_name = out_mask.format(global_ind)
            shutil.copy(in_file_name, out_file_name)
            global_ind += 1
        
if (__name__ == "__main__"):
    run(args=sys.argv[1:])