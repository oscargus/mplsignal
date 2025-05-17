Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

Added
^^^^^

- A logotype.
- A label will automatically be added to all ``freq*``-plots that will show up when
  using a legend. These are "Magnitude", "Phase", and "Group delay". If you pass a label,
  this will not happen.
- ``style='twin'`` now plots lines with different colors from the color cycle to
  distinguish the two lines. The same holds for :func:`mplsignal.scipyplot.freqz_twin`,
  which also adds a legend.
- Code coverage at CodeCov.
- :func:`mplsignal.scipyplot.freqz_tristacked` for plotting magnitude, phase, and group
  delay in a single plot.
- BREAKING: argument *align_ylabels* to all ``freq*``-plots which is ``True`` by default.
- Initial typing information.

Changed
^^^^^^^

- BREAKING: The *only_name_when_one* argument to :class:`.FactorFormatter` was replaced with
  *name_on_all_numbers*, so that, e.g., the degree sign is always shown.
- BREAKING: All functions in :mod:`mplsignal.scipyplot` now use a constrained layout. This
  will in general make the plot clearer, although at the expense of less margin.
- Minimum Python version is increased to 3.10.
- Minimum adjustText version is set to 1.3.
- Minimum Matplotlib version is increased to 3.9.

Fixed
^^^^^

- ``freq_unit`` was not propagated properly in all ``freq_plots.zfreq*`` functions and
  ``style``-combinations.
- The ``adjust`` argument to the ``*plane`` functions is removed as it is not supported by newer versions of adjustText.

[0.2.0] - 2023-03-05
--------------------

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

- `unreleased <https://github.com/oscargus/mplsignal/compare/v0.2.0...HEAD>`_
- `0.2.0 <https://github.com/oscargus/mplsignal/compare/v0.1.1...v0.2.0>`_
- `0.1.1 <https://github.com/oscargus/mplsignal/compare/v0.1.0...v0.1.1>`_
- `0.1.0 <https://github.com/oscargus/mplsignal/releases/tag/v0.1.0>`_
