import logging

from httpclient.client import Client
from openmanoapi.config import BASE_URL

logger = logging.getLogger(__name__)


class Action(object):
    """ Class for Action API
    """

    def __init__(self):
        self.__client = Client(verify_ssl_cert=True)

    def get_any(self, tenant_id, headers=None, query_params=None):
        """Fetch the list of actions for an instance by given tenant ID

        Args:
            tenant_id (str): The tenant UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.actions import Action
            >>> obj = Action()
            >>> actions = obj.get_any('f35d06af-ed24-40ca-87c1-4e6ae81008b4')
            >>> print(int(actions.status_code))
            200
            >>> print(actions.json())

        Openmano cli:
            $ openmano action-list --all ALL --debug
        """
        endpoint = '{}/{}/instances/any/action'.format(BASE_URL, tenant_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response

    def get_list(self, tenant_id, instance_id, headers=None, query_params=None):
        """Fetch the list of actions by given tenant ID and instance ID

        Args:
            tenant_id (str): The tenant UUID
            instance_id (str): The instance UUID
            headers (dict, optional): the required HTTP headers, e.g., Accept: application/json
            query_params (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object

        Examples:
            >>> from httpclient.client import Client
            >>> from openmanoapi.actions import Action
            >>> obj = Action()
            >>> actions = obj.get_list('f35d06af-ed24-40ca-87c1-4e6ae81008b4', '22bbb91d-51a6-43ba-9850-d9697915921b')
            >>> print(int(actions.status_code))
            200
            >>> print(actions.json())

        Openmano cli:
            $ openmano action-list --instance {instance_id} --debug
        """
        endpoint = '{}/{}/instances/{}/action'.format(BASE_URL, tenant_id, instance_id)
        response = self.__client.get(endpoint, headers=headers, query_params=query_params)
        logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                     "".format(response.url, response.status_code, response.headers, response.text))
        return response
