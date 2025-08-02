from .. import errors as errors
from ..utils import normalize_links as normalize_links, version_lt as version_lt

class EndpointConfig(dict):
    def __init__(self, version, aliases=None, links=None, ipv4_address=None, ipv6_address=None, link_local_ips=None, driver_opt=None, mac_address=None) -> None: ...

class NetworkingConfig(dict):
    def __init__(self, endpoints_config=None) -> None: ...

class IPAMConfig(dict):
    def __init__(self, driver: str = 'default', pool_configs=None, options=None) -> None: ...

class IPAMPool(dict):
    def __init__(self, subnet=None, iprange=None, gateway=None, aux_addresses=None) -> None: ...
