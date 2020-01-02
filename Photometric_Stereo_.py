from ij import IJ, ImagePlus
from ij.plugin import ImageCalculator
from ij.process import ImageProcessor
from ij.process import FloatProcessor
from org.ejml.simple import SimpleMatrix 
from fiji.util.gui  import GenericDialogPlus

#Input parameters
gd = GenericDialogPlus("Photometric Stereo")  
gd.addDirectoryOrFileField("Select lighting direction file","")
gd.showDialog()  

directory_w = gd.getNextString()

imp2 = IJ.getImage()
IJ.run("32-bit")
imp2 = IJ.getImage()

#path to lighting directions
IJ.run("Text Image... ", "open="+str(directory_w))
imp = IJ.getImage()
imp.setTitle("Lighting directions")

# constructing lighting direction matrix
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
B = SimpleMatrix(L) 
C = SimpleMatrix(I)
kN = B.solve(C).getMatrix().data# calculate normals via least squares
L = [kN[i:i+imp2.height*imp2.width] for i in range(0, len(kN), imp2.height*imp2.width)]

S = ImagePlus("X", FloatProcessor(imp2.width,imp2.height,L[0])).show()
U = ImagePlus("Y", FloatProcessor(imp2.width,imp2.height,L[1])).show()
V = ImagePlus("Z", FloatProcessor(imp2.width,imp2.height,L[2])).show()

IJ.run("Images to Stack", "name=Stack title=[] use")
imp = IJ.getImage()
imp.setTitle("Normal Vector Map")
IJ.run("Z Project...", "projection=[Max Intensity]")
impt = IJ.getImage()

N = ImageCalculator().run("Divide create 32-bit stack", imp, impt)
N.show()
impf = IJ.getImage()
impf.setTitle("32 bit Surface Normal Map")
IJ.run("Make Composite", "display=Composite")

imp.close()
impt.close()

