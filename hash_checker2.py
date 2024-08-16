import os
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor

def compute_file_hash(file_path):
    """Compute the MD5 hash of the file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def read_hashes_from_file(hash_file):
    """Read the file hashes from the hash file."""
    file_hashes = {}
    with open(hash_file, "r") as f:
        for line in f:
            try:
                file, file_hash = line.strip().split(',')
                file_hashes[file] = file_hash
            except ValueError:
                # Skip lines that don't match the expected format
                continue
    return file_hashes

def check_file(file_path, expected_hash):
    """Check if a file exists and if its hash matches the expected hash."""
    if os.path.exists(file_path):
        actual_hash = compute_file_hash(file_path)
        return (file_path, actual_hash == expected_hash)
    else:
        return (file_path, False)

def check_files(directory, hash_file):
    """Check the files listed in the hash file."""
    file_hashes = read_hashes_from_file(hash_file)
    
    missing_files = []
    mismatched_files = []

    start_time = time.time()

    # Use ThreadPoolExecutor to parallelize file checks
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(check_file, os.path.join(directory, file), file_hash): file
                   for file, file_hash in file_hashes.items()}

        for future in futures:
            file_path, is_valid = future.result()
            if not is_valid:
                if os.path.exists(file_path):
                    mismatched_files.append(file_path)
                else:
                    missing_files.append(file_path)

    end_time = time.time()
    print(f"Missing Files: {len(missing_files)}")
    for file in missing_files:
        print(f"Missing: {file}")

    print(f"Mismatched Files: {len(mismatched_files)}")
    for file in mismatched_files:
        print(f"Mismatched: {file}")

    print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    directory_to_check = "files"  # Folder named 'files' in the same directory
    hash_file = "hash.md5"  # Hash file in the same directory as this script
    check_files(directory_to_check, hash_file)
