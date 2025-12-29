import sys
import traceback

try:
    print("Starting launcher...")
    import launcher
    print("Launcher module imported")
    launcher.main()
    print("Main function called")
except Exception as e:
    print(f"\n=== ERROR ===")
    print(f"Error: {e}")
    print(f"\nTraceback:")
    print(traceback.format_exc())
    input("\nPress Enter to exit...")
