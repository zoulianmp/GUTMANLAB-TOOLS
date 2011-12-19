'''
Created on December 12, 2011
This program will search a file and determine project and experiment and determine 
if the patient has been uploaded to XNAT


@author: dgutman, aanghel
'''
import os,glob,re , sys
from pyxnat import Interface



PROJECT_ID="GTP_PROD"

def check_xnat_to_see_if_experiment_id_exists(SUBJECT_ID,EXPERIMENT_ID):
    '''This function will query an XNAT server and see if a project exists '''
    return xnat.select.project(PROJECT_ID).subject(SUBJECT_ID).experiment(EXPERIMENT_ID).exists()


# setup the connection
xnat= Interface(server='http://xnat.cci.emory.edu:8080/xnat',
                user='nbia',password='nbia',
                cachedir=os.path.join(os.path.expanduser('~'),'.store'))
 

project_object  = xnat.select.project(PROJECT_ID)


ROOT_DIRECTORY_TO_CHECK = '/SGE_RAID/RESSLER_TRAUMA_IMAGING/'
T1_IMAGE_LIST = glob.glob(ROOT_DIRECTORY_TO_CHECK+"RESIL*/structural_data/T1_flipped.nii.gz")


for individual_image in T1_IMAGE_LIST:
    print individual_image
    patient_id = re.search(r'Subject_(\d{2,5})',individual_image)
#   print patient_id.group(1)
# I now need to determine the experiment ID for this subject
    experiment_id_list_for_patient = project_object.subject(patient_id.group(1)).experiments().get()
    print len(experiment_id_list_for_patient)," experiments were found for patient ",patient_id.group(1)
    if ( not len(experiment_id_list_for_patient) == 1 ):
	print "This patient had more than one experiment and needs cleanup.."
    else:
#       print experiment_id_list_for_patient[0],"was the found experiment id"
	print "Will now determine if a T1_MPRAGE alraedy exists for this experiment ID..... ",experiment_id_list_for_patient[0],patient_id.group(1)
	expt_obj = project_object.subject(patient_id.group(1)).experiment(experiment_id_list_for_patient[0])
#	print expt_obj.get()
#	print experiment_id_list_for_patient[0]
	# nw I need to see if the resource NIFTI_GZ and the folder STRUCTURAL_IMAGES exists...
	print individual_image
	t1_file_name = patient_id.group(1)+"_T1_flipped.nii.gz"
	if( expt_obj.resource('NIFTI_GZ').file(t1_file_name).exists()):
	    print "Image",t1_file_name,"already exists for this subject"
	else:
	    expt_obj.resource('NIFTI_GZ').file(t1_file_name).put(individual_image,content='T1_STRUCT_FLIPPED',format='NIFTI_GZ',tags='T1_MPRAGE')	

#	scan_list_for_experiment = project_object.experiment(experiment_id_list_for_patient[0]).scans(constraints={'xnat:mrScanData/type':'t1_mprage_sag'}).get()
#	print scan_list_for_experiment


project_object  = xnat.select.project(PROJECT_ID)
subject_list_for_project = project_object.subjects().get('label')
print len(subject_list_for_project),"patients are in the ",PROJECT_ID," set"


# first iterate through subjects
#for current_patient in subject_list_for_project:
#    print current_patient
# now iterate through subjects with associated experiemnts
#    experiments_for_this_subject = project_object.subject(current_patient).experiments().get()
                               
