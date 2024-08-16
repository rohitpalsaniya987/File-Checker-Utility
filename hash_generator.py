import hashlib
import os

def generate_file_hashes(directory, hash_file):
    with open(hash_file, 'w') as f:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                # Calculate hash and get the file size
                file_hash = hashlib.sha256(open(filepath, 'rb').read()).hexdigest()
                file_size = os.path.getsize(filepath)
                # Write the filename, hash, and size to hash.txt
                f.write(f"{filename},{file_hash},{file_size}\n")
    print("Hashes, sizes, and names generated and saved to hash.txt")

# Example usage
directory_to_scan = "files"
hash_file = "hash.txt"
generate_file_hashes(directory_to_scan, hash_file)
