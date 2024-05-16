import os

file_path = "Overall_survival.xlsx" # Replace with the path to your file

# Check if the file exists
if os.path.exists(file_path):
    # Check read permission
    if os.access(file_path, os.R_OK):
        print("Read permission: Allowed")
    else:
        print("Read permission: Not allowed")

    # Check write permission
    if os.access(file_path, os.W_OK):
        print("Write permission: Allowed")
    else:
        print("Write permission: Not allowed")

    # Check execute permission (for directories)
    if os.access(file_path, os.X_OK):
        print("Execute permission: Allowed")
    else:
        print("Execute permission: Not allowed")
else:
    print("File not found:", file_path)
