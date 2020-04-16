import logging.config

import requests
import urllib3
from django.conf import settings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


def bearer_token(username, password):
    """Get bearer authorization token from OSM

    Args:
        username (str): The admin OSM username
        password (str): The admin OSM password

    Returns:
        token (str): An authorization token

    Examples:
        >>> from nbiapi.identity import bearer_token
        >>> from django.conf import settings
        >>> token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'), settings.OSM_ADMIN_CREDENTIALS.get('password'))

    """
    if not isinstance(username, str):
        raise TypeError("The given type of username is `{}`. Expected str.".format(type(username)))
    if not isinstance(password, str):
        raise TypeError("The given type of password is `{}`. Expected str.".format(type(password)))
    endpoint = '{}/osm/admin/v1/tokens'.format(settings.OSM_COMPONENTS.get('NBI-API'))
    params = {'username': username, 'password': password}
    headers = {'Accept': 'application/json'}
    response = requests.post(url=endpoint, params=params, headers=headers, verify=False)
    logger.debug("Request `GET {}` returns HTTP status `{}`, headers `{}` and body `{}`."
                 .format(response.url, response.status_code, response.headers, response.text))
    if response.status_code == 200:
        return response.json()['id']
    return None
