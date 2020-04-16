import logging

from httpclient.client import Client
from openmanoapi.config import BASE_URL

logger = logging.getLogger(__name__)


class Scenario(object):
    """ Class for Scenario API
    See more: https://osm.etsi.org/wikipub/index.php/RO_Northbound_Interface#GET_.2Fopenmano.2F.7Btenant_id.7D.2Fscenarios
    """

    def __init__(self):
        self.__client = Client(verify_ssl_cert=True)

    def get_list(self, openmano_tenant_id, headers=None, query_params=None):
        """Fetch the list of Openmano scenarios by given tenant ID

        Args:
            openmano_tenant_id (str): The tenant UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.scenarios import Scenario
            >>> sc = Scenario()
            >>> scenarios = sc.get_list('f35d06af-ed24-40ca-87c1-4e6ae81008b4')
            >>> print(int(scenarios.status_code))
            200
            >>> print(scenarios.json())

        Openmano cli:
            $ openmano scenario-list -a --debug
        """
        endpoint = '{}/{}/scenarios'.format(BASE_URL, openmano_tenant_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response

    def get(self, openmano_tenant_id, scenario_id, headers=None, query_params=None):
        """Fetch details for an Openmano scenario by given tenant ID and scenario ID

        Args:
            openmano_tenant_id (str): The tenant UUID
            scenario_id (str): The scenario UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.scenarios import Scenario
            >>> sc = Scenario()
            >>> scenario = sc.get('f35d06af-ed24-40ca-87c1-4e6ae81008b4', '577185b4-45dc-4a94-980a-72e1f0068022')
            >>> print(int(scenario.status_code))
            200
            >>> print(scenario.json())

        Openmano cli:
            $ openmano scenario-list {scenario_id} --debug
        """
        endpoint = '{}/{}/scenarios/{}'.format(BASE_URL, openmano_tenant_id, scenario_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response
