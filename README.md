pyiso
============

[![Build Status](https://travis-ci.org/WattTime/pyiso.svg?branch=master)](https://travis-ci.org/WattTime/pyiso)
[![Coverage Status](https://coveralls.io/repos/WattTime/pyiso/badge.png?branch=master)](https://coveralls.io/r/WattTime/pyiso?branch=master)
[![Downloads](https://pypip.in/download/pyiso/badge.png)](https://pypi.python.org/pypi/pyiso/)

pyiso provides Python client libraries for ISO and other power grid data sources.
It powers the WattTime Impact API (code https://github.com/WattTime/watttime-grid-api, live http://api.watttime.org/).

Documentation: http://pyiso.readthedocs.org/

PyPI: https://pypi.python.org/pypi/pyiso/


Changelog
---------
* 0.2.21: Major feature: generation mix in NYISO. Bug fix: time zone handling in NYISO.
* 0.2.18: Minor change: enforce pandas version 0.17 or higher.
* 0.2.17: Minor change: Limit retries in `base.request`, and increase time between retries.
* 0.2.16: Major fix: PJM deprecated the data source that was used in previous releases. This release uses a new data source that has load and tie flows, but not wind. So PJM generation mix has been deprecated for the moment--hopefully it will return in a future release.
* 0.2.15: Minor changes: enforce pandas 0.16.2 and change NYISO index labelling to fix NYISO regression in some environments.
* 0.2.14: Major features: forecast load in ERCOT, MISO, NYISO, PJM; forecast genmix in MISO; forecast trade in MISO. Minor changes: fixed DST bug in BPA, refactored several to better use pandas.
* 0.2.13: Minor bugfix: Better able to find recent data in NVEnergy.
* 0.2.12: Major features: EU support, support for throttling in CAISO. Minor upgrades: Improve docs, dedup logging messages.
* 0.2.11: Minor bugfixes. Also, made a backward-incompatible change to the data structure that's returned from `get_ancillary_services` in CAISO.
* 0.2.10: Fixed bug in CAISO LMP DAM.
* 0.2.9: Added load and generation mix for SVERI (AZPS, DEAA, ELE, HGMA, IID, GRIF, PNM, SRP, TEPC, WALC)
* 0.2.8: Added lmp in ISONE. Also, made a backward-incompatible change to the data structure that's returned from `get_lmp` in CAISO.
* 0.2.7: Added load and trade in Nevada Energy (NEVP and SPPC)
* 0.2.1: Added load (real-time 5-minute and hourly forecast) in ISONE
* 0.2.0: Maintained Python 2.7 support and added Python 3.4! Thanks @emunsing
