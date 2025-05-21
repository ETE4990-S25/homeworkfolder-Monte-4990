import os
import hashlib

def menu():
    while True:
        print("\n--- File Duplicate Finder ---")
        print("1. Enter directory to search")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            directory = input("Enter the directory path to scan: ")
            find_duplicates(directory)  # Call the function
        elif choice == "2":
            print("Exiting program.")
            break  # Exit the loop
        else:
            print("Invalid option. Try again.")

def find_duplicates(directory):
    print(f"Scanning directory: {directory}")  # Debugging print
    file_dict = {}  # Dictionary to store filenames and their paths
    duplicates = []  # List to store duplicate files

    for root, _, files in os.walk(directory):
        print(f"Checking in: {root}")  # Debugging print
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Found file: {file_path}")  # Debugging print

            if file in file_dict:
                print(f"Possible duplicate found: {file}")  # Debugging print
                # Compare checksums
                if get_checksum(file_path) == get_checksum(file_dict[file]):
                    duplicates.append((file_dict[file], file_path))
            else:
                file_dict[file] = file_path

    if duplicates:
        print("\nDuplicate Files Found:")
        for original, duplicate in duplicates:
            print(f"Duplicate: {duplicate} (matches {original})")
    else:
        print("\nNo duplicate files found.")

def get_checksum(file_path):
    """Generate SHA-256 checksum of a file"""
    hash_obj = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return hash_obj.hexdigest()

if __name__ == "__main__":
    menu()