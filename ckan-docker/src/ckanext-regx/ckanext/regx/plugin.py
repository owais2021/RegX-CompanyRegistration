import os
import subprocess
import logging
from ckan.plugins import SingletonPlugin, implements
from ckan.plugins import toolkit as tk
from ckan.plugins.interfaces import IBlueprint, IConfigurer
from flask import Blueprint, render_template, abort, request
from ckanext.regx.controllers.sherry_controller import SherryController
from ckanext.regx.controllers.company_controller import CompanyController
from ckanext.regx.controllers.admin_controller import AdminController
from ckanext.regx.controllers.admin_user_controller import AdminUserController
from ckanext.regx.controllers.claim_profile_controller import ClaimProfileController
from ckanext.regx.lib.database import (
    connect_to_db,
    create_tables,
    close_db_connection
)
from ckanext.regx.main import run_fetching

# Configure logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class RegxPlugin(SingletonPlugin):
    implements(IBlueprint)
    implements(IConfigurer)

    def _check_access(self, admin_only=False):
        """
        Check access based on user role.
        :param admin_only: If True, only admin users can access the page.
        """
        user = tk.c.userobj
        if not user:
            # If no user is logged in, return 404
            tk.abort(404, "Page not found")
        if admin_only and not user.sysadmin:
            # If the page requires admin access and the user is not admin, return 404
            tk.abort(404, "Page not found")

    def get_blueprint(self):
        blueprint = Blueprint(
            'regx',
            __name__,
            template_folder=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'public'),
            url_prefix='/regx'
        )

        # Index route
        @blueprint.route('/')
        def index():
            """
            Index route for the plugin.
            """
            self._check_access()  # Accessible to all logged-in users
            return tk.render('index.html')

        # Routes for the Sherry form
        blueprint.add_url_rule('/sherry_form', 'sherry_form',
                               SherryController.sherry_form, methods=['GET'])
        blueprint.add_url_rule('/submit_sherry', 'submit_sherry',
                               SherryController.submit_sherry, methods=['POST'])

        # Routes for the Company form
        @blueprint.route('/company_form', methods=['GET'])
        def company_form():
            """
            Page for creating a company profile.
            Accessible only to logged-in users.
            """
            self._check_access()  # Ensure only logged-in users can access
            return CompanyController.company_form()
        blueprint.add_url_rule('/submit_company', 'submit_company',
                               CompanyController.submit_company, methods=['POST'])

        # Claim Your Profile Routes
        @blueprint.route('/claim_profile', methods=['GET'])
        def claim_profile():
            """
            Route to render claim profile form.
            """
            log.debug("Accessing Claim Profile page.")
            return ClaimProfileController.claim_profile()

        blueprint.add_url_rule(
            '/submit_claim_profile',
            'submit_claim_profile',
            ClaimProfileController.submit_claim_profile,
            methods=['POST']
        )

        blueprint.add_url_rule(
            '/verify_otp',
            'verify_otp',
            ClaimProfileController.verify_otp,
            methods=['POST']
        )

        # Admin Panel Routes

        @blueprint.route('/admin_all_profiles')
        def admin_all_profiles():
            """
            Admin-only page to manage all profiles.
            """
            self._check_access(admin_only=True)
            return AdminController.admin_all_profiles()

        @blueprint.route('/toggle_status', methods=['POST'])
        def toggle_status():
            """
            Admin-only endpoint to toggle the status of a company profile.
            """
            self._check_access(admin_only=True)
            return AdminController.toggle_status()

        @blueprint.route('/download_dataset/<int:company_id>', methods=['GET'])
        def download_dataset(company_id):
            """
            Admin-only endpoint to download a dataset.
            """
            self._check_access(admin_only=True)
            return AdminController.download_dataset(company_id)

        @blueprint.route('/admin_all_user_profiles')
        def admin_all_user_profiles():
            """
            Admin-only page to view all user profiles.
            """
            self._check_access(admin_only=True)
            return AdminUserController.admin_all_user_profiles()

        return blueprint

    def update_config(self, config):
        """
        Update CKAN configuration and initialize database tables.
        """
        tk.add_template_directory(config, 'templates')
        tk.add_public_directory(config, 'public')

        config['ckan.auth.create_user_via_web'] = 'true'
        
        # Create tables during plugin initialization
        connection = connect_to_db()
        if connection:
            try:
                create_tables(connection)
            except Exception as e:
                log.error(f"Error initializing database tables: {e}")
            finally:
                close_db_connection(connection)
        else:
            log.error(
                "Failed to connect to the database during plugin initialization.")
        log.debug("Start main ###############")
        
        # Command to run the script with sudo
        #command = ['python3', '/srv/app/src_extensions/ckanext-regx/ckanext/regx/main.py']

        # Run the command
        #subprocess.run(command)

        # Create a thread and specify the target method and arguments
       # my_thread = threading.Thread(target=run_fetching)
       # my_thread.start()


