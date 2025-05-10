import os
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor
import platform
from pptx import Presentation
import olefile
import psutil

# Set up logging
logging.basicConfig(
    filename='file_search.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_connected_drives():
    """Returns a list of connected drive paths."""
    if platform.system() == 'Windows':
        # Get all Windows drive letters
        drives = []
        for disk in psutil.disk_partitions():
            drives.append(disk.mountpoint)
        return drives
    else:
        # For Unix-based systems, assume / is the main drive
        return ['/']

def get_author(file_path):
    """Extracts the author from a .ppt or .pptx file."""
    try:
        logging.info(f"Processing file: {file_path}")
        # Normalize the file path
        file_path = os.path.normpath(file_path)
        
        if not os.path.isfile(file_path):
            logging.error(f"File does not exist: {file_path}")
            return None
        
        if file_path.endswith('.pptx'):
            try:
                presentation = Presentation(file_path)
                author = presentation.core_properties.author
                if author:
                    logging.info(f"Author found: {author}")
                    return author.strip()
            except Exception as e:
                logging.error(f"Error reading .pptx file: {e}")
                return None
        elif file_path.endswith('.ppt'):
            try:
                if olefile.isOleFile(file_path):
                    ole = olefile.OleFileIO(file_path)
                    metadata = ole.get_metadata()
                    author = metadata.author
                    if author:
                        logging.info(f"Author found: {author}")
                        return author.strip()
                else:
                    logging.error(f"File is not a valid OLE2 file: {file_path}")
            except Exception as e:
                logging.error(f"Error reading .ppt file: {e}")
                return None
        return None
    except Exception as e:
        logging.error(f"Unexpected error processing file: {file_path} - {e}")
        return None

def process_file(file_path, destination_folder, target_author):
    """Processes a single file and copies it if it matches the criteria."""
    try:
        author = get_author(file_path)
        if author and author.lower() == target_author.lower():
            dest_path = os.path.join(destination_folder, os.path.basename(file_path))
            # Handle duplicate files
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(dest_path)
                counter = 1
                while os.path.exists(dest_path):
                    new_file = f"{base}_{counter}{ext}"
                    dest_path = os.path.join(destination_folder, new_file)
                    counter += 1
            shutil.copy2(file_path, dest_path)
            logging.info(f"File '{os.path.basename(file_path)}' copied to '{destination_folder}'")
            return True
    except Exception as e:
        logging.error(f"Failed to process file: {file_path} - {e}")
        return False

def search_files(search_root, destination_folder, target_author):
    """Searches for files in the specified root and copies matching files."""
    try:
        files_processed = 0
        files_copied = 0

        for root, dirs, files in os.walk(search_root):
            # Skip system directories
            if any(name in root for name in ['Windows', 'Program Files', 'AppData', 'System']):
                dirs.clear()
                continue
            
            for file in files:
                if file.lower().endswith(('.ppt', '.pptx')):
                    file_path = os.path.join(root, file)
                    # Skip temporary files
                    if file.startswith('~'):
                        continue
                    
                    if process_file(file_path, destination_folder, target_author):
                        files_copied += 1
                    files_processed += 1
        
        logging.info(f"Search completed in {search_root}: {files_processed} files processed, {files_copied} files copied.")
        return files_copied
    except Exception as e:
        logging.error(f"Error searching {search_root}: {e}")
        return 0

def main():
    target_author = "*********"
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    destination_folder = os.path.join(desktop, 'new_ppt_files')
    os.makedirs(destination_folder, exist_ok=True)
    logging.info(f"Destination folder created: {destination_folder}")

    # Get connected drives
    drives = get_connected_drives()
    logging.info(f"Connected drives: {drives}")

    # Use ThreadPoolExecutor to process multiple drives and files simultaneously
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = []
        for drive in drives:
            if os.path.exists(drive):  # Ensure the drive exists
                futures.append(executor.submit(search_files, drive, destination_folder, target_author))
        
        total_copied = 0
        for future in futures:
            total_copied += future.result()
        
        logging.info(f"Total files copied: {total_copied}")

if __name__ == "__main__":
    if platform.system() == 'Windows':
        os.chdir(os.path.join(os.path.expanduser('~')))
    main()