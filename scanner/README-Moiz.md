
# Example function that would be called by the rest of program
def handle_analysis_output(output):
    json_data = process_capabilities(output)

    # Save JSON file
    save_json(json_data)

    # Print to console for testing
    print(json.dumps(json_data, indent=4))