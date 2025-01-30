import requests
import json
import sys
import os
from dotenv import load_dotenv
from database import connect_to_db, create_table, insert_company_data, insert_tender_data, close_db_connection

######### Load environment variables file ###########
load_dotenv()

CKAN_BASE_URL = os.getenv("CKAN_BASE_URL")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")

sys.stdout.reconfigure(encoding='utf-8')

def fetch_all_datasets(organization_id):
    """
    Fetch all datasets for a specific organization from CKAN API, handling pagination.
    """
    url = f"{CKAN_BASE_URL}package_search"
    params = {"fq": f"organization:{organization_id}", "start": 0, "rows": 100}  # Adjust 'rows' as needed

    all_datasets = []
    
    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                datasets = data["result"]["results"]
                print(f"Datasets for organization '{organization_id}' retrieved successfully!")
                all_datasets.extend(datasets)

                if len(datasets) < params["rows"]:  # Less than requested means no more pages
                    break

                params["start"] += params["rows"]  # Increment start for the next page
            else:
                print(f"Error fetching datasets: {data.get('error')}")
                break
        else:
            print(f"Failed to connect to CKAN API: {response.status_code}")
            print(f"Response: {response.text}")
            break

    return all_datasets

def get_json_resource_url(resources):
    """
    Find the resource named 'Meta.json' in the dataset.
    """
    if not resources:
        print("No resources found in this dataset!")
    for resource in resources:
        # print(f"Resource found: {resource}")
        # Check if the resource name is 'Meta.json'
        if resource.get("name", "").lower() == "meta.json":
            print(f"Processing resource: {resource.get('name')}")
            return resource.get("url")
    print("No 'Meta.json' resource found in the dataset!")
    return None

def download_and_parse_json(resource_url):
    """
    Download the JSON resource and extract 'legalName' and 'ocid' fields.
    """
    response = requests.get(resource_url)
    if response.status_code == 200:
        try:
            data = response.json()
            print("JSON file parsed successfully!")
            return extract_names_and_ocids_from_json(data)
        except json.JSONDecodeError:
            print("Error parsing JSON!")
    else:
        print(f"Failed to download resource: {response.text}")
    return []

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
    ##### Step 1: Fetch the datasets for the specified organization ######
    datasets = fetch_all_datasets(ORGANIZATION_ID)  # Updated function call

    if not datasets:
        print("No datasets found.")
        return

    ####### Print the total dataset count ######
    print(f"Total datasets retrieved: {len(datasets)}")

    ####### Limit to 5 datasets for processing ######
    datasets_to_process = datasets  # You can limit this if needed

    ####### File path for saving all parsed data #######
    output_file_path = "scripts/parse-data/all_datasets_data.json"
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    ####### Step 2: Loop through the datasets ######
    all_extracted_data = []
    for dataset in datasets_to_process:
        print(f"Processing dataset: {dataset.get('title')}")
        ####### Step 3: Get the JSON resource URL ######
        json_url = get_json_resource_url(dataset.get("resources", []))
        if not json_url:
            continue

        ####### Step 4: Download and parse the JSON file ######
        extracted_names = download_and_parse_json(json_url)
        if extracted_names:
            all_extracted_data.extend(extracted_names)
            print(f"Extracted legalName: {extracted_names}")

    if not all_extracted_data:
        print("No legalName extracted.")
        return

    ####### Step 5: Save all extracted data to a single JSON file ######
    save_to_single_file(all_extracted_data, output_file_path)

    ###### Step 6: Insert unique names and OCID (tender ID) into the database ######
    connection = connect_to_db()
    create_table(connection)

    if connection:
     for entry in all_extracted_data:
        print(f"Attempting to insert: ocid={entry['ocid']}, legalName={entry['legalName']}")
        insert_company_data(entry["legalName"], connection)
        insert_tender_data(entry["ocid"], entry["legalName"], connection)

    close_db_connection(connection)

if __name__ == "__main__":
    main()
