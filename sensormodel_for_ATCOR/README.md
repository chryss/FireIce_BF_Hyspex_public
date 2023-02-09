# Selection of ATCOR Sensor Model

The sensor model is installed in the `sensor` folder of the ATCOR-4 installation. For example, C:\ReSe_Software_Win64\atcor_4_v73\atcor_4\sensor . 

The model HySpex_super_Fovx2_BH was generated for manually stacked supercubes using bands 1-170 VNIR and 2-288 SWIR (old method).

The model HySpex_459_FoV2_Husky was generated for use with PARGE's "integrated processing" where 954 nm is selected as the cut-over frequency between VNIR and SWIR. This yields 459 spectral bands. 

# If you need to generate a new sensor model...

For example, you decide a different cut-over frequency with integrated processing, or want to atmospherically correct a different subset of bands, you need to generate a new `.wvl` file using Jupyter Notebook 09, and follow the instructions in the ATCOR-4 manual (and our old documentation). 