from flask import request, redirect, url_for
from flask import jsonify
from ckan.plugins import toolkit as tk
from ckanext.regx.lib.database import connect_to_db, close_db_connection
import logging
from ckanext.regx.main import main, clear_all_scheduled_jobs, toggle_pause_job

log = logging.getLogger(__name__)


class FetchCompanyController:
    
    @staticmethod
    def start_fetching():
        log.debug("Start fetching")

        try:
            main()
            return jsonify({"message": "Start fetching data!"}), 200
        except Exception as e:
            log.error(f"Error while fetching: {str(e)}")
            return jsonify({"message": "Fetching failed", "error": str(e)}), 400
        

    @staticmethod
    def pause_fetching():
 
        log.debug("Pause fetching")

        try:
            toggle_pause_job(pause=True)
            return jsonify({"message": "Pause fetching data!"}), 200
        except Exception as e:
            log.error(f"Error while fetching: {str(e)}")
            return jsonify({"message": "Fetching failed", "error": str(e)}), 400
        
    @staticmethod
    def continue_fetching():
 
        log.debug("Continue fetching")

        try:
            toggle_pause_job(pause=False)
            return jsonify({"message": "Continue fetching data!"}), 200
        except Exception as e:
            log.error(f"Error while fetching: {str(e)}")
            return jsonify({"message": "Fetching failed", "error": str(e)}), 400
        
    @staticmethod
    def stop_fetching():
 
        log.debug("Stop fetching")

        try:
            clear_all_scheduled_jobs()
            return jsonify({"message": " Stop fetching data!"}), 200
        except Exception as e:
            log.error(f"Error while fetching: {str(e)}")
            return jsonify({"message": "Fetching failed", "error": str(e)}), 400
        
    


        