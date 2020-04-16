import logging.config

from django.conf import settings

from httpclient.client import Client

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


class OsmAdmin(object):
    """OSM Admin Class.

    This class serves as a wrapper for the Admin part of the Northbound Interface (NBI) offered
    by OSM. The methods defined in this class help to retrieve the administrative entities of OSM,
    i.e. VIM accounts, users, projects, tokens and SDNs as lists or single objects.

    Attributes:
        bearer_token (str): The OSM Authorization Token

    Args:
        token (str): The OSM Authorization Token

    """

    def __init__(self, token):
        """NsInstance Class Constructor."""
        self.__client = Client(verify_ssl_cert=False)
        self.bearer_token = token

    def get_vim_list(self):
        """Fetch a list of all VIM accounts.

        Returns:
            vim_list_obj (Response): A list of VIMs as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.osm_admin import OsmAdmin
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> osm_admin = OsmAdmin(token)
            >>> vim_list_obj = osm_admin.get_vim_list()

        OSM Cli:
            $ osm vim-list

        """
        endpoint = '{}/osm/admin/v1/vim_accounts'.format(settings.OSM_COMPONENTS.get('NBI-API'))
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_vim(self, vim_uuid):
        """Fetch details of a specific VIM account

        Args:
            vim_uuid (str): The UUID of the VIM to fetch

        Returns:
            vim_obj (Response): A VIM as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.osm_admin import OsmAdmin
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> osm_admin = OsmAdmin(token)
            >>> vim_obj = osm_admin.get_vim('27183ec9-55f9-47b4-a850-fd0c528dc9fc')

        OSM Cli:
            $ osm vim-show 27183ec9-55f9-47b4-a850-fd0c528dc9fc

        """
        endpoint = '{}/osm/admin/v1/vim_accounts/{}'.format(settings.OSM_COMPONENTS.get('NBI-API'), vim_uuid)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_user_list(self):
        """Fetch a list of all users

        Returns:
            user_list_obj (Response): A list of users as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.osm_admin import OsmAdmin
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> osm_admin = OsmAdmin(token)
            >>> user_list_obj = osm_admin.get_user_list()

        """
        endpoint = '{}/osm/admin/v1/users'.format(settings.OSM_COMPONENTS.get('NBI-API'))
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_user(self, user_name):
        """Fetch details of a user

        Args:
            user_name (str) : The name of the user to fetch details for

        Returns:
            user_obj (Response): A user as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.osm_admin import OsmAdmin
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> osm_admin = OsmAdmin(token)
            >>> user_obj = osm_admin.get_user('user5gmedia')

        """
        endpoint = '{}/osm/admin/v1/users/{}'.format(settings.OSM_COMPONENTS.get('NBI-API'), user_name)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_project_list(self):
        """Fetch a list of all projects

        Returns:
            project_list_obj (Response): A list of projects as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.osm_admin import OsmAdmin
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> osm_admin = OsmAdmin(token)
            >>> project_list_obj = osm_admin.get_project_list()

        """
        endpoint = '{}/osm/admin/v1/projects'.format(settings.OSM_COMPONENTS.get('NBI-API'))
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_project(self, project_name):
        """Fetch details of a specific project

        Args:
            project_name (str): The name of the project to fetch details for

        Returns:
            project_obj (Response): A project as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.osm_admin import OsmAdmin
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> osm_admin = OsmAdmin(token)
            >>> project_obj = osm_admin.get_project('5gmedia')

        """
        endpoint = '{}/osm/admin/v1/projects/{}'.format(settings.OSM_COMPONENTS.get('NBI-API'), project_name)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_token_list(self):
        """Fetch a list of all authorization tokens.

        Returns:
            token_list_obj (Response): A list of tokens as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.osm_admin import OsmAdmin
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> osm_admin = OsmAdmin(token)
            >>> token_list_obj = osm_admin.get_token_list()

        """
        endpoint = '{}/osm/admin/v1/tokens'.format(settings.OSM_COMPONENTS.get('NBI-API'))
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_token(self, token):
        """Fetch details of a token.

        Args:
            token (str): An OSM authorization token

        Returns:
            token_list_obj (Response): A list of tokens as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.osm_admin import OsmAdmin
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> osm_admin = OsmAdmin(token)
            >>> token_obj = osm_admin.get_token('HESHId7l6HHwURmLGm4hnuGxa6njLABE')

        """
        endpoint = '{}/osm/admin/v1/tokens/{}'.format(settings.OSM_COMPONENTS.get('NBI-API'), token)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_sdn_list(self):
        """Fetch a list of all SDNs.

        Returns:
            sdn_list_obj (Response): A list of SDNs as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.osm_admin import OsmAdmin
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> osm_admin = OsmAdmin(token)
            >>> sdn_list_obj = osm_admin.get_sdn_list()

        OSM Cli:
            $ osm sdnc-list

        """
        endpoint = '{}/osm/admin/v1/sdns'.format(settings.OSM_COMPONENTS.get('NBI-API'))
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_sdn(self, sdn_uuid):
        """Fetch details of a specific SDN.

        Args:
            sdn_uuid (str): The UUID of the SDN to fetch details for

        Returns:
            sdn_obj (Response): An SDN as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.osm_admin import OsmAdmin
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> osm_admin = OsmAdmin(token)
            >>> sdn_obj = osm_admin.get_sdn('n1u9k3l1-55f9-47b4-a850-fd0c5780c9fc')

        OSM Cli:
            $ osm sdnc-show n1u9k3l1-55f9-47b4-a850-fd0c5780c9fc

        """
        endpoint = '{}/osm/admin/v1/sdns/{}'.format(settings.OSM_COMPONENTS.get('NBI-API'), sdn_uuid)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response
