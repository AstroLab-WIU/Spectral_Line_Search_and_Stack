import os
import glob
import numpy as np
import csv
import sys


def chans_rm_continuum(cube_input,new_path):
    #Stats for each cube
    channels_use=[]
    chans=0
    last=''
    for cube in cube_input:
        array_channel=[]
        stats=imstat(imagename=new_path+cube,  box='50,50,300,300', axes=[0,1])
        a =np.array(stats['rms'])
        b =np.array(stats['flux'])
        c=np.array(stats['mean'])
        rms_mean=a.mean()
        rms_std=a.std()
        flux_mean=b.mean()
        flux_std= b.std()
        lower_lim=rms_mean-rms_std
        upper_lim=rms_mean+rms_std
        channel_conti=''
        num=len(stats['rms'])
        channel_join = ''
        for i in range(num):
            chan_stats = stats['rms'][i]
            if chan_stats == 0.0:
                pass
                chans=i+1
            else:
                #print("Lower Lim {0:2.3e} , Upper Lim {1:2.3e} RMS {2:2.3e}".format(lower_lim,upper_lim,chan_stats))
                if chan_stats > lower_lim and chan_stats < upper_lim:
                    channs_end=i-1
                    #if chans<channs_end:
                    channel_conti = str(i) #EA
                    #print( channel_conti)
                    #print str(i)+" Out limits" 
                    chans=i+1
                    array_channel.append(channel_conti)
                    channel_join=','.join(array_channel)
        channels_use.append(channel_join)       
    return channels_use

def stack(cube_input,new_path):                    
    if os.path.exists(new_path + "stacked_cube.image"):
        return "Already Stacked"
    channels =chans_rm_continuum(cube_input,new_path)

    ## Remove continuum: this is better if done in the UV plane before tclean
    cube =[]
    for i in range(len(cube_input)):
        spw_to=cube_input[i]
        if not os.path.exists(new_path+spw_to+'.NC'):
            linefile = new_path +cube_input[i]+'.NC'
            imcontsub(
            imagename = new_path+cube_input[i]
            ,linefile = new_path +cube_input[i]+'.NC'
            ,contfile = new_path+cube_input[i]+'.C'            
            ,chans = channels[i] #this is cube dependent
            #fitorder=1
            )
            
            cube.append(linefile)
        else:
            linefile = new_path+cube_input[i]+'.NC' 
            cube.append(linefile) 
    if len(cube) == 1:
        raise SystemExit

    ## Regrid spectrum, to be able to average them.

    cube_to_stack = [cube[0]]
    for i in range(len(cube)-1):
        output = cube[i+1] +'.imregrid'
        imregrid(
        imagename = cube[i+1]
        ,template = cube[0]
        ,output =  cube[i+1] +'.imregrid'
        #axes=3
        ,asvelocity = True
        ,overwrite = True)
        cube_to_stack.append(output)

    ## Get RMS of the cubes
    imstat_cube = []
    for i in range(len(cube_to_stack)):
        imstat_cube.append(imstat(cube_to_stack[i], box='50,50,300,300'))
        a =np.array(imstat_cube[i]['rms'])
                
    ## Define weights for stacking:
    weight_total = sum(1.0/item['rms']**2 for item in imstat_cube)
    print('Weight normalization factor: ',weight_total)
    weights= []
    for i in range(len(cube)):
        weights.append(1.0/imstat_cube[i]['rms'][0]**2)
    weights = weights/weight_total
    print('Weights: ',weights)
    
    ## Creates the new stacked cube using the previous weights

    stacked_image = new_path+'stacked_cube.image'

    ex = '(IM0*'+str(weights[0]) 
    for i in range(len(weights)-1):
        ex = ex + ' + IM'+str(i+1)+'*'+str(weights[i+1])
    ex = ex + ')'

    
    immath(
    imagename = cube_to_stack
    ,mode = 'evalexpr'
    ,outfile = stacked_image
    ,expr = ex )

    ## Print the RMS of all the cubes
    imstat_cube.append(imstat(new_path+'stacked_cube.image', box='50,50,300,300'))
    cube_to_stack.append("stacked_cube.image")
    for i in range(len(imstat_cube)):
        a =np.array(imstat_cube[i]['rms'])
        print('RMS of  '+cube_to_stack[i]+' is %1.2e Jy/b' % a.mean())
'''

def export_image(img_name):
    img=''
    path_conti='/path/to/continuum/sources/*'
    select='/path/to/cubes/*'
    levels = []
    unit = 1e-6
    while True:
        folder=glob.glob(path_conti)
        for i in folder:
            print( i)
        select= raw_input('\nSelect Folder: ')
        if '.image' in select:
            img=select
            break
        else:
            path_conti=select+'/*'

    if img=='':
        pass
    else:
        image='stacked_cube.image'
        imview(raster={'file':new_path+image,'colorwedge':True} ,
               contour={'file': img, 'levels': levels , 'unit':unit}) 


def sub_images():
    os.chdir(new_path)
    files = glob.glob("*.image")
    for f in files:
        if "image." not in f:
            print (f)
            stats=imstat(imagename=new_path+f,  box='50,50,300,300' ,axes=[0,1])
            a =np.array(stats['rms'])
            num_chans=len(a)
            
            imsubimage(
                imagename=new_path+f,outfile=new_path+f+'.sub',
                chans='1~'+str(num_chans-1),
                overwrite=True )
            
    os.chdir(path_analysis)

def view_img(image_name):
    global raster
    global contour
    level=[]
    ### Enter the path of your csv/txt file with levels and rms
    csv_file_path = ''
    with open(csv_file_path) as image_file:
        Reader=csv.reader(image_file,delimiter=',')
        next(Reader)#Skip the header
        for row in Reader:
            if row[1]==image_name:
                cont=row[2]
                levels2=row[3].split(",")
                for i in levels2:
                    if '[' in i:
                        
                        level.append(float(i[1:]))
                    if ']' in i:
                        
                        level.append(float(i[:-1]))
                    elif '[' not in i and ']' not in i:
                        level.append(float(i))
                uni=float(row[4])
    img='/path/of/stacked_cube.image'
    imview(
        raster={'file':img,'colorwedge':True} , 
        contour={'file':cont, 'levels': level , 'unit':uni})


def sub_stacked(image_name):
    global imagename
    global outfile
    global region
    global overwrite
    stack_folder='/path/to/stacked_images/'
    os.chdir(stack_folder)
    imsubimage(
        imagename=image_name+'_stacked_cube.image',
        outfile=imagename+'.sub',
        region='regions/'+imagename+'.reg',
        overwrite=True )
    os.chdir(path_analysis)
'''
