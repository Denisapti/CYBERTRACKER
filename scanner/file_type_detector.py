import os

# ////////////////////////////////
# Investigation functions
# These functions represent the different analysis modules
# that will run depending on the detected file type.
# For now they just print a message, but later they can
# call deeper malware analysis tools.
# ////////////////////////////////

def investigateEXE(file_path):
    print(f"Investigating EXE file: {file_path}")


def investigatePDF(file_path):
    print(f"Investigating PDF file: {file_path}")


def investigateDOCX(file_path):
    print(f"Investigating DOCX file: {file_path}")


def investigateZIP(file_path):
    print(f"Investigating ZIP file: {file_path}")

# Fallback if the file type is not supported yet
def investigateUNKNOWN(file_path):
    print(f"Unknown file type: {file_path}")


# ////////////////////////////////
# Detect file type
# Purpose: Determine the file type based on its extension.
# Example:
#   malware.exe -> ".exe"
#   document.pdf -> ".pdf"
# ////////////////////////////////

def detect_file_type(file_path):
    _, extension = os.path.splitext(file_path)
    return extension.lower()


# ////////////////////////////////
# Dispatcher
# Purpose:
# 1. Detect the file type
# 2. Call the correct investigation function

# This acts as the dispatcher that routes the file to the
# appropriate analyzer module based on its type.
# ////////////////////////////////

def investigate_file(file_path):
    # Detect file extension
    file_type = detect_file_type(file_path)
    # Route the file to the correct investigation function
    if file_type == ".exe":
        investigateEXE(file_path)

    elif file_type == ".pdf":
        investigatePDF(file_path)

    elif file_type == ".docx":
        investigateDOCX(file_path)

    elif file_type == ".zip":
        investigateZIP(file_path)

    else:
        investigateUNKNOWN(file_path)