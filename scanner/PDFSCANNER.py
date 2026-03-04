"""
PDF Scanner Module
This module provides PDF scanning functionality for the CYBERTRACKER application.
"""

from pypdf import PdfReader
from pypdf.generic import DictionaryObject, ArrayObject, IndirectObject


class Capability:
    """Represents a capability of the PDF scanner."""
    def __init__(self, name: str):
        self.name = name


class PDFScanner:
    """Handles PDF scanning operations."""
    
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

    def __init__(self):
        """Initialize the PDF Scanner."""
        self.output = {
            "File Type": "PDF",
            "capabilities": []
        }

    def scan(self, file_path: str):
        """
        Scan a PDF file and extract structural capabilities.
        """
        reader = PdfReader(file_path)
        capabilities = set()
        visited = set()

        # Explicit encryption check
        if reader.is_encrypted:
            capabilities.add("is_encrypted")

        def walk(obj):
            obj_id = id(obj)
            if obj_id in visited:
                return
            visited.add(obj_id)

            # Resolve indirect objects
            if isinstance(obj, IndirectObject):
                obj = obj.get_object()

            # Dictionary traversal
            if isinstance(obj, DictionaryObject):
                for key, value in obj.items():
                    if key in self.SUSPICIOUS_KEYS:
                        capabilities.add(self.SUSPICIOUS_KEYS[key])
                    walk(value)

            # Array traversal
            elif isinstance(obj, ArrayObject):
                for item in obj:
                    walk(item)

        # Start traversal from trailer (top-level structure)
        walk(reader.trailer)

        # Convert to Capability objects (keep them as objects, not dicts)
        self.output["capabilities"] = [Capability(name) for name in sorted(capabilities)]

        return self.output


def main(file_path: str):
    """Main entry point for PDF Scanner module."""
    scanner = PDFScanner()
    result = scanner.scan(file_path)

    # Print capability names for demonstration
    print("PDF Capabilities:")
    for cap in result["capabilities"]:
        print(f"- {cap.name}")

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_scanner.py <path_to_pdf>")
    else:
        pdf_path = sys.argv[1]
        main(pdf_path)