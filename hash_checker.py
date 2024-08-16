import hashlib
import os
import time

def check_files(directory, hash_file):
    start_time = time.time()
    missing_files = []
    mismatched_files = []

    # Load expected files, their hashes, and sizes from hash.txt
    with open(hash_file, 'r') as f:
        expected_files = f.readlines()

    for line in expected_files:
        try:
            filename, original_hash, original_size = line.strip().split(',')
            filepath = os.path.join(directory, filename)
            if os.path.exists(filepath):
                # Check size and hash
                current_size = os.path.getsize(filepath)
                if current_size != int(original_size):
                    mismatched_files.append(f"{filename} - Size mismatch")
                    continue
                
                current_hash = hashlib.sha256(open(filepath, 'rb').read()).hexdigest()
                if current_hash != original_hash:
                    mismatched_files.append(f"{filename} - Hash mismatch")
            else:
                missing_files.append(filename)
        except ValueError:
            print(f"Error processing line: {line.strip()}")

    end_time = time.time()

    # Report results
    if missing_files:
        print("Missing files:")
        for file in missing_files:
            print(file)
    else:
        print("No missing files.")

    if mismatched_files:
        print("\nFiles with issues:")
        for file in mismatched_files:
            print(file)
    else:
        print("All files have correct hashes and sizes.")

    print(f"File checking completed in {end_time - start_time:.2f} seconds.")

# Example usage
directory_to_check = "files"
hash_file = "hash.txt"
check_files(directory_to_check, hash_file)
