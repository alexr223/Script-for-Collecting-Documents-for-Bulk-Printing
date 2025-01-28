import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def show_alert(message, title):
    """Show a quick alert before opening the directory dialog."""
    messagebox.showinfo(title, message)

def select_parent_directory():
    """Open a dialog to let the user select the parent directory."""
    show_alert("Please select the parent directory that contains the subfolders with 'Complete' folders.", "Select Parent Directory")
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    parent_directory = filedialog.askdirectory(title="Select Parent Directory")
    return parent_directory

def select_save_directory():
    """Open a dialog to let the user select where to save the compiled PDFs."""
    show_alert("Please select the destination folder where the PDFs will be saved.", "Select Save Directory")
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    save_directory = filedialog.askdirectory(title="Select Destination Folder")
    return save_directory

def gather_pdfs(parent_directory):
    """Gather all PDF files from the 'Complete' folders in each subfolder of the parent directory."""
    pdf_files = []
    # Iterate through each subfolder
    for subdir, dirs, files in os.walk(parent_directory):
        # Check if the "Complete" folder exists in the current directory
        if "Complete" in os.path.basename(subdir):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(subdir, file))
    return pdf_files

def create_destination_folder(save_directory, parent_name, num_pdfs):
    """Create a new folder to save the compiled PDFs, named with the parent folder name and the number of PDFs."""
    new_folder_name = f"{num_pdfs}_files_{parent_name}"
    new_folder_path = os.path.join(save_directory, new_folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    return new_folder_path

def copy_pdfs(pdf_files, destination_folder):
    """Copy the gathered PDFs into the destination folder."""
    for pdf in pdf_files:
        shutil.copy(pdf, destination_folder)

def run_process():
    """Main process that collects PDFs and saves them."""
    while True:
        # Step 1: Select the parent directory
        parent_directory = select_parent_directory()
        if not parent_directory:
            messagebox.showerror("Error", "No parent directory selected!")
            return

        # Step 2: Gather PDFs from each "Complete" folder
        pdf_files = gather_pdfs(parent_directory)

        if not pdf_files:
            messagebox.showwarning("No PDFs Found", "No PDFs were found in the 'Complete' folders.")
            continue  # Skip to the next directory

        # Step 3: Select the save location for the compiled PDFs
        save_directory = select_save_directory()
        if not save_directory:
            messagebox.showerror("Error", "No destination folder selected!")
            return

        # Step 4: Create a destination folder with the number of PDFs and parent folder name
        parent_name = os.path.basename(parent_directory)
        destination_folder = create_destination_folder(save_directory, parent_name, len(pdf_files))

        # Step 5: Copy PDFs to the new folder
        copy_pdfs(pdf_files, destination_folder)

        # Step 6: Success message
        messagebox.showinfo("Success", f"All PDFs have been copied to: {destination_folder}")

        # Step 7: Ask if the user wants to select another parent directory
        answer = messagebox.askyesno("Continue", "Do you want to select another parent directory?")
        if not answer:
            break  # Exit the loop and close the app

    messagebox.showinfo("Goodbye", "Thank you for using the PDF Collector. Goodbye!")

def main():
    """Start the PDF collection process."""
    run_process()

if __name__ == "__main__":
    main()
