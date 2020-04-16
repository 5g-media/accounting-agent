import logging

from httpclient.client import Client
from openmanoapi.config import BASE_URL

logger = logging.getLogger(__name__)


class Vnfd(object):
    """ Class for VNF API
    See more: https://osm.etsi.org/wikipub/index.php/RO_Northbound_Interface#VNFs
    """

    def __init__(self):
        self.__client = Client(verify_ssl_cert=True)

    def get_list(self, openmano_tenant_id, headers=None, query_params=None):
        """Fetch the list of Openmano VNF descriptors by given tenant ID

        Args:
            openmano_tenant_id (str): The tenant UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.vnfds import Vnfd
            >>> vnfd = Vnfd()
            >>> vnfds = vnfd.get_list('f35d06af-ed24-40ca-87c1-4e6ae81008b4')
            >>> print(int(vnfds.status_code))
            200
            >>> print(vnfds.json())

        Openmano cli:
            $ openmano vnf-list -a -d
        """
        endpoint = '{}/{}/vnfs'.format(BASE_URL, openmano_tenant_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response

    def get(self, openmano_tenant_id, vnfd_id, headers=None, query_params=None):
        """Fetch details for an Openmano datacenter by given tenant ID and VNF descriptor ID

        Args:
            openmano_tenant_id (str): The tenant UUID
            vnfd_id (str): The VNF descriptor UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.vnfds import Vnfd
            >>> vnfd = Vnfd()
            >>> vnfd_entity = vnfd.get('f35d06af-ed24-40ca-87c1-4e6ae81008b4', 'cfa284c1-a6de-48d4-ac10-1d943ee279c8')
            >>> print(int(vnfd_entity.status_code))
            200
            >>> print(vnfd_entity.json())

        Openmano cli:
            $ openmano vnf-list {vnfd_id} -d
        """
        endpoint = '{}/{}/vnfs/{}'.format(BASE_URL, openmano_tenant_id, vnfd_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response
