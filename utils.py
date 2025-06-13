import sys
import os

def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller.

    Args:
        relative_path: The path to the resource relative to the application's
                       root (if running from source) or the temporary folder
                       (if running as a frozen PyInstaller bundle).

    Returns:
        The absolute path to the resource.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # This attribute is set by PyInstaller at runtime.
        base_path = sys._MEIPASS
    except AttributeError:
        # sys._MEIPASS is not defined, so we are likely running in a normal
        # Python environment (e.g., during development).
        # Use the directory of the main script or the current working directory.
        # os.path.abspath(".") gives the current working directory.
        # If your assets are relative to your main script's location,
        # you might prefer: os.path.dirname(os.path.abspath(__main__.__file__))
        # However, for simplicity and common project structures where assets are
        # relative to the project root (where you run the script from),
        # os.path.abspath(".") is often suitable.
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    # Example Usage (for testing utils.py directly)
    # These examples assume you have an 'assets/icon.ico' and 'config/theme.json'
    # relative to where you run 'python utils.py' from, or in the _MEIPASS folder if frozen.

    # Create dummy files for testing if they don't exist
    if not os.path.exists("assets"):
        os.makedirs("assets")
    if not os.path.exists("config"):
        os.makedirs("config")

    if not os.path.exists("assets/icon.ico"):
        with open("assets/icon.ico", "w") as f:
            f.write("dummy icon content")

    if not os.path.exists("config/theme.json"):
        with open("config/theme.json", "w") as f:
            f.write("{}") # dummy json content

    icon_path = resource_path("assets/icon.ico")
    theme_path = resource_path("config/theme.json")
    non_existent_path = resource_path("non_existent_folder/non_existent_file.txt")

    print(f"Running from: {os.path.abspath('.')}")
    if hasattr(sys, '_MEIPASS'):
        print(f"Frozen mode detected. _MEIPASS: {sys._MEIPASS}")
    else:
        print("Development mode detected (no _MEIPASS attribute).")

    print(f"Calculated icon path: {icon_path}")
    print(f"Does icon path exist? {os.path.exists(icon_path)}")

    print(f"Calculated theme path: {theme_path}")
    print(f"Does theme path exist? {os.path.exists(theme_path)}")

    print(f"Calculated non-existent path: {non_existent_path}")
    print(f"Does non-existent path exist? {os.path.exists(non_existent_path)}")

    # Clean up dummy files
    # os.remove("assets/icon.ico")
    # os.remove("config/theme.json")
    # os.rmdir("assets")
    # os.rmdir("config")
    # print("Cleaned up dummy files/folders.")
