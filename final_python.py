import sys
import logging
import shutil
import tempfile
import os
from argparse import ArgumentParser

# Function to remove folders that do not contain "__init__.py" files.
def remove_non_init_folders(directory):
    deleted_folders = []
    for dirpath, dirnames, files in os.walk(directory):
        contains_init = False
        if os.path.basename(dirpath) == os.path.basename(directory):
            continue
        for file_name in files:
            if file_name == "__init__.py":
                contains_init = True
                break
        if not contains_init:
            remove_directory(dirpath)
            deleted_folders.append(dirpath)
    return deleted_folders

# Function to unarchive a file to a specified path.
def unarchive_file(archive_file, path):
    try:
        shutil.unpack_archive(archive_file, path)
    except Exception as E:
        logger.error("Error while extracting the archive")

# Function to save the list of deleted folders to a text file.
def remove_folders_cleaned_txt(filename, deleted_folders):
    deleted_folders.sort()
    with open(filename, 'w') as file:
        for path in deleted_folders:
            file.write(os.path.relpath(path, os.path.dirname(filename))
                       )
            file.write("\n")

# Function to remove a directory and handle exceptions.
def remove_directory(directory):
    try:
        logger.info(f"directory removed {directory}")
        shutil.rmtree(directory)
    except Exception as e:
        logger.error(f'Error removing folder: {directory} - {e}')
        sys.exit(0)

def main():
    parser = ArgumentParser()
    parser.add_argument("archive_file", help="Path to archived file")
    args = parser.parse_args()

    # Create a temporary directory to extract the archive.
    with tempfile.TemporaryDirectory() as temp_dir:
        unarchive_file(args.archive_file, temp_dir)
        deleted_folders = remove_non_init_folders(temp_dir)

        # Save the list of deleted folders to a text file.
        remove_folders_cleaned_txt(os.path.join(temp_dir, 'cleaned.txt'), deleted_folders)

        # Build the new archived file
        archive_name = os.path.basename(args.archive_file)
        archive_name_without_extension = os.path.splitext(archive_name)[0]
        cleaned_archive = f"{archive_name_without_extension}_new"
        shutil.make_archive(cleaned_archive, 'zip', temp_dir)

# Initialize the logger and set the logging level to INFO.
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    main()
