import logging.config

from django.conf import settings

from httpclient.client import Client

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


class NsiLcm(object):
    """NSI LCM Class.

    This class serves as a wrapper for the Network Slice Instance Lifecycle Management (NSILCM) part
    of the Northbound Interface (NBI) offered by OSM. The methods defined in this class help
    retrieve the NSI-related entities of OSM, and instantiate or terminate an NSI.

    Attributes:
        bearer_token (str): The OSM Authorization Token

    Args:
        token (str): The OSM Authorization Token

    """

    def __init__(self, token):
        """NSI LCM Class Constructor."""
        self.__client = Client(verify_ssl_cert=False)
        self.bearer_token = token

    def get_netslice_list(self):
        """Fetch a list of all Netslice Instances

        Returns:
            nsi_list_obj (Response): A list of Netslice Instances as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.nsilcm import NsiLcm
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> nsilcm = NsiLcm(token)
            >>> nsi_list_obj = nsilcm.get_netslice_list()

        OSM Cli:
            $ osm nsi-list

        """
        endpoint = '{}/osm/nsilcm/v1/netslice_instances'.format(settings.OSM_COMPONENTS.get('NBI-API'))
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_netslice(self, nsi_uuid):
        """Fetch details of a specific Netslice Instance

        Args:
            nsi_uuid (str): The UUID of the NS to fetch details for

        Returns:
            nsi_obj (Response): A NS as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.nsilcm import NsiLcm
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> nsilcm = NsiLcm(token)
            >>> nsi_obj = nsilcm.get_netslice('07048175-660b-404f-bbc9-5be7581e74de')

        OSM Cli:
            $ osm nsi-show 07048175-660b-404f-bbc9-5be7581e74de

        """
        endpoint = '{}/osm/nsilcm/v1/netslice_instances/{}'.format(settings.OSM_COMPONENTS.get('NBI-API'), nsi_uuid)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response
