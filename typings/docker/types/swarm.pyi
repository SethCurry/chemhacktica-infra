from ..errors import InvalidVersion as InvalidVersion
from ..utils import version_lt as version_lt

class SwarmSpec(dict):
    def __init__(self, version, task_history_retention_limit=None, snapshot_interval=None, keep_old_snapshots=None, log_entries_for_slow_followers=None, heartbeat_tick=None, election_tick=None, dispatcher_heartbeat_period=None, node_cert_expiry=None, external_cas=None, name=None, labels=None, signing_ca_cert=None, signing_ca_key=None, ca_force_rotate=None, autolock_managers=None, log_driver=None) -> None: ...

class SwarmExternalCA(dict):
    def __init__(self, url, protocol=None, options=None, ca_cert=None) -> None: ...
