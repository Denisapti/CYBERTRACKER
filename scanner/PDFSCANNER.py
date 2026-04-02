"""
PDF Scanner Module
This module provides PDF scanning functionality for the CYBERTRACKER application.
"""

from pypdf import PdfReader
from pypdf.generic import DictionaryObject, ArrayObject, IndirectObject


class PDFScanner:

    SUSPICIOUS_KEYS = {
        "/JavaScript": "contains_javascript",
        "/JS": "contains_javascript",
        "/OpenAction": "has_open_action",
        "/AA": "has_additional_actions",
        "/Launch": "has_launch_action",
        "/URI": "contains_uri_action",
        "/EmbeddedFiles": "contains_embedded_files",
        "/XFA": "uses_xfa_forms",
        "/AcroForm": "uses_acroform",
        "/RichMedia": "contains_rich_media",
        "/SubmitForm": "has_submit_form_action",
        "/GoToR": "has_remote_goto_action",
        "/ObjStm": "uses_object_streams",
    }

    RISK_WEIGHTS = {
        "contains_javascript": 8,
        "has_open_action": 6,
        "has_additional_actions": 6,
        "has_launch_action": 9,
        "contains_uri_action": 5,
        "contains_embedded_files": 7,
        "uses_xfa_forms": 6,
        "uses_acroform": 3,
        "contains_rich_media": 6,
        "has_submit_form_action": 4,
        "has_remote_goto_action": 7,
        "uses_object_streams": 3,
        "is_encrypted": 5
    }

    def __init__(self):

        self.output = {
            "File Type": "PDF",
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

        reader = PdfReader(file_path)
        capabilities = set()
        visited = set()

        if reader.is_encrypted:
            capabilities.add("is_encrypted")

        def walk(obj):

            obj_id = id(obj)

            if obj_id in visited:
                return

            visited.add(obj_id)

            if isinstance(obj, IndirectObject):
                obj = obj.get_object()

            if isinstance(obj, DictionaryObject):

                for key, value in obj.items():

                    if key in self.SUSPICIOUS_KEYS:
                        capabilities.add(self.SUSPICIOUS_KEYS[key])

                    walk(value)

            elif isinstance(obj, ArrayObject):

                for item in obj:
                    walk(item)

        walk(reader.trailer)

        capabilities = sorted(capabilities)

        risk_percentage, risk_level = self._calculate_risk(capabilities)

        self.output["capabilities"] = capabilities
        self.output["risk_percentage"] = risk_percentage
        self.output["risk_level"] = risk_level

        return self.output


def scan(file_path: str):
    scanner = PDFScanner()
    return scanner.scan(file_path)