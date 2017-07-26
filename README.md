# ImageJ-Photometric-Stereo-Tools
The set of tools described here are routinely used by the Northwestern University / Art Institute of Chicago Center for Scientific Studies in the Arts (NU-ACCESS) to make surface-shape measurements of works of art and specifically painted surfaces. The scripts were written in Python for use in ImageJ and are based on algorithms detailed in the forthcoming paper: Salvant et. al., "Photometric stereo by UV-induced fluorescence to detect protrusions on Georgia O’Keeffe’s paintings" in **Metal Soaps in Art – Conservation & Research**.

We use ImageJ (Fiji) because it has a great user interface, it is open source, and provides access to a powerful set of image processing tools that can be readily adapted for extracting surface gradients using the method of [photometric stereo](https://en.wikipedia.org/wiki/Photometric_stereo), as shown here, or many other problems related to computational imaging in cultural heritage. 

## Getting Started with the Scripts

Download the latest version of [Fiji](https://fiji.sc) and place the scripts into the plugins folder. Launch Fiji or "refresh menus" if already running.

The scripts can be accessed in the plugins dropdown menu.

### Prerequisites

To make full use of these tools you will also need to install two additional ImageJ plugins:

[Polynomial fit](https://imagej.nih.gov/ij/plugins/polynomial-fit/index.html) and [Polynomial shading corrector](http://www.optinav.info/Polynomial_Shading_Corrector.htm)

## What do each of the scripts do?

**Photometric Stereo**: This script is the main workhorse tool. It solves a set of linear equations, using the least squares method, to produce a surface normal vector map. To use, capture a series of raking light images using the same methods described for making an ["RTI image"]( http://culturalheritageimaging.org/Technologies/RTI/). 

In ImageJ, create a stack from the images, convert them from RGB to 32-bit, and then run the script. You will be prompted to upload a text file that contains the lighting directions corresponding to each image in the stack (tab deliminted with no header information).

Outputs are an RGB image showing the surface normal vectors (8-bit) and a stack of the x-, y-, and z-gradient images (32-bit).

Beware that the script is still being optimized for speed. If you have a large image it may be better to crop it into sections and then apply to each crop separately.

**Find Lights Blind**: Typically a mirror ball is used to capture the azimuthal and polar direction of the light source. In this script we utilize the fact that in most cases non-ideal near lights illuminate the object (e.g., an object is illuminated within a spherical envelope, the radius of which is less than 3 times the largest dimension of the object). By fiting linear equations in the x and y directions of the image via the [Polynomial fit](https://imagej.nih.gov/ij/plugins/polynomial-fit/index.html) plugin, a map of how light drops-off accross the image is produced. Applying a 5 x 5 Sobel filter to the light drop-off maps in both x and y directions gives the polar orientation of the light. An assumption is made that all lights are approximately equidistant from the object in order to find the azimuthal light orientation. 

To use, apply the polynomial fit plugin to the entire stack of images and then run the **Find Lights Blind** script to the stack of light drop-off maps. 

Calculated outputs are a lighting direction file that can be then be used with the **Photometric Stereo** script.

**Gradient Integration**: In development. This beta script integrates the x-, y- surface gradient images using the Frankot-Chellapa method and was ported from this Matlab code at http://www.peterkovesi.com/matlabfns/Shapelet/frankotchellappa.m

The input to this script is the 32-bit float stack produced from the **Photometric Stereo** plugin. The output is a gray-scale image in which brightness correlates to height. 

**Find Lights Ball**: In development. This script uses a mirror ball to extract the same information as **Find Lights Blind** script.

**Lighting Direction Viewer**: In development. The input to this script is the 32-bit float stack produced from the **Photometric Stereo** plugin and it can produce any novel lighting direction with a mouse click. 

## A Working Example
**Step 1:**
Download the tiff stack [pedernal](https://www.dropbox.com/s/rd6hrf3nqu3mgp8/Pedernal.tif?dl=0). This is a stack of 31 images of a painting surface with the advanced formation of soap protrusions. Each image is illuminated with a unique lighting direction. Also note there is no mirror ball or other calibration sources. All information about the lighting is extracted directly from the images themselves.

**Step 2:**
In Fiji, convert the stack to 32 bits and run [Polynomial fit](https://imagej.nih.gov/ij/plugins/polynomial-fit/index.html). In the dialog box the degree x and degree y should both be set to 1. When prompted, select process the whole stack, press ok.

**Step 3:**
The resulting image stack of light-drop off maps should be named "Poly_Fit_1_1Pedernal". For speed, reduce the dimensions of this stack so it has a width of 500 pixels. Run **Find_Lights_Blind.py** on this reduced size stack. Save the results file as "Light_Dir.txt".

**Step 4:**
Close "Poly_Fit_1_1Pedernal" (we are done with this). You may want to use the [Polynomial shading corrector](http://www.optinav.info/Polynomial_Shading_Corrector.htm), again with polynomial degrees of 1 in both x and y direction to compensate for the uneven illumination. Crop a region of Pedernal.tif for further processing (e.g., 1500 x 1500 pixels on a Macbook Pro with 16Gb RAM this is pretty fast). Run **Photomertric_Stereo.py** on this region. You will be guided to select the "Light_Dir.txt" generated in the last step. The processing can take a while, especially for large files.

If desired you can save both the 8-bit and 32-bit "Surface Normal Map" images produced.

**Step 5:**
Close all images except 32-bit "Surface Normal Map". Run **Gradient_Integration.py**. Since integration is done in frequency space, the images are automatically padded to 1024 x 1024 (factors of 2). The image will be automatically cropped to this size (if another pad size is desired you will need to modify the script). Adjust the brightness/contrast of the "imaginary" image to see the corresponding height map. You can close the "real" image whcih has only been retained for experimental purposes.

**Step 6:**
Try the **Light_Direction_Viewer.py** by selecting the 32-bit "Surface Normal Map" and then running the script. Click on different parts of the image to generate a new illumination direction.
