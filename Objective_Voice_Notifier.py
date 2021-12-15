



"""
	Author
	-----------
	Bongani Detilisi
	
	Description
    -----------
	    This python script serves as the main source for the sofware's audio output stream, 
	    it uses text to speech for audio output

	Classes
	-------- 
		Text_To_Speech
	
	Attributes
    ----------
    	None

    Methods
    ----------
    	None
"""





#Dependenices
import pyttsx3
import threading 




#----------------Begin class---------------#

class Text_To_Speech:
	'''
	Description
    -----------
	This class converts string text into audible speech.

    Attributes
    ----------
    synthesizer : pyttsx3
    	text to speech object
	voice_rate : int
		voice speed of the synthesizer object
	voices : pyttsx3.voices
		voice properties of the synthesizer object

    Methods
    -------
    set_voice_speed(speed): void
    	sets the voice rate for synthesizer object.
	set_voice_type(voice_gender): void
		sets the voice type for synthesizer object, i.e Male or Female voice.
    speak(text): void
        converts given text into audible sound
    say_current_date_time(): void
    	uses the speak() function to articulate the current date and time.
    say_greeting(): void
    	uses the speak() function to articulate a greeting.
    articulate_breifing(): void
    	greets the user.
	'''

	def __init__(self):
		"""
        Constructs all the necessary attributes for the Audio_Output object.

        Parameters
        ----------
            None
        """
		self.synthesizer = pyttsx3.init()
		self.voice_rate = 180
		self.voices = None
		self.set_voice_type('female')


	def set_voice_speed(self, speed = 1):
		self.voice_rate = speed
		self.synthesizer.setProperty('rate', self.voice_rate)

	def set_voice_type(self, voice_gender):
		this_voice = None
		if(voice_gender.lower == "male"):
			this_voice = 0
		else:
			this_voice = 1
		self.voices = self.synthesizer.getProperty('voices')
		self.synthesizer.setProperty('voice', self.voices[this_voice].id)

	def speak(self, text):
		self.synthesizer.say(text)
		self.synthesizer.runAndWait()

	def articulate_breifing(self, machine_clock, profile_info, task_list, random_quote):
		#extract objectives
		objectives = []
		for count, task in enumerate(task_list):
			objectives.append((count+1, task[0]))

		if(len(objectives) == 0):
			objectives = "You currently don't have any objectives yet."
		else:
			objectives = f"Your objectives are as follows; {objectives}"

		#prepare briefing message
		breif_message = f"Good {machine_clock.get_time_of_day()} {profile_info[1]} {profile_info[0]}, the time is {machine_clock.get_time()},\
						today is {machine_clock.get_date()}, {machine_clock.get_day_of_week()}, and {objectives},\
						here is the hourly quote; {random_quote[0]}, {random_quote[1]}"
		#say breif message
		threading.Thread(target = self.speak, args = (breif_message, )).start()

#****************End class*****************#

