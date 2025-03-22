import os
import hashlib
from collections import defaultdict
# This program finds duplicate files in a given directory.
def menu():
    while True:
        print("\n--- File Duplicate Finder ---")
        print("1. Enter directory to search")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            directory = input("Enter the full path of the directory to search: ")
            if os.path.isdir(directory):
                find_duplicates(directory)
            else:
                print("Invalid directory. Please try again.")
        elif choice == '2':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

def get_checksum(file_path):
    hash_obj = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        print(f"Could not read file {file_path}: {e}")
        return None

def find_duplicates(directory):
    name_map = defaultdict(list)
    
    # Traverse directories recursively
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            name_map[file].append(file_path)

    # Compare files with the same name
    print("\n--- Duplicate Files Found ---")
    found_any = False
    for name, paths in name_map.items():
        if len(paths) > 1:
            checksums = defaultdict(list)
            for path in paths:
                checksum = get_checksum(path)
                if checksum:
                    checksums[checksum].append(path)

            for checksum, dup_paths in checksums.items():
                if len(dup_paths) > 1:
                    found_any = True
                    print(f"\nDuplicate name: {name}")
                    for p in dup_paths:
                        print(f"  {p}")
                    print("--------------------------")
    if not found_any:
        print("No duplicates found.")

if __name__ == "__main__":
    menu()
