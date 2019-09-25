def get_filter(json_data):
        name = json_data.get('filter')

        if name != None and len(name) > 0:
            return name
        else:
            return None

def get_filter_id(json_data):
    filter_id = json_data.get('filter_id')

    if filter_id != None and len(filter_id) > 0:
        return filter_id
    else:
        return None

def get_trash(json_data):
    trash = json_data.get('trash')

    if trash != None and (trash == 'True' or trash == 'False'):
        return trash
    else:
        return None

def get_details(json_data):
    details = json_data.get('details')

    if details != None and (details == 'True' or details == 'False'):
        return details
    else:
        return None

def get_scanner_id(json_data):
    scanner_id = json_data.get('scanner_id')

    if scanner_id != None and len(scanner_id) > 0:
        return scanner_id
    else:
        return None