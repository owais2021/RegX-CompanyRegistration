import ckan.plugins.toolkit as tk
import ckanext.regx.logic.schema as schema


@tk.side_effect_free
def regx_get_sum(context, data_dict):
    tk.check_access(
        "regx_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.regx_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }

@tk.side_effect_free
def my_custom_action(context, data_dict):
        '''
        This action performs a custom task, for example, creating a new object or
        updating an existing one.

        :param param1: description of the parameter
        :type param1: string
        :param param2: description of the parameter
        :type param2: int

        :returns: result of the operation
        :rtype: dictionary
        '''

        # Do something with the data_dict here
        # For example, let's just return the input data as output

        result = {
            'status': 'success',
            'message': 'Action completed successfully',
            'data': data_dict
        }

        return result


def get_actions():
    return {
        'regx_get_sum': regx_get_sum,
        'my_custom_action': my_custom_action,
    }
