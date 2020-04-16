import logging.config

from django.conf import settings
from requests import Response

from httpclient.client import Client

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


class NsLcm(object):
    """NS LCM Class.

    This class serves as a wrapper for the Network Service Lifecycle Management (NSLCM) part
    of the Northbound Interface (NBI) offered by OSM. The methods defined in this class help
    retrieve the NS-related entities of OSM, i.e. NS and VNFs or terminate an NS instance.

    Attributes:
        bearer_token (str): The OSM Authorization Token

    Args:
        token (str): The OSM Authorization Token

    """

    def __init__(self, token):
        """NS LCM Class Constructor."""
        self.__client = Client(verify_ssl_cert=False)
        self.bearer_token = token

    def get_ns_list(self):
        """Fetch a list of all NS Instances

        Returns:
            ns_list_obj (Response): A list of NSs as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.nslcm import NsLcm
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> nslcm = NsLcm(token)
            >>> ns_list_obj = nslcm.get_ns_list()

        OSM Cli:
            $ osm ns-list

        """
        endpoint = '{}/osm/nslcm/v1/ns_instances'.format(settings.OSM_COMPONENTS.get('NBI-API'))
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_ns(self, ns_uuid):
        """Fetch details of a specific NS Instance

        Args:
            ns_uuid (str): The UUID of the NS to fetch details for

        Returns:
            ns_obj (Response): A NS as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.nslcm import NsLcm
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> nslcm = NsLcm(token)
            >>> ns_obj = nslcm.get_ns('07048175-660b-404f-bbc9-5be7581e74de')

        OSM Cli:
            $ osm ns-show 07048175-660b-404f-bbc9-5be7581e74de

        """
        endpoint = '{}/osm/nslcm/v1/ns_instances/{}'.format(settings.OSM_COMPONENTS.get('NBI-API'), ns_uuid)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def terminate_ns(self, ns_uuid):
        """Terminate a NS Instance.

        Args:
            ns_uuid (str): The UUID of the NS to terminate

        Returns:
            response (Response): A requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.nslcm import NsLcm
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> nslcm = NsLcm(token)
            >>> response = nslcm.terminate_ns('07048175-660b-404f-bbc9-5be7581e74de')

        """
        endpoint = '{}/osm/nslcm/v1/ns_instances/{}/terminate'.format(settings.OSM_COMPONENTS.get('NBI-API'), ns_uuid)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.post(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_vnf_list(self):
        """Fetch a list of all VNFs.

        Returns:
            vnf_list_obj (Response): A list of VNFs as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.nslcm import NsLcm
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> nslcm = NsLcm(token)
            >>> vnf_list_obj = nslcm.get_vnf_list()

        OSM Cli:
            $ osm vnf-list

        """
        endpoint = '{}/osm/nslcm/v1/vnf_instances'.format(settings.OSM_COMPONENTS.get('NBI-API'))
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_vnf(self, vnf_uuid):
        """Fetch details of a specific VNF

        Args:
            vnf_uuid (str): The UUID of the VNF to fetch details for

        Returns:
            vnf_obj (Response): A VNF as a requests object

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.nslcm import NsLcm
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> nslcm = NsLcm(token)
            >>> vnf_obj = nslcm.get_vnf('a5f506e9-45c7-42fd-b12d-b5c657ed87fb')

        OSM Cli:
            $ osm vnf-show a5f506e9-45c7-42fd-b12d-b5c657ed87fb
        """
        endpoint = '{}/osm/nslcm/v1/vnf_instances/{}'.format(settings.OSM_COMPONENTS.get('NBI-API'), vnf_uuid)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_vnf_list_by_ns(self, ns_uuid):
        """Fetch list of VNFs for specific NS Instance.

        Args:
            ns_uuid (str): The UUID of the NS to fetch VNFs for.

        Returns:
            vnf_list_obj (Response): A list of VNFs as a requests object.

        Examples:
            >>> from django.conf import settings
            >>> from nbiapi.identity import bearer_token
            >>> from nbiapi.nslcm import NsLcm
            >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))
            >>> nslcm = NsLcm(token)
            >>> vnf_list_obj = nslcm.get_vnf('a5f506e9-45c7-42fd-b12d-b5c657ed87fb')

        """
        endpoint = '{}/osm/nslcm/v1/vnf_instances?nsr-id-ref={}'.format(settings.OSM_COMPONENTS.get('NBI-API'), ns_uuid)
        headers = {"Authorization": "Bearer {}".format(self.bearer_token), "Accept": "application/json"}
        response = self.__client.get(endpoint, headers)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     .format(response.url, response.status_code, response.headers, response.text))
        return response
