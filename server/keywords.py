from enum import Enum

class RequestKeywordType(Enum):
    """
    The JSON keywords the server can expect in a request
    from the client.
    """

    FILTER = 'filter'
    FILTER_ID = "filter_id"
    TRASH = 'trash'
    DETAILS = 'details'
    SCANNER_ID = 'scanner_id'
    NAME = 'name'
    COMMENT = 'comment'
    LOGIN = 'login'
    PASSWORD = 'password'
    ALLOW_INSECURE = 'allow_insecure'
    CONFIG_ID = 'config_id'
    TARGET_ID = 'target_id'
    ALERT_IDS = 'alert_ids'
    MAKE_UNIQUE = 'make_unique'
    ASSET_HOSTS_FILTER = 'asset_hosts_filter'
    HOSTS = 'hosts'
    EXCLUDE_HOSTS = 'exclude_hosts'
    SSH_CREDENTIAL_ID = 'ssh_credential_id'
    SSH_CREDENTIAIL_PORT = 'ssh_credential_port'
    ALIVE_TEST = 'alive_test'
    REVERSE_LOOKUP_ONLY = 'reverse_lookup_only'
    REVERSE_LOOKUP_UNIFY = 'reverse_lookup_unify'
    PORT_RANGE = 'port_range'
    PORT_LIST_ID = 'port_list_id'
    TASK_ID = 'task_id'
    REPORT_ID = 'report_id'
    REPORT_FORMAT_ID = 'report_format_id'


class RequestMethodDataType(Enum):
    # Keywords for Send to host method
    SEND_HOST = 'send_host'
    SEND_PORT = 'send_port'
    SEND_REPORT_FORMAT = 'send_repot_format'

    # Keywords for SCP method
    SCP_REPORT_FORMAT = "scp_report_format"
    SCP_PATH = "scp_path"
    SCP_KNOWN_HOSTS = "scp_known_hosts"
    SCP_HOST = "scp_host"
    SCP_CREDENTIAL = "scp_credential"


class RequestEventDataType(Enum):
    STATUS = 'status'


class ResponseKeywordType(Enum):
    """
    The keywords the client can expect to find in a JSON 
    response from the server
    """

    NAME = 'name'
    ID = 'id'
    STATUS = 'status'
    STATUS_TEXT = 'status_text'
    DATA = 'data'
