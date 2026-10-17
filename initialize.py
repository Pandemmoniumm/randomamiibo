#!/usr/bin/env python3
import os
import sys

local_repo_path = os.path.expanduser("~/git-repos/randomamiibo/") 

if os.path.exists(local_repo_path):
    sys.path.insert(0, local_repo_path)
else:
    print(f"Error: Could not find your pyamiibo repository at {local_repo_path}")
    print("Please verify the folder path on line 7!")
    sys.exit(1)

from amiibo import AmiiboDump, AmiiboMasterKey

if not os.path.exists("key_retail.bin"):
    print("Error: key_retail.bin not found in the current working directory!")
    sys.exit(1)

with open("key_retail.bin", "rb") as k:
    master_keys = AmiiboMasterKey.from_combined_bin(k.read())

os.makedirs("./1_Fresh_Initialized", exist_ok=True)

print("processing")
for filename in os.listdir("."):
    if filename.endswith(".bin") and "key_retail" not in filename:
        try:
            with open(filename, "rb") as f:
                dump = AmiiboDump(f.read())
            
            dump.decrypt(master_keys)
            
            dump.data[0x1B4] = 0x01  # Stat Ceiling Calculation Flag
            dump.data[0x1B5] = 0x01  # App Initialized Identifier
            
            dump.encrypt(master_keys)
            
            with open(f"./1_Fresh_Initialized/{filename}", "wb") as out:
                out.write(dump.data)
            print(f" -> Initialized: {filename}")
                
        except Exception as e:
            print(f"Skipping {filename}: {e}")

print("\ndone")
