



"""
	Author
	-----------
	Bongani Detilisi
	
	Description
    -----------
	    This python provides backend support to the software's GUI
	    components

	Classes
	-------- 
		None.
	
	Attributes
    ----------
    	None.
    Methods
    ----------
    	None.

"""




#Dependencies
from abc import ABC, abstractmethod
import random
import webbrowser

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from Objective_Time_Awarness import Clock
from Objective_Voice_Notifier import Text_To_Speech
import Objective_Graphics_Toolkit as graphics_toolkit
from Objective_Database_Manager import Activities_table, Profile_table, Quotes_table




#----------------Begin class---------------#

class Task_label_frame(tk.LabelFrame):

	'''
	Description
    -----------
	This class provides a labelframe widget with two buttons.

    Attributes
    ----------
    activities_table: Activities_table
    	activities table object.
	goal_entry : tuple
		tuple with the the goal title, description and due date.
	task_view_button : button
		tkinter button for viewing goal information.
	task_check_button : button
		tkinter button for checking out a goal entry.

    Methods
    -------
	prepare_widgets(): void
		prepares sub-widgets ready for display
	superimpose_widgets(): void
    	places widgets ontop of labelframe.
    check_task_action() : void
    	removes current goal entry from database and destroys labelframe.
    view_task_action() : void
    	views current goal in depth detail.
    initialize_label_frame() : void
    	prepares entire labelframe for display.

	'''

	frame_color = '#D3D3D3'

	def __init__(self, master_window, root, param_goal_entry):
		tk.LabelFrame.__init__(self, root, bg = self.frame_color)

		self.master_window = master_window
		self.activities_table = Activities_table()
		self.goal_entry = param_goal_entry
		self.task_view_button = tk.Button(self, bg = self.frame_color)
		self.task_check_button = tk.Button(self, bg = self.frame_color)

		self.initialize_label_frame()

	def set_widget_text(self):
		machine_clock = Clock()
		date_text = machine_clock.convert_string_date_2_numeric_date(self.goal_entry[2].split(' '))
		lateness_text = machine_clock.check_lateness(date_text)
		#when task is late
		if(lateness_text[0]):
			if(lateness_text[1] == 'Today'):
				self.task_view_button.configure(fg = 'green')
			elif(lateness_text[1] == 'Tomorrow'):
				self.task_view_button.configure(fg = '#DE9101')
			else:
				self.task_view_button.configure(fg = 'red')

			self.task_view_button.config(text = f"{self.goal_entry[0]} | Due: {lateness_text[1]}")
		#when task is not late
		else:
			self.task_view_button.config(text = f"{self.goal_entry[0]} | Due: {self.goal_entry[2]}")

	def prepare_widgets(self):
		#config button font
		self.task_view_button.configure(anchor = 'w')
		self.task_view_button.configure(font =('Verdana', 10, 'bold'))
		#config text
		self.set_widget_text()
		#config border
		self.task_check_button.configure(bd = 0)
		self.task_view_button.configure(bd = 0)
		#config button action listeners
		self.task_check_button.configure(command = self.check_task_action)
		self.task_view_button.configure(command = self.view_task_action)
		#config cursors
		self.task_check_button.configure(cursor = 'hand2')
		self.task_view_button.configure(cursor = 'hand1')
		#config button graphics
		check_box_picture = graphics_toolkit.icons_folder_path + r'\blank-check-box.png'
		graphics_toolkit.superimpose_image_to_Widget(self.task_check_button, check_box_picture, (20, 20))

	def superimpose_widgets(self):
		self.task_check_button.place(relx=0.01, rely=0.2, relwidth = 0.1, relheight = 0.5)
		self.task_view_button.place(relx=0.13, rely=0.02, relwidth = 0.87, relheight = 0.9)

	def check_task_action(self):
		self.activities_table.remove_goal_entry(self.goal_entry)
		self.destroy()
		self.master_window.restore_goal_entries_displays()

	def view_task_action(self):
		task_viewer_window = Task_Viewer_Window(self.master_window, self.goal_entry)
		task_viewer_window.launch_window()

	def initialize_label_frame(self):
		self.prepare_widgets()
		self.superimpose_widgets()

#****************End class*****************#





#----------------Begin class---------------#

class Toplevel_Window_Husk(tk.Toplevel, ABC):

	'''
	Description
    -----------
	This class provides an abstraction for a Toplevel window GUI.

    Attributes
    ----------
    None

    Methods
    -------
    setup_master_window(title, width, height) : void
    	set the basic properties of the window with with the paramitrized values.
    initialize_window() : void
    	prepares the Toplevel window for display.
    launch_window() : void
    	displays window.

	'''

	def __init__(self, root):
		tk.Toplevel.__init__(self)
		self.master_window = root

	@abstractmethod
	def prepare_widgets(self):
		raise NotImplementedError

	@abstractmethod
	def superimpose_widgets(self):
		raise NotImplementedError

	def set_window_icon(self):
		objective_icon =  graphics_toolkit.icons_folder_path + r'\monkey_ico.ico'
		self.iconbitmap(objective_icon)

	def setup_master_window(self, title, width = 500, height = 500):
		self.title(str(title))
		self.resizable(False, False)
		self.grab_set()
		self.transient()
		#display window in the middle of the screen
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()
		x_cordinate = int((screen_width/2) - (width/2))
		y_cordinate = int((screen_height/2) - (height/2))
		self.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate-20))

	def initialize_window(self):
		self.set_window_icon()
		self.prepare_widgets()
		self.superimpose_widgets()

	def launch_window(self):
		self.initialize_window()
		self.mainloop()

#****************End class*****************#





#----------------Begin class---------------#

class Task_Entry_Window(Toplevel_Window_Husk):

	'''
	Description
    -----------
	This class provides the Task Entry window GUI.

    Attributes
    ----------
    MONTHS, DAYS, YEARS, HOURS, MINUTES, MERIDIUMS: lists
    	supporting variables.
    frame1, frame2 : tkinter Frame widgets
    	contain all wigdets.
    title_label_frame, description_label_frame, time_label_frame, date_label_frameL: tkinter Labelframe widgtes
    	decorative widgets
    hour_combo, minute_combo, meridium_combo, date_combo, month_combo, year_combo: tkinter Combo box widgets
    	allows user to insert due date and time for a goal.
    task_title_entry : tkinter Entry widget
    	allows user to type in a goal's/task's title.
    task_description_text : tkinter Text widget
    	allows user to type in a goal's/task's description.
    add_task_button : tkinter Button widget.
    	allows user to store their goal/task entry into the OBJECTIVE database.

    Methods
    -------
    set_datetime_displayparam_time, param_date) : void
    	assigns paramitrized values to combo box widgets.
	prepare_widgets(): void
		prepares sub-widgets ready for display
	superimpose_widgets(): void
    	places widgets ontop of toplevel window.
    get_user_input() : tuple
    	returns the current data extracted from all input fields.
    add_task_action() : void
    	stores user input into database and terminates toplevel window.
	update_task() : void
		updates a goal entry from the database.
	'''

	frame_color1 = "#F5F5F5" 
	frame_color2= "#B0C4DE"

	def __init__(self, root):
		super().__init__(root)
		self.setup_master_window('Task Entry', 500, 500)

		#supporting fields
		self.MONTHS = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"] 
		self.DAYS = ['{}'.format(i) for i in range(1, 32)]
		self.YEARS = ['{}'.format(j) for j in range(2021, 2031)]

		self.HOURS = ['{}'.format(k) for k in range(1, 13)]
		self.MINUTES = ['{}'.format(l) for l in range(0, 60)]
		self.MERIDIUMS = ['AM', 'PM']

		#widgets
		self.root_window = root
		self.frame1 = tk.Frame(self, bg = self.frame_color1)
		self.frame2 = tk.Frame(self, bg = self.frame_color2)

		self.title_label_frame = tk.LabelFrame(self.frame1, bg = self.frame_color1, text = 'Goal Title')
		self.description_label_frame = tk.LabelFrame(self.frame2, bg = self.frame_color2, text = "Goal Description")
		self.date_label_frame = tk.LabelFrame(self.frame1, bg = self.frame_color1, text = 'Due-Date')
		self.time_label_frame = tk.LabelFrame(self.frame1, bg = self.frame_color1, text = 'Due-Time')
		
		self.task_title_entry = tk.Entry(self.title_label_frame, bg = self.frame_color1, bd = 0)
		self.task_description_text = tk.Text(self.description_label_frame, bg = self.frame_color2, bd = 0)
		
		self.add_task_button = tk.Button(self.frame2, bg = self.frame_color2, command = lambda : self.add_task_action(old_goal_entry = None))

		self.date_combo = ttk.Combobox(self.date_label_frame, values= self.DAYS)
		self.month_combo = ttk.Combobox(self.date_label_frame, values= self.MONTHS)
		self.year_combo = ttk.Combobox(self.date_label_frame, values= self.YEARS)

		self.hour_combo = ttk.Combobox(self.time_label_frame, values= self.HOURS)
		self.minute_combo = ttk.Combobox(self.time_label_frame, values= self.MINUTES)
		self.meridium_combo = ttk.Combobox(self.time_label_frame, values= self.MERIDIUMS)

		self.prepare_widgets_true()

	def set_datetime_display(self, param_time, param_date):
		self.hour_combo.set(str(param_time[0]))
		self.minute_combo.set(str(param_time[1]))
		self.meridium_combo.set(str(param_time[2]))

		self.date_combo.set(str(param_date[0]))
		self.month_combo.set(str(param_date[1]))
		self.year_combo.set(str(param_date[2]))

	def set_widget_text(self, goal_title, goal_description, goal_due_date, goal_due_time):
		self.task_title_entry.delete(0, 'end')
		self.task_description_text.delete(0.0, 'end')

		self.task_title_entry.insert(0, str(goal_title))
		self.task_description_text.insert(0.0, str(goal_description))
		self.set_datetime_display(goal_due_time, goal_due_date)

	def prepare_widgets(self):
		purpose = "dummy function"

	def prepare_widgets_true(self):
		machine_clock = Clock()
		#config font
		self.task_title_entry.configure(font =('arial', 10, 'italic'))
		self.task_description_text.configure(font =('arial', 10, 'italic'))
		
		#config text
		self.set_widget_text('Insert goal title here...', 'Insert goal description here...',\
							machine_clock.get_date(), machine_clock.get_time())
		
		#config button graphics
		self.add_task_button.configure(cursor = 'hand2')
		add_picture = graphics_toolkit.icons_folder_path + r'\add.png'
		graphics_toolkit.superimpose_image_to_Widget(self.add_task_button, add_picture, (70, 70))

	def superimpose_widgets(self):
		#frames
		self.frame1.place(relx=0, rely=0, relwidth = 1, relheight = 0.3)
		self.frame2.place(relx=0, rely=0.301, relwidth = 1, relheight = 0.7)

		#combo boxes
		self.date_combo.place(relx=0.01, rely=0.01, relwidth = 0.2, relheight = 0.7)
		self.month_combo.place(relx=0.23, rely=0.01, relwidth = 0.4, relheight = 0.7)
		self.year_combo.place(relx=0.67, rely=0.01, relwidth = 0.3, relheight = 0.7)

		self.hour_combo.place(relx=0.01, rely=0.01, relwidth = 0.3, relheight = 0.7)
		self.minute_combo.place(relx=0.35, rely=0.01, relwidth = 0.3, relheight = 0.7)
		self.meridium_combo.place(relx=0.67, rely=0.01, relwidth = 0.3, relheight = 0.7)
		
		#entries
		self.task_title_entry.place(relx=0.01, rely=0.01, relwidth = 0.98, relheight = 0.98)
		self.task_description_text.place(relx=0.01, rely=0.01, relwidth = 0.98, relheight = 0.98)

		#label frames
		self.title_label_frame.place(relx=0.01, rely=0.02, relwidth = 0.98, relheight = 0.5)
		self.description_label_frame.place(relx=0.01, rely=0.03, relwidth = 0.98, relheight = 0.85)
		self.date_label_frame.place(relx=0.48, rely=0.55, relwidth = 0.5, relheight = 0.3)
		self.time_label_frame.place(relx=0.01, rely=0.55, relwidth = 0.35, relheight = 0.3)

		#buttons
		self.add_task_button.place(relx=0.77, rely=0.78, relwidth = 0.2, relheight = 0.2)
	
	def get_user_input(self):
		goal_title = str(self.task_title_entry.get())
		goal_description = str(self.task_description_text.get("1.0","end-1c"))
		goal_due_time = f"{self.hour_combo.get()}:{self.minute_combo.get()}:{self.meridium_combo.get()}"
		goal_due_date = f"{self.date_combo.get()} {self.month_combo.get()} {self.year_combo.get()}"

		return (goal_title, goal_description, goal_due_date, goal_due_time)

	def add_task_action(self, old_goal_entry):
		activites_table = Activities_table()
		my_goal = self.get_user_input()
		try:
			activites_table.remove_goal_entry(old_goal_entry)
		except:
			error_log = 'No need to delete old Entry'
		activites_table.insert_new_goal_entry(my_goal)

		self.master_window.restore_goal_entries_displays()
		self.destroy()

	def update_task(self, goal_entry):
		self.set_widget_text(goal_entry[0], goal_entry[1], goal_entry[2].split(' '), goal_entry[3].split(':'))
		self.add_task_button.configure(command = lambda : self.add_task_action(old_goal_entry = goal_entry))
		self.launch_window()

#****************End class*****************#




#----------------Begin class---------------#

class Task_Viewer_Window(Toplevel_Window_Husk):

	'''
	Description
    -----------
	This class provides the Task Viewer window GUI.

    Attributes
    ----------
 
    frame1: tkinter Frame widgets
    	contain all wigdets.
    title_label_frame, description_label_frame, date_label_frameL: tkinter Labelframe widgtes
    	decorative widgets
    task_title_label : tkinter Label widget
    	displays the goal's/task's title.
    task_description_text : tkinter Text widget
    	displays the goal's/task's description.
    edit_task_button : tkinter Button widget.
    	allows user to update their goal/task entry from the OBJECTIVE database.

    Methods
    -------
	prepare_widgets(): void
		prepares sub-widgets ready for display
	superimpose_widgets(): void
    	places widgets ontop of toplevel window.
    edit_task_action() : void
    	displays the Task_Entry_Window to edit the current goal entry.
	'''

	frame_color = '#E6E6FA'

	def __init__(self, root, param_goal_entry):

		super().__init__(root)
		self.goal_entry = param_goal_entry

		self.setup_master_window('Task Viewer', 400, 400)
		self.frame1 = tk.Frame(self, bg = self.frame_color)
		#label frames
		self.title_label_frame = tk.LabelFrame(self.frame1, bg = self.frame_color)
		self.description_label_frame = tk.LabelFrame(self.frame1, bg = self.frame_color, text = 'Description')
		self.date_label_frame = tk.LabelFrame(self.frame1, bg = self.frame_color, text = "Task completion is due")
		#buttons
		self.edit_task_button = tk.Button(self.frame1, bg = self.frame_color, command = self.edit_task_action)
		#display widgets
		self.task_title_label = tk.Label(self.title_label_frame, anchor = 'w', bg = self.frame_color)
		self.task_description_text = tk.Text(self.description_label_frame, bg = self.frame_color, bd = 0)
		self.datetime_display_label = tk.Label(self.date_label_frame, anchor = 'w', bg = self.frame_color)

	def set_widget_text(self):
		#goal title text
		self.task_title_label.config(text = self.goal_entry[0])
		#goal description text
		self.task_description_text.configure(state  = 'normal')
		self.task_description_text.delete(float(2), float(5))
		self.task_description_text.insert(float(2), self.goal_entry[1])
		self.task_description_text.configure(state  = 'disabled')
		#goal due date text
		self.datetime_display_label.config(text = f'{self.goal_entry[3]}, {self.goal_entry[2]}')

	def prepare_widgets(self):
		#config font
		self.task_title_label.configure(font =('Georgia', 11, 'bold', 'italic'))
		self.datetime_display_label.configure(font =('arial', 11))
		self.task_description_text.configure(font =('Calibri', 9))
		#config text
		self.set_widget_text()
		#config button graphics
		self.edit_task_button.configure(cursor = 'hand2')
		edit_picture = graphics_toolkit.icons_folder_path + r'\edit.png'
		graphics_toolkit.superimpose_image_to_Widget(self.edit_task_button, edit_picture, (60, 60))

	def superimpose_widgets(self):
		#frames
		self.frame1.place(relx=0, rely=0, relwidth = 1, relheight = 1)
		#label frames
		self.title_label_frame.place(relx=0.02, rely=0.03, relwidth = 0.96, relheight = 0.15)
		self.description_label_frame.place(relx=0.02, rely=0.23, relwidth = 0.96, relheight = 0.5)
		self.date_label_frame.place(relx=0.02, rely=0.78, relwidth = 0.7, relheight = 0.15)
		#display widgets
		self.task_title_label.place(relx=0.01, rely=0.2, relwidth = 0.98, relheight = 0.5)
		self.datetime_display_label.place(relx=0.01, rely=0.2, relwidth = 0.98, relheight = 0.5)
		self.task_description_text.place(relx=0.01, rely=0.02, relwidth = 0.98, relheight = 0.8)
		#buttons
		self.edit_task_button.place(relx=0.77, rely=0.78, relwidth = 0.2, relheight = 0.15)

	def edit_task_action(self):
		self.destroy()
		task_updator = Task_Entry_Window(self.master_window)
		task_updator.update_task(self.goal_entry)
		
#****************End class*****************#




#----------------Begin class---------------#

class Profile_Editor_Window(Toplevel_Window_Husk):
	
	'''
	Description
    -----------
	This class provides the Task Entry window GUI.

    Attributes
    ----------
    profile_table: Profile database table
    	stores profile details
    frame1, frame2 : tkinter Frame widgets
    	contain all wigdets.
    name_label_frame, title_label_frame: tkinter Labelframe widgtes
    	decorative widgets
    profile_picture_label : tkinter Label widget
    	displays profile picture.
    profile_name_entry : tkinter Entry widget
    	allows user to type in a custom profile name.
    profile_title_entry : tkinter Entry widget
    	allows user to type in a custom profile title.
    change_picture_button : tkinter Button widget.
    	allows user to select a new profile picture.
    save_changes_button : tkinter Button widget.
    	allows user to save changes they have made to the current profile account.

    Methods
    -------
	prepare_widgets(): void
		prepares sub-widgets ready for display
	superimpose_widgets(): void
    	places widgets ontop of toplevel window.
    change_picture_action() : void
    	opens a file dialogue, allowing user to select an image file.
    save_changes_action() : void
    	stores user input into database and terminates toplevel window.
	'''

	frame_color1 = "#777777"
	frame_color2 = "#DDDDDD"

	def __init__(self, root):
		super().__init__(root)
		self.setup_master_window('Profile Editor', 500, 500)

		#supporting fields
		self.profile_table = Profile_table()
		self.profile_picture = None
		try:
			self.profile_name, self.profile_title = self.profile_table.get_profile()[0]
		except:
			self.profile_name, self.profile_title = ('User', 'New')

		#widgets
		self.frame1 = tk.Frame(self, bg = self.frame_color1)
		self.frame2 = tk.Frame(self, bg = self.frame_color2)

		self.name_label_frame = tk.LabelFrame(self.frame2, bg = self.frame_color2, text = 'Name')
		self.title_label_frame = tk.LabelFrame(self.frame2, bg = self.frame_color2, text = "Title")

		self.profile_picture_label = tk.Label(self.frame1, bg = self.frame_color1, bd = 0)

		self.profile_name_entry = tk.Entry(self.name_label_frame, bg = self.frame_color2, bd = 0)
		self.profile_title_entry = tk.Entry(self.title_label_frame, bg = self.frame_color2, bd = 0)

		self.change_picture_button = tk.Button(self.frame1, bg = self.frame_color1, command = self.change_picture_action)
		self.save_changes_button = tk.Button(self.frame2, bg = self.frame_color2, command = self.save_changes_action)

	def prepare_widgets(self):
		#config font
		self.profile_name_entry.configure(font =('arial', 9, 'italic', 'bold'))
		self.profile_title_entry.configure(font =('arial', 9, 'italic', 'bold'))
		#config text
		self.profile_name_entry.insert(0, self.profile_name)
		self.profile_title_entry.insert(0, self.profile_title)
		#config cursors
		self.save_changes_button.configure(cursor = 'hand2')
		self.change_picture_button.configure(cursor = 'hand2')
		#config button graphics
		try:
			profile_picture = graphics_toolkit.icons_folder_path + r'\profile_picture.png'
			graphics_toolkit.superimpose_image_to_Widget(self.profile_picture_label, profile_picture, (200, 200))
		except:
			#display default user profile picture
			profile_picture = graphics_toolkit.icons_folder_path + r'\user.png'
			graphics_toolkit.superimpose_image_to_Widget(self.profile_picture_label, profile_picture, (200, 200))

		camera_picture = graphics_toolkit.icons_folder_path + r'\camera.png'
		save_picture = graphics_toolkit.icons_folder_path + r'\edit_profile.png'

		graphics_toolkit.superimpose_image_to_Widget(self.change_picture_button, camera_picture, (60, 60))
		graphics_toolkit.superimpose_image_to_Widget(self.save_changes_button, save_picture, (70, 70))

	def superimpose_widgets(self):
		#frames
		self.frame1.place(relx=0, rely=0, relwidth = 1, relheight = 0.6)
		self.frame2.place(relx=0, rely=0.61, relwidth = 1, relheight = 0.4)
		#label frames 
		self.name_label_frame.place(relx=0.25, rely=0.4, relwidth = 0.55, relheight = 0.25)
		self.title_label_frame.place(relx=0.25, rely=0.1, relwidth = 0.55, relheight = 0.25)
		#label
		self.profile_picture_label.place(relx=0.28, rely=0.1, relwidth = 0.5, relheight = 0.7)
		#entry widgets
		self.profile_name_entry.place(relx=0.01, rely=0.01, relwidth = 0.98, relheight = 0.98)
		self.profile_title_entry.place(relx=0.01, rely=0.01, relwidth = 0.98, relheight = 0.98)
		#buttons
		self.change_picture_button.place(relx=0.63, rely=0.67, relwidth = 0.13, relheight = 0.21)
		self.save_changes_button.place(relx=0.83, rely=0.6, relwidth = 0.15, relheight = 0.35)

	def change_picture_action(self):
		new_image = filedialog.askopenfilename()
		try:
			self.profile_picture = graphics_toolkit.circle_crop_image(new_image)
			graphics_toolkit.superimpose_image_to_Widget(self.profile_picture_label, new_image, (200, 200))
		except Exception as ex:
			print(ex)
			error_msg = "Error! Invalid format, please select a different image file."
			messagebox.showwarning("INVALID FILE!", error_msg)

	def save_changes_action(self):
		new_profile_data = (self.profile_name_entry.get(), self.profile_title_entry.get())
		self.profile_table.insert_new_profile_entry(new_profile_data)
		try:
			graphics_toolkit.save_image(self.profile_picture)
			self.master_window.prepare_frame1_widgets()
		except Exception as ex:
			print(ex)
		self.destroy()
		self.master_window.prepare_frame1_widgets()

#****************End class*****************#





#----------------Begin class---------------#

class About_Window(Toplevel_Window_Husk):

	'''
	Description
    -----------
	This class provides the About window GUI.

    Attributes
    ----------
    copyright_text: string
    	copyright information.
    frame1: tkinter Frame widgets
    	contain all wigdets.
    objective_title_label : tkinter Label widget
    	displays application name.
    copyright_label_frame : tkinter Labelframe widgtes
    	contains the copyright text area widget.
    copyright_text_area : tkinter Text area widget
    	displays the copyright text.
    hypertext_link : tkinter Label widget.
    	hyper text link that allows a user to access the Objective description website.

    Methods
    -------
	prepare_widgets(): void
		prepares sub-widgets ready for display
	superimpose_widgets(): void
    	places widgets ontop of toplevel window.
    hypertext_link_action() : void
    	opens the browser to access the Objective description website.
	'''

	frame_color1 = "#C0C0C0"

	def __init__(self, root):
		super().__init__(root)
		self.setup_master_window('About', 600, 500)

		#supporting fields
		self.copyright_text = '' 
		copyright_file = graphics_toolkit.resources_folder_path + r'\Database_Storage\MIT License.txt'
		with open(copyright_file, "r") as file:
			self.copyright_text = file.read()	
		#widgets
		self.frame1 = tk.Frame(self, bg = self.frame_color1)

		self.objective_title_label = tk.Label(self.frame1, bg = self.frame_color1, bd = 0)
		self.copyright_label_frame = tk.LabelFrame(self.frame1, bg = self.frame_color1, text = 'Copyright')
		self.copyright_text_area = tk.Text(self.copyright_label_frame, bg = self.frame_color1, bd = 0)
		self.hypertext_link = tk.Label(self.frame1, bg = self.frame_color1, bd = 0)

	def prepare_widgets(self):
		#config font
		self.objective_title_label.configure(font =('MV Boli', 40))
		self.copyright_text_area.configure(font =('arial', 9))
		self.hypertext_link.configure(font =('arial', 15, 'italic'))
		#config text
		self.objective_title_label.configure(text = "OBJECTIVE")
		self.copyright_text_area.insert(0.0, self.copyright_text)
		self.copyright_text_area.configure(state  = 'disabled')
		self.hypertext_link.configure(anchor = 'w')
		self.hypertext_link.configure(text = "[More information...]")
		#config cursors
		self.hypertext_link.configure(cursor = 'hand2')
		#config callback action
		self.hypertext_link.bind("<Button-1>", self.hypertext_link_action)

	def superimpose_widgets(self):
		#frames
		self.frame1.place(relx=0, rely=0, relwidth = 1, relheight = 1)
		#widgets
		self.objective_title_label.place(relx=0.1, rely=0.01, relwidth = 0.8, relheight = 0.15)
		self.copyright_label_frame.place(relx=0.01, rely=0.17, relwidth = 0.98, relheight = 0.7)
		self.copyright_text_area.place(relx=0.01, rely=0.01, relwidth = 0.98, relheight = 0.98)
		self.hypertext_link.place(relx=0.03, rely=0.87, relwidth = 0.4, relheight = 0.1)

	def hypertext_link_action(self, event):
		website_link = "https://hashnode.com/post/objective-task-reminder-software-ckxc1prlh00au1ts1fd4x1llh"
		try:
			webbrowser.open_new(website_link)
		except Exception as ex:
			error_msg = "Error! Something went wrong."
			messagebox.showwarning("Error!", error_msg)

#****************End class*****************#




#----------------Begin class---------------#

class Objective_App_Window(tk.Tk):


	'''
	Description
    -----------
	This class provides the Main window GUI for the Objective Software.

    Attributes
    ----------
    activites_table, machine_voice, machine_clock, profile_info, random_quote: objects
    	supporting variables.
    frame1, frame2, frame3 : tkinter Frame widgets
    	contain all wigdets.
    profile_picture_label, profile_name_label, today_date_label : tkinter widgets
    	frame1 wigdets.
    datetime_label_frame, today_time_label, today_date_label : tkinter widgets
    	frame2 wigdets.
    all_task_label_frames, quote_display_text, add_task_button : tkinter widgets
    	frame3 wigdets.

    Methods
    -------
    setup_master_window(title, width, height) : void
    	set the basic properties of the window with with the paramitrized values.
    prepare_frame1_widgets(), prepare_frame2_widgets(), prepare_frame3_widgets(): void
		prepares sub-widgets ready for display
	superimpose_widgets(): void
    	places widgets ontop of the main window.
    superimpose_new_task_label_widget(): void
    	places a task label frame widget ontop of the main window.
    display_all_goal_entries(): void
    	places all task label frame widget ontop of the main window.
    restore_goal_entries_displays() : void
    	updates the task label frames display.
    update_datetime_display() : void
    	updates the frame 2 every 3 seconds
    edit_profile_action() void
    	launches the profile editor window.
    add_task_action() : void
    	launches the task entry window.
    initialize_window() : void
    	prepares the Toplevel window for display.
    launch_window() : void
    	displays window.

	'''
	
	frame_color1 = '#e6e6e6'
	frame_color2 = '#999999'
	frame_color3 = '#D3D3D3'

	task_label_frame_vertical_position_count = 0.01

	def __init__(self):
		tk.Tk.__init__(self)

		#supporting fields
		self.activites_table = Activities_table()
		self.profile_table = Profile_table()
		self.machine_voice = Text_To_Speech()
		self.machine_clock = Clock()
		try:
			self.profile_info = self.profile_table.get_profile()[0]
		except:
			new_profile = ('User', 'New')
			self.profile_table.insert_new_profile_entry(new_profile)
			self.profile_info = self.profile_table.get_profile()[0]

		self.random_quote = random.choice(Quotes_table().get_all_quotes())
		
		#frames
		self.frame1 = tk.Frame(self, bg = self.frame_color1)
		self.frame2 = tk.Frame(self, bg = self.frame_color2)
		self.frame3 = tk.Frame(self, bg = self.frame_color3)

		#frame 1 wigets
		self.profile_picture_label = tk.Label(self.frame1, bg = self.frame_color1)
		self.profile_name_label = tk.Label(self.frame1, bg = self.frame_color1)
		self.edit_profile_button = tk.Button(self.frame1, bg = self.frame_color1, command = self.edit_profile_action)

		#frame 2 widgets
		self.datetime_label_frame = tk.LabelFrame(self.frame2, bg = self.frame_color2)
		self.today_time_label = tk.Label(self.datetime_label_frame, bg = self.frame_color2)
		self.today_date_label = tk.Label(self.datetime_label_frame, bg = self.frame_color2)

		#frame 3 wigets
		self.all_task_label_frames = []
		self.quote_display_text = tk.Text(self.frame3, bg = self.frame_color3, bd = 0)
		self.about_button = tk.Button(self.frame3, bg = self.frame_color3, text = 'About', command = self.about_action)
		self.add_task_button = tk.Button(self.frame3, bg = self.frame_color3, text = 'Add Task', command = self.add_task_action)

	def setup_master_window(self, title = 'OBJECTIVE: Task Reminder', width = 900, height = 600):
		self.title(str(title))
		self.configure(background= "black")
		#display window in the middle of the screen
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()
		x_cordinate = int((screen_width/2) - (width/2))
		y_cordinate = int((screen_height/2) - (height/2))
		self.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate-20))

	def set_window_icon(self):
		objective_icon =  graphics_toolkit.icons_folder_path + r'\monkey_ico.ico'
		self.iconbitmap(objective_icon)

	#widget preparation
	def prepare_frame1_widgets(self):
		#config profile name label
		self.profile_name_label.configure(fg = '#36454F')
		self.profile_name_label.configure(font =('Verdana', 20, 'bold'))
		self.profile_name_label.configure(text = self.profile_info[0])

		#config edit button
		self.edit_profile_button.configure(font =('Verdana', 10, 'bold', 'italic'))
		self.edit_profile_button.configure(text = "Edit Profile")
		self.edit_profile_button.configure(cursor = 'hand2')
		self.edit_profile_button.configure(border = 0)

		#config profile button graphics
		try:
			profile_picture = graphics_toolkit.icons_folder_path + r'\profile_picture.png'
			graphics_toolkit.superimpose_image_to_Widget(self.profile_picture_label, profile_picture, (130, 130))
		except:
			#display default user profile picture
			profile_picture = graphics_toolkit.icons_folder_path + r'\user.png'
			graphics_toolkit.superimpose_image_to_Widget(self.profile_picture_label, profile_picture, (130, 130))

	def prepare_frame2_widgets(self):
		dd, mm, yy = self.machine_clock.get_date()
		date_text = f"{self.machine_clock.get_day_of_week()}, {dd} {mm[0:3]} {yy}"
		time_text =self.machine_clock.get_time()

		#config font
		self.today_time_label.configure(font =('arial', 40, 'bold'))
		self.today_time_label.configure(fg = '#36454F')
		self.today_date_label.configure(font =('arial', 15, 'italic', 'bold'))
		#config text
		self.today_time_label.configure(text = f"{time_text[0]}:{time_text[1]} {time_text[2]}")
		self.today_date_label.configure(text = date_text)

	def prepare_frame3_widgets(self):
		#config text
		self.quote_display_text.configure(font =('Calibri', 11, 'italic', 'bold'))
		self.quote_display_text.insert(0.0, f"'{self.random_quote[0]}' \n-{self.random_quote[1]}")
		self.quote_display_text.configure(state  = 'disabled')
		#config  button cursor
		self.add_task_button.configure(cursor = 'hand2')
		self.about_button.configure(cursor = 'hand2')
		#config  button graphics
		about_picture = graphics_toolkit.icons_folder_path + r'\help.png'
		graphics_toolkit.superimpose_image_to_Widget(self.about_button, about_picture, (38, 37))

		add_picture = graphics_toolkit.icons_folder_path + r'\add.png'
		graphics_toolkit.superimpose_image_to_Widget(self.add_task_button, add_picture, (100, 100))

	#widgets superimposition
	def superimpose_widgets(self):
		#frames
		self.frame1.place(relx=0, rely=0, relwidth = 0.33, relheight = 0.3)
		self.frame2.place(relx=0, rely=0.301, relwidth = 0.33, relheight = 0.699)
		self.frame3.place(relx=0.331, rely=0, relwidth = 0.67, relheight = 1)

		#for frame1
		self.profile_picture_label.place(relx=0.02, rely=0.03, relwidth = 0.5, relheight = 0.8)
		self.profile_name_label.place(relx=0.51, rely=0.03, relwidth = 0.4, relheight = 0.7)
		self.edit_profile_button.place(relx=0.02, rely=0.82, relwidth = 0.5, relheight = 0.1)

		#for frame2
		self.datetime_label_frame.place(relx=0.02, rely=0.03, relwidth = 0.97, relheight = 0.3)
		self.today_time_label.place(relx=0.1, rely=0.1, relwidth = 0.85, relheight = 0.45)
		self.today_date_label.place(relx=0.1, rely=0.65, relwidth = 0.85, relheight = 0.25)
		
		#for frame 3
		self.quote_display_text.place(relx=0.01, rely=0.83, relwidth = 0.65, relheight = 0.16)
		self.about_button.place(relx=0.89, rely=0.01, relwidth = 0.07, relheight = 0.07)
		self.add_task_button.place(relx=0.75, rely=0.8, relwidth = 0.2, relheight = 0.19)

	#supporting methods
	def superimpose_new_task_label_widget(self, param_goal_entry):
		task_label_frame = Task_label_frame(self, self.frame3, param_goal_entry)
		task_label_frame.place(relx=0.01, rely= self.task_label_frame_vertical_position_count, relwidth = 0.85, relheight = 0.07)
		self.task_label_frame_vertical_position_count += 0.08
		#store task label frame in all_task_label_frames list
		self.all_task_label_frames.append(task_label_frame)

	def display_all_goal_entries(self):
		#extract all goal/task entries from database
		all_goal_entries = self.activites_table.get_all_goals()
		#display all goal entries
		for goal_entry in all_goal_entries:
			self.superimpose_new_task_label_widget(goal_entry)

	def restore_goal_entries_displays(self):
		#remove current goal entries display
		for task_label_frame in self.all_task_label_frames:
			task_label_frame.destroy()
		#display updated goal entries
		self.all_task_label_frames = []
		self.task_label_frame_vertical_position_count = 0.01
		self.display_all_goal_entries()

	def update_datetime_display(self):
		self.prepare_frame2_widgets()
		self.after(5000, self.update_datetime_display)

	#action handler methods
	def edit_profile_action(self):
		profile_editor = Profile_Editor_Window(self)
		profile_editor.launch_window()

	def about_action(self):
		about_window = About_Window(self)
		about_window.launch_window()

	def add_task_action(self):
		total_num_of_goal_entries = len(self.activites_table.get_all_goals())
		if(total_num_of_goal_entries < 9):
			task_entry_window = Task_Entry_Window(self)
			task_entry_window.launch_window()
		else:
			error_msg = "OVERFLOW! Progress is all about execution. Complete some of the tasks already on your list so that you add others later."
			messagebox.showwarning("ECXEEDED MAX WORKLOAD CAPACITY!", error_msg)

	#display main window
	def initialize_window(self):
		self.setup_master_window()
		self.set_window_icon()
		self.prepare_frame1_widgets()
		self.prepare_frame2_widgets()
		self.prepare_frame3_widgets()
		self.superimpose_widgets()
		self.display_all_goal_entries()

	def launch_window(self):
		self.initialize_window()
		self.machine_voice.articulate_breifing(self.machine_clock, self.profile_info, self.activites_table.get_all_goals(), self.random_quote)
		self.update_datetime_display()
		self.mainloop()

#****************End class*****************#

