# Third-party notices

## Swiss Ephemeris / pyswisseph

Milestone 1 uses `pyswisseph`, the Python binding to Swiss Ephemeris, as the
astronomical calculation foundation. Swiss Ephemeris is dual-licensed under
the GNU Affero General Public License or the Swiss Ephemeris Professional
Licence. This repository selects the free AGPL option. The binding and
ephemeris data remain subject to their upstream notices and licence terms.

Upstream: <https://www.astro.com/swisseph/>  
Python package: <https://pypi.org/project/pyswisseph/>

## Runtime dependencies

The runtime dependency list is declared in `pyproject.toml`. Each dependency
retains its own copyright and licence. Dependency metadata should be reviewed
before every release.

## Development-only validation oracle: PyJHora

The optional `validation` dependency group pins PyJHora 4.8.7 (AGPL-3.0) and
its required non-UI dependencies. It is used only to generate and verify
independent expected values for Shodashavarga tests. No PyJHora source is
distributed or copied into this repository.

## Jagannatha Hora comparison

Jagannatha Hora 8.0 by P.V.R. Narasimha Rao was used only as an attempted
external validation reference. It is not bundled, imported, linked at runtime,
or required by this project. The official publisher page and installer were
checked during release preparation; no automated report was produced in the
available environment.

## Lockfile and licence review

`requirements-lock.txt` records the Python 3.12 validation environment for
reproducible review. Review dependency copyright and licence metadata before
redistribution. The project itself remains AGPL-3.0-or-later, and Swiss
Ephemeris is used under its free AGPL option.
