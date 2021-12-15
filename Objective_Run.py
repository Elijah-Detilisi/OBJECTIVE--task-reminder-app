


"""
	Author
	-----------
	Bongani Detilisi
	
	Description
    -----------
	    This python script provides the main function for the Objective Window.
	Classes
	-------- 
		None
	
	Attributes
    ----------
    	None

    Methods
    ----------
    	main() : void
    		launches the Objective_App_Window every 60 minutes.
"""





#Dependenices

import time
from Objective_Graphic_User_Interface import Objective_App_Window




#----------------Begin Function Definition---------------#

def main():
	'''
    Description
    -----------
        This functions launches the Objective_App_Window every 60 minutes throughout the day.

    Parameter Arguements
    ----------
        None.
    '''
	minutes = 60
	while(True):
		window = Objective_App_Window()
		window.launch_window()
		time.sleep(60 * minutes)

#****************End Function Definition*****************#




#--------------------------Execute------------------------#
if __name__ == '__main__':
	main()