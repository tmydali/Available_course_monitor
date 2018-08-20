import time, os, psycopg2
import threading as thrd
from .websiteParser import Course_list
from . import sender


def multithrd(userID, DeptNo, CrsNo, dept):
	t = thrd.Thread(target = checkCourse, args = (
		userID, DeptNo, CrsNo, dept))
	t.start()


def checkCourse(userID, DeptNo, CrsNo, dept):
	is_1st_round = True
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
				
			if is_1st_round == True:
				write_database(
					'''
					INSERT INTO user_data 
					VALUES (%s, %s, %s, %s, %s)
					''', 
					(userID, DeptNo, CrsNo, CrsName, False)
					)
			
			if CrsSpace >= 10:
				sender.message_sender(
					userID,
					"{0:s} {1:s} {2:s}\n有空位了！快搶".format(
						DeptNo,CrsNo,CrsName))
				write_database(
					'''
					UPDATE user_data 
					SET done = True
					WHERE 
						user_id = %(userID)s AND
						department = %(DeptNo)s AND
						course_no = %(CrsNo)s
					''',
					{'userID':userID, 'DeptNo':DeptNo, 'CrsNo':CrsNo}
					)
				print("{0:s} is available!".format(CrsName))
				break
				
			elif is_1st_round == True and CrsSpace < 10:
				sender.message_sender(
					userID,
					"{0:s} {1:s} {2:s}額滿了\n有餘額時會通知喔~".format(
						DeptNo,CrsNo,CrsName))
				print("{0:s} is almost out of space!".format(CrsName))
			
			is_1st_round = False
			time.sleep(2)
			
	except KeyError:
		sender.message_sender(
			userID,
			"找不到 {0:s} {1:s} 這堂課耶".format(
					DeptNo, CrsNo))
		print("Course not found!\n")
		
		
def  write_database(command, data):
	DATABASE_URL = os.environ['DATABASE_URL']
	conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
	c = conn.cursor()
	c.execute(command, data)
	conn.commit()
	conn.close()
					