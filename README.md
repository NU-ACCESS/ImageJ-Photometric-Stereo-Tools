# ImageJ-Photometric-Stereo-Tools
The set of tools described here are routinely used by the Northwestern University / Art Institute of Chicago Center for Scientific Studies in the Arts (NU-ACCESS) to make surface-shape measurements of works of art and specifically painted surfaces. The scripts were written in Python for use in ImageJ and are described in the forthcoming paper: Salvant et. al., "Photometric stereo by UV-induced fluorescence to detect protrusions on Georgia O’Keeffe’s paintings" in **Metal Soaps in Art – Conservation & Research**.

We use ImageJ (Fiji) because it has a great user interface and access to a powerful set of image processing tools that could be readily adapted for extracting surface gradients using the method of [photometric stereo](https://en.wikipedia.org/wiki/Photometric_stereo).

## Getting Started with the scripts

Download the latest version of [Fiji](https://fiji.sc) and place the scripts into the distribution plugins folder. Launch Fiji.

### Prerequisites

To make full use of these tools you will also need to install two additional ImageJ plugins:

[Polynomial fit](https://imagej.nih.gov/ij/plugins/polynomial-fit/index.html) and [Polynomial shading corrector](http://www.optinav.info/Polynomial_Shading_Corrector.htm)

## What do each of the scripts do?

**Photometric Stereo**: This script is the main workhorse tool. Its solves a set of linear equations using the least squares methods to produce a surface normal vector map. To use, create a series of raking light images using the same methods as those described for making an ["RTI image"]( http://culturalheritageimaging.org/Technologies/RTI/). ImageJ can import jpegs, tifs, even raw image formats.

Create a stack from the images and then run the script. You will be prompted to upload a text file that contains your lighting directions that correspond to each image in the image stack (tab deliminted with no header information).

Outputs are an 8bit RGB image showing the surface normal vectors and a stack of 32 bit float images that are the x-, y- and z-gradient images.

Beware that the script is still being optimized for speed. If you have a large image it may be better to crop it into sections and then apply to each crop separately.

**Find Lights Blind**: Typically a mirror ball is used to capture the azimuthal and polar direction of the light source. In this script we utilize the fact that in most cases non-ideal near lights illuminate the object (e.g., one lights the object with a spherical envelope the radius of which is less than 3x largest dimension of the object). By fiting linear equations in the x and y directions of the image via the [Polynomial fit](https://imagej.nih.gov/ij/plugins/polynomial-fit/index.html) (equivalent of a large Gaussian blur kernal) plugin a map of how light falls off accross the image is produced. 

To use, apply the polynomial fit plugin to the entire stack of images and then run the **Find Lights Blind** script to the lighting drop-off maps. 

Calculated outputs are a lighting direction file that can be then be used with the **Photometric Stereo** script.

**Find Lights Ball**: In development. This script uses a mirror ball to extract the same information as **Find Lights Blind** script.

**Gradient Integration**: In development. This beta script integrates the x-, y- surface gradient images using the Frankot-Chellapa method and was ported from this Matlab code at http://www.peterkovesi.com/matlabfns/Shapelet/frankotchellappa.m

The input to this script is the 32-bit float stack produced from the **Photometric Stereo** plugin. The output is a gray-scale image in which brightness maps height information. 

**Lighting Direction Viewer**: In development. The input to this script is the 32-bit float stack produced from the **Photometric Stereo** plugin and it can produce any novel lighting direction with a mouse click. 
