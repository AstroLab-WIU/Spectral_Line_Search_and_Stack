import numpy as np
import glob
import os
import csv
import imp
import sys
sys.path.append(os.getcwd())
import stacking_module

mylines =[]
parameters_dict = {}                            
with open ('parameters.txt', 'r') as myfile:
    for myline in myfile:
        if myline.startswith('##'):
            dict_temp ={}
            mylines =[]
            group = myline.replace('#','').rstrip('\n').strip(' ')
            parameters_dict[group]={}

        elif not myline.startswith('#'):
            print(myline.strip('\n'))
            key,val = myline.strip('\n').replace(' ', '').split('=')
            if "[" in val:
                ls = val.strip('[]').replace('"', '').replace(' ', '').split(',')
                val =ls
            if val =="True" or val == "False":
                val = bool(val)
            mylines.append(( key,val ))
            parameters_dict[group].update(mylines )

print(parameters_dict)

####### Variables ####### 

#band=parameters_dict['path']['band']
path=parameters_dict['path']['path_to_MS'] 
f =  parameters_dict['visibilities']['field']


path_analysis=os.getcwd()+'/'
out_path=path_analysis+'/Output/'
species_path=path_analysis+'/Species'

sources= parameters_dict['visibilities']['vis']

try:
    os.mkdir(out_path)
    os.mkdir(species_path)
except OSError:
    print ("\nCreation of the directory %s failed is already created" %out_path )
    print ("\nCreation of the directory %s failed is already created" %species_path )
else:  
    print ("\nSuccessfully created the directory %s " %out_path)  
    print ("\nSuccessfully created the directory %s " % species_path)

print('Visibilities to explorer: {}'.format(sources))
#Generate listobs for the data using CASA
def list(mySDM,new_path):
    default(listobs)
    global vis ,verbose,overwrite,listfile
    vis=path+mySDM
    verbose=False
    listfile=new_path+'/log.txt'
    overwrite=True
    inp(listobs)
    go(listobs)


#Creating the SPW's array
def lines(new_path):
    with open(new_path+"/log.txt",'r') as log_file:
        line=log_file.readline()
        cnt=1
        while line:
            #print("Line {}: {}".format(cnt, line.strip()))
            if 'SpwID' in line: 
                spw_line=cnt
            if 'Antennas:' in line:
                anten=cnt
            if 'Fields' in line:
                field=cnt+1
            if 'Spectral Windows' in line:
                spw=cnt
                print( spw)
            line = log_file.readline()
            cnt += 1
        foot2=cnt-spw
        footer=cnt-anten        
        return spw_line,footer,field,foot2

def ploting(fields,temp,new_path):
    #Create the plotms and move to the Output folder
    global vis
    global xaxis
    global yaxis
    global field
    global spw
    global avgtime
    global avgbaseline
    global plotfile
    global expformat
    global overwrite
    global showgui
    for i in range(len(temp)):
        default(plotms)
        vis=path+mySDM
        xaxis = 'freq'       
        yaxis ='amp'       
        field =fields
        spw =str(i)
        avgtime ='1.0e10'        #  Average over time (blank = False, otherwise value in
        avgbaseline = True        #  Average over all baselines (mutually exclusive with
        plotfile=new_path+'/spw'+ str(i) +'.txt'
        expformat='txt'
        overwrite=True
        showgui=False
        inp(plotms)
        go(plotms)


def select_file():
    os.chdir(new_path)
    files = glob.glob("*.txt")
    os.chdir(path_analysis+'Species/')
    species=glob.glob("*")
    if len(species)==0:
        return
        print("You need a file from Splatalogue DataBase")
    for specie in species:
        print(specie)
    os.chdir(path_analysis)
    Select=raw_input("\nWrite the name of the Species file to review: ") 
    return Select

def create_freq(sel_mole, energy_cut,new_path):
    spw_found=[]
    os.chdir(new_path)
    files = glob.glob("*.txt")
    os.chdir(path_analysis)
    Select=sel_mole
    print(files)
    for spw in files:  # Extract the frequencies
         if os.stat(new_path+'/'+spw).st_size > 100:
             i=np.genfromtxt(new_path+'/'+spw,comments='#',usecols=(0))
             min_v=np.amin(i)
             max_v=np.amax(i)
             with open(path_analysis+'Species/'+Select) as Species_file:
                 Reader=csv.reader(Species_file,delimiter='\t')
                 next(Reader)#Skip the Blank line
                 next(Reader)#Skip the Header
                 for row in Reader:
                     rest_freq= float(row[2].split(',')[0])
                     specie=row[0]
                     quatum_trans=row[3]
                     energy=float(row[7])
                     if min_v <= rest_freq <= max_v and energy<=energy_cut :
                         print("SPW: {} Quatum {} Rest_freq: {} GHz Energy {} K".format(spw,quatum_trans,rest_freq,energy))
                         spw_found.append([spw,min,max,1,specie,quatum_trans,rest_freq])
                         spw_n=spw[3:-4]
                         print("&{0:s}&\t&{1:s}\t &{2:2.6f}&\t {3:3.3f}".format(specie,spw_n,rest_freq,energy))
         else:
             pass
    
    os.chdir(path_analysis)
    return spw_found

def create_img(spws,fields,mySDM,new_path):
    #Global Variables
    images_array=[]
    global vis
    global imagename
    global datacolumn
    global field
    global spw
    global specmode
    #global width 
    global restfreq
    #global start 
    global outframe 
    global nchan 
    global threshold  
    global imsize
    global cell
    global niter  
    global deconvolver
    global weighting 
    global robust
    global pbcor  
    global pblimit 
    global restoringbeam 
    global chanchunks  
    global gridder  
    global interactive
    global phasecenter
    global stokes
    for i in range(len(spws)):
        spw_to_do= str(spws[i][0])[:-4] +'-' +spws[i][4]+'-'+spws[i][5]
        spw_to_do=spw_to_do.replace('&','')
        spw_to_do=spw_to_do.replace(';','')
        spw_to_do=spw_to_do.replace('=','')
        spw_to_do=spw_to_do.replace(',','_')
        spw_to_do=spw_to_do.replace('/','_')
        spw_number=str(spws[i][0])[3:-4]
        spw_rest_freq=str( spws[i][6])+ ' GHz' 
        images_array.append(spw_to_do + '.image') # Create the array with the SPW to stacking
        default(tclean)
        vis=path+mySDM
        imagename=new_path+spw_to_do 
        datacolumn=parameters_dict['cube_gen']['datacolumn'] #'corrected'
       
        spw=spw_number
        
        field=fields
        specmode=parameters_dict['cube_gen']['specmode']#'cube'  
        #width='30km/s' 
        restfreq = spw_rest_freq
        #start='550km/s' 
        #outframe='LSRK' 
        threshold= parameters_dict['cube_gen']['threshold']  #'0.5mJy' # 0.4 '0.05mJy'  
        imsize= [int(parameters_dict['cube_gen']['imsize'])] # [1000]
        cell= parameters_dict['cube_gen']['cell'] #['0.035arcsec']  
        niter=  int(parameters_dict['cube_gen']['niter'])
        deconvolver=parameters_dict['cube_gen']['deconvolver']#'hogbom'  
        weighting= parameters_dict['cube_gen']['weighting'].strip() #'briggs' 
        robust=float(parameters_dict['cube_gen']['robust']) # 0.5 
        pbcor=bool(parameters_dict['cube_gen']['pbcor']) # True  
        pblimit=float(parameters_dict['cube_gen']['pblimit']) #0.2  
        restoringbeam=parameters_dict['cube_gen']['restoringbeam'] #'common' 
        interactive= False
        stokes=parameters_dict['cube_gen']['stokes'] #'I'
        #phasecenter =parameters_dict['cube_gen']['phasecenter']
        #'J2000 19h29m33s +18d00m54s'
        #'J2000 19:28:55.58 17.52.03.11'
        #'J2000 19:29:33.52 18.00.54.20'
        #'J2000 18h21m09s -14d31m48s'
        #'J2000 19h29m33s +18d00m54s'
        #'J2000 19h29m33s +18d00m54s'
        # 19282 'J2000 19h30m23s +18d20m26.0s'
        #go_img= 'N'#raw_input("Create image Y/N: ")
        #if '9(2)-9' in spw_to_do:
        if not os.path.exists(new_path+spw_to_do+'.image'):
            print("Did not Found -> Start Image")
            inp(tclean)
            print("Image Created {0:} out of {1:}".format(i,len(spws)))
            go(tclean)
            max_min(imagename+'.image')
        else:
            max_min(imagename+'.image')
            print("Exist")

    return images_array
   
def max_min(image):
    global imagename
    global moments
    global outfile
    if not os.path.exists(image+".moments.maximum"):
        default(immoments)
        imagename=image
        moments=[8,10]
        outfile=image+'.moments'
        inp(immoments)
        go(immoments)
        print("Min and Max done")
    else:
        print("Min and Max done")
    
    
#####################################################################################################
global new_path

def main():
    global mySDM
    
    for i in sources:
        mySDM = i
        mySDM_Folder=str(mySDM[0:-3])  

        #Create Folder for the plotms Outputs
        
        try:  
            new_path=path_analysis+'Output/'+mySDM_Folder
            os.mkdir(new_path)
        except OSError:  
            print ("Creation of the directory %s failed is already created" % new_path)
        else:  
            print ("Successfully created the directory %s " % new_path)

        #Creation of the listobs
        if not os.path.exists(new_path+'/log.txt'):
            list(mySDM,new_path)
    
        header,foot,f_header,f_foot=lines(new_path)
        
        temp=np.genfromtxt(new_path+"/log.txt",skip_header=header,skip_footer=foot,usecols=(0))

        print('Spw to observed ', temp)
        
        #Create freq vs amp txt files

        plots=glob.glob(new_path+'/*.txt*')
        if len(plots)<2:
            ploting(f,temp,new_path)

        #Function to find acording to the species

        sel_file= parameters_dict['Frequency_File']['molecule']  #select_file() #'CH3OH.tsv'#'OH.tsv'# 'OH.tsv' 
        energy_cut = float(parameters_dict['Frequency_File']['upper_energy'])

        array_spws=create_freq(sel_file,energy_cut,new_path)
        if array_spws==[]:
           print("The MS analyzed does not contain any match with the file" ,sel_file)
           next
        #Creates a new folder for cubes that are going to be created. 

        try:  
            tc_path=path_analysis+'Output/'+mySDM_Folder+'/'+sel_file[:-4]+'/'
            os.mkdir(tc_path)
        except OSError:
            print ("Creation of the directory %s failed is already created" % tc_path)
        else:  
            print ("Successfully created the directory %s " % tc_path)


        #Create images of the previous findings 

        images_cube=create_img(array_spws,f,mySDM,tc_path)

        #Stacking detected lines

        if parameters_dict['Stacking']['stack_boolean']==True:
            temp=[]
            temp2=[]
            for cube in images_cube:
                stats=imstat(imagename=tc_path+cube,  box='50,50,300,300', axes=[0,1])
                if len(stats['rms'])>256:
                    images_cube.remove(cube)
                    print('Removed from the stacking %s' %cube)
                else: 
                    temp.append(cube[cube.find('(')+1:cube.find(')')])
                    #temp.append(int(filter(str.isdigit,cube))) 
            temp.sort(reverse=True)
            temp=[str(x) for x in temp]
            for n in temp:
                for name in images_cube:
                    if n in name:
                        temp2.append(name)
            images_cube=temp2
            print( images_cube)
            images_cube.append(tc_path)
            
            #Stacking Cubes
            execfile("stacking_module.py",globals())
            #print images_cube
            stack(images_cube)


if __name__ == '__main__':
    main()

