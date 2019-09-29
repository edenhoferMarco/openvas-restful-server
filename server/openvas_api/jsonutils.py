def get_filter(json_data):
    """
    Returns the value (if available) for the filter key, used for the openvas rest-api, from an json input.
    """
    filter = json_data.get('filter')

    return validate_string_input(filter)

def get_filter_id(json_data):
    """
    Returns the value (if available) for the filter_id key, used for the openvas rest-api, from an json input.
    """
    filter_id = json_data.get('filter_id')

    return validate_string_input(filter_id)

def get_trash(json_data):
    """
    Returns the value (if available) for the trash key, used for the openvas rest-api, from an json input.
    """
    trash = json_data.get('trash')

    return validate_bool_input(trash)

def get_details(json_data):
    """
    Returns the value (if available) for the details key, used for the openvas rest-api, from an json input.
    """
    details = json_data.get('details')

    return validate_bool_input(details)

def get_scanner_id(json_data):
    """
    Returns the value (if available) for the scanner_id key, used for the openvas rest-api, from an json input.
    """
    scanner_id = json_data.get('scanner_id')

    return validate_string_input(scanner_id)

def get_name(json_data):
    """
    Returns the value (if available) for the name key, used for the openvas rest-api, from an json input.
    """

    name = json_data.get('name')

    return validate_string_input(name)

def get_status(json_data):
    status = json_data.get('status')

    return validate_string_input(status)

def get_send_host(json_data):
    send_host = json_data.get('send_host')

    return validate_string_input(send_host)

def get_send_port(json_data):
    send_port = json_data.get('send_port')
    port = int(validate_int_input(send_port))

    # check if value is in a valid port range
    if port in range(0, 65535):
        return port
    else:
        return None

    
def get_send_report_format(json_data):
    send_report_format = json_data.get('send_report_format')

    return validate_string_input(send_report_format)

def get_comment(json_data):
    comment = json_data.get('comment')

    return validate_string_input(comment)

def get_login(json_data):
    login = json_data.get('login')

    return validate_string_input(login)

def get_password(json_data):
    password = json_data.get('password')

    return validate_string_input(password)

def get_allow_insecure(json_data):
    allow_insecure = json_data.get('allow_insecure')

    return validate_bool_input(allow_insecure)

def get_config_id(json_data):
    config_id = json_data.get('config_id')

    return validate_string_input(config_id)

def get_target_id(json_data):
    target_id = json_data.get('target_id')

    return validate_string_input(target_id)

def get_alert_ids(json_data):
    alert_ids = []
    ids = json_data.get('alert_ids')

    for id in ids:
        current_id = validate_string_input(id)
        if current_id:
            alert_ids.append(current_id)

    return alert_ids

def get_make_unique(json_data):
    make_unique = json_data.get('make_unique')

    return validate_bool_input(make_unique)

def get_asset_hosts_filter(json_data):
    asset_hosts_filter = json_data.get('asset_hosts_filter')

    return validate_string_input(asset_hosts_filter)

def get_hosts(json_data):
    hosts = []

    hosts_data = json_data.get('hosts')

    for host in hosts_data:
        current_host = validate_string_input(host)
        if current_host:
            hosts.append(host)

    return hosts

def get_exclude_hosts(json_data):
    exclude_hosts = []

    hosts_data = json_data.get('exclude_hosts')

    for host in hosts_data:
        current_host = validate_string_input(host)
        if current_host:
            exclude_hosts.append(current_host)

    return exclude_hosts

def get_ssh_credential_id(json_data):
    ssh_credential_id = json_data.get('ssh_credential_id')

    return validate_string_input(ssh_credential_id)

def get_ssh_credential_port(json_data):
    ssh_credential_port = json_data.get('ssh_credential_port')
    port = int(validate_int_input(ssh_credential_port))

    # check if value is in a valid port range
    if port in range(0, 65535):
        return port
    else:
        return None

def get_alive_test(json_data):
    alive_test = json_data.get('alive_test')

    return validate_string_input(alive_test)

def get_reverse_lookup_only(json_data):
    reverse_lookup_only = json_data.get('reverse_lookup_only')

    return validate_bool_input(reverse_lookup_only)

def get_reverse_lookup_unify(json_data):
    reverse_lookup_unify = json_data.get('reverse_lookup_unify')

    return validate_bool_input(reverse_lookup_unify)

def get_port_range(json_data):
    port_range = json_data.get('port_range')

    return validate_string_input(port_range)

def get_port_list_id(json_data):
    port_list_id = json_data.get('port_list_id')

    return validate_string_input(port_list_id)



# util methods for input validation
def validate_string_input(string):
    if string:
        return string
    else:
        return None

def validate_bool_input(bool_value):
    if bool_value == 'True' or bool_value == 'False':
        return bool_value
    else:
        return None

def validate_int_input(int_as_string):
    try:
        return int(validate_string_input(int_as_string))
    except ValueError:
        return None