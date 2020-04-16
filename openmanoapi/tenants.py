import logging

from httpclient.client import Client
from openmanoapi.config import BASE_URL

logger = logging.getLogger(__name__)


class Tenant(object):
    """ Class for Tenant API
    See more: https://osm.etsi.org/wikipub/index.php/RO_Northbound_Interface#Tenants
    """

    def __init__(self):
        self.__client = Client(verify_ssl_cert=True)

    def get_list(self, headers=None, query_params=None):
        """Fetch the list of Openmano tenants

        Args:
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.tenants import Tenant
            >>> tn = Tenant()
            >>> tenants = tn.get_list()
            >>> print(int(tenants.status_code))
            200
            >>> print(tenants.json())
            {"tenants": [{"created_at": "2018-05-03T16:00:04", "description": null, "uuid": "f35d06af-ed24-40ca-87c1-4e6ae81008b4", "name": "osm"} ] }

        Openmano cli:
            $ openmano tenant-list -d
        """
        endpoint = '{}/tenants'.format(BASE_URL)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response

    def get(self, openmano_tenant_id, headers=None, query_params=None):
        """Fetch details for an Openmano tenant by given tenant ID

        Args:
            openmano_tenant_id (str): The tenant UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.tenants import Tenant
            >>> tn = Tenant()
            >>> tenant = tn.get('f35d06af-ed24-40ca-87c1-4e6ae81008b4')
            >>> print(int(tenant.status_code))
            200
            >>> print(tenant.json())

        Openmano cli:
            $ openmano tenant-list {openmano_tenant_id} -d
        """
        endpoint = '{}/tenants/{}'.format(BASE_URL, openmano_tenant_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response
