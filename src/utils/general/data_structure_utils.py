from typing import Dict, List

def key_given_value(dict: Dict[str, List[str]], value: str) -> str:
    for key, values in dict.items():
        if value in values:
            return key
    return ''