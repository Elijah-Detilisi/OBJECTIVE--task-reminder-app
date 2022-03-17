



"""
	Author
	-----------
	Bongani Detilisi
	
	Description
    -----------
	    This python provides graphical support to the software's GUI
	    components

	Classes
	-------- 
		None
	
	Attributes
    ----------
    	resources_folder_path: str
    		path to the Resources folder.
    	icons_folder_path: str
    		path to the Icons and Images folder.

    Methods
    ----------
    	circle_crop_image(image_file_name): image object
    		This functions returns a circulatr cropped version of the parametrized image.
    	save_image(image_object, image_file_name): void
    		This functions saves the parametrized image object as a png file into the
        	the Resources folder.
    

"""




#Dependencies
from tkinter.tix import *
import os
import numpy as np
from PIL import Image, ImageDraw, ImageTk




#global variables
resources_folder_path = os.getcwd() + r'\Resources'
icons_folder_path = resources_folder_path + r'\Icons and Images'




#----------------Begin Function Definition---------------#

def circle_crop_image(image_file_name):

	'''
    Description
    -----------
        This functions returns a circulatr cropped version of the parametrized image.
    
    Parameter Arguements
    ----------
        image_file_name: str
        	file path/location of the image to be cropped.
    '''
	image_photo = Image.open(image_file_name)
	image_photo.convert("RGB")

	np_image = np.array(image_photo)
	image_height, image_width = image_photo.size

	alpha_image_layer = Image.new('L', image_photo.size, 0)

	cropped_image = ImageDraw.Draw(alpha_image_layer)
	cropped_image.pieslice([0, 0, image_height, image_width], 0, 360, fill=255)

	np_alpha_image = np.array(alpha_image_layer)
	np_image = np.dstack((np_image, np_alpha_image))

	cropped_image = Image.fromarray(np_image)

	return cropped_image

#****************End Function Definition*****************#




#----------------Begin Function Definition---------------#

def save_image(image_object, image_file_name = 'profile_picture.png'):
	'''
    Description
    -----------
        This functions saves the parametrized image object as a png file into the
        the Resources folder.
    
    Parameter Arguements
    ----------
        image_object: numpy array
        	image to be saved.
        image_file_name: str
        	name of the new saved image.
    '''
	try:
		saved_file_name = icons_folder_path + "\\" + image_file_name
		image_object.save(saved_file_name)
	except Exception as ex:
		print(ex)

#****************End Function Definition*****************#




#----------------Begin Function Definition---------------#

def superimpose_image_to_Widget(widget, image_file_name, dimensions):
	'''
    Description
    -----------
        This functions superimposes the parametrized image ontop of the 
        parametrized GUI widget.
    
    Parameter Arguements
    ----------
        widget: tkinter widget
        	tkinter widget to superimpose image ontop of.
        image_file_name: str
        	image path
        dimensions : tuple/list
        	dimension of the size of the superimposed image. 
    '''

	copy_of_image = Image.open(image_file_name)
	
	image = copy_of_image.resize((dimensions[0], dimensions[1]))
	photo = ImageTk.PhotoImage(image)
	widget.config(image=photo)
	widget.config(border = 0)

	widget.image = photo

#****************End Function Definition*****************#


