from app.exc.invalids_keys import InvalidsKeys, InvalidsValues


key_names = ["name", "last_name", "email", "password" ]


def check_keys(data: dict):
    data_keys = data.keys()
    missing_keys = [key for key in key_names if key not in data_keys]

    print(missing_keys)

    if missing_keys:
        raise InvalidsKeys(missing_keys, key_names)


def check_values(data: dict):
    
    for key in key_names:
        if type(data[key]) != str:
            raise InvalidsValues({f'{key}: {data[key]}'}, type(data[key]))