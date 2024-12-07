import sys
import math
import os

# Get the input parameters
file_name = sys.argv[1]
print("File name:", file_name)
offset = int(sys.argv[2], 16)
print("Offset:", hex(offset))
len_to_delete = int(sys.argv[3])
print("Length to delete:", len_to_delete)
value = sys.argv[4]
print("Value to insert:", value)

# Calculate the byte length of the value (based on its hex representation)
l = math.ceil(len(value) / 2)
val = int(value, 16).to_bytes(l, "little")
print("Value as bytes:", val)

# Open the original file in read/write binary mode
with open(file_name, "r+b") as file:
    # Read the initial part of the file up to the offset
    start = file.read(offset)
    
    # Skip the section to delete
    file.seek(offset + len_to_delete)
    
    # Read the remaining part of the file
    end = file.read()
    
    # Open a new file to save the modified contents
    with open(file_name + ".break", "wb") as out_file:
        # Write the start of the file
        out_file.write(start)
        
        # Write the new value to insert
        out_file.write(val)
        
        # Write the rest of the file
        out_file.write(end)
    
    print(f"Modified file saved as: {file_name}.break")
