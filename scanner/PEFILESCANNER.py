"""
PE Scanner Module
This module provides Windows PE scanning functionality for the CYBERTRACKER application.
"""

import pefile


class PEScanner:

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

    RISK_WEIGHTS = {
        "file_access": 3,
        "file_write": 6,
        "file_read": 2,
        "process_execution": 8,
        "process_injection": 10,
        "network_activity": 6,
        "downloads_file": 8,
        "registry_modification": 7
    }

    def __init__(self):

        self.output = {
            "File Type": "PE",
            "capabilities": [],
            "risk_percentage": 0,
            "risk_level": "NONE"
        }

    def _calculate_risk(self, capabilities):

        score = sum(self.RISK_WEIGHTS.get(cap, 1) for cap in capabilities)
        max_score = sum(self.RISK_WEIGHTS.values())

        percentage = round((score / max_score) * 100, 2)

        if percentage >= 70:
            level = "CRITICAL"
        elif percentage >= 50:
            level = "HIGH"
        elif percentage >= 25:
            level = "MEDIUM"
        elif percentage > 0:
            level = "LOW"
        else:
            level = "NONE"

        return percentage, level

    def scan(self, file_path: str):

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

        capabilities = sorted(capabilities)

        risk_percentage, risk_level = self._calculate_risk(capabilities)

        self.output["capabilities"] = capabilities
        self.output["risk_percentage"] = risk_percentage
        self.output["risk_level"] = risk_level

        return self.output


def scan(file_path: str):
    scanner = PEScanner()
    return scanner.scan(file_path)