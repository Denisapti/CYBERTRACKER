import json

def process_capabilities(output):
    """
    Takes the analysis output object and extracts capability names.
    Builds a JSON structure containing all detected capabilities.
    """

    capability_names = []

    # Loop through capability objects
    for capability in output.capabilities:
        try:
            capability_names.append(capability.name)
        except AttributeError:
            # Skip if capability object doesn't contain expected attribute
            continue

    # Build JSON structure
    result = {
        "analysis_result": {
            "capability_count": len(capability_names),
            "capabilities": capability_names
        }
    }

    return result


def save_json(data, filename="capability_results.json"):
    """Save results to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

