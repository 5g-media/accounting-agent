import logging

from httpclient.client import Client
from openmanoapi.config import BASE_URL

logger = logging.getLogger(__name__)


class Instance(object):
    """ Class for Instance API
    See more: https://osm.etsi.org/wikipub/index.php/RO_Northbound_Interface#Instances
    """

    def __init__(self):
        self.__client = Client(verify_ssl_cert=True)

    def get_list(self, openmano_tenant_id, headers=None, query_params=None):
        """Fetch the list of Openmano instances by given tenant ID

        Args:
            openmano_tenant_id (str): The tenant UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.instances import Instance
            >>> obj = Instance()
            >>> instances = obj.get_list('f35d06af-ed24-40ca-87c1-4e6ae81008b4')
            >>> print(int(instances.status_code))
            200
            >>> print(instances.json())

        Openmano cli:
            $ openmano instance-scenario-list -a -d
        """
        endpoint = '{}/{}/instances'.format(BASE_URL, openmano_tenant_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response

    def get(self, openmano_tenant_id, instance_id, headers=None, query_params=None):
        """Fetch details for an Openmano instance by given tenant ID and instance ID

        Args:
            openmano_tenant_id (str): The tenant UUID
            instance_id (str): The instance UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.instances import Instance
            >>> obj = Instance()
            >>> instance = obj.get('f35d06af-ed24-40ca-87c1-4e6ae81008b4', '661d343f-740a-4a98-9e7b-bbfd31ff24ef')
            >>> print(int(instance.status_code))
            200
            >>> print(instance.json())

        Openmano cli:
            $ openmano instance-scenario-list {instance_id} -d
        """
        endpoint = '{}/{}/instances/{}'.format(BASE_URL, openmano_tenant_id, instance_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response
