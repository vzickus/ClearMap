import sys
import numpy as np

if sys.version_info[0] >= 3:
	import PySimpleGUI as sg
else:
	import PySimpleGUI27 as sg

            ############################################################
            #----------------Data paths and processing tasks----------------#
            ############################################################

layout = [  [sg.Frame(layout=[
            # Path to base directory
			[sg.Text('Base directory ', size=(20, 1),
            tooltip="Directory to save all the results, usually containing the data for one sample"),
            sg.InputText(),
            sg.FolderBrowse(tooltip="Directory to save all the results, usually containing the data for one sample",
            key = "_baseDir_")],

            # Path to channel 1 (in this case cFos)
            [sg.Text('cFos directory ', size=(20, 1), tooltip="Directory where the raw cFos data is"),
            sg.InputText(), sg.FolderBrowse(tooltip="Directory where the raw cFos data is",
            key = "_channelOneDir_")],

            #Path to template/atlas file
            [sg.Text('Template file ', size=(20, 1),
            tooltip="Directory where the template file is (for mouse data, that would be the ABA annotated dataset)"),
            sg.InputText(),
            sg.FolderBrowse(tooltip="Directory where the template file is (for mouse data, that would be the ABA annotated dataset)",
            key = "_templateDir_")],

            #Path to directory containing Elastix parameter files
            [sg.Text('Elastix param dir ', size=(20, 1),
            tooltip="Directory where the Elastix parameters are"),
            sg.InputText(),
            sg.FolderBrowse(tooltip="Directory where the Elastix parameters are",
            key = "_elastixParams_")],

            [sg.Text('Processing tasks', font = ('Helvetica', 14))],

            [sg.Checkbox('Resample data', default=True,
            tooltip="Enable/disable data resampling", key = "_resampleOrNot_"),
            sg.Checkbox('Register to template', default=True,
            tooltip="Enable/disable registration to template",
            key = "_registerOrNot_"),

            sg.Checkbox('Detect cells', default=True,
            tooltip="Enable/disable cell detection", key = "_detectOrNot_"),
            sg.Checkbox('Check cells', default=False,
            tooltip="Enable/disable plotting detected cell centres." +
            "\nWARNING: use only on a subset of the data, otherwise you will resave the full-res image!",
            key = "_checkOrNot")]],

            title="Paths and processing tasks",title_color="red", font = ('Helvetica', 14), relief= "groove")],
            ############################################################
            #----------------Data parameters----------------#
            ############################################################
            [sg.Frame(layout=[

            [sg.Text('Raw data x,y,z resolution', font = ('Arial', 10, 'bold') , size=(30, 1), tooltip="Pixel sizes in microns" )],
            [sg.Text('X ', size=(1, 1), tooltip="Pixel width in microns"),sg.Spin( [i for i in range(0, 6) ] , initial_value= 4.8,
            key = '_resX_', size=(3, 1)),

            sg.Text('Y ', size=(1, 1), tooltip="Pixel height in microns"), sg.Spin( [i for i in range(0, 6)], initial_value= 4.8,
            key = '_resY_', size=(3, 1) ),

            sg.Text('Z step size ', size=(1, 1), tooltip="Z step in microns"), sg.Spin( [i for i in range(1, 26)], initial_value= 4.0,
            key = '_resZ_', size=(3, 1) )],

            [sg.Text('Raw data x,y,z range', font = ('Arial', 10, 'bold') , size=(30, 1), tooltip="Volumetric region of interest to be analysed. Used for tuning parameters.\nDoes not affect registration. Leave 'all' to process the whole stack." )],
            [sg.Text('Start X ', size=(8, 1), tooltip="pixels"),sg.Spin( [i for i in range(0, 2160) ] , initial_value= 'all',
            key = '_startX_', size=(5, 1)),

            sg.Text('Start Y ', size=(8, 1), tooltip="pixels"), sg.Spin( [i for i in range(0, 2560)], initial_value= 'all',
            key = '_startY_', size=(5, 1) ),

            sg.Text('Start Z ', size=(8, 1), tooltip="Z slice"), sg.Spin( [i for i in range(0, 3000)], initial_value= 'all',
            key = '_startZ_', size=(5, 1) )],

            [sg.Text('End X ', size=(8, 1), tooltip="pixels"),sg.Spin( [i for i in range(1, 2160) ] , initial_value= 'all',
            key = '_endX_', size=(5, 1)),

            sg.Text('End Y ', size=(8, 1), tooltip="pixels"), sg.Spin( [i for i in range(1, 2560)], initial_value= 'all',
            key = '_endY_', size=(5, 1) ),

            sg.Text('End Z ', size=(8, 1), tooltip="Z slice"), sg.Spin( [i for i in range(1, 3000)], initial_value= 'all',
            key = '_endZ_', size=(5, 1) )],


            [sg.Text('Resampled resolution', font = ('Arial', 10, 'bold') , size=(30, 1), tooltip="Resolution to which raw data will be resampled to (for registration, and heatmaps)" )],
            [sg.Text('X ', size=(1, 1), tooltip="Pixel width in microns"),sg.Spin( [i for i in range(10, 25) ] , initial_value= 16,
            key = '_resampleXres_', size=(3, 1)),

            sg.Text('Y ', size=(1, 1), tooltip="Pixel height in microns"), sg.Spin( [i for i in range(10, 25)], initial_value= 16,
            key = '_resampleYres_', size=(3, 1) ),

            sg.Text('Z step size ', size=(1, 1), tooltip="Z step in microns"), sg.Spin( [i for i in range(10, 25)], initial_value= 16,
            key = '_resmpleZres_', size=(3, 1) )],

            [sg.Text('Template x,y,z resolution', font = ('Arial', 10, 'bold'), size=(30, 1), tooltip="Pixel sizes in microns" )],
            [sg.Text('X ', size=(1, 1), tooltip="Pixel width in microns"),sg.Spin( [i for i in range(0, 100) ] , initial_value= 25,
            key = '_templateResX_'),

            sg.Text('Y ', size=(1, 1), tooltip="Pixel height in microns"), sg.Spin( [i for i in range(0, 100)], initial_value= 25,
            key = '_templateResY_' ),

            sg.Text('Z step size ', size=(1, 1), tooltip="Z step in microns"), sg.Spin( [i for i in range(1, 100)], initial_value= 25,
            key = '_templateResZ_' )],


            [sg.Text('Data orientation w.r.t. template', font = ('Arial', 10, 'bold'), size=(35, 1), tooltip="x,y,z order. (1,2,-3) would mean flip z axis.")],
            [sg.InputCombo(('(1,2,3)', '(-1,2,3)', '(1,2,-3)', '(1,-2,3)', '(-1,-2,3)', '(-1,-2,-3)', '(1,-2,-3)', '(-1,2,-3)' ), size=(10, 2),
            key = '_templateOrientation_') ]],

            title="Data parameters",title_color="red", font = ('Helvetica', 14), relief= "groove")],

            ############################################################
            #----------------Cell detection parameters----------------#
            ############################################################
            [sg.Frame(layout=[

            [sg.Text('Background removal parameters', font = ('Arial', 10, 'bold'), size=(45, 1), tooltip="size in pixels (x,y) for the structure element of the morphological opening")],
            [sg.Text('X ', size=(1, 1)), sg.Spin( [i for i in range(3, 50) ] , initial_value= 7,
            key = "_backRemX_"),

            sg.Text('Y ', size=(1, 1)), sg.Spin( [i for i in range(3, 50) ] , initial_value= 7,
            key = "_backRemY_"),

            sg.Checkbox('Save filtered images', default=False,
            tooltip="Enable/disable saving intermediate results. WARNING: use only when working with a small subset!",
            key = "_saveRemBackOrNot_"),],


            [sg.Text('Difference of Gaussians (DoG) parameters', font = ('Arial', 10, 'bold'), size=(45, 1), tooltip="size in pixels (x,y,z) for the structure element")],
            [sg.Checkbox('Use DoG', default=False, tooltip="Enable/disable this filter.",
            key = "_DogOrNot_"),
            sg.Text('X ', size=(1, 1)), sg.Spin( [i for i in range(3, 50) ] , initial_value= 7,
            key = "_DogX_"),

            sg.Text('Y ', size=(1, 1)), sg.Spin( [i for i in range(3, 50) ] , initial_value= 7,
            key = "_DogY_"),

            sg.Text('Z ', size=(1, 1)), sg.Spin( [i for i in range(3, 50) ] , initial_value= 7,
            key = "_DogZ_"),

            sg.Checkbox('Save filtered images', default=False,
            tooltip="Enable/disable saving intermediate results. WARNING: use only when working with a small subset!",
            key = "_saveDogOrNot_"),],


            [sg.Text('Watershed parameters', font = ('Arial', 10, 'bold'), size=(45, 1), tooltip="Intesity threshold where to stop watershedding")],
            [sg.Checkbox('Use watershed', default=False, tooltip="Enable/disable this filter.",
            key = "_waterOrNot_"),

            sg.Text('Threshold ', size=(10, 1)), sg.Spin( [i for i in range(0, 2**16) ] , initial_value= 1500,
            key = "_waterIntThresh_"),

            sg.Checkbox('Save filtered images', default=False,
            tooltip="Enable/disable saving intermediate results. WARNING: use only when working with a small subset!",
            key = "_saveWaterOrNot_"),],

            [sg.Text('Cell size threshold', font = ('Arial', 10, 'bold'), size=(45, 1), tooltip="Smaller and largest particle to detect, volume in pixels (of raw data resolution)")],
            [sg.Text('Min cell size ', size=(15, 1)), sg.Spin( [i for i in range(0, 10000) ] , initial_value= 100,
            key = "_minCellSize_"),

            sg.Text('Max cell size ', size=(15, 1)), sg.Spin( [i for i in range(0, 10000) ] , initial_value= 500,
            key = "_maxCellSize_")
            ],

            [sg.Text('Voxel parameters (heatmaps)', font = ('Arial', 10, 'bold'), size=(35, 1), tooltip="Parameters for voxels used for the heatmap (size is in RESAMPLED pixels).")],
            [sg.Text('Size X ', size=(6, 1), tooltip="Size is in RESAMPLED pixels"), sg.Spin( [i for i in range(0, 100) ] , initial_value= 15,
            key = '_voxX_', size=(3, 1)),
            sg.Text('Size Y ', size=(6, 1), tooltip="Size is in RESAMPLED pixels"), sg.Spin( [i for i in range(0, 100)], initial_value= 15,
            key = '_voxY_', size=(3, 1) ),

            sg.Text('Size Z step size ', size=(6, 1), tooltip="Size is in RESAMPLED pixels"), sg.Spin( [i for i in range(1, 26)], initial_value= 15,
            key = '_voxZ_', size=(3, 1) ),

            sg.Text('Method ', size=(6, 1), tooltip="Shape of the voxels: Spherical, Rectangular, Gaussian"), sg.InputCombo(('Spherical', 'Rectangular', 'Gaussian'), size=(10, 2),
            key = '_voxMethod_')]],

            title="Cell detection parameters",title_color="red", font = ('Helvetica', 14), relief= "groove")],

            ############################################################
            #----------------Computational resource parameters----------------#
            ############################################################

            [sg.Frame(layout=[
            [sg.Text('Nr of processes for resampling', size=(35, 1), tooltip="Normally twice the number of CPUs"),
            sg.Spin( [i for i in range(2, 18, 2) ],
            initial_value= 12,
            key = '_resamplingProc_', size=(2, 1))],

            [sg.Text('Nr of parallel processes for cell detection', size=(35, 2),
            tooltip="Reduce this, and then chunkSize parameters if running into 'OutOfMemmory issues'"),
            sg.Spin( [i for i in range(2, 10, 2) ], initial_value= 6,
            key = '_stackProc_', size=(2, 1) )],

            [sg.Text('chunkSizeMax parameter', size=(35, 1),
            tooltip="Maximum number of image planes processed at once."),
            sg.Spin( [i for i in range(10, 100) ] , initial_value= 30,
            key = '_chunkSizeMax_', size=(3, 1) )],

            [sg.Text('chunkSizeMin parameter', size=(35, 1),
            tooltip="Minimum number of image planes processed at once."),
            sg.Spin( [i for i in range(10, 50) ], initial_value= 20,
            key = '_chunkSizeMin_', size=(3, 1) )],

            [sg.Text('chunkOverlap parameter', size=(35, 1),
            tooltip="Overlap between image planes (so you don't miss particles 'in-between stack chunks')"),
            sg.Spin( [i for i in range(10, 50) ] , initial_value= 10,
            key = '_chunkOverlap_', size=(3, 1) )]],

            title="Computational resources",title_color="red", font = ('Helvetica', 14), relief= "groove")],

			[sg.Submit(), sg.Cancel()]]

window = sg.Window('ClearMap toolbox GUI', layout,resizable=True, auto_size_text = True)

event, values = window.Read()

####Extracted values####
#----------------Data paths and processing tasks----------------#

#----------------Data parameters----------------#

#----------------Cell detection parameters----------------#

#----------------Computational resource parameters----------------#


#folder_path, file_path = values[0], values[1]       # get the data from the values dictionary


# sg.Popup('Title',
#          'The results of the window.',
#          'The button clicked was "{}"'.format(event),
#          'The values are', values)
