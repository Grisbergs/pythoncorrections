import os
import shutil
from pathlib import Path

def organize_files_interactive():
    """
    Interactive version - lets you choose file types and directory
    """
    print("=== File Organizer ===")
    
    # Get source directory
    source_dir = input("Enter source directory (press Enter for current): ").strip()
    if not source_dir:
        source_dir = "."
    
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"Error: Directory '{source_dir}' does not exist!")
        return
    
    # Get file extensions
    extensions_input = input("Enter file extensions (e.g., .jpg,.png,.pdf): ").strip()
    if not extensions_input:
        print("No extensions provided. Exiting.")
        return
    
    extensions = [ext.strip() for ext in extensions_input.split(",")]
    
    # Confirm before proceeding
    print(f"\nWill organize files with extensions: {', '.join(extensions)}")
    print(f"From directory: {source_path.absolute()}")
    confirm = input("Continue? (y/n): ").lower()
    if confirm != 'y':
        return
    
    total_moved = 0
    for ext in extensions:
        files = list(source_path.glob(f"*{ext}"))
        print(f"\nProcessing {ext} files ({len(files)} found):")
        
        for file_path in files:
            folder_name = file_path.stem
            folder_path = source_path / folder_name
            
            folder_path.mkdir(exist_ok=True)
            destination = folder_path / file_path.name
            shutil.move(str(file_path), str(destination))
            
            print(f"  ✓ {file_path.name} → {folder_name}/")
            total_moved += 1
    
    print(f"\n✅ Done! Moved {total_moved} files.")

def organize_files_by_extensions(extensions, source_directory="."):
    """
    Organize multiple file types at once
    
    Args:
        extensions (list): List of extensions like ['.jpg', '.png', '.pdf']
        source_directory (str): Directory to search in
    """
    source_path = Path(source_directory)
    
    total_moved = 0
    for ext in extensions:
        files = list(source_path.glob(f"*{ext}"))
        for file_path in files:
            folder_name = file_path.stem
            folder_path = source_path / folder_name
            
            folder_path.mkdir(exist_ok=True)
            destination = folder_path / file_path.name
            shutil.move(str(file_path), str(destination))
            
            print(f"Moved '{file_path.name}' → '{folder_name}/'")
            total_moved += 1
    
    print(f"\n✅ Organized {total_moved} files!")

# SINGLE FILE TYPE FUNCTION (the missing one!)
def organize_files_by_name(file_extension, source_directory="."):
    """
    Organize files of a specific extension into folders named after themselves.
    """
    return organize_files_by_extensions([file_extension], source_directory)

# FIXED MAIN SECTION - Now it works perfectly!
if __name__ == "__main__":
    print("Choose an option:")
    print("1. Quick: Organize JPG files")
    print("2. Multiple types")
    print("3. Interactive mode")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        organize_files_by_name('.jpg')
    elif choice == "2":
        organize_files_by_extensions(['.jpg', '.png', '.pdf'])
    elif choice == "3":
        organize_files_interactive()
    else:
        print("Running interactive mode by default...")
        organize_files_interactive()