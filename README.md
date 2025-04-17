# checkhacktica-infra

The only usable part of this at the moment is the `chemgr` binary.

## chemgr

`chemgr` is a CLI to assist in administering instances of ChemHacktica.

### Installation

`go install github.com/SethCurry/chemhacktica-infra/bin/chemgr`

### Usage

Running healthchecks

```bash
chemgr healthcheck
```

This will look to ensure that all of the expected containers are running,
and check how many 5xx errors the webserver has seen from backends in the past.

It will currently cause a failing healthcheck if there have been more than 5 5xx errors
from backends in the past hour. Future versions will make the lookback period and max
error count configurable.
