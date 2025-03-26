# Import relevant libraries
# Image processing
import nibabel as nib
from nilearn.image import math_img, resample_img
import nilearn

# Data management
import numpy as np
import pandas as pd
from itertools import chain
import csv

# Statistics
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.multitest import fdrcorrection

# Plotting
import matplotlib
from nilearn import plotting

# Set the correct matplotlib backend
matplotlib.use('Qt5Agg')

# Set the root directory to your ROI images
data_dir = 'file_directory'

# Set the path to the atlas images you want to split into multiple ROIs
glasser = data_dir + 'mri/atlas/MMP 1.0 MNI projections/MMP_in_MNI_corr.nii.gz'
# Set the path to the atlas labels
Glasserlabels = data_dir + 'mri/atlas/glasser_UniqueRegionList.csv'
# Set an output directory
output_dir = data_dir + 'mri/atlas/glasser_asym_rois/stats_images/'
# Load a table statistics with labels in a different column called 'roi'
glasser_lme = pd.read_csv(data_dir + 'glasser_results_maze.txt', sep='\t', names=None)
glasser_lme = glasser_lme.astype({'roi': str})

# Define area of PHC to be replaced with our PHC
phc = ['ParaHippocampal_Area_1_L', 'ParaHippocampal_Area_1_R',
       'Entorhinal_Cortex_L', 'Entorhinal_Cortex_R']

# Efficient way to iterate over values in csv file and import them as a list
with open(Glasserlabels, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    labelsList = list(chain.from_iterable((list(reader))))

labelsList.sort()
glasser_lme = glasser_lme.sort_values(by='roi')
glasser_lme['roi'] = labelsList

# Remove atlas PHC regions and add our own
phc_lme = pd.read_csv(data_dir + 'lme_df_phg_evoked.txt', sep='\t', names=None)
glasser_lme = glasser_lme[~glasser_lme['roi'].isin(phc)]
glasser_lme = pd.concat([glasser_lme, phc_lme])

for roi in np.arange(0, len(glasser_lme)):
    pvals = glasser_lme.iloc[roi,6:11]
    #pvals = glasser_lme.iloc[roi, 3:5]
    pvals_corr = multipletests(pvals, alpha=0.05, method='fdr_bh')[1]
    #pvals_corr = fdrcorrection(pvals, alpha=0.05)[1]
    glasser_lme.iloc[roi, 6:11] = pvals_corr
    #glasser_lme.iloc[roi, 3:5] = pvals_corr

glasser_lme.to_csv(data_dir + 'glasser_results_maze_mc.txt', sep='\t', index=False)

#for statistic in ['delta', 'theta1', 'theta2', 'theta3', 'alpha']:
for statistic in ['theta1', 'theta2']:

    # Set the name of the column containing p-values
    pVal = statistic + '.p'
    # Create an empty list to collect the names of all significant ROIs
    sig_roi_list = []
    # Load Glasser atlas image
    glasser_atlas = nib.load(glasser)
    # Create a copy of the Glasser atlas data with only zeros
    empty_glasser_data = np.zeros(shape=glasser_atlas.get_fdata().shape)
    # Using the zeros array, create a copy of the glasser atlas image object
    atlas_stats_img = nib.Nifti1Image(empty_glasser_data, glasser_atlas.affine, glasser_atlas.header)

    # Initiate a loop to iterate over all ROI labels
    for roi in glasser_lme['roi'].tolist():

        # Create the full path for the roi image
        if roi in phc_lme['roi'].tolist():
            file = data_dir + 'mri/roi/PHC_clusters/' + roi

        else:
            file = data_dir + 'mri/atlas/glasser_asym_rois/' + roi

        # Load the current ROI image
        img = nib.load(file + '.nii')
        # Extract the data from the ROI image
        data = img.get_fdata()

        # Identify the unique values in the data array except 0
        ROIvalue = np.unique(data)[np.unique(data) != 0]

        # If desired, only change the values in ROIs with a statistic whose corresponding p-value is below a certain
        # significance threshold
        if glasser_lme[glasser_lme['roi'] == roi][pVal].iloc[0] < 0.05:
            # Identify the indices of the values in the data array that are equal to the unique ROI value and replace them with
            # the statistic you would like this ROI to have
            data[data == ROIvalue] = glasser_lme[glasser_lme['roi'] == roi][statistic].iloc[0]
            # Add the name of the significant ROI to the list
            sig_roi_list.extend([roi])
        else:
            # If p-value is larger than threshold, set the ROI value to 0
            data[data == ROIvalue] = 0

        # Create a new image object with the same header and shape as the ROI image but with the new data array
        stats_img = nib.Nifti1Image(data, img.affine, img.header)

        if roi in phc_lme['roi'].tolist():
            stats_img = resample_img(stats_img, target_affine=glasser_atlas.affine,
                                     target_shape=glasser_atlas.get_fdata().shape)

        # Combine the images by addition
        # Since all non-zero values are in unique locations, this will effectively result in joining all images together
        atlas_stats_img = math_img('img1 + img2',
                                   img1=atlas_stats_img, img2=stats_img)

    # Save the combined image
    nib.save(atlas_stats_img, output_dir + statistic + '_maze_sig_mc.nii')

##### Plotting test

# Set the font
font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 22}
matplotlib.rc('font', **font)

statisticsLabels = ['5-6 Hz', '7-8 Hz']
statInd = 0

for statistic in ['theta1', 'theta2']:

    statisticsLabel = statisticsLabels[statInd]

    for condition in ['maze']:

        # Load a stats image you want to check
        stats_image = nib.load(output_dir + statistic + '_' + condition + '_sig_mc.nii')

        # Plot the image on a glass brain
        fig = plotting.plot_glass_brain(stats_image, cmap='RdBu_r', colorbar=False, title=None,
                                        vmax=.2, vmin=-.2, plot_abs=False)
        fig.title(text=statisticsLabel, size=16, color='black', bgcolor='white')
        fig.savefig('/plots/figure9/lmeBeta_glassBrain_' + statistic + '_' + condition + '_mc.pdf')
        fig.savefig('/plots/figure9/lmeBeta_glassBrain_' + statistic + '_' + condition + '_mc.jpg')

    statInd = statInd + 1

stats_image = nib.load(
    '/mri/atlas/glasser_asym_rois/stats_images/theta2_maze_sig_mc.nii')

plotting.plot_img_on_surf(stats_image,
                          views=['medial'],
                          hemisphere=['left', 'right'],
                          colorbar=True,
                          bg_on_data=True,
                          alpha=.4,
                          cmap='RdBu_r',
                          vmax=.05)
plotting.show()
view.open_in_browser()
