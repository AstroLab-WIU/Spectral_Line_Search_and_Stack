

# Installation and Configuration 

1. Download source files using the git command:

```
git clone https://github.com/AstroLab-WIU/Spectral_Line_Search_and_Stack.git
```

This will create the folder Spectral Line Search and Stack containing the Python (.py) scripts and other necessary files to execute the routine.

 
2. Open and edit the file parameters.txt. This file contains multiple parameters that CASA requries to execute each task. The variables are separated in the following sections:

* Path:
  - path to MS = Reference path of where the visibility (*.ms) files are located.

 
* Visibilities
   - vis = list of calibrated visibilities: could be one or multiple visibility files, e.g., [?vis1.ms?,?vis2.ms?, ...].
   - field = ALL or index (ID number) or field/source name, e.g., 2, or ?sourceA?. List of sources can be obtained with the CASA task listobs.

* Frequency Files
   - molecule = The name of the file that contains the frequencies of interest, e.g., CH3OH.tsv. Frequency files are  in the ./Species/ folder.
   - upper energy = Upper limit of the energy level measured in Kelvin (i.e., maximum El/kB) to search for lines with energy levels below this limit.

* Control Parameters

  - generate cubes = True, the script will find the SPWs that contain rest frequencies listed in the Frequency File, and create cubes accordingly. 
  - stack cubes = True, the script will run the stacking algorithm. In this case, the cubes from different spectral lines will be stacked to increase sensitivity
* Cube_Gen
  - Parameters of tclean for imaging. [CASA reference](https://casadocs.readthedocs.io/en/stable/api/tt/casatasks.imaging.tclean.html)
  

# Execution
3. Execute script in a IPython CASA (version 5.1 or higher) terminal: 
```
execfile('main_script.py')
```

4. The script will run multiple routines, execution time will depend on size of the file and workstation capabilities



### Imaging generation

The program will use the default settings for each source that you selected. The output of the images will be located at /Output/'Source Name'


# Splatalogue - Files
[Splatalogue](https://www.cv.nrao.edu/php/splat/index.php)

After the initial variables, you must download the files from Splatalogue and save them in the 'Species' folder. The file must be download in '.tsv' format following these two parameters. 
Field Separator: Tab

Range: All Records
