# Brieven van Hooft - Notebook

This is a notebook that provides access to the linguistic and socio-linguistic
annotations that were added to the letters by P.C van Hooft in an annotation
project in 2017 by Marjo van Koppen and Marijn Schraagen. The letters come from
*"De briefwisseling van Pieter Corneliszoon Hooft, edited by H.W van Tricht
e.a.,"*, as published by the [DBNL](https://www.dbnl.org) in the following
three parts:

* [Part 1](https://www.dbnl.org/tekst/hoof001hwva02_01/)
* [Part 2](https://www.dbnl.org/tekst/hoof001hwva03_01/)
* [Part 3](https://www.dbnl.org/tekst/hoof001hwva04_01/)

License information for these works can be found
[here](https://www.dbnl.org/titels/gebruiksvoorwaarden.php?id=hoof001hwva03).
We did not receive the rights to publish the editorial parts of the texts that
are not from the 17th century. They will still be available in this notebook as
they can be downloaded from DBNL directly, but republishing them is not
permitted unfortunately. The notebook's code itself is under the GNU General Public License v3.

The annotations were initially published in a combination of FoLiA XML and
other stand-off formats. In 2024, they have been re-aligned with the original
DBNL sources and published as a [STAM](https://annotation.github.io/stam)
model. You can also inspect the full [pipeline that produced this
model](https://github.com/knaw-huc/brieven-van-hooft-pipeline).

This [Marimo](https://marimo.io) notebook provides search and visualisation
functionality on this STAM model. We will guide you through several examples.
All code in this notebook can be executed, and if needed, modified to your
liking.

## Installation & Usage

Make sure you have an up-to-date Python installation on your system then, from
the command line, do:

1. Clone this git repository: `git clone https://github.com/knaw-huc/brieven-van-hooft-notebook`
2. Make a virtual environment: `python3 -m venv env`
3. Activate the virtual environment: `source env/bin/activate` (on UNIX systems), on Windows PowerShell do `env\bin\Activate.ps1` instead).
4. Install all dependencies: `python3 -m pip install -r requirements.txt`. 
5. Run the notebook: `marimo run brieven-van-hooft-notebook.py`

The notebook will open in your default web-browser and automatically run. Note
that it runs locally, only the models and texts will be automatically downloaded once on
first run. This may take a while.

Steps 3 and 5 need to be repeated whenever you want to open the notebook again.
The rest only needs to be done once.
