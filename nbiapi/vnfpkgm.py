import logging.config

from django.conf import settings

from httpclient.client import Client

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


class VnfPkgM(object):
    """VNF Descriptor Class.

    This class serves as a wrapper for the Virtual Network Function Descriptor (VNFD)
    part of the Northbound Interface (NBI) offered by OSM. The methods defined in this
    class help retrieve the VNFDs of OSM.

    Attributes:
        bearer_token (str): The OSM Authorization Token.

    Args:
        token (str): The OSM Authorization Token.
    """

    def __init__(self, token):
        """VNF Descriptor Class Constructor."""
        self.__client = Client(verify_ssl_cert=False)
        self.bearer_token = token

    def get_vnfd_list(self):
        """Fetch a list of all VNF descriptors.

        Returns:
            vnfd_list_obj (Response): A list of VNFDs as a requests object.

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.vnfpkgm import VnfPkgM
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> vnfpkgm = VnfPkgM(token)
            >>> vnfd_list_obj = vnfpkgm.get_vnfd_list()

        OSM Cli:
            $ osm vnfd-list

        """
        endpoint = '{}/osm/vnfpkgm/v1/vnf_packages'.format(settings.OSM_COMPONENTS.get('NBI-API'))
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_vnfd(self, vnfd_uuid):
        """Fetch details of a specific VNF descriptor.

        Args:
            vnfd_uuid (str): The UUID of the VNFD to fetch details for.

        Returns:
            vnfd_obj (Response): A VNFD as a requests object.

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.vnfpkgm import VnfPkgM
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> vnfpkgm = VnfPkgM(token)
            >>> vnfd_obj = vnfpkgm.get_vnfd('89f66f1b-73b5-4dc1-8226-a473a2615627')

        OSM Cli:
            $ osm vnfd-show cirros_vnf

        """
        endpoint = '{}/osm/vnfpkgm/v1/vnf_packages/{}'.format(settings.OSM_COMPONENTS.get('NBI-API'), vnfd_uuid)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response
