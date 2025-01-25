from flask import request, redirect, url_for
from ckan.plugins import toolkit as tk
from ckanext.regx.lib.database import connect_to_db, close_db_connection
import logging
from ckanext.regx.main import run_fetching

# Configure logging
log = logging.getLogger(__name__)


class FetchCompanyController:
    

    @staticmethod
    def start_fetching():
        """
        Handle the form submission and save data into the 'sherry' table.
        """
        log.debug(" OOOOO Start fetching")
        run_fetching()
        