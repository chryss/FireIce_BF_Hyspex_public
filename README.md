# Alaska EPSCoR Fire & Ice Boreal Forest team - HySpex Processing

This repository is intended to be used as the initial step to set up a new HySpex processing environment for HySpex data acquired during the EPSCoR Fire & Ice aerial data acquisition campaigns. It is currently (February 2020) being developed primarily within the Boreal Forests team, and intends to serve users beyond this team, as demand arises.

The scripts are written to work on the EPSCoR Windows processing system. But if processing takes place elsewhere, changes or additions should be made to work on all systems in use.

Currently, this is work under constant development. Feel free to check with Chris Waigl (cwaigl@alaska.edu) if you have any questions or suggestions. Collaborators are encouraged.

How to use the repository:

1. The first step when starting a new HySpex processing task (ie, new data has been acquired) is to clone (or download/unzip) the repository. 
2. Under `Conda_environemnt` you will find an `environment.yml` file to create a Python environment using the Conda packet manager (installed as Anaconda or Miniconda on the EPSCoR systems), as explained here:  https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file . If you don't use Conda: The scripts require Python 3.6 or higher, and you'll have to manage external libraries yourself. 
3. Under `Jupyter_notebooks` you will find a growing collection of scripts to automate tasks that can be automated
4. Under `NEO_Software` you will find the latest version of NEO HySpex NAV and RAD, as well as a settings file for NAV. It is strongly suggested that every data processing environment has its own copy of the software and the settings file. Running the software will overwrite files, and keeping a reference of the exact software used for processing is good practice for reproducibility.
