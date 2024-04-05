# PERG Viewer
This software application handles the reading and pre-processing of the CSV files from the "The PERG-IOBA Database", a repository of pattern electroretinograms. This database can denoise the signal using wavelet transform based on the input level of decomposition.

This is the graphical user interface of PERG Viewer.
![PERG Viewer graphical interface](https://github.com/arrecto/PERGViewer/blob/main/PERG_Viewer_interface.png)
## Dependencies
The application is written in Python and heavily used **PySimpleGUI** library for the graphical user interface and **PyWavelet** for the wavelet decomposition. It also uses **Pandas** extensive dataframe processing functions.
