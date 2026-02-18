# SIDT
Automated data cleaning and generation of normative values on large datasets with SIDT: statistical iterative data truncation.

**Publication**: Bartz, K.M., Wei, S. _et al._ (in press), "Construction of a normative database of human retinal thicknesses from existing UK Biobank OCT Participants," in [_Proceedings of SPIE Medical Imaging (SPIE-MI 2026), Vancouver, Canada, February 15-19, 2026_], (2026).

```
@inproceedings{bartz2026inpressSIDT,
  title={Construction of a normative database of human retinal thicknesses from existing UK Biobank OCT Participants},
  author={Bartz, Kathleen M and Shuwen Wei and Prince, Jerry L and Carass, Aaron},
  booktitle={"Proceedings of SPIE Medical Imaging~(SPIE-MI 2026), Vancouver, Canada, February 15 -- 19, 2026"},
  year={2026}
}
```

## Quick Start

We recommend starting from a fresh python and R installation.

```
conda create -n sidt python=3.11 r-base=4.1.3
conda activate sidt
```

Clone and install this repository.

```
git clone https://github.com/katembartz/SIDT
cd SIDT
pip install .
```

Run SIDT on a csv file containing your databank. The first column of the database must hold the variables of interests (e.g. regions) and the first row much correspond to subjects.

```
sidt \
  --data-path {path_to_csv} \
  --tmp-dir {dir_to_store_intermediate_steps} \
  [--tol-m {tolerance_for_mean}] \
  [--tol-s {tolerance_for_standard_dev}] \
  [--maxIter {int_num_max_iterations}] \
  --k {tolerance_for_variables_OOD}
```

## 1. Introduction and Motivation

Optical coherence tomography (OCT) is a non-invasive imaging technique that can visualize the retinal layers in the human macula. Deep learning algorithms segment these layers, from which mean thickness values are computed for each retinal layer in different regions of the macula. However, artifacts in OCT volumes can mislead segmentation results, in turn corrupting corresponding thickness measures. To establish an accurate database of retinal layer thicknesses, we propose statistical iterative data truncation (SIDT), an algorithm to perform automated data cleaning to generate normative measures on large datasets. We apply this method to more than 170,000 OCT volumes from the UK Biobank database, inspecting thickness values for nine retinal layers in 14 macular regions of interest.

## 2. OCT Segmentation

We compiled a dataset of 172,768 OCT volumes from the UK Biobank, inspecting nine retinal layer thicknesses over fourteen ROIs, giving rise to 126 measurements for each eye. Our approach relies on two preprocessing steps. First, the database of OCT volumes is segmented, which is done using the deep learning algorithm proposed by He _et al_[^1]. 

Software for the OCT segmentation method is located at https://www.nitrc.org/projects/aura_tools/.

From this segmentation we calculate the mean thickness of the nine retinal layers in 14 different macular regions based on the ETDRS grid. The nine retinal layer thickness measurements come from: retinal nerve fiber layer (RNFL), ganglion cell-inner plexiform layer (GCIPL), inner nuclear layer (INL), outer plexiform layer (OPL), outer nuclear layer (ONL), inner segment (IS), outer segment (OS), retinal pigment epithelium (RPE), and total retina, which are labeled on a segmented OCT B-scan below in part (a).

<p align="center">
  <img width="600" height="430" alt="Retinal_OCT_Layers (2)" src="https://github.com/user-attachments/assets/55eec00f-f677-4873-8451-1fa8c92e4c48" />
</p>

The ETDRS grid, overlayed on OCT retinal fundus images in part (b) of the above figure, divides the macula into nine regions, which are defined by three rings centered on the fovea: a central macular disc with a radius of 0.5 mm; an inner macular ring with inner and outer radii of 0.5 mm to 1.5 mm, respectively; and an outer macular ring with inner and outer radii of 1.5 mm to 2.5 mm, respectively. Both the inner and outer macular rings are equally divided into quadrants representing the nasal, temporal, inferior, and superior regions. In addition to the nine regions depicted, we also investigate four regions—inferior nasal, inferior temporal, superior nasal, and superior temporal—that divide the 2.5 mm macular disc centered at the fovea. Finally, we also include a total macular area of 5 × 5 $mm^2$ centered on the fovea.

Normative measures for the OCT retinal layer/region pairs can be found in `normative_measures_OCT_retinal_layers`.


## 3. SIDT Algorithm

SIDT is an automated method that iteratively truncates data that are statistical outliers to generate a reliable database of normative values. This method can operate on datasets containing multiple variables, such as various ROIs in image segmentation applications. 

<p align="center">
<img width="625" height="532" alt="Screenshot 2026-02-17 at 10 44 12 PM" src="https://github.com/user-attachments/assets/0c37ec91-fac0-4b9f-9dad-e863e5f61b52" />
</p>

## 4. Acknowledgements

This work was partially supported by CDMRP W81XWH2010912 (PI: J.L. Prince), a grant from the NIH through the NIBIB R01-EB036013 (PI: J.L. Prince), and a Johns Hopkins Discovery Grant (PI: A. Carass). This research has been conducted using the UK Biobank Resource under Application Number 61229. You can find out more about UK Biobank at http://www.ukbiobank.ac.uk. We refer to the manuscript associated with this work for full citations.

[^1]: He, Y. et al., “Structured layer surface segmentation for retina OCT using fully convolutional regression networks,” Medical Image Analysis 68, 101856 (2021).
