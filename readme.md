### How to Use `collect_pdfs.py`

You will need Python, which you can install here: https://www.python.org/downloads/
Also, VS Code: https://code.visualstudio.com/download

### To run in VS Code (without executable)

1. Download this project by running this command in Windows PowerShell: ```git clone https://github.com/alexr223/Script-for-Collecting-Documents-for-Bulk-Printing``` You can also do this: https://github.com/alexr223/Script-for-Collecting-Documents-for-Bulk-Printing/archive/refs/heads/main.zip.

2.  **Run the Script**  
   Open a terminal, navigate to the folder containing `collect_pdfs.py`, and run the script in VS Code or just in Windows PowerShell with:
   ```terminal
   python collect_pdfs.py
   ```

3. **Select Parent Directory**  
   The script will prompt you to select the parent directory that contains subfolders with a `Complete` folder. This is where it will search for PDFs.

4. **Select Save Directory**  
   After gathering the PDFs, you'll be asked to choose a destination folder where the compiled PDFs will be saved.

5. **Repeat or Exit**  
   After saving, you can choose to select another parent directory or exit the script. If no more directories are selected, the script will close.

### Key Points:
- The script searches for PDFs inside `Complete` folders. It uses the package called Tkinter, which should come preinstalled with Python.
- It will create a new folder at the save location named with the number of PDFs collected and the parent folder name.
- I added some example PDFs for testing to this same directory, so you can try it here first. There's 4 subfolders, with 1 pdf in the complete folder in each.

### To run as an executable:
Go to ```dist/collect_pdfs.exe``` and run it

### Improvements to be Made
```diff
- Maybe look for PDFs in folders that maybe spelled "Complete " or "Completed"/folders with almost the exact same name but slight variations.~~~
```

> Above was added on 1/28/25

# Errors
- Printing was out of order due not to sorting the subfolders first by name in ascending order. Should be fixed.