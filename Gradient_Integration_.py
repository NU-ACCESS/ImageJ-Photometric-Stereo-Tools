# Jython implementation of Frankot-Chellapa algorithm for use on ImageJ- Generates integrable surface from gradients
# Takes advantage of many ImageJ commands.
# Robert T. Frankot and Rama Chellappa
# A Method for Enforcing Integrability in Shape from Shading
# IEEE PAMI Vol 10, No 4 July 1988. pp 439-451

#ruthlessly stolen from Matlab code at http://www.peterkovesi.com/matlabfns/Shapelet/frankotchellappa.m

from ij import IJ, ImagePlus, ImageStack
from ij.process import ImageProcessor, FloatProcessor
from ij.plugin import ImageCalculator
from ij.plugin import ChannelSplitter
from ij.gui import GenericDialog

IJ.run("FFT Options...", "complex")

# grab current normal map image and get x and y gradients. 
IJ.run("Canvas Size...", "width=1024 height=1024 position=Center")
Norms = IJ.getImage()

# grab current normal stack image and get x and y gradients. 
Norms = IJ.getImage()
Norms.setSlice(1)
dzdx = Norms.crop()
dzdx.show()
dzdx = IJ.getImage()
IJ.run("FFT") #Needs to be a complex Fourier transform, ImageJ generates a stack with both real and imaginary
DZDX = IJ.getImage()
dzdx.close()

Norms.setSlice(2)
dzdy = Norms.crop()
dzdy.show()
dzdy = IJ.getImage()
IJ.run("FFT") #Needs to be a complex Fourier transform
DZDY = IJ.getImage()
dzdy.close()


# Create two images with a ramp gradient from left to right (wx and wy in Frankot Chellapa).
# Size of ramp needs to be a square of same dimensions as FFT image generated by ImageJ.
# Make sure that "Complex Fourier Transform" button under "Process, FFT" is selected or else it will not work...

imp = ImagePlus("wx", FloatProcessor(1024, 1024))# for later create a dialog box for choosing pads of 512x512, 1024x1024, 2048x2048, etc.
pix = imp.getProcessor().getPixels()
n_pixels = len(pix) # total number of pixels
w = imp.getWidth()# length of one row

for i in range(len(pix)): # fill row with linear ramp from 0 to whatever the image width; for 512 size, values range 0 to 512
  pix[i] = i % w
  
imp.getProcessor()
imp.show()
imp = IJ.getImage()

#adjust min and max so the ramp ranges from -0.5 cycles/pixel to + 0.5 cycles/pixel
IJ.run(imp, "Enhance Contrast...", "saturated=0 normalize")
IJ.run(imp, "Subtract...", "value=0.5")
IJ.run("Swap Quadrants")

IJ.run(imp, "Duplicate...", "title=wy") #create wy by rotating wx by 90 degrees
IJ.run("Rotate 90 Degrees Left")
imp2 = IJ.getImage()
imp2.changes = False

#integration in the phase domain by shifting Pi/2, see equation 21 in Frankot-Chellapa
A = ImageCalculator().run("Multiply create 32-bit stack", DZDX, imp)
B = ImageCalculator().run("Multiply create 32-bit stack", DZDY, imp2) # numerator of 
C = ImageCalculator().run("Add create 32-bit stack", A, B)	      # eq 21
D = ImageCalculator().run("Multiply create 32-bit", imp, imp)		  # square wx
E = ImageCalculator().run("Multiply create 32-bit", imp2, imp2)		  # square wy
F = ImageCalculator().run("Add create 32-bit", D, E)				  # demnominator of eq 21
Z = ImageCalculator().run("Divide create 32-bit stack", C, F)		  # solve eq 21
Z.show()
IJ.run("Inverse FFT") #results of integration
IJ.run("Stack to Images") #separate real and imaginary... why does imaginary produce result? more reading needed.

#clean-up by closing un-necessary images
imp2.close()
DZDX.close()
DZDY.close()
imp.changes = False
imp.close()
A.changes = False
A.close()
Z.close()









