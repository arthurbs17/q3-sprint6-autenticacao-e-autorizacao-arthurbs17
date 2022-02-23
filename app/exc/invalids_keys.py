class InvalidsKeys(Exception):
    def __init__(self, missing_keys, keys_list: list) -> None:
        self.message = {
            "requireds_keys": keys_list,
            "miss_keys": missing_keys
        }


class InvalidsValues(Exception):
    def __init__(self, data: dict, type: str) -> None:
        self.message = {
            "error": f'Type of {data} is {type}',
            "msg": "The values must be passing in STRING!"
        }