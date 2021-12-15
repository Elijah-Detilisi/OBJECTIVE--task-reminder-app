



"""
	Author
	-----------
	Bongani Detilisi
	
	Description
    -----------
	    This python script is responsible for handlng the locally stored database
	    for the OBJECTIVE software.

	Classes
	-------- 
		Objective_database_husk, Activities_table, Quotes_table, Profile_table
	
	Attributes
    ----------
    	None

    Methods
    ----------
    	None
"""




#Dependencies
import sqlite3
from abc import ABC, abstractmethod




#----------------Begin class---------------#

class Objective_database_husk(ABC):

	'''
	Description
    -----------
	This class allows for the access to the Objective Database file.

    Attributes
    ----------
    database_name: stri
    	file name of the database file.
	connection : ?
		provides access to the VAES database
	cursor : ?
		allows for the storing and retrieval of data of the database.

    Methods
    -------
	reset_database(table_name): void
		drops the paramitrized table and deletes all of its contents.
	get_all_records(table_name): list
    	return a list with all the entries stored in the paramitrized table.
	'''

	def __init__(self):
		self.database_name = 'Resources\Database_Storage\Objectives_Database.db'
		self.connection = sqlite3.connect(self.database_name)
		self.cursor = self.connection.cursor()
		self.create_table()

	@abstractmethod
	def create_table(self):
		raise NotImplementedError

	def reset_database_table(self, table_name):
		with self.connection:
			sql = 'DELETE FROM '+ table_name
			self.cursor.execute(sql)

	def get_all_records(self, table_name):
		with self.connection:
			sql = "SELECT * FROM "+ table_name
			self.cursor.execute(sql)
			return self.cursor.fetchall()

#****************End class*****************#




#----------------Begin class---------------#

class Activities_table(Objective_database_husk):

	'''
	Description
    -----------
	This class allows for the storing, retrieval and manipulation of the data in the Activities table.

    Attributes
    ----------
    Inherited from Objective_database_husk class.

    Methods
    -------
    create_table(): void
    	creates a new table with columns; title, description, due_date, due_time and progress status
    insert_new_goal_entry(new_goal): void
    	appends a new entry of the parametrized new_goal tuple, storing the info into the database.

    update_goal_title(old_goal, new_goal_title): void
    	replaces the title value of the parametrized old_goal entry with the value
    	of the parametrized new_goal_title
    update_goal_description(old_goal, new_goal_description): void
    	replaces the description value of the parametrized old_goal entry with the value
    	of the parametrized new_goal_description arguement variable.
    update_goal_start_time(old_goal, new_goal_start_time): void
    	replaces the start_time value of the parametrized old_goal entry with the value
    	of the parametrized new_goal_start_time arguement variable.
    update_goal_due_date(old_goal, new_goal_due_date): void
    	replaces the due_date value of the parametrized old_goal entry with the value 
    	of the parametrized new_goal_due_date arguement variable.
    update_goal_progress_status(old_goal, new_goal_progress_status): void
    	replaces the progress_status value of the parametrized old_goal entry with the value 
    	of the parametrized new_goal_progress_status arguement variable.

    update_goal_entry(old_goal, new_goal):void
    	replaces all the values of the parametrized old_goal entry with the values of
    	the parametrized new_goal values.
    remove_goal_entry(my_goal): void
    	drops/deleltes the entry of the parametrized goal.
    get_all_goals(table_name): list
    	return a list with all the entries stored in the Activities table.
	'''

	def __init__(self):
		super().__init__()

	def create_table(self):
		try:
			sql = 	"""CREATE TABLE GOALS (
							title text,
							description text, 
							due_date text, 
							due_time text)
					"""

			self.cursor.execute(sql)
		except:
			pass

	def insert_new_goal_entry(self, new_goal):
		with self.connection:
			sql = ''' INSERT INTO GOALS(title, description, due_date, due_time) VALUES(?,?,?,?) '''
			data = new_goal
			self.cursor.execute(sql, data)

	def update_goal_title(self, old_goal, new_goal_title):
		with self.connection:
			sql = ''' UPDATE GOALS SET title = ? WHERE title = ? AND description = ?'''
			data = (new_goal_title, old_goal[0], old_goal[1], )
			self.cursor.execute(sql, data)

	def update_goal_description(self, old_goal, new_goal_description):
		with self.connection:
			sql = ''' UPDATE GOALS SET description = ? WHERE title = ? AND description = ?'''
			data = (new_goal_description, old_goal[0], old_goal[1], )
			self.cursor.execute(sql, data)

	def update_goal_due_date(self, old_goal, new_goal_due_date):
		with self.connection:
			sql = ''' UPDATE GOALS SET due_date = ? WHERE title = ? AND description = ?'''
			data = (new_goal_due_date, old_goal[0], old_goal[1], )
			self.cursor.execute(sql, data)

	def update_goal_due_time(self, old_goal, new_goal_due_time):
		with self.connection:
			sql = ''' UPDATE GOALS SET due_time = ? WHERE title = ? AND description = ?'''
			data = (new_goal_start_time, old_goal[0], old_goal[1], )
			self.cursor.execute(sql, data)


	def update_goal_entry(self, old_goal, new_goal):
		self.update_goal_title(old_goal, new_goal[0])
		self.update_goal_description(old_goal, new_goal[1])
		self.update_goal_due_date(old_goal, new_goal[2])
		self.update_goal_due_time(old_goal, new_goal[3])

	def remove_goal_entry(self, my_goal):
		with self.connection:
			sql = 'DELETE FROM GOALS WHERE title=? AND description=? AND due_date = ? AND due_time=?'
			data = (my_goal[0], my_goal[1], my_goal[2], my_goal[3],)
			self.cursor.execute(sql, data)

	def get_all_goals(self):
		all_goals = self.get_all_records('GOALS')
		return all_goals

#****************End class*****************#




#----------------Begin class---------------#

class Quotes_table(Objective_database_husk):

	'''
	Description
    -----------
	This class allows for the storing, retrieval and manipulation of the data in the Activities table.

    Attributes
    ----------
    Inherited from Objective_database_husk class.

    Methods
    -------
    create_table(): void
    	creates a new table with columns; quote and qoutee_name.
    insert_new_quote_entry(new_quote): void
    	appends a new entry of the parametrized quote tuple, storing the info into the database.
    populate_quote_table() : void
    	reads inspirational quotes from a text file and stores each quote as an entry into the Quotes table 
    	of the Objective's database.
    get_all_goals(table_name): list
    	return a list with all the entries stored in the Quotes table.
	'''

	def __init__(self):
		super().__init__()

	def create_table(self):
		try:
			sql =	"""CREATE TABLE QUOTES (
                            quote text,
                            qoutee_name text)
                    """
			self.cursor.execute(sql)
		except:
			pass

	def insert_new_quote_entry(self, new_quote):
		with self.connection:
			sql = ''' INSERT INTO QUOTES(quote, qoutee_name) VALUES(?,?) '''
			data = (new_quote[0], new_quote[1])
			self.cursor.execute(sql, data)

	def populate_quote_table(self):
		FILE_PATH = r"Resources\Database_Storage"
		file_name = r"\Inspiritional_quotes.txt"
		inspirational_quotes_file = FILE_PATH + file_name
		quotes = []
		#open text file 
		try:
			file = open(inspirational_quotes_file, encoding="utf8")
			quotes = file.read()
			quotes = quotes.split('\n')
		except:
			print(f"Error: {ex}")
		finally:
			file.close()
		#store text contents into the Qoutes table.
		for quote in quotes:
			self.insert_new_quote_entry(quote.split('-'))

	def get_all_quotes(self):
		all_quotes = self.get_all_records('QUOTES')
		if(len(all_quotes) == 0):
			self.populate_quote_table()
			all_quotes = self.get_all_records('QUOTES')

		return all_quotes

#****************End class*****************#




#----------------Begin class---------------#

class Profile_table(Objective_database_husk):

	'''
	Description
    -----------
	This class allows for the storing, retrieval and manipulation of the data in the Profile table.

    Attributes
    ----------
    Inherited from Objective_database_husk class.

    Methods
    -------
    create_table(): void
    	creates a new table with columns; profile name and profile title.
    insert_new_profile_entry(new_profile): void
    	appends a new entry of the parametrized profile tuple, storing the info into the database.
    get_profile(): list
    	return a list with all the entries stored in the Profile table.
	'''

	def __init__(self):
		super().__init__()

	def create_table(self):
		try:
			sql =	"""CREATE TABLE PROFILE (
                            name text,
                            title text)
                    """
			self.cursor.execute(sql)
		except:
			pass

	def insert_new_profile_entry(self, new_profile):
		with self.connection:
			self.reset_database_table('PROFILE')
			sql = ''' INSERT INTO PROFILE(name, title) VALUES(?,?) '''
			data = (new_profile[0], new_profile[1])
			self.cursor.execute(sql, data)

	def get_profile(self):
		profile = self.get_all_records('PROFILE')
		return profile

#****************End class*****************#
