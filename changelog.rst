Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

[0.2.0] 2023-03-05
------------------

Added
^^^^^

- ``PiRationalFormatter`` that prints rational multiples of pi.
- ``zero_props`` and ``pole_props`` argument to ``plane_plots.*plane*``-functions
  that allows more detailed styling of pole/zero markers.
- ``multiplicity_props`` argument to ``plane_plots.*plane*``-functions that allows
  styling of pole/zero multiplicity texts.
- This changelog.

Fixed
^^^^^

- ``freq_unit`` was not propagated properly in all ``freq_plots.zfreq*`` functions and
  ``style``-combinations.

Changed
^^^^^^^

- Change to src-layout

[0.1.1] - 2023-02-27
--------------------

Fixed
^^^^^

- Smaller wheel.
- Fix issue with adjustText 0.8, where the text coordinates were not correctly extracted
  for some situations.

[0.1.0] - 2023-02-26
--------------------

Initial version

- `unreleased <https://github.com/oscargus/mplsignal/compare/v0.1.1...HEAD>`_
- `0.1.1 <https://github.com/oscargus/mplsignal/compare/v0.1.0...v0.1.1>`_
- `0.1.0 <https://github.com/oscargus/mplsignal/releases/tag/v0.1.0>`_
