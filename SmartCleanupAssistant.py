
import os
import hashlib
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk
import shutil
from tkinter.font import Font

# ================================================== duplicate files =====================================================

def detect_duplicate_files():
    folder_path = filedialog.askdirectory() 
    if folder_path:  
        file_list = os.walk(folder_path)
        total_deleted_size = 0
        unique = dict()
        duplicate_files=[]
        for root, folders, files in file_list:
            for file in files:
                path1 = Path(os.path.join(root, file))
                fileHash = hashlib.md5(open(path1, 'rb').read()).hexdigest()
                if fileHash not in unique:
                    unique[fileHash] = path1
                else:
                    file_size = os.path.getsize(path1)
                    duplicate_files.append(path1)
                    total_deleted_size += file_size
                    # print(f"{path1} has been deleted")
                    
        if duplicate_files:
            print("-------------------------Duplicates  files------------------------------")
            for files in duplicate_files:
                print(files)
            permission=messagebox.askyesno("Delete Duplicate Files", "Duplicate files found. Do you want to delete them?")
            if permission:
                for i in duplicate_files:
                    os.remove(i)
                print('Deletion successful')
                if total_deleted_size > 999 * 1024 * 1024:  # If size is greater than 999 MB
                    total_deleted_size_gb = total_deleted_size / (1024 * 1024 * 1024)
                    messagebox.showinfo("Deletion Successful", f"You have cleared {total_deleted_size_gb:.2f} GB")
                else:
                    total_deleted_size_mb = total_deleted_size / (1024 * 1024)
                    messagebox.showinfo("Deletion Successful", f"You have cleared {total_deleted_size_mb:.2f} MB")
            else:
                messagebox.showinfo("deletion cancel", "deletion canceled.") 


        else:
            messagebox.showinfo("No Duplicates Found", "No duplicate files found in the selected folder.")  # Show info message if no duplicate files found



# ===================================================== detect large files =====================================================

def detect_large_files():
    def find_large_files(folder_path):
        large_files = []
        min_file_size_mb=7
        min_file_size_bytes = min_file_size_mb * 1024 * 1024  
        total_deleted_size_bytes = 0

        for root, _, files in os.walk(folder_path):
            # Check for large files
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                if file_size >= min_file_size_bytes:
                    large_files.append((file_path, file_size))
                    total_deleted_size_bytes += file_size

        return large_files, total_deleted_size_bytes

    def delete_large_files(files_to_delete):
        total_deleted_size_bytes = 0
        for file_path, file_size in files_to_delete:
            os.remove(file_path)
            total_deleted_size_bytes += file_size
            print(f"Deleted file: {file_path}")
        return total_deleted_size_bytes

    folder_path = filedialog.askdirectory()  # Open a file dialog to select a folder
    if folder_path:
        large_files, _ = find_large_files(folder_path)

        if large_files:
            print("Large files found:")
            for file_path, file_size in large_files:
                file_size_mb = file_size / (1024 * 1024)  # Convert bytes to MB
                print(f"File: {file_path} | Size: {file_size_mb:.2f} MB")

            delete_choice = messagebox.askyesno("Delete Files", "Do you want to delete these files?")
            if delete_choice:
                total_deleted_size_mb = delete_large_files(large_files) / (1024 * 1024)  # Convert bytes to MB
                if total_deleted_size_mb >= 999:
                    total_deleted_size_gb = total_deleted_size_mb / 1024  # Convert MB to GB
                    messagebox.showinfo("Deletion Successful", f"You have cleared {total_deleted_size_gb:.2f} GB")
                else:
                    messagebox.showinfo("Deletion Successful", f"You have cleared {total_deleted_size_mb:.2f} MB")
            else:
                messagebox.showinfo("deletion cancel", "deletion canceled.") 


        else:
            messagebox.showinfo("No Large Files", "No large files found in the selected directory.")
    else:
        messagebox.showinfo("No Folder Selected", "No folder selected.")


# ===================================================== smart organizer =====================================================


def file_organizer():
    folder_path = filedialog.askdirectory()  # Open a file dialog to select a folder
    permission=messagebox.askyesno("Permission", "Do you want to organize files")
    if permission:

        files = os.listdir(folder_path)
        arranged_files = False
        counter=0
        for file in files:

            if (os.path.isfile(os.path.join(folder_path, file))):
                counter+=1

            filename, extension = os.path.splitext(file)
            extension = extension[1:]  

            if os.path.exists(os.path.join(folder_path, extension)):
                shutil.move(os.path.join(folder_path, file), os.path.join(folder_path, extension, file))
                arranged_files = True
            else:
                os.makedirs(os.path.join(folder_path, extension))
                shutil.move(os.path.join(folder_path, file), os.path.join(folder_path, extension, file))
                arranged_files = True
        if counter<1:
            messagebox.showinfo("No Files", "No files to organize")

        else:
            if arranged_files:
                messagebox.showinfo("Done", "Your Folder Is Organized")
    else:
        messagebox.showinfo("Canceled", "Canceled")



#===================================================== Storageinformation =====================================================

def get_disk_space_info():
    total, used, free = shutil.disk_usage("/")  # Get disk space information for the root directory
    return total, used, free  # Return total space, used space, and free space

# ===================================================== main window =====================================================

root = tk.Tk()
root.title("Smart Cleanup Assistant")
root.geometry("600x350+400+200")  
# root.configure(background='cyan')
# Configure font for title
title_font = Font(family="Arial", size=28, weight="bold" )

# Create and place title label
title_label = tk.Label(root, text="Smart Cleanup Assistant", font=title_font,fg='blue')
title_label.pack(pady=10)

# Create and place buttons for different options
detect_duplicate_button = tk.Button(root, text="Detect Duplicate Files in a Folder", command=detect_duplicate_files,width="25")
detect_duplicate_button.pack(pady=5)

detect_large_files_button = tk.Button(root, text="Detect Large Files", command=detect_large_files,width="25")
detect_large_files_button.pack(pady=5)

file_organizer_button = tk.Button(root, text="Smart File Organizer", command=file_organizer,width="25")
file_organizer_button.pack(pady=5)

# Create labels to display disk space information
disk_space_label = tk.Label(root, text="""
-----------------------------
STORAGE INFORMATION
----------------------------""",font=("Arial", 12,"bold"))
disk_space_label.pack(pady=5)

# Get disk space information
total_space, used_space, free_space = get_disk_space_info()

# Create labels to display disk space information
total_space_label = tk.Label(root, text=f"Total Space: {total_space / (1024**3):.2f} GB", fg="blue",font=("Arial", 10,"bold"))
total_space_label.pack()
used_space_label = tk.Label(root, text=f"Used Space: {used_space / (1024**3):.2f} GB", fg="red",font=("Arial", 10,"bold"))
used_space_label.pack()
free_space_label = tk.Label(root, text=f"Free Space: {free_space / (1024**3):.2f} GB", fg="green",font=("Arial", 10,"bold"))
free_space_label.pack()

# Run the application
root.mainloop()
