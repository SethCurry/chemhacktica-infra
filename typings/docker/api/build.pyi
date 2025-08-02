from .. import auth as auth, constants as constants, errors as errors, utils as utils
from _typeshed import Incomplete

log: Incomplete

class BuildApiMixin:
    def build(self, path=None, tag=None, quiet: bool = False, fileobj=None, nocache: bool = False, rm: bool = False, timeout=None, custom_context: bool = False, encoding=None, pull: bool = False, forcerm: bool = False, dockerfile=None, container_limits=None, decode: bool = False, buildargs=None, gzip: bool = False, shmsize=None, labels=None, cache_from=None, target=None, network_mode=None, squash=None, extra_hosts=None, platform=None, isolation=None, use_config_proxy: bool = True): ...
    def prune_builds(self, filters=None, keep_storage=None, all=None): ...

def process_dockerfile(dockerfile, path): ...
