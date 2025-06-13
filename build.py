import subprocess
import os
import platform

# --- Configuration ---
APP_NAME = "AetherEditor"
ENTRY_POINT = "main.py"  # Your application's main script
ICON_PATH = "assets/icon.ico"  # Path to your application's icon file (.ico for Windows, .icns for macOS)
ASSETS_DIR = "assets"  # Directory containing additional assets (images, themes, etc.)

# --- PyInstaller Command Construction ---
# Base command for PyInstaller
pyinstaller_command = [
    "pyinstaller",
    "--noconfirm",  # Automatically overwrite the output directory if it exists
]

# Platform-specific options
if platform.system() == "Windows":
    pyinstaller_command.extend([
        "--windowed",  # Suppress the console window (for GUI applications on Windows)
        f"--icon={ICON_PATH}",  # Set the application icon
    ])
elif platform.system() == "Darwin":  # macOS
    # For macOS, .app bundles are inherently windowed.
    # PyInstaller typically expects a .icns file for icons on macOS.
    mac_icon_path = ICON_PATH.replace(".ico", ".icns")
    if os.path.exists(mac_icon_path):
        pyinstaller_command.append(f"--icon={mac_icon_path}")
    elif os.path.exists(ICON_PATH): # Fallback to .ico if .icns not found but .ico exists
        pyinstaller_command.append(f"--icon={ICON_PATH}")
    # Example for setting a bundle identifier (optional, but good practice for macOS apps)
    # pyinstaller_command.extend(["--osx-bundle-identifier", "com.yourdomain.aethereditor"])
else: # Linux and other OS
    # Icons on Linux are typically handled via .desktop files, not directly embedded by PyInstaller.
    # No '--windowed' needed as behavior is different.
    pass

# Common options for all platforms
pyinstaller_command.extend([
    "--onefile",  # Package the application into a single executable file
    f"--name={APP_NAME}",  # Specify the name of the executable
])

# Add data files (assets)

# 1. Add the ASSETS_DIR (e.g., 'assets/' -> 'assets/')
# This option tells PyInstaller to include the entire ASSETS_DIR.
# The content of ASSETS_DIR will be available in a directory named 'assets'
# relative to the executable at runtime.
# The path separator (':' for Unix-like, ';' for Windows) is handled by PyInstaller.
if os.path.exists(ASSETS_DIR):
    pyinstaller_command.append(f"--add-data={ASSETS_DIR}{os.pathsep}{ASSETS_DIR}")
else:
    # This warning is fine, but ICON_PATH also depends on ASSETS_DIR, so an icon might fail to load.
    print(f"Warning: Main assets directory '{ASSETS_DIR}' (for icon, etc.) not found. Skipping --add-data for it.")

# 2. Add the 'config' directory (e.g., 'config/' -> 'config/')
CONFIG_DIR = "config"
if os.path.exists(CONFIG_DIR):
    pyinstaller_command.append(f"--add-data={CONFIG_DIR}{os.pathsep}{CONFIG_DIR}")
else:
    print(f"Warning: Configuration directory '{CONFIG_DIR}' not found. theme.json might be missing.")

# 3. Add 'styling.qss' from the root (e.g., 'styling.qss' -> 'styling.qss')
STYLESHEET_FILE = "styling.qss"
if os.path.exists(STYLESHEET_FILE):
    pyinstaller_command.append(f"--add-data={STYLESHEET_FILE}{os.pathsep}.") # '.' means place in root of bundle
else:
    print(f"Warning: Stylesheet '{STYLESHEET_FILE}' not found. Global styles might be missing.")

# Specify the main Python script (entry point) for the application
pyinstaller_command.append(ENTRY_POINT)

# --- Execute Build Command ---
print("----------------------------------------------------------------------")
print(f"Attempting to build '{APP_NAME}' using PyInstaller...")
print(f"Command: {' '.join(pyinstaller_command)}")
print("----------------------------------------------------------------------")

try:
    # Run the PyInstaller command
    # `check=True` will raise a CalledProcessError if PyInstaller returns a non-zero exit code.
    # `text=True` (or `universal_newlines=True`) decodes stdout/stderr as text.
    # `capture_output=True` captures stdout and stderr.
    result = subprocess.run(pyinstaller_command, check=True, text=True, capture_output=True)
    print("\n--- PyInstaller STDOUT ---")
    print(result.stdout)
    print("--------------------------")
    if result.stderr: # Print stderr only if it's not empty
        print("\n--- PyInstaller STDERR ---")
        print(result.stderr)
        print("--------------------------")

    print("\n======================================================================")
    print(" BUILD SUCCEEDED!")
    output_filename = f"{APP_NAME}{'.exe' if platform.system() == 'Windows' else ''}"
    print(f" The executable should be located in: dist/{output_filename}")
    print("======================================================================")

except subprocess.CalledProcessError as e:
    # This block catches errors specifically from the PyInstaller process itself
    print("\n======================================================================")
    print(" BUILD FAILED: PyInstaller returned an error.")
    print("======================================================================")
    print(f"Command attempted: {' '.join(e.cmd)}")
    print(f"Return code: {e.returncode}")
    print("\n--- PyInstaller STDOUT ---")
    print(e.stdout)
    print("\n--- PyInstaller STDERR ---")
    print(e.stderr)
    print("----------------------------------------------------------------------")
    print("Common issues to check:")
    print(" - Ensure all dependencies are installed in your Python environment.")
    print(" - Check for errors in the PyInstaller output above for missing hooks or hidden imports.")
    print(" - Verify all paths in this script (ENTRY_POINT, ICON_PATH, ASSETS_DIR) are correct.")

except FileNotFoundError:
    # This block catches the error if the `pyinstaller` command itself isn't found
    print("\n======================================================================")
    print(" BUILD FAILED: PyInstaller command not found.")
    print("======================================================================")
    print("Please ensure PyInstaller is installed and added to your system's PATH.")
    print("You can install it by running: pip install pyinstaller")
    print("----------------------------------------------------------------------")

except Exception as e:
    # Catch any other unexpected errors during the script's execution
    print("\n======================================================================")
    print(f" BUILD FAILED: An unexpected error occurred: {e}")
    print("======================================================================")
    print("----------------------------------------------------------------------")

# --- How to Run This Script ---
# 1. Save this script as `build.py` in the root directory of your project.
# 2. Make sure you have PyInstaller installed:
#    pip install pyinstaller
# 3. Create an `assets` folder in the root directory and place your icon (`icon.ico` or `icon.icns`)
#    and any other necessary asset files/folders (e.g., themes, images) into it.
#    If your icon or assets are located elsewhere, update ICON_PATH and ASSETS_DIR variables at the top.
# 4. Open a terminal or command prompt in your project's root directory.
# 5. Run the script using Python:
#    python build.py
# 6. If the build is successful, the standalone executable will be found in the `dist` folder
#    (e.g., `dist/AetherEditor.exe` on Windows, `dist/AetherEditor.app` on macOS, or `dist/AetherEditor` on Linux).
#
# --- Notes ---
# - The `build` folder and `.spec` file generated by PyInstaller are temporary files
#   and can usually be ignored or deleted after a successful build (though the .spec file
#   can be useful for more advanced configurations).
# - If the build fails, carefully review the error messages printed in the console.
#   The output from PyInstaller (STDOUT and STDERR) is crucial for debugging.
