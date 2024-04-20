import os
import shutil
import multiprocessing
import sys


folder_list = []


def traverse_folder(root):
    folder_list.append(root)
    for _, dirs, _ in os.walk(root):
        for dir in dirs:
            traverse_folder(os.path.join(root, dir))



def sort_files(folder, destination_folder):
    for root, _, files in os.walk(folder):
        for file in files:
            _, ext = os.path.splitext(file)
            ext_folder = os.path.join(destination_folder, ext[1:])  # Remove dot from extension
            os.makedirs(ext_folder, exist_ok=True)
            source_file = os.path.join(root, file)
            destination_file = os.path.join(ext_folder, file)
            shutil.copy2(source_file, destination_file)
            print(f"Copying {source_file} to {destination_file}")


def clean_destination(destination_folder):
    # Check if the destination folder exists
    if os.path.exists(destination_folder):
        # Iterate over the files and subdirectories in the destination folder
        for root, dirs, files in os.walk(destination_folder, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)


def main(source_folder, destination_folder, num_threads):
    # Create destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
     
    # Clean dest folder 
    clean_destination(destination_folder)

    # Create list of folders (subfolders, etc.)   
    traverse_folder(source_folder)

    # Show folders
    for file in folder_list:
        print(file)


    # Divide folders into chunks
    chunk_size = (len(folder_list) + num_threads - 1) // num_threads
    folder_chunks = [folder_list[i:i + chunk_size] for i in range(0, len(folder_list), chunk_size)]


    # Launch processes for each folder chunk
    processes = []
    for chunk in folder_chunks:
        for folder in chunk:
            

            process = multiprocessing.Process(target=sort_files, args=(folder, destination_folder))
            process.start()
            processes.append(process)

   

    # Wait for all processes to finish
    for process in processes:
        process.join()




if __name__ == "__main__":

   
    # Check if enough arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python script.py <source_path> <destination_path>")
        sys.exit(1)

    # Extract source and destination paths from command line arguments
    source_path = sys.argv[1]
    destination_path = sys.argv[2]


    main(source_path, destination_path, num_threads=2)

    
