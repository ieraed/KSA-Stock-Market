#!/usr/bin/env python3
"""
🧹 Empty File Detector & Cleaner
Automatically finds and optionally removes empty files in the workspace
"""

import os
from pathlib import Path

def find_empty_files(directory="."):
    """Find all empty files in the directory"""
    empty_files = []
    for root, dirs, files in os.walk(directory):
        # Skip .git and __pycache__ directories
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'node_modules']]
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.getsize(file_path) == 0:
                    empty_files.append(file_path)
            except (OSError, IOError):
                continue
    
    return empty_files

def main():
    print("🔍 Scanning for empty files...")
    empty_files = find_empty_files()
    
    if not empty_files:
        print("✅ No empty files found!")
        return
    
    print(f"📋 Found {len(empty_files)} empty files:")
    for file in empty_files:
        print(f"  📄 {file}")
    
    print("\n❓ Options:")
    print("1. List only (do nothing)")
    print("2. Delete all empty files")
    print("3. Interactive delete (ask for each file)")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "2":
        print("\n🗑️ Deleting all empty files...")
        for file in empty_files:
            try:
                os.remove(file)
                print(f"  ✅ Deleted: {file}")
            except Exception as e:
                print(f"  ❌ Failed to delete {file}: {e}")
        print(f"\n✅ Cleanup completed! Deleted {len(empty_files)} files.")
    
    elif choice == "3":
        print("\n🗑️ Interactive deletion:")
        deleted = 0
        for file in empty_files:
            response = input(f"Delete '{file}'? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                try:
                    os.remove(file)
                    print(f"  ✅ Deleted: {file}")
                    deleted += 1
                except Exception as e:
                    print(f"  ❌ Failed: {e}")
            else:
                print(f"  ⏭️ Skipped: {file}")
        print(f"\n✅ Deleted {deleted} out of {len(empty_files)} files.")
    
    else:
        print("\n✅ No files deleted.")

if __name__ == "__main__":
    main()
