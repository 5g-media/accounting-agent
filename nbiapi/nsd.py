import logging.config

from django.conf import settings

from httpclient.client import Client

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


class Nsd(object):
    """NS Descriptor Class.

    This class serves as a wrapper for the Network Service Descriptor (NSD) part
    of the Northbound Interface (NBI) offered by OSM. The methods defined in this
    class help retrieve the NSDs of OSM.

    Attributes:
        bearer_token (str): The OSM Authorization Token.

    Args:
        token (str): The OSM Authorization Token.

    """

    def __init__(self, token):
        """NS Descriptor Class Constructor."""
        self.__client = Client(verify_ssl_cert=False)
        self.bearer_token = token

    def get_nsd_list(self):
        """Fetch a list of all NS descriptors.

        Returns:
            nsd_list_obj (Response): A list of NSDs as a requests object.

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.nsd import Nsd
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> nsd = Nsd(token)
            >>> nsd_list_obj = nsd.get_nsd_list()

        OSM Cli:
            $ osm nsd-list

        """
        endpoint = '{}/osm/nsd/v1/ns_descriptors'.format(settings.OSM_COMPONENTS.get('NBI-API'))
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_nsd(self, nsd_uuid):
        """Fetch details of a specific NS descriptor.

        Args:
            nsd_uuid (str): The UUID of the NSD to fetch details for.

        Returns:
            nsd_obj (Response): A NSD as a requests object.

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.nsd import Nsd
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> nsd = Nsd(token)
            >>> nsd_obj = nsd.get_nsd('9c4a8f58-8317-40a1-b9fe-1db18cff6965')

        OSM Cli:
            $ osm nsd-show cirros_2vnf_ns

        """
        endpoint = '{}/osm/nsd/v1/ns_descriptors/{}'.format(settings.OSM_COMPONENTS.get('NBI-API'), nsd_uuid)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response
