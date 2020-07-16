#OpenMvg and OpenMvs

When I use OpenMvg and OpenMvs to build a 3D scenery, there are some codes I wrote down in case lost.

ReadfromOpenMvgJason :
A process is neccesary that I have to read the jason, and change it to a type that colmap can read in. 

changeCamSamepara:
There are a folder saving the camera parameters of each image, so I have to combine those to a file so that the openmvs can use it. 

changeSize，tolog：
Two simple codes, one can change the size of images, another can combine the tanks data's camera parameters.

colmap3.sh: 
My first script, it includes the processers of our experiment.
