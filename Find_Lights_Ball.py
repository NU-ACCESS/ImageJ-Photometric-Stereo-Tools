from ij import IJ, ImagePlus
from ij.plugin.frame import RoiManager

imp = IJ.getImage()

rm = RoiManager.getInstance()
if not rm:
  rm = RoiManager()
rm.reset()

n_slices = imp.getStack().getSize()
for i in range(1, n_slices+1):
	imp.setSlice(i) 
	roi = IJ.run("Find Maxima...", "noise=300 output=[Point Selection]")
	rm.addRoi(roi)

rm.runCommand(imp, "Show All")
rm.runCommand(imp,"Measure")