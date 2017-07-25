#This solves the photometric stereo problem via least squares method.
#Requires Jama jar to be downloaded from http://math.nist.gov/javanumerics/jama/
#Rename the current downloaded version as just "Jama.jar" and place into plugins folder
#This script relies on yython but is really bits and pieces from the macro recorder
#Improvements  to come in the next version

from ij import IJ, ImagePlus
from ij.plugin import ImageCalculator
from ij.process import ImageProcessor
from ij.process import FloatProcessor
import sys
sys.path.append('Jama.jar')
from Jama import Matrix

imp2 = IJ.getImage()
IJ.run("32-bit")
imp2 = IJ.getImage()

#path to lighting directions
IJ.run("Text Image... ", "open=")
imp = IJ.getImage()
imp.setTitle("Lighting directions")

# making a jython nested list for constructing lighting direction matrix
m = imp.getProcessor().getPixels()
m2 = [val for val in m]
L = [m2[i:i+imp.width] for i in range(0, len(m2), imp.width)]
imp.close()

# reshape image stack as an n x m matrix
n_slices = imp2.getStack().getSize()
I =[]
for i in range(1, n_slices+1):
  imp2.setSlice(i) 
  n = imp2.getProcessor().getPixels()   
  n2 = [val for val in n]
  I.append(n2)

# construct Jama matrices and calculate normals
B = Matrix(L) 
C = Matrix(I)
kN = B.solve(C).getColumnPackedCopy()# calculate normals via least squares

#return matrices to images 
ipFloat = FloatProcessor(3, imp2.height*imp2.width,  kN)
impa = ImagePlus("kN", ipFloat)
impa.show()

#reshape as using montage and reslice commands (need a better way to do this) 
IJ.run(impa,"Montage to Stack...", "images_per_row=1 images_per_column=%d border=0" % imp2.height)
impb = IJ.getImage()
IJ.run("Reslice [/]...", "output=1.000 start=Left avoid")
impc = IJ.getImage()

impa.close()
impb.close()

#calculating albedo
IJ.run("Z Project...", "projection=[Max Intensity]")
impd = IJ.getImage()
impd.setTitle("albedo")

#calculating normals
N = ImageCalculator().run("Divide create 32-bit stack", impc, impd)
N.show()
#IJ.run("Rotate 90 Degrees Right")
#IJ.run("Flip Horizontally", "stack")
impf = IJ.getImage()
impf.setTitle("32 bit Surface Normal Map")

#converting to 8 bit color image
IJ.run("Duplicate...", "duplicate")
IJ.run("8-bit")
impe = IJ.getImage()
impe.changes = False
IJ.run("Stack to RGB")
impg = IJ.getImage()
impg.setTitle("8 bit Surface Normal Map")

impc.close()
impd.close()
impe.close()







