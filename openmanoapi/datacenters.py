import logging

from httpclient.client import Client
from openmanoapi.config import BASE_URL

logger = logging.getLogger(__name__)


class Datacenter(object):
    """ Class for Datacenter API
    See more: https://osm.etsi.org/wikipub/index.php/RO_Northbound_Interface#Datacenters
    """

    def __init__(self):
        self.__client = Client(verify_ssl_cert=True)

    def get_list(self, openmano_tenant_id, headers=None, query_params=None):
        """Fetch the list of Openmano datacenter entities by given tenant ID

        Args:
            openmano_tenant_id (str): The tenant UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.datacenters import Datacenter
            >>> dc = Datacenter()
            >>> datacenters = dc.get_list('f35d06af-ed24-40ca-87c1-4e6ae81008b4')
            >>> print(int(datacenters.status_code))
            200
            >>> print(datacenters.json())
            {"datacenters": [{"vim_url": "http://192.168.1.194/identity/v2.0", "created_at": "2018-05-04T09:07:22", "type": "openstack", "uuid": "8e430688-4f7a-11e8-b3e2-00163edc3180", "name": "devstack-pike"} ] }

        Openmano cli:
            $ openmano datacenter-list -a --debug
        """
        endpoint = '{}/{}/datacenters'.format(BASE_URL, openmano_tenant_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response

    def get(self, openmano_tenant_id, datacenter_id, headers=None, query_params=None):
        """Fetch details for an Openmano datacenter by given tenant ID and datacenter ID

        Args:
            openmano_tenant_id (str): The tenant UUID
            datacenter_id (str): The datacenter UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.datacenters import Datacenter
            >>> dc = Datacenter()
            >>> datacenters = dc.get('f35d06af-ed24-40ca-87c1-4e6ae81008b4', '8e430688-4f7a-11e8-b3e2-00163edc3180')
            >>> print(int(datacenters.status_code))
            200
            >>> print(datacenters.json())

        Openmano cli:
            $ openmano datacenter-list {datacenter_id} -d
        """
        endpoint = '{}/{}/datacenters/{}'.format(BASE_URL, openmano_tenant_id, datacenter_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response
