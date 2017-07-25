# ImageJ-Photometric-Stereo-Tools
The set of tools described here are routinely used by the Northwestern University / Art Institute of Chicago Center for Scientific Studies in the Arts (NU-ACCESS) to make surface-shape measurements of works of art and specifically painted surfaces. The scripts were written in Python for use in ImageJ and are based on algorithms detailed in the forthcoming paper: Salvant et. al., "Photometric stereo by UV-induced fluorescence to detect protrusions on Georgia O’Keeffe’s paintings" in **Metal Soaps in Art – Conservation & Research**.

We use ImageJ (Fiji) because it has a great user interface, its open source, and provides access to a powerful set of image processing tools that can be readily adapted for extracting surface gradients using the method of [photometric stereo](https://en.wikipedia.org/wiki/Photometric_stereo), as shown here, or many other problems related to computational imageing in cultural heritage. 

## Getting Started with the Scripts

Download the latest version of [Fiji](https://fiji.sc) and place the scripts into the distribution plugins folder. Launch Fiji or "refresh menus" if already running.

### Prerequisites

To make full use of these tools you will also need to install two additional ImageJ plugins:

[Polynomial fit](https://imagej.nih.gov/ij/plugins/polynomial-fit/index.html) and [Polynomial shading corrector](http://www.optinav.info/Polynomial_Shading_Corrector.htm)

## What do each of the scripts do?

**Photometric Stereo**: This script is the main workhorse tool. It solves a set of linear equations using the least squares methods to produce a surface normal vector map. To use, produce a series of raking light images using the same methods described for making an ["RTI image"]( http://culturalheritageimaging.org/Technologies/RTI/). 

In ImageJ, create a stack from the images, convert them from RGB to 32-bit, and then run the script. You will be prompted to upload a text file that contains the lighting directions corresponding to each image in the stack (tab deliminted with no header information).

Outputs are an 8-bit RGB image showing the surface normal vectors and a stack of three 32-bit float images that are the x-, y- and z-gradient images.

Beware that the script is still being optimized for speed. If you have a large image it may be better to crop it into sections and then apply to each crop separately.

**Find Lights Blind**: Typically a mirror ball is used to capture the azimuthal and polar direction of the light source. In this script we utilize the fact that in most cases non-ideal near lights illuminate the object (e.g., an object is illuminated within a spherical envelope, the radius of which is less than 3 times the largest dimension of the object). By fiting linear equations in the x and y directions of the image via the [Polynomial fit](https://imagej.nih.gov/ij/plugins/polynomial-fit/index.html) plugin, a map of how light drops-off accross the image is produced. By applying a 5 x 5 Sobel filter to the light drop-off maps, the polar orientation of the light can be calculated. An assumption is made that all lights are approximately equidistant from the object in order to find the azimuthal light orientation. 

To use, apply the polynomial fit plugin to the entire stack of images and then run the **Find Lights Blind** script to the stack of light drop-off maps. 

Calculated outputs are a lighting direction file that can be then be used with the **Photometric Stereo** script.

**Gradient Integration**: In development. This beta script integrates the x-, y- surface gradient images using the Frankot-Chellapa method and was ported from this Matlab code at http://www.peterkovesi.com/matlabfns/Shapelet/frankotchellappa.m

The input to this script is the 32-bit float stack produced from the **Photometric Stereo** plugin. The output is a gray-scale image in which brightness correlates to height. 

**Find Lights Ball**: In development. This script uses a mirror ball to extract the same information as **Find Lights Blind** script.

**Lighting Direction Viewer**: In development. The input to this script is the 32-bit float stack produced from the **Photometric Stereo** plugin and it can produce any novel lighting direction with a mouse click. 

## A Working Example

More to come.
