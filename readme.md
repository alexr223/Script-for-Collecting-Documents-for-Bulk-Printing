### How to Use `collect_pdfs.py`

1. Download this project: git clone https://github.com/alexr223/pdf-collector.git

2.  **Run the Script**  
   Open a terminal, navigate to the folder containing `collect_pdfs.py`, and run the script in VS Code or just in Windows Command Prompt with:
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
- The script searches for PDFs inside `Complete` folders.
- It will create a new folder at the save location named with the number of PDFs collected and the parent folder name.
- I added some example PDFs for testing to this same directory, you can try it here first


### Improvements to be Made
- Maybe look for PDFs in folders that maybe spelled "Complete " or "Completed"/folders with almost the exact same name but slight variations.
