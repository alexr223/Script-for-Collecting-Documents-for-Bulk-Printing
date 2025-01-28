import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

def show_alert(message, title):
    """Show a quick alert before opening the directory dialog."""
    messagebox.showinfo(title, message)

def select_parent_directory():
    """Open a dialog to let the user select the parent directory."""
    show_alert("Select the parent directory containing the subfolders.", "Select Parent Directory")
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    return filedialog.askdirectory(title="Select Parent Directory")

def select_save_directory():
    """Open a dialog to let the user select where to save the compiled PDFs."""
    show_alert("Select the destination folder for the compiled PDFs.", "Select Save Directory")
    root = tk.Tk()
    root.withdraw()  
    return filedialog.askdirectory(title="Select Destination Folder")

def get_pdf_order_from_csv(csv_path):
    """Reads 'addresses.csv' from the parent directory and extracts the ordered list of PDF file paths."""
    df = pd.read_csv(csv_path)
    return df["File Name"].dropna().tolist()  # Get ordered list of file paths

def find_complete_folders(subfolder):
    """Finds possible 'Complete' folders inside a given subfolder."""
    possible_names = ["Complete", "Complete ", "Completed", "complete", "complete ", "completed"]
    complete_folders = [os.path.join(subfolder, d) for d in os.listdir(subfolder) if any(d.startswith(name) for name in possible_names)]
    return complete_folders

def gather_pdfs(parent_directory, pdf_order):
    """Collect PDFs from 'Complete' folders, renaming them with the parent folder name, and sorting before copying."""
    pdf_dict = {}  

    # Get a sorted list of subdirectories
    subfolders = sorted(
        [os.path.join(parent_directory, d) for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]
    )

    for subfolder in subfolders:
        complete_folders = find_complete_folders(subfolder)  # Find possible 'Complete' folders
        for complete_folder in complete_folders:
            if os.path.exists(complete_folder):
                for file in os.listdir(complete_folder):
                    if file.lower().endswith(".pdf"):
                        original_path = os.path.join(complete_folder, file)
                        new_file_name = f"{os.path.basename(subfolder)}_{file}"  # Append subfolder name
                        pdf_dict[original_path] = new_file_name  

    # Sort collected PDFs based on order in CSV file
    sorted_pdfs = []
    for pdf in pdf_order:
        for stored_pdf, renamed_file in pdf_dict.items():
            if os.path.basename(stored_pdf) == os.path.basename(pdf):
                sorted_pdfs.append((stored_pdf, renamed_file))
                break

    # Final sorting of files by name in ascending order
    sorted_pdfs.sort(key=lambda x: x[1])

    return sorted_pdfs

def create_destination_folder(save_directory, parent_name, num_pdfs):
    """Create a destination folder named with the parent folder name and number of PDFs."""
    new_folder_name = f"{num_pdfs}_files_{parent_name}"
    new_folder_path = os.path.join(save_directory, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    return new_folder_path

def copy_pdfs_with_progress(pdf_files, destination_folder):
    """Copy PDFs into the destination folder while preserving order and showing progress."""
    
    # Initialize progress bar window
    progress_window = tk.Tk()
    progress_window.title("Copying PDFs")
    progress_window.geometry("400x150")
    
    tk.Label(progress_window, text="Copying files... Please wait.", font=("Arial", 12)).pack(pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate", variable=progress_var)
    progress_bar.pack(pady=10)

    status_label = tk.Label(progress_window, text="", font=("Arial", 10))
    status_label.pack()

    total_files = len(pdf_files)
    progress_increment = 100 / total_files if total_files else 1

    progress_window.update_idletasks()  # Force UI update

    # Copy files with progress updates
    for index, (pdf_path, new_name) in enumerate(pdf_files, start=1):
        shutil.copy(pdf_path, os.path.join(destination_folder, new_name))
        
        # Update progress
        progress_var.set(index * progress_increment)
        status_label.config(text=f"Copied {index}/{total_files}: {new_name}")
        progress_window.update_idletasks()  # Refresh UI

    progress_window.destroy()  # Close progress window when done

def run_process():
    """Main process to collect PDFs and save them in order."""
    while True:
        parent_directory = select_parent_directory()
        if not parent_directory:
            messagebox.showerror("Error", "No parent directory selected!")
            return

        csv_path = os.path.join(parent_directory, "addresses.csv")
        if not os.path.exists(csv_path):
            messagebox.showerror("Error", f"'addresses.csv' not found in {parent_directory}!")
            return

        save_directory = select_save_directory()
        if not save_directory:
            messagebox.showerror("Error", "No destination folder selected!")
            return

        pdf_order = get_pdf_order_from_csv(csv_path)
        pdf_files = gather_pdfs(parent_directory, pdf_order)

        if not pdf_files:
            messagebox.showwarning("No PDFs Found", "No matching PDFs were found in the 'Complete' folders.")
            continue

        parent_name = os.path.basename(parent_directory)
        destination_folder = create_destination_folder(save_directory, parent_name, len(pdf_files))

        copy_pdfs_with_progress(pdf_files, destination_folder)  # Copy with progress bar

        messagebox.showinfo("Success", f"All PDFs have been copied to: {destination_folder}")

        answer = messagebox.askyesno("Continue", "Do you want to select another parent directory?")
        if not answer:
            break

    messagebox.showinfo("Goodbye", "Thank you for using the PDF Collector. Goodbye!")

def main():
    """Start the PDF collection process."""
    run_process()

if __name__ == "__main__":
    main()
