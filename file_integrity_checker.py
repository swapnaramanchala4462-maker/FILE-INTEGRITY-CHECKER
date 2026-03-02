import os
import hashlib
import json
from datetime import datetime
BASELINE_FILE="baseline.json"
#--------HASH FUNCTION----------
def calculate_hash(file_path):
    sha256=hashlib.sha256()
    try:
        with open(file_path,"rb") as f:
            while True:
                chunk=f.read(4096)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    except(FileNotFoundError,PermissionError):
        return None
#-------DIRECTORY SCAN----------
def scan_directory(folder_path):
    file_hashes={}
    for root, dirs,files in os.walk(folder_path):
        for file in files:
            full_path=os.path.join(root,file)
            file_hash=calculate_hash(full_path)
            if file_hash:
                file_hashes[full_path]=file_hash
    return file_hashes
#-------BASELINE FUNCTION-----
def load_baseline():
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    return{}
def save_baseline(data):
    with open(BASELINE_FILE,"w") as f:
        json.dump(data,f,indent=4)
#---------comparison---------
def compare_files(old_data,new_data):
    print("\n FILE INTEGRITY CHECK ")
    print("time:",datetime.now())
    print(" \n ")
    changes_detected=False
    for file in new_data:
        if file not in old_data:
            print("[NEW FILE]",file)
            changes_detected =True
        elif old_data[file]!=new_data[file]:
            print("[MODIFIED]",file)
            changes_detected=True
    for file in old_data:
        if file not in new_data:
            print("[DELETED]",file)
            changes_detected=True
    if not changes_detected:
        print("No changes detected. File Integrity Maintained.")
#-----MAIN-------- 
def main():
    print("File Integrity Checker")
    folder_path=input("enter folde path to monitor:").strip()
    if not os.path.exists(folder_path):
        print("Invalid folder path")
        return
    old_data=load_baseline()
    new_data=scan_directory(folder_path)
    if not old_data:
        print("No baseline found. creating baseline...")
        save_baseline(new_data)
        print("Baseline created successfully.")
    else:
        compare_files(old_data,new_data)
        save_baseline(new_data)
if __name__=="__main__":
    main()
