import numpy as np
import glob,os

file_name = 'Images_CASA_Stats.txt'
image_list = [['source','image','b_minor (arcsec)','b_major (arcsec)','b_angle (rad)','rms (Jy / Beam)','mean (Jy / Beam)']] #File_Header

def calc_beam_stats(folder):
    try:
        images=glob.glob(folder+'/*.image')
        print(len(images))
        for img in images:
            head = imhead(img,verbose=True,mode='list')
            beam_minor = head['beamminor']['value']
            beam_major = head['beammajor']['value']
            beam_angle = head['beampa']['value']
            folder_path = os.path.basename(os.path.dirname(folder +'/'))
            image_path = os.path.basename(os.path.dirname(img + '/'))

            stat=imstat(img ,box='50,50,300,300')
            rms_value = stat['rms'][0]
            mean_value = stat['mean'][0]
            image_list.append([folder_path,image_path,beam_minor,beam_major,beam_angle,rms_value,mean_value])
    except OSError as error:
        pass
    print(image_list)
    beam_array = np.array(image_list)
    np.savetxt(file_name,beam_array,delimiter=",",fmt='%s')
    print('File created correctly %s' % file_name)

def calc_rms_stats(folder):
    '''
    Calculate the rms of a the images of a given folder. 
    '''
    
