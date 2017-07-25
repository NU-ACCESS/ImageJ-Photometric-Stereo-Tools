from ij import IJ, ImagePlus
from ij.process import ImageProcessor
from ij.process import ImageStatistics
from ij.measure import ResultsTable
import math


#create 5 x 5 Sobel kernels for x and y directions
kernel_X = [-1, -2, 0, 2, 1, -4, -8, 0, 8, 4, -6, -12, 0, 12, 6, -4, -8, 0, 8, 4, -1, -2, 0, 2, 1] 
kernel_Y = [1, 4, 6, 4, 1, 2, 8, 12, 8, 2, 0, 0, 0, 0, 0, -2, -8, -12, -8, -2, -1, -4, -6, -4, -1] 


img = IJ.getImage()

I = []
T = []

#interate over all images in stack
n_slices = img.getStack().getSize()
for i in range(1, n_slices+1):
	img.setSlice(i) 
	img2 = img.crop()
	img3 = img.crop()

    #calculate x-slope
	ip1 = img2.getProcessor().convertToFloat() 
	ip1.convolve(kernel_X, 5, 5)
	mX = img2.getStatistics().mean
	
	#calculate y-slope
	ip2 = img3.getProcessor().convertToFloat() 
	ip2.convolve(kernel_Y, 5, 5)
	mY = img3.getStatistics().mean

	#append slopes for all images
	I.append(mX)
	T.append(mY)

#fiddly bits to normalize values (range -1 to 1)
I_mx = max(I)
I_mn = min(I)
maxi = math.sqrt(I_mx*I_mx + I_mn*I_mn)

#ig = [I_mx, I_mna]
#maxi = max(ig)

T_mx = max(T)
T_mn = min(T)
maxiT = math.sqrt(T_mx*T_mx + T_mn*T_mn)

#iT = [T_mx, T_mna]
#maxiT = max(iT)

Xdir = map(lambda x: x/maxi, I)
Ydir = map(lambda x: x/maxiT, T)

#calculate z direction from X and Y. Assumes that lights are all equidistant from image center, e.g. a "dome" configuration
z = [math.sqrt(a*a + b*b) for a,b in zip(Xdir,Ydir)]
zt = map(lambda x: math.sqrt(abs(1-x*x)), z)	
         
#write results to table
table = ResultsTable() 
for i in range(len(Xdir)): 
        table.incrementCounter() 
        table.addValue('X', Xdir[i]) 
        table.addValue('Y', Ydir[i]) 
        table.addValue('Z', zt[i]) 

table.show('Results') 


