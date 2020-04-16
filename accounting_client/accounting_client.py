import json
import logging
from time import time

from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from accounting_client.config import BASE_URL, ACCOUNTING_PASSWORD, ACCOUNTING_USERNAME, AUTH_URL, CLOSE_SESSIONS
from httpclient.client import Client

logger = logging.getLogger(__name__)


class AccountingClient(object):
    """Accounting Client Class.

    This class serves as a wrapper for the Accounting/Billing services of 5G-MEDIA project,
    as they are deployed in ENG's cloud. The methods implemented in this class are intended
    for logging in to the services and opening/closing of NS, VNF and VDU sessions.

    """

    __instance = None

    def __init__(self):
        """Accounting Client Class Constructor."""
        self.__client = Client(verify_ssl_cert=True)
        self.__headers = {'Content-Type': 'application/json'}
        self.login()

    # Singleton Class
    def __new__(cls):
        if cls.__instance is not None:
            return cls.__instance
        else:
            cls.__instance = super(AccountingClient, cls).__new__(cls)
            return cls.__instance

    def login(self):
        """Login to the Accounting/Billing Service."""
        payload = {
            'username': ACCOUNTING_USERNAME,
            'password': ACCOUNTING_PASSWORD
        }
        response = self.__client.post(url=AUTH_URL, headers=self.__headers, payload=json.dumps(payload))
        if response.status_code == HTTP_200_OK:
            self.__headers['Authorization'] = 'Bearer {}'.format(json.loads(response.text)['id_token'])
            logger.info('Successfully logged on the accounting service')

    def available_user_resource_list(self):
        """Get the available user resource list.

        Returns:
            user_resource_obj (object): A user resource list as a requests objects

        """
        url = BASE_URL + '/availableUserResourceList'
        response = self.__client.get(url=url, headers=self.__headers)
        if response.status_code == HTTP_200_OK:
            return response
        return None

    def open_session_retrial(self, url, payload):
        """Retry opening a session after the authorization token has expired.

        Args:
            url (str): The url for the session opening request
            payload (dict): The essential data to post for session opening

        Returns:
            session_id (int): The ID of the session that was opened

        """
        self.login()
        response = self.__client.post(url=url, headers=self.__headers, payload=json.dumps(payload))
        if response.status_code == HTTP_200_OK:
            session_id = int(response.text)
            logger.info('Opened session with id {}'.format(session_id))
            return session_id

    def open_ns_session(self, ns):
        """Open a Network Service (NS) Session.

        Args:
            ns (obj): An NS Instance object

        Returns:
            ns_session_id (int): The ID of the opened NS session

        """
        url = BASE_URL + '/openNsSession'
        payload = {
            'timestamp_sec': time(),
            'catalog_tenant': ns.catalog_tenant,
            'catalog_user': ns.catalog_user,
            'mano_id': ns.mano_id,
            'mano_project': ns.mano_project,
            'mano_user': ns.mano_user,
            'nfvipop_id': ns.nfvipop_id,
            'ns_id': ns.uuid,
            'ns_name': ns.name
        }
        logger.info('Attempting to open ns session with payload {}'.format(payload))
        response = self.__client.post(url=url, headers=self.__headers, payload=json.dumps(payload))
        logger.debug('Open ns session response: {}, Status code: {}'.format(response.text, response.status_code))
        if response.status_code == HTTP_200_OK:
            ns_session_id = int(response.text)
            logger.info('Opened ns session with id {}'.format(ns_session_id))
            return ns_session_id
        elif response.status_code in [HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN]:
            logger.warning('Token has expired  and open_ns_sesion failed; retrying')
            return self.open_session_retrial(url, payload)

    def open_vnf_session(self, ns_session_id, vnf_uuid, vnf_name):
        """Open a Virtual Network Function (VNF) Session.

        Args:
            ns_session_id (int): The id of the NS session where the VNF belongs
            vnf_uuid (str): The UUID of the VNF
            vnf_name (str): The name of the VNF

        Returns:
            vnf_session_id (int): The ID of the opened VNF session

        """
        url = BASE_URL + '/openVnfSession'
        payload = {
            'timestamp_sec': time(),
            'ns_session_id': ns_session_id,
            'vnf_id': vnf_uuid,
            'vnf_name': vnf_name
        }
        logger.info('Attempting to open vnf session with payload {}'.format(payload))
        response = self.__client.post(url=url, headers=self.__headers, payload=json.dumps(payload))
        logger.debug('Open vnf session response: {}, Status code: {}'.format(response.text, response.status_code))
        if response.status_code == HTTP_200_OK:
            vnf_session_id = int(response.text)
            logger.info('Opened vnf session with id {}'.format(vnf_session_id))
            return vnf_session_id
        elif response.status_code in [HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN]:
            logger.warning('Token has expired  and open_vnf_sesion failed; retrying')
            return self.open_session_retrial(url, payload)

    def open_vdu_session(self, vnf_session_id, vdu):
        """Open a Virtual Deployment Unit (VDU) session.

        Args:
            vnf_session_id (int): The id of the VNF session where the VDU belongs.
            vdu (obj): A VDU object

        Returns:
            vdu_session_id (int): The VDU session id.

        """
        url = BASE_URL + '/openVduSession'
        payload = {
            'timestamp_sec': time(),
            'flavorCpuCount': vdu.vcpu,
            'flavorDiskGb': vdu.vdisk,
            'flavorMemoryMb': vdu.vram,
            'nfvipop_id': vdu.nfvipop_id,
            'vdu_id': vdu.uuid,
            'vdu_type': 'FAAS_VNF' if 'faas' in vdu.nfvipop_id.lower() else 'PLAIN_VNF',
            'vnf_session_id': vnf_session_id
        }
        logger.info('Attempting to open vdu session with payload {}'.format(payload))
        response = self.__client.post(url=url, headers=self.__headers, payload=json.dumps(payload))
        logger.debug('Open vdu session response: {}, Status code: {}'.format(response.text, response.status_code))
        if response.status_code == HTTP_200_OK:
            vdu_session_id = int(response.text)
            logger.info('Opened vdu session with id {}'.format(vdu_session_id))
            return vdu_session_id
        elif response.status_code in [HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN]:
            logger.warning('Token has expired  and open_vdu_sesion failed; retrying')
            return self.open_session_retrial(url, payload)

    def log_vdu_consumption(self, metric_type, metric_value, vdu_session_id):
        """Send measurement of VDU consumption for logging.

        Args:
            metric_type (str): The type of metric
            metric_value (double): The value of metric
            vdu_session_id (int): The id of the VDU session that the metric refers to

        """
        url = BASE_URL + '/logVduConsumption'
        payload = {
            'timestamp': time(),
            'consumption_type': metric_type,
            'consumption_value': metric_value,
            'vdu_session_id': vdu_session_id
        }
        logger.info('Sending vdu consumption with payload {}'.format(payload))
        response = self.__client.post(url=url, headers=self.__headers, payload=json.dumps(payload))
        logger.debug('Log vdu consumption response: {}, Status code: {}'.format(response.text, response.status_code))
        if response.status_code == HTTP_200_OK:
            logger.info('Vdu consumption logged successfully')
            return
        elif response.status_code in [HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN]:
            logger.warning('Token has expired and log_vdu_consumption failed; retrying')
            self.login()
            response = self.__client.post(url=url, headers=self.__headers, payload=json.dumps(payload))
            if response.status_code == HTTP_200_OK:
                logger.info('Vdu consumption logged successfully')
                return json.loads(response.text)['id']

    def close_session_retrial(self, url, payload):
        """Retry closing a session after the authorization token has expired.

        Args:
            url (str): The url of the API call
            payload (dict): The payload to send to the API call

        """
        self.login()
        response = self.__client.post(url=url, headers=self.__headers, payload=json.dumps(payload))
        if response.status_code == HTTP_200_OK:
            logger.warning('Session was closed')
            return
        return

    def close_session(self, session_id, session_type):
        """Close a NS, VNF or VDU session.

        Args:
            session_id (int): The ID of the session
            session_type (str): The type of the session

        """
        url = BASE_URL + CLOSE_SESSIONS[session_type]
        payload = {'id': session_id}
        logger.info('Closing {} session with id {}'.format(session_type, session_id))
        response = self.__client.post(url=url, headers=self.__headers, payload=json.dumps(payload))
        logger.debug('Close {} session response: {}, Status code: {}'.format(session_type, response.text,
                                                                             response.status_code))
        if response.status_code == HTTP_200_OK:
            logger.info('Successfully closed {} session'.format(session_type))
            return
        elif response.status_code in [HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN]:
            logger.warning('Token has expired and close_session failed; retrying')
            self.close_session_retrial(url, payload)


accounting_client = AccountingClient()
