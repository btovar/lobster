Installation
============

.. warning::
   Lobster will need python 3.10 or greater.  
   CMSSW version `CMSSW_10_6_26` or above are recommended to
   use.


Dependencies
~~~~~~~~~~~~

* Setuptools

  Install the python package manager ``pip``, with::

    wget -O - https://bootstrap.pypa.io/get-pip.py|python - --user

  This installs pip in your `~/.local` directory. In order to access these
  executables, add them to your path with::

    export PATH=$HOME/.local/bin:$PATH

* Conda
  
  Install the conda package manager with::

    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh

  Follow the instructions to install conda.  After installation, you will need to
  source the conda environment with::

    source ~/.bashrc

Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~

Lobster can be installed from a local git checkout, which will allow for
easy modification of the source::

    git clone https://github.com/NDCMS/lobster.git
    cd lobster
    conda env create -f lobster_env.yaml -n lobster
    pip install -e .

Confirm Installation
~~~~~~~~~~~~~~~~~~~~

Check your python version after running `conda env create -f lobster_env.yaml -n lobster`::

    $ python -V
    Python 3.10.14


Setup
-----

To elimate conflicts with other installed packages, before running lobster do::
  
    unset PYTHONPATH
    unset PERL5LIB

You will need to use lobster in a `virtualenv`, which is used to keep
all dependencies of lobster within one directory and not interfere with
other python packages and their dependencies (e.g. CRAB3)::

    conda env create -f lobster_env.yaml -n lobster

And activate the `virtualenv`.  This step has to be done every time lobster
is run, to set the right paths for dependencies::

    conda activate lobster

To exit the `virtualenv`, use::

    conda deactivate

.. _Notre Dame Cooperative Computing Lab: http://www3.nd.edu/~ccl/software/download.shtml

.. rubric:: Footnotes
