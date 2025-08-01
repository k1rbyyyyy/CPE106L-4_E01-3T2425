# CPE106L Laboratory 5 - Main Runner
# Colonial Adventure Tours Database Lab

import sys
import os
import importlib.util

# Add project directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'prelab'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'inlab'))

# Import the activity functions
try:
    from prelab_activities import run_prelab_activities
    from inlab_activities import run_inlab_activities
except ImportError:
    # Alternative import method
    
    # Load prelab module
    prelab_spec = importlib.util.spec_from_file_location("prelab_activities", "prelab/prelab_activities.py")
    prelab_module = importlib.util.module_from_spec(prelab_spec)
    prelab_spec.loader.exec_module(prelab_module)
    run_prelab_activities = prelab_module.run_prelab_activities
    
    # Load inlab module  
    inlab_spec = importlib.util.spec_from_file_location("inlab_activities", "inlab/inlab_activities.py")
    inlab_module = importlib.util.module_from_spec(inlab_spec)
    inlab_spec.loader.exec_module(inlab_module)
    run_inlab_activities = inlab_module.run_inlab_activities

def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 60)
    print("CPE106L Laboratory 5 - Colonial Adventure Tours Database")
    print("=" * 60)
    print("1. Run PreLab Activities")
    print("   - Create ADVENTURE_TRIP table")
    print("   - Insert sample record")
    print("   - Delete table")
    print()
    print("2. Run InLab Activities") 
    print("   - Setup complete database with all tables")
    print("   - Display table contents")
    print("   - Perform database queries")
    print("   - Generate statistics")
    print()
    print("3. Run Both PreLab and InLab")
    print("4. Exit")
    print("=" * 60)

def main():
    """Main function to run the lab activities"""
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                print("\nRunning PreLab Activities...")
                run_prelab_activities()
                input("\nPress Enter to return to menu...")
                
            elif choice == '2':
                print("\nRunning InLab Activities...")
                run_inlab_activities()
                input("\nPress Enter to return to menu...")
                
            elif choice == '3':
                print("\nRunning Both PreLab and InLab Activities...")
                run_prelab_activities()
                print("\n" + "="*40)
                print("Moving to InLab Activities...")
                print("="*40)
                run_inlab_activities()
                input("\nPress Enter to return to menu...")
                
            elif choice == '4':
                print("\nThank you for using CPE106L Lab 5!")
                print("Colonial Adventure Tours Database Lab completed.")
                break
                
            else:
                print("\nInvalid choice. Please enter 1, 2, 3, or 4.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
