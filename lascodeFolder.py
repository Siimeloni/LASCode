#######################################################
#
# Change the class code on LAS Datasets
#
# run with: python3 /path/to/root_folder
#
#######################################################

# Dependencies
import os
import sys
import pylas
import numpy as np
import numpy_indexed as npi

root_folder = sys.argv[1]

# Remap Dictionary
print("----------------------------------------------------------")
print("All classcodes will be remapped using the following table:")
dict_remap = {2: 1, 8: 11, 9: 19, 10: 3, 11: 10, 20: 5, 30: 6, 31: 14, 13: 9}
for key, value in dict_remap.items():
    print(key, ' → ', value)
print("\nAll other values will not be changed!\n")
print("WITHHELD tag will be removed.")
print("---------------------------------------------------------- \n")


def remapLas(file, file_path, dict_remap) :

    # Load data
    las = pylas.read(file_path + '/' + file)
    

    print("Occurring class codes:")
    print(np.unique(las.classification), "\n")

    

    # Remap function using numpy_indexed
    las.classification = npi.remap(las.classification, list(dict_remap.keys()), list(dict_remap.values()))

    # Remove withheld tag
    las.withheld = npi.remap(las.withheld, [True], [False])

    # Output data
    out_folder = path + '/output/'
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    las.write(out_folder + file)


for (path,directories, files) in os.walk(root_folder):
    for file in files:
        # Check file extension and path
        if (os.path.splitext(file)[1] != '.las' or path[-6:] == 'output'):
            continue
        
        print( "->  " + path + "/" + file + ":")
        remapLas(file, path, dict_remap)
        