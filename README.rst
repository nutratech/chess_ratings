****************
 Chess rankings
****************

.. image:: https://github.com/nutratech/chess_ratings/actions/workflows/test.yml/badge.svg
  :target: https://github.com/nutratech/chess_ratings/actions/workflows/test.yml
  :alt: Test status unknown

.. image:: https://github.com/nutratech/chess_ratings/actions/workflows/install-linux.yml/badge.svg
  :target: https://github.com/nutratech/chess_ratings/actions/workflows/install-linux.yml
  :alt: Install status unknown


Link to the Google Sheet
########################

https://docs.google.com/spreadsheets/d/14N1cdQFe0Rzbi8x1VUQ7GTCQkv6Kej6Vnh079ZWmd24/edit#gid=2029955395



Setup (Linux)
#############

Install ``venv``.

.. code-block:: bash

  sudo apt install python3-venv

Set up ``venv``. Install ``pip`` dependencies and ``glicko2`` submodule.

.. code-block:: bash

  make init deps



Running
#######

You can rate and download with this.

``./cr rank``

To download separately use this.

``./cr fetch``

To skip downloading (assume cached) AND print match ups & graphs, do this.

``./cr rank -smg``


Filtering Players
~~~~~~~~~~~~~~~~~

**TODO:** Filter by people who showed up, or aggregate by club?
