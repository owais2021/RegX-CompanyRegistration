import sys
import logging
from ckanext.regx.lib.process_ckan_data import main as process_ckan_data_main
from ckanext.regx.lib.google_search import main as google_search_main
from ckanext.regx.lib.ckan_api import main as ckan_api_main
from ckanext.regx.lib.ckan_api import test3
from ckanext.regx.lib.database import insert_test, update_sherry_address, connect_to_db, close_db_connection
import time
import schedule

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Ensure logs go to stdout
)
log = logging.getLogger(__name__)

def run_fetching():
    log.debug(" RUNYNYNYNNYNYNYNYY")
    connection = connect_to_db()
    if connection is None:
        log.error("Failed to establish a database connection. Exiting...")
        return
    update_sherry_address(connection, "1")
    close_db_connection(connection)
    
    #test3()
    try:

        # Step 1: Process CKAN data
        log.debug("Step 1: Processing CKAN data Parsing...")
        #process_ckan_data_main()

        # Step 2: Perform Google search for company details
       # log.debug("Step 2: Performing Google search for company details...")
       # google_search_main()

        # Step 3: Interact with CKAN API to create/update dataset
        log.debug("Step 3: Interacting with CKAN API...")
       # ckan_api_main()

        log.debug("All steps completed successfully!!!!!!!!!!")

    except Exception as e:
        log.error(f"Error during execution: {e}")
        sys.exit(1)


def main():
    connection = connect_to_db()
    if connection is None:
        log.error("Failed to establish a database connection. Exiting...")
        return
    insert_test(connection, "test", "1")
    close_db_connection(connection)
    log.debug("Running my task!")

    print("Running periodic task...", file=sys.stdout)

    # Later: schedule.every().day.at("02:00").do(run_fetching)
    schedule.every(30).seconds.do(run_fetching) # For testing

    while True:
        schedule.run_pending()
        time.sleep(1)

    

if __name__ == "__main__":
    main()