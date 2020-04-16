import logging

from httpclient.client import Client
from openmanoapi.config import BASE_URL

logger = logging.getLogger(__name__)


class Vim(object):
    """ Class for VIMs API
    See more: https://osm.etsi.org/wikipub/index.php/RO_Northbound_Interface#VIMs
    """

    def __init__(self):
        self.__client = Client(verify_ssl_cert=True)

    def get_networks(self, openmano_tenant_id, datacenter_id, headers=None, query_params=None):
        """Fetch the list of VIM networks by given tenant ID and datacenter ID

        Args:
            openmano_tenant_id (str): The tenant UUID
            datacenter_id (str): The tenant UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.vims import Vim
            >>> vim = Vim()
            >>> networks = vim.get_networks('f35d06af-ed24-40ca-87c1-4e6ae81008b4', '8e430688-4f7a-11e8-b3e2-00163edc3180')
            >>> print(int(networks.status_code))
            200
            >>> print(networks.json())

        Openmano cli:
            $ openmano vim-net-list --datacenter {datacenter_id} -d
        """
        endpoint = '{}/{}/vim/{}/networks'.format(BASE_URL, openmano_tenant_id, datacenter_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_network(self, openmano_tenant_id, datacenter_id, vim_network_id, headers=None, query_params=None):
        """Fetch details for a VIM datacenter by given tenant ID, datacenter ID and VIM network ID

        Args:
            openmano_tenant_id (str): The tenant UUID
            datacenter_id (str): The tenant UUID
            vim_network_id (str): The VIM network UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.vims import Vim
            >>> vim = Vim()
            >>> network = vim.get_network('f35d06af-ed24-40ca-87c1-4e6ae81008b4', '8e430688-4f7a-11e8-b3e2-00163edc3180', 'deed712a-8a90-42a7-ba8c-98f4c116fca7')
            >>> print(int(network.status_code))
            200
            >>> print(network.json())

        Openmano cli:
            $ openmano vim-net-list --datacenter {datacenter_id} {vim_network_id} -d
        """
        endpoint = '{}/{}/vim/{}/networks/{}'.format(BASE_URL, openmano_tenant_id, datacenter_id, vim_network_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_tenants(self, openmano_tenant_id, datacenter_id, headers=None, query_params=None):
        """Fetch the list of VIM tenants (ie. admin, demo, alt_demo in devstack) by given openmano tenant ID and datacenter ID

        Args:
            openmano_tenant_id (str): The openmano tenant UUID
            datacenter_id (str): The tenant UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.vims import Vim
            >>> vim = Vim()
            >>> network = vim.get_tenants('f35d06af-ed24-40ca-87c1-4e6ae81008b4', '8e430688-4f7a-11e8-b3e2-00163edc3180')
            >>> print(int(network.status_code))
            200
            >>> print(network.json())

        Openmano cli:
            $ openmano vim-tenant-list --datacenter {datacenter_id} -d
        """
        endpoint = '{}/{}/vim/{}/tenants'.format(BASE_URL, openmano_tenant_id, datacenter_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response
