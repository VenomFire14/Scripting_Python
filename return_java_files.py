import os
import shutil

def extract_java_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".java"):
                # Get full path of source file
                src_file_path = os.path.join(root, file)

                # Compute relative path from source root
                rel_path = os.path.relpath(root, src_dir)

                # Destination folder path (preserving structure)
                dest_folder_path = os.path.join(dest_dir, rel_path)
                os.makedirs(dest_folder_path, exist_ok=True)

                # Destination file path
                dest_file_path = os.path.join(dest_folder_path, file)

                # Copy file
                shutil.copy2(src_file_path, dest_file_path)
                print(f"Copied: {src_file_path} -> {dest_file_path}")

# Example usage
if __name__ == "__main__":
    source_directory = input("Enter source directory path: ").strip()
    destination_directory = input("Enter destination directory path: ").strip()

    extract_java_files(source_directory, destination_directory)
