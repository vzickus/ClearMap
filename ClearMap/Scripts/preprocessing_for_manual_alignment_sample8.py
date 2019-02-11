# -*- coding: utf-8 -*-
"""
Pre-processing before the manual alignment procedure
"""

#load the parameters:
runfile('/home/user/ClearMap/docs/conf.py')
import ClearMap

######################### Import modules

import os, numpy, math

import ClearMap.Settings as settings
import ClearMap.IO as io

from ClearMap.Alignment.Resampling import resampleData;
from ClearMap.Alignment.Elastix import alignData, transformPoints
from ClearMap.ImageProcessing.CellDetection import detectCells
from ClearMap.Alignment.Resampling import resamplePoints, resamplePointsInverse
from ClearMap.Analysis.Label import countPointsInRegions
from ClearMap.Analysis.Voxelization import voxelize
from ClearMap.Analysis.Statistics import thresholdPoints
from ClearMap.Utils.ParameterTools import joinParameter
from ClearMap.Analysis.Label import labelToName


######################### Data parameters

#Directory to save all the results, usually containing the data for one sample
BaseDirectory = '/media/user/a8fece16-8488-4abe-8878-80df6b8a233e/Sample_5/';

#Data File and Reference channel File, usually as a sequence of files from the microscope
#Use \d{4} for 4 digits in the sequence for instance. As an example, if you have cfos-Z0001.ome.tif :
#os.path.join() is used to join the BaseDirectory path and the data paths:
# TODO Maren: 
cFosFile = os.path.join(BaseDirectory, 'Source/Red_Sample_5_BackgroundReduced/12-38-42_PV-TdTom 62479 Het red _UltraII_C00_xyz-Table Z\d{4}.ome.tif');
AutofluoFile = os.path.join(BaseDirectory, 'Source/180913_PV-TdTom 62479 Het green _11-47-48/11-47-48_PV-TdTom 62479 Het _UltraII_C\d{4}.ome.tif');

#Specify the range for the cell detection. This doesn't affect the resampling and registration operations
cFosFileRange = {'x' : all, 'y' : all, 'z' : (0,1500)};

#Resolution of the Raw Data (in um / pixel)
OriginalResolution = (3.25, 3.25, 3);

#Orientation: 1,2,3 means the same orientation as the reference and atlas files.
#Flip axis with - sign (eg. (-1,2,3) flips x). 3D Rotate by swapping numbers. (eg. (2,1,3) swaps x and y)
FinalOrientation = (1,2,3);

#Resolution of the Atlas (in um/ pixel)
AtlasResolution = (25, 25, 25);

#Path to registration parameters and atlases
PathReg        = BaseDirectory;
AtlasFile      = os.path.join(PathReg, 'template_25.tif');
AnnotationFile = os.path.join(PathReg, 'annotation_25_full.nrrd');

############################ Config parameters

#Processes to use for Resampling (usually twice the number of physical processors)
ResamplingParameter = {
    "processes": 8 
};


#Stack Processing Parameter for cell detection
StackProcessingParameter = {
    #max number of parallel processes. Be careful of the memory footprint of each process!
    "processes" : 3,
   
    #chunk sizes: number of planes processed at once
    #Default: 100,50,32
    "chunkSizeMax" : 25,
    "chunkSizeMin" : 13,
    "chunkOverlap" : 6,

    #optimize chunk size and number to number of processes to limit the number of cycles
    "chunkOptimization" : True,
    
    #increase chunk size for optimization (True, False or all = automatic)
    "chunkOptimizationSize" : all,
   
    "processMethod" : "parallel"
   };


######################## Run Parameters, usually you don't need to change those


### Resample Fluorescent and CFos images
# Autofluorescent cFos resampling for aquisition correction

ResolutionAffineCFosAutoFluo =  (16, 16, 16);

CorrectionResamplingParameterCfos = ResamplingParameter.copy();

CorrectionResamplingParameterCfos["source"] = cFosFile;
CorrectionResamplingParameterCfos["sink"]   = os.path.join(BaseDirectory, 'cfos_resampled.tif');
    
CorrectionResamplingParameterCfos["resolutionSource"] = OriginalResolution;
CorrectionResamplingParameterCfos["resolutionSink"]   = ResolutionAffineCFosAutoFluo;

CorrectionResamplingParameterCfos["orientation"] = FinalOrientation;
   
   
   
#Files for Auto-fluorescence for acquisition movements correction
CorrectionResamplingParameterAutoFluo = CorrectionResamplingParameterCfos.copy();
CorrectionResamplingParameterAutoFluo["source"] = AutofluoFile;
CorrectionResamplingParameterAutoFluo["sink"]   = os.path.join(BaseDirectory, 'autofluo_for_cfos_resampled.tif');
   
#Files for Auto-fluorescence (Atlas Registration)
RegistrationResamplingParameter = CorrectionResamplingParameterAutoFluo.copy();
RegistrationResamplingParameter["sink"]            =  os.path.join(BaseDirectory, 'autofluo_resampled.tif');
RegistrationResamplingParameter["resolutionSink"]  = AtlasResolution;
   

#resampling operations:
#######################
#resampling for the correction of stage movements during the acquisition between channels:
resampleData(**CorrectionResamplingParameterCfos);
resampleData(**CorrectionResamplingParameterAutoFluo);

#Downsampling for alignment to the Atlas:
resampleData(**RegistrationResamplingParameter);

"""
After you're done, open the "autofluo_resampled.tif" file and the "template_25.tif" file in ImageJ. 
Go to Plugins -> Big Data Viewer -> Bigwarp. Open template_25 first, then autofluo_resampled. 
In both images, hit Shift + A to flip both to coronal view. 
Scroll around and match the files as closely as possible (left click + pull around to tilt your plane of view in 3d. Ctrl + Y to reset to starter view.)
Landmark procedure: 
    click on one of the windows to make sure you are active in the right window. 
    Press Space bar to activate the landmark mode. 
    Click on one of the landmarks. 
    click the other window, re-activate landmark mode by pressing space bar(twice, if need be)
    Mark the same landmark. 
    Repeat until approx. 50-100 landmarks are marked. 
Go to the landmarks window -> File -> Export landmarks. 
Open the resulting landmarks.csv file in LibreOffice/Excel. 
The first two columns can be ignored. Columns C-E are for the template_25 (and are measured in microns). Columns F-H are for the autofluo_resampled. 
Rescale the template_25 to pixels: In a different column, enter "=C1*0.04" (minus quotation marks). Extend until all the template_25 landmarks (NOT the autofluo landmarks, those are already in pixel coordinates!) are converted. 
Export the points to two different text files, atlas_landmarks.txt and autofluo_landmarks.txt. They should look as follows: 
    point                          <- Not "point" (quotation marks), not "points" (note the S), not "Point" (Capitalized). Clearmap will throw obscure errors if this is not correct! 
    [number of points]             <- not the number of coordinates, but the number of points 
    [Points X][Points Y][Points Z] <- Those should all be in 3 different columns, separated by a space. 
Copy both landmarks files to the folder of your sample. 
Mark the files in the parameter template (almost all the way down, ctrl+F "landmarks"). 
Save both parameter and process template
Klick run, set in the popup window the directory to current workdirectory

That's it! You should be good to go. 
"""
