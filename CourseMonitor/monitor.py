import time, sqlite3
import threading as thrd
from .websiteParser import Course_list
from . import sender


def multithrd(DeptNo, CrsNo, dept, userID):
	conn = sqlite3.connect('user_data.db')
	t = thrd.Thread(target = checkCourse, args = (
		userID, DeptNo, CrsNo, dept, conn))
	c = conn.cursor()
	c.execute("""INSERT INTO users
		VALUES(?, ?, ?, ?, ?, ?)""", (userID, None, DeptNo, CrsNo, t, None))
	conn.commit()
	t.start()


def checkCourse(userID, DeptNo, CrsNo, dept, conn):
	c = conn.cursor()
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
				c.executescript("""
					UPDATE users
					SET CourseName = ?, stopped = True
					WHERE ? AND ? AND ?
					""", (CrsName, userID, DeptNo, CrsNo))
				conn.commit()
				conn.close()
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