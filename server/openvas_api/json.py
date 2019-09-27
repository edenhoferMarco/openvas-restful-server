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

    return validate_string_input(send_port)

def get_send_report_format(json_data):
    send_report_format = json_data.get('send_report_format')

    return validate_string_input(send_report_format)



# util methods for input validation
def validate_string_input(string):
    if string != None and len(string) > 0:
        return string
    else:
        return None

def validate_bool_input(bool_value):
    if bool_value != None and (bool_value == 'True' or bool_value == 'False'):
        return bool_value
    else:
        return None