"""
PE Scanner Module
This module provides Windows PE scanning functionality for the CYBERTRACKER application.
"""

import pefile


class Capability:
    """Represents a capability of the PE scanner."""
    def __init__(self, name: str):
        self.name = name


class PEScanner:
    """Handles PE scanning operations."""

    SUSPICIOUS_APIS = {
        "CreateFile": "file_access",
        "WriteFile": "file_write",
        "ReadFile": "file_read",
        "WinExec": "process_execution",
        "ShellExecute": "process_execution",
        "CreateRemoteThread": "process_injection",
        "VirtualAllocEx": "process_injection",
        "InternetOpen": "network_activity",
        "InternetConnect": "network_activity",
        "URLDownloadToFile": "downloads_file",
        "RegSetValue": "registry_modification",
        "RegCreateKey": "registry_modification"
    }

    def __init__(self):
        """Initialize the PE Scanner."""
        self.output = {
            "File Type": "PE",
            "capabilities": []
        }

    def scan(self, file_path: str):
        """
        Scan a PE file and extract capabilities based on imported APIs.
        """

        pe = pefile.PE(file_path)
        capabilities = set()

        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:

                for imp in entry.imports:

                    if imp.name is None:
                        continue

                    api_name = imp.name.decode(errors="ignore")

                    if api_name in self.SUSPICIOUS_APIS:
                        capabilities.add(self.SUSPICIOUS_APIS[api_name])

        self.output["capabilities"] = [
            Capability(name) for name in sorted(capabilities)
        ]

        return self.output


def main(file_path: str):
    """Main entry point for PE Scanner module."""

    scanner = PEScanner()
    result = scanner.scan(file_path)

    print("PE Capabilities:")

    for cap in result["capabilities"]:
        print(f"- {cap.name}")

    return result


if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:
        print("Usage: python pe_scanner.py <path_to_executable>")
    else:
        pe_path = sys.argv[1]
        main(pe_path)