import sys
import logging
from ckanext.regx.lib.process_ckan_data import main as process_ckan_data_main
from ckanext.regx.lib.google_search import main as google_search_main
from ckanext.regx.lib.ckan_api import main as ckan_api_main

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def run_fetching():
    log.debug(" RUNYNYNYNNYNYNYNYY")
    
    try:

        # Step 1: Process CKAN data
        log.debug("Step 1: Processing CKAN data Parsing...")
        process_ckan_data_main()

        # Step 2: Perform Google search for company details
        log.debug("Step 2: Performing Google search for company details...")
        #google_search_main()

        # Step 3: Interact with CKAN API to create/update dataset
        log.debug("Step 3: Interacting with CKAN API...")
        ckan_api_main()

        log.debug("All steps completed successfully!!!!!!!!!!")

    except Exception as e:
        log.error(f"Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_fetching()