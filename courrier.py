import shutil
import os

# Remove frontend git directory if it exists
if os.path.exists("frontend/.git"):
    shutil.rmtree("frontend/.git")
    print("Removed frontend/.git directory")
