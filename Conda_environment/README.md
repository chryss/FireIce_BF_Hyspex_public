# Conda environment setup

How to use the `remotesensing_conda.yml` file: 

Once Anaconda (or, for a more lightweight install, Miniconda) is installed, you can use the following commands at the Anaconda Prompt. 

```
conda config --set pip_interop_enabled True
conda env create -f remotesensing_conda.yml
```

This will create a new Conda environment with Python 3.7 and some basic geospatial raster and vector processing libraries, called `hyspex_proc`. If you prefer a different name, just edit the `remotesensing_conda.yml` file. It's pretty self-explanatory.

For reference:
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file 

How to install Miniconda: https://docs.conda.io/en/latest/miniconda.html 