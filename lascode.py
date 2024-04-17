#######################################################
#
# Change the class code on LAS Datasets
#
# run with: python3 mode input_file output_file count(y to count points per cc)
#
#######################################################

# Dependencies
import sys
import pylas
import numpy as np
import numpy_indexed as npi
from collections import Counter

in_file = sys.argv[2]
out_file = sys.argv[3]
mode = sys.argv[1]

if len(sys.argv) == 5:
    count = sys.argv[4]

# Load data
las = pylas.read(in_file)

print("Mode: ", mode)
print("File: ", in_file, " → ", las, "\n")
print("Occurring class codes:")
print(np.unique(las.classification), "\n")


if mode == 'remap':
    # Remap Dictionary
    print("----------------------------------------------------------")
    print("All classcodes will be remapped using the following table:")
    dict_remap = {2: 1, 8: 11, 9: 11, 10: 3, 11: 10, 20: 5, 30: 6, 31: 14, 13: 9}
    for key, value in dict_remap.items():
        print(key, ' → ', value)
    print("\nAll other values will not be changed!")
    print("---------------------------------------------------------- \n")

    # Remap function using numpy_indexed
    las.classification = npi.remap(las.classification, list(dict_remap.keys()), list(dict_remap.values()))
elif mode == 'remove':
    # Remove classification
    dict_remove = {0:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:1, 10:1, 11:1, 12:1, 13:1, 14:1, 15:1, 16:1, 17:1, 18:1, 19:1, 20:1, 21:1, 22:1, 23:1, 24:1, 25:1, 26:1, 27:1, 28:1, 29:1, 30:1, 31:1}
    print("----------------------------------------------------------")
    print("All values will be set to background class (1).")
    print("---------------------------------------------------------- \n")
    las.classification = npi.remap(las.classification, list(dict_remove.keys()), list(dict_remove.values()))
else:
    print("ERROR: Mode is invalid. Please enter \'remove\' or \'remap\'")
    sys.exit(1)


# Point count per class
if count == 'y':
    print("Point count per class code in the output file:")
    point_count = Counter(las.classification)
    for key, value in sorted(point_count.items()):
        print(key, ' : ', value)
    print()

print("Result will be written to", out_file, " → ", las)
las.write(out_file)