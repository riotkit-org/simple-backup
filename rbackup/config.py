import os

def from_dict_or_env(d: dict, key: str, env: str, defaults: str = '') -> str:
    if key in d:
        return d[key]
    val = os.getenv(env, defaults)

    if defaults is None and val is None:
        raise Exception(f"'{key}' not set. Alternatively you can use '{env}' environment variable")

    return val
