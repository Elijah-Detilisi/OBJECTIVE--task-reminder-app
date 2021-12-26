



"""
	Author
	-----------
	Bongani Detilisi
	
	Description
    -----------
	    This python script serves as the main source for the sofware's time consciousness.

	Classes
	-------- 
		Clock
	
	Attributes
    ----------
    	None

    Methods
    ----------
    	None
"""





#Dependenices
import datetime



#----------------Begin class---------------#
class Clock:

	'''
	Description
    -----------
	This class provides information what the current time and date.

    Attributes
    ----------
    current_time : datetime
    	object of the datetime class.

    Methods
    -------
    get_date(): tuple
    	returns a tuple with the current; day of week, day of month, month and year.
    get_day_of_week() : str
    	returns the current day of the week.
    get_time(): tuple
    	returns a tuple with the current; hour, minute and meridiem.
    get_time_of_day(): str
    	returns a tuple with the current time of day; morning/afternoon or evening.
    convert_string_date_2_numeric_date(param_string_date) : tuple
		converts a string date into a numerical format
	check_lateness(param_date): tuple
		returns the lateness of a date.
	
	'''
	def __init__(self):
		self.current_time = datetime.datetime.now()

	def get_date(self):
		self.current_time = datetime.datetime.now()
		day = self.current_time.strftime("%d")
		month = self.current_time.strftime("%B")
		year = self.current_time.strftime("%Y")
		
		return (day, month, year)

	def get_day_of_week(self):
		self.current_time = datetime.datetime.now()
		day_of_Week = self.current_time.strftime("%A")

		return day_of_Week

	def get_time(self):
		self.current_time = datetime.datetime.now()

		hour = int(self.current_time.strftime("%H"))
		minute = self.current_time.strftime("%M")
		meridiem = self.current_time.strftime("%p")
		return (hour, minute, meridiem)

	def get_time_of_day(self):
		self.current_time = datetime.datetime.now()
		hour = int(self.current_time.strftime("%H"))
		time_of_day = ""

		if(hour>=0 and hour<=12):
			time_of_day = 'Morning'
		elif(hour>12 and hour<18):
			time_of_day = 'Afternoon'
		elif(hour>=18 and hour<=23):
			time_of_day = 'Evening'

		return time_of_day

	def convert_string_date_2_numeric_date(self, param_string_date):
		self.current_time = datetime.datetime.now()
		num_month = 0

		try:
			num_month = self.current_time.strptime(param_string_date[1], "%B").month
		except:
			num_month = self.current_time.strptime(param_string_date[1], "%B").month

		return(int(param_string_date[0]), num_month, int(param_string_date[2]))

	def check_lateness(self, param_date):
		self.current_time = datetime.datetime.now()
		is_late = (False, param_date)

		#year late
		if(self.current_time.year > param_date[2]):
			is_late = (True, 'Overdue')
		#same year
		elif(self.current_time.year == param_date[2]):
			#month late
			if(self.current_time.month > param_date[1]):
				is_late = (True, 'Overdue')
			#same month
			elif(self.current_time.month == param_date[1]):
				#due tomorrow
				if((param_date[0]-self.current_time.day) == 1):
					is_late = (True, 'Tomorrow')
				#due today
				elif((param_date[0]-self.current_time.day) == 0):
					is_late = (True, 'Today')
				#overdue
				elif(self.current_time.day > param_date[0]):
					#due yesterday
					if((param_date[0]-self.current_time.day) == -1):
						is_late = (True, 'Yesterday')
					else:
						is_late = (True, 'Overdue')
		return is_late
					

				

#****************End class*****************#
