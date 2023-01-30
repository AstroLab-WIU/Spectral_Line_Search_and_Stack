

# Installation and Configuration 

**This version of the program runs in python 2.X and CASA 5.1 or higher**

The program will be updated for python 3.X and CASA 6.X

Extract the files in the path. 

Before running the python program we need to define all the variables inside the python script. 

Open the **parameters.txt** and edit each individual variable.

The variables are separete in the following sections: 

* Path:
  - path_to_MS = Reference path of where the *ms* files are storage.
 
* Visibilities

  - vis = list of visibilities 1 or multiple visibilities e.g [vis1,vis2...] 
  
  - field =  index of the field from (0,1,2....n)
   
* Frequency Files
    - molecule = Type the name file with the frequencies
    - Upper limit of the energy level measure in Kelvin 
 

# Execution

The next step will be run the main script from casa interface using the command

```
execfile('main_script.py')
```

### Imaging generation

The program will use the default  settings for each source that you selected. The output of the images will be located at /Output/'Source Name'


# Splatalogue - Files
[Splatalogue](https://www.cv.nrao.edu/php/splat/index.php)

After the initial variables you must download the files from Splatalogue and saved it in the 'Species' folder. The file must be download in '.tsv' format following the this two parameters. 
Field Separator: Tab

Range: All Records
