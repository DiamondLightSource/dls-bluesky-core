dls-bluesky-core
===========================

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

This module stores Bluesky functionality that may be common to multiple technique repositories within Diamond Light
Source.
The 'plans' package stores fully realised instruction sets that perform an experiment and capture data.
The 'plan_stubs' package stores modular partial instructions that may act as a building block for constructing 'plans'
or may be run to test operations without capturing data.
It should be assumed that a plan opens at least one 'Run', while a plan_stub does not contain a complete Run, although
it may open or close one.

============== ==============================================================
PyPI           ``pip install dls-bluesky-core``
Source code    https://github.com/DiamondLightSource/dls-bluesky-core
Documentation  https://DiamondLightSource.github.io/dls-bluesky-core
Releases       https://github.com/DiamondLightSource/dls-bluesky-core/releases
============== ==============================================================

The module built from this repository is intended to either act directly as a source of plans for an instance of
Bluesky directly by being a planFunctions source in the config of an instance.

.. code-block:: yaml

    worker:
      env:
        sources:
          - kind: planFunctions
            module: dls_bluesky_core.plans

Or else contributing towards the functionality required by a technique specific repository under the Diadmong

.. code-block:: python

    import dls_bluesky_core.plan_stubs  as cps

    def technique_specific_plan(*args, **kwargs):
        yield from cps.common_diamond_setup()


Or if it is a commandline tool then you might put some example commands here::

    $ python -m dls_bluesky_core --version

.. |code_ci| image:: https://github.com/DiamondLightSource/dls-bluesky-core/actions/workflows/code.yml/badge.svg?branch=main
    :target: https://github.com/DiamondLightSource/dls-bluesky-core/actions/workflows/code.yml
    :alt: Code CI

.. |docs_ci| image:: https://github.com/DiamondLightSource/dls-bluesky-core/actions/workflows/docs.yml/badge.svg?branch=main
    :target: https://github.com/DiamondLightSource/dls-bluesky-core/actions/workflows/docs.yml
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/DiamondLightSource/dls-bluesky-core/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/DiamondLightSource/dls-bluesky-core
    :alt: Test Coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/dls-bluesky-core.svg
    :target: https://pypi.org/project/dls-bluesky-core
    :alt: Latest PyPI version

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache License

..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

See https://DiamondLightSource.github.io/dls-bluesky-core for more detailed documentation.
