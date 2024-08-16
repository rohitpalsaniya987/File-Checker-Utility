import os
import hashlib

def compute_file_hash(file_path):
    """Compute the MD5 hash of the file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def generate_hash_file(directory, hash_file):
    """Generate a hash file with the MD5 hashes of all files in the directory."""
    with open(hash_file, "w") as f:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = compute_file_hash(file_path)
                relative_path = os.path.relpath(file_path, directory)
                f.write(f"{relative_path},{file_hash}\n")
    
    print(f"Hash file '{hash_file}' has been created.")

if __name__ == "__main__":
    directory_to_scan = "files"  # Replace with your directory name
    hash_file = "hash.md5"  # Replace with your desired hash file name
    generate_hash_file(directory_to_scan, hash_file)
