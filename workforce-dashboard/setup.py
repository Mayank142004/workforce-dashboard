#!/usr/bin/env python3
"""
Workforce Dashboard Setup Script
Helps configure the backend to connect to your agent's storage
"""

import os
import json
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def find_storage_folders():
    """Search for potential agent storage folders (Windows-safe)"""
    print("Searching for agent storage folders...")
    potential_paths = []

    search_paths = [
        Path.home(),
        Path.cwd(),
        Path.cwd().parent,
    ]

    EXCLUDE_DIRS = ("node_modules", ".pnpm", "npm", "AppData")

    for base_path in search_paths:
        try:
            for path in base_path.rglob("storage"):
                path_str = str(path)

                # 🚫 Skip dangerous directories
                if any(excl in path_str for excl in EXCLUDE_DIRS):
                    continue

                try:
                    if (path / "device.json").exists() or (path / "local.db").exists():
                        potential_paths.append(path)
                except (FileNotFoundError, OSError):
                    continue

        except (PermissionError, FileNotFoundError, OSError):
            continue

    return potential_paths


def verify_storage(storage_path):
    """Verify storage folder has required structure"""
    path = Path(storage_path)
    
    checks = {
        "Storage folder exists": path.exists(),
        "device.json found": (path / "device.json").exists(),
        "local.db found": (path / "local.db").exists(),
        "activity_logs folder": (path / "activity_logs").exists(),
        "screenshots folder": (path / "screenshots").exists(),
    }
    
    print("\nVerification Results:")
    print("-" * 40)
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}")
    
    return all(checks.values())

def read_device_info(storage_path):
    """Read employee info from device.json"""
    try:
        with open(Path(storage_path) / "device.json", 'r') as f:
            info = json.load(f)
            return info
    except Exception as e:
        print(f"Warning: Could not read device.json - {e}")
        return None

def update_backend_config(storage_path):
    """Update backend main.py with storage path"""
    backend_path = Path(__file__).parent / "backend" / "main.py"
    
    if not backend_path.exists():
        print(f"Error: Backend file not found at {backend_path}")
        return False
    
    try:
        with open(backend_path, 'r') as f:
            content = f.read()
        
        # Replace storage path
        old_line = 'STORAGE_PATH = Path("../agent/storage")'
        new_line = f'STORAGE_PATH = Path("{storage_path}")'
        
        updated_content = content.replace(old_line, new_line)
        
        with open(backend_path, 'w') as f:
            f.write(updated_content)
        
        print(f"\n✓ Backend configured successfully!")
        print(f"  Storage path set to: {storage_path}")
        return True
    except Exception as e:
        print(f"Error updating backend config: {e}")
        return False

def main():
    print_header("Workforce Dashboard Setup")
    
    print("This script will help you configure the dashboard backend")
    print("to connect to your desktop agent's storage folder.\n")
    
    # Option 1: Auto-detect
    print("Searching for agent storage folders...")
    found_paths = find_storage_folders()
    
    if found_paths:
        print(f"\nFound {len(found_paths)} potential storage folder(s):")
        for i, path in enumerate(found_paths, 1):
            print(f"  {i}. {path}")
            
        print(f"\n  0. Enter path manually")
        
        choice = input("\nSelect option (0-{}): ".format(len(found_paths)))
        
        try:
            choice = int(choice)
            if choice > 0 and choice <= len(found_paths):
                storage_path = found_paths[choice - 1]
            elif choice == 0:
                storage_path = input("\nEnter full path to storage folder: ").strip()
            else:
                print("Invalid choice")
                return
        except ValueError:
            print("Invalid input")
            return
    else:
        print("\nNo storage folders found automatically.")
        storage_path = input("Enter full path to storage folder: ").strip()
    
    # Verify the path
    print(f"\nVerifying storage folder: {storage_path}")
    
    if verify_storage(storage_path):
        print("\n✓ Storage folder verified successfully!")
        
        # Show employee info
        employee_info = read_device_info(storage_path)
        if employee_info:
            print("\nEmployee Information:")
            print("-" * 40)
            print(f"Name: {employee_info.get('employee_name', 'N/A')}")
            print(f"ID: {employee_info.get('employee_id', 'N/A')}")
            print(f"Email: {employee_info.get('email', 'N/A')}")
            print(f"Department: {employee_info.get('department', 'N/A')}")
        
        # Update backend config
        confirm = input("\nUpdate backend configuration? (y/n): ").lower()
        if confirm == 'y':
            if update_backend_config(storage_path):
                print_header("Setup Complete!")
                print("Next steps:")
                print("1. cd backend")
                print("2. pip install -r requirements.txt")
                print("3. python main.py")
                print("\nThen in another terminal:")
                print("4. cd frontend")
                print("5. npm install")
                print("6. npm run dev")
                print("\nAccess dashboard at: http://localhost:3000")
        else:
            print("\nSetup cancelled.")
    else:
        print("\n✗ Storage folder verification failed!")
        print("Please ensure:")
        print("  - The path is correct")
        print("  - device.json exists")
        print("  - activity_logs folder exists")
        print("  - You have read permissions")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
