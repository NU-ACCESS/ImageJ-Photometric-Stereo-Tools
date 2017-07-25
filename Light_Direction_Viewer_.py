from ij import IJ
from ij.gui import Toolbar
from ij import WindowManager
from time import sleep
from java.awt.event import MouseAdapter


#IJ.run("Duplicate...", "duplicate")
#imp2 = IJ.getImage()
 
class ML(MouseAdapter):
 def mousePressed(self, event):
   from ij import IJ, ImagePlus
   from ij.process import FloatProcessor
   import math
   from ij.plugin import ImageCalculator
   imp = IJ.getImage()
   
   imp.setSlice(3)
   ip = imp.getProcessor().convertToFloat() # as a copy 
   pixels = ip.getPixels() 

   imp.setSlice(2)
   ip1 = imp.getProcessor().convertToFloat() # as a copy 
   pixels1 = ip1.getPixels()

   imp.setSlice(1)
   ip2 = imp.getProcessor().convertToFloat() # as a copy 
   pixels2 = ip2.getPixels()
   
   canvas = event.getSource()
   p = canvas.getCursorLoc()
   imp = canvas.getImage()
   x = p.x * 1.0000
   y = p.y * 1.0000
   nx = x - imp.width / 2
   ny = y - imp.height / 2
   n_y = ny * -1
   n_xx = nx / imp.width /2
   n_yy = n_y / imp.height /2
   z = math.sqrt(n_xx*n_xx + n_yy*n_yy)
   z1 = math.sqrt(1 - z*z) 
   
   Xdir = map(lambda x: x*n_xx, pixels2)
   Ydir = map(lambda x: x*n_yy, pixels1)
   Zdir = map(lambda x: x*z1, pixels)
   
   ip3 = FloatProcessor(ip.width, ip.height, Xdir, None) 
   imp3 = ImagePlus("", ip3)
   
   ip4 = FloatProcessor(ip.width, ip.height, Ydir, None) 
   imp4 = ImagePlus("", ip4)

   ip5 = FloatProcessor(ip.width, ip.height, Zdir, None) 
   imp5 = ImagePlus("", ip4)
   
   imp6 = ImageCalculator().run("Add create 32-bit stack", imp3, imp4)
   
   imp7 = ImageCalculator().run("Add create 32-bit stack", imp5, imp6)
   imp7.setTitle("Lighting Direction")
   
   imp7.show()  
   
listener = ML()
can = WindowManager.getCurrentImage().getCanvas()
 
for imp in map(WindowManager.getImage, WindowManager.getIDList()):
 win = imp.getWindow()
 if win is None:
   continue
 win.getCanvas().addMouseListener(listener)