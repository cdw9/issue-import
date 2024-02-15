# The field names here need to match what is set up in the GitHub Project
# IDs are populated by the script after querying the Project
FIELDS = {
    'Status': {
        'type': 'Single Select',
        'default': 'New',
    },
    'Job Code': {
        'type': 'Single Select',
        'default': '',  # will be set to the only option if there is only one
    },
    'Type': {
        'type': 'Single Select',
        'default': 'Task',  # value for items that are not User Stories or Requirements
    },
    'Priority': {
        'type': 'Single Select',
        'default': 'Major',
    },
    'Component': {
        'type': 'Single Select',
        'default': '',  # leave this blank, get value from CSV
    },
    'Complexity (pts.)': {
        'type': 'Number',
        'default': '',  # leave this blank, get value from CSV
    },
    'Effort Planned': {
        'type': 'Number',
        'default': '',  # leave this blank, get value from CSV
    },
    'User Story': {
        'type': 'Text',
        'default': '',  # leave this blank, get value from CSV
    },
}

def reconcile_fields(fields):
    # reconcile the fields above with the fields in the Project
    # add ID information for the field and default option
    for field in fields:
        if field['name'] in FIELDS:
            current_field = FIELDS[field['name']]
            current_field['id'] = field['id']
            if 'options' not in field:
                continue
            all_options = {option['name']: option['id'] for option in field['options']}
            current_field['options'] = all_options
            if not current_field.get('default'):
                continue
            current_field['default_id'] = all_options[current_field['default']]
    return FIELDS