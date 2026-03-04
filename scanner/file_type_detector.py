import os

# //////////////////////////////////////////////
# Investigation functions
# These represent the analysis modules for supported file types.
# For the prototype we are only supporting EXE and PDF files.
# //////////////////////////////////////////////

def investigateEXE(file_path):
    print(f"Investigating EXE file: {file_path}")


def investigatePDF(file_path):
    print(f"Investigating PDF file: {file_path}")


# //////////////////////////////////////////////
# Function: detect_file_type
# Purpose: Extract the file extension from the given file path
# Example:
#   malware.exe -> ".exe"
#   document.pdf -> ".pdf"
# //////////////////////////////////////////////
def detect_file_type(file_path):
    _, extension = os.path.splitext(file_path)
    return extension.lower()


# //////////////////////////////////////////////
# Function: investigate_file
# Purpose:
# 1. Detect the file type
# 2. Call the correct investigation function
# If the file type is not supported, print a message.
# //////////////////////////////////////////////
def investigate_file(file_path):

    file_type = detect_file_type(file_path)

    if file_type == ".exe":
        investigateEXE(file_path)

    elif file_type == ".pdf":
        investigatePDF(file_path)

    else:
        print(f"File type '{file_type}' is not supported in this prototype.")
