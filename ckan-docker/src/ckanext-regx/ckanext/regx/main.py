import sys
import logging
import time
import schedule
import threading

from ckanext.regx.lib.process_ckan_data import main as process_ckan_data_main
from ckanext.regx.lib.google_search import main as google_search_main
from ckanext.regx.lib.ckan_api import main as ckan_api_main
from ckanext.regx.lib.database import insert_test, update_sherry_address, connect_to_db, close_db_connection

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]  # Explicitly target stdout
)
log = logging.getLogger(__name__)

pause_job = False

def run_fetching():
    global pause_job
    if not pause_job:
        logging.info("################################# This is a log message!")
        ##### Testing
        connection = connect_to_db()
        if connection is None:
            log.error("Failed to establish a database connection. Exiting...")
            return
        update_sherry_address(connection, "1")
        close_db_connection(connection)
        #####
        
        try:
            # Step 1: Process CKAN data
            log.debug("Step 1: Processing CKAN data Parsing...")
            #process_ckan_data_main()

            # Step 2: Perform Google search for company details
            # log.debug("Step 2: Performing Google search for company details...")
            #google_search_main()

            # Step 3: Interact with CKAN API to create/update dataset
            log.debug("Step 3: Interacting with CKAN API...")
            ckan_api_main()

            log.debug("All steps completed successfully!!!!!!!!!!")

        except Exception as e:
            log.error(f"Error during execution: {e}")
            sys.exit(1)

def run_schedule():
    schedule.every(30).seconds.do(run_fetching)  # For testing
    while True:
        schedule.run_pending()
        time.sleep(1)

def toggle_pause_job(pause=True):
    """Pauses or resumes the scheduled job."""
    global pause_job
    pause_job = pause
    status = "paused" if pause else "resumed"
    logging.debug(f"Job has been {status}.")

def clear_all_scheduled_jobs():
    schedule.clear()

def main():
    scheduler_thread = threading.Thread(target=run_schedule)
    scheduler_thread.daemon = True
    scheduler_thread.start()


if __name__ == "__main__":
    main()
