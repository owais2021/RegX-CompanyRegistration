########### For testing using ckan local env (localhost:5000) place meta.json in my code for testing#########

import json
import os

def load_meta_json(file_path):
    """
    Load the Meta.json file from the specified path.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        print(f"Meta.json loaded successfully from {file_path}")
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading Meta.json: {e}")
        return None

def extract_names_and_ocids_from_json(data):
    """
    Extract 'legalName', 'ocid', and 'roles' (supplier) from nested JSON data.
    Always process data if numberOfTenderers > 0 and role is 'supplier'.
    """
    extracted_entries = []
    seen_legalNames = set()  # Track unique legalNames

    def extract(data):
        if isinstance(data, dict):
            # Process numberOfTenderers if present
            number_of_tenderers = data.get("numberOfTenderers")
            if number_of_tenderers:
                print(f"Found numberOfTenderers: {number_of_tenderers}")  # Debugging numberOfTenderers

            if number_of_tenderers and number_of_tenderers > 0:
                ocid = data.get("ocid", "")
                # Retain only the numeric part of the OCID (after the last hyphen)
                ocid_number = ocid.split("-")[-1] if ocid else ""

                print(f"Processing OCID: {ocid_number}")
                # Process parties and roles
                parties = data.get("parties", [])
                for party in parties:
                    roles = party.get("roles", [])
                    print(f"Found roles in party: {roles}")  # Debugging roles in each party
                    if "supplier" in roles:
                        # Ensure the legalName exists under 'identifier' key
                        legal_name = party.get("identifier", {}).get("legalName", party.get("name"))
                        if legal_name and legal_name not in seen_legalNames:
                            seen_legalNames.add(legal_name)
                            extracted_entries.append({
                                "ocid": ocid_number,
                                "legalName": legal_name,
                                "roles": ["supplier"]
                            })

            # Recursively process all nested dictionaries and lists
            for value in data.values():
                if isinstance(value, (dict, list)):
                    extract(value)

        elif isinstance(data, list):
            for item in data:
                extract(item)

    # Start extraction
    extract(data)
    return extracted_entries

def save_to_single_file(data, file_path):
    """
    Save all extracted data to a single JSON file.
    """
    try:
        # Check if the file already exists and load existing data
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        else:
            existing_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    ###### Create a set of existing names for fast look-up ######
    existing_entries = {(entry["ocid"], entry["legalName"]) for entry in existing_data}

    ####### Add only new entries that don't exist in the existing data ######
    new_data = [entry for entry in data if (entry["ocid"], entry["legalName"]) not in existing_entries]

    ####### Add new data to the existing data list ######
    existing_data.extend(new_data)

    ####### Save the updated data back to the JSON file ######
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)
    print(f"All extracted data saved to {file_path}")

def main():
    # File path to Meta.json for testing
    meta_file_path = r"C:\Drive Folder\Bremen University\Semester 3\Project\ckan\ckanext\regx_ckan\Meta.json"

    # Load the Meta.json data for testing
    meta_data = load_meta_json(meta_file_path)
    if not meta_data:
        return

    # Step 1: Directly process the loaded data (No need to fetch datasets from CKAN)
    extracted_data = extract_names_and_ocids_from_json(meta_data)

    if extracted_data:
        print(f"Extracted data: {extracted_data}")
    else:
        print("No data extracted. Please check the conditions or structure of the input JSON.")

    # Step 2: Save the extracted data to a file
    output_file_path = "scripts/parse-data/all_datasets_data.json"
    save_to_single_file(extracted_data, output_file_path)

if __name__ == "__main__":
    main()
