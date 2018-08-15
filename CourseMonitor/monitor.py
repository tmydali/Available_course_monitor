import time, sqlite3
import threading as thrd
from .websiteParser import Course_list
from . import sender


def multithrd(userID, DeptNo, CrsNo, dept):
	t = thrd.Thread(target = checkCourse, args = (
		userID, DeptNo, CrsNo, dept))
	#write_database("""INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)""",
	#	(userID, None, DeptNo, CrsNo, None, None))
	t.start()


def checkCourse(userID, DeptNo, CrsNo, dept):
	# set up a loop and wait for several seconds between each turn
	try:
		while True:
			course = Course_list(DeptNo, dept)
			CrsName = course[CrsNo][0]
			try:
				CrsSpace = int(course[CrsNo][1])
			except ValueError:
				CrsSpace = 0;
			except:
				print("Error!")
				break
                
			if CrsSpace >= 10:
				sender.message_sender(
					userID,
					"{0:s} {1:s} {2:s}\n now is available!".format(
						DeptNo,CrsNo,CrsName))
				#write_database(
				#	"""
				#	UPDATE users
				#	SET CourseName = ?, stopped = True
				#	WHERE ? AND ? AND ?
				#	""", 
				#	(CrsName, userID, DeptNo, CrsNo))
				print("{0:s} is available!".format(CrsName))
				break

				
			#print("{0:s}，餘額: {1:s}".format(CrsName, CrsSpace))
			time.sleep(2)
	except KeyError:
		sender.message_sender(
			userID,
			"Could not find {0:s} {1:s}!".format(
					DeptNo, CrsNo))
		print("Course not found!\n")
		
		
		
"""	
def  write_database(command, data):
	conn = sqlite3.connect('user_data.db')
	c = conn.cursor()
	c.execute(command, data)
	conn.commit()
	conn.close()
			
def remove_dead_threads():
    global threads
    threads = {key : t for key, t in threads.items() if t.is_alive()}

def input_dealer(message,dept)
	Q = queue.queue()
	try:
		usr_DeptNo, usr_CrsNo = message.split()
		multithrd(usr_DeptNo, usr_CrsNo, dept, Q)
		CrsName
		return Q.get()
	except:
		print("Format error!\n")
		return "Format error!"
	finally:
		remove_dead_threads()
"""