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

def fetch_dataset(organization_id):
    """
    Fetch dataset details for a specific organization from CKAN API.
    """
    url = f"{CKAN_BASE_URL}package_search"
    params = {"fq": f"organization:{organization_id}"}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print(f"Datasets for organization '{organization_id}' retrieved successfully!")
            return data["result"]["results"]
        else:
            print(f"Error fetching datasets: {data.get('error')}")
    else:
        print(f"Failed to connect to CKAN API: {response.status_code}")
        print(f"Response: {response.text}")

    return None

def get_json_resource_url(resources):
    """
    Find the first JSON resource in the dataset.
    """
    for resource in resources:
        if resource.get("format", "").lower() == "json":
            print(f"Processing JSON resource: {resource.get('legalName')}")
            return resource.get("url")
    print("No JSON resource found in the dataset!")
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
    Recursively extract 'legalName' and 'ocid' from nested JSON data.
    No duplicate legalNames are parsed.
    """
    extracted_entries = []
    current_ocid = None
    seen_legalNames = set()#### LegalNames to avoid duplicates ######

    def extract(data):
        nonlocal current_ocid
        if isinstance(data, dict):
            if "ocid" in data:
                current_ocid = data["ocid"]  ###### Update current ocid #######
            if "legalName" in data and current_ocid:
                legal_name = data["legalName"]
                if legal_name not in seen_legalNames:
                    seen_legalNames.add(legal_name)
                    extracted_entries.append({
                        "ocid": current_ocid,
                        "legalName": legal_name
                    })
            for value in data.values():
                if isinstance(value, (dict, list)):
                    extract(value)
        elif isinstance(data, list):
            for item in data:
                extract(item)

    extract(data)
    return extracted_entries

def save_to_single_file(data, file_path):
    """
    Save all extracted data to a single JSON file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    ###### Create a set of existing names for fast look-up ######
    existing_entries = {(entry["ocid"], entry["legalName"]) for entry in existing_data}

    ####### Add only new entries that don't exist in the existing data ######
    new_data = [entry for entry in data if (entry["ocid"], entry["legalName"]) not in existing_entries]

    ####### Add new data to the existing data list ######
    existing_data.extend(new_data)

    ####### Save the updated data back to the JSON file ######
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)
    print(f"All extracted data saved to {file_path}")

def main():
    ####### Step 1: Fetch the datasets for the specified organization ######
    datasets = fetch_dataset(ORGANIZATION_ID)
    if not datasets:
        return

    ####### Limit to 5 datasets for processing ######
    #datasets_to_process = datasets[:5]  # Process first 5 datasets
    datasets_to_process = datasets

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

    ####### Step 6: Insert unique names and OCID (tender ID) into the database ######
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
