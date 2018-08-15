import requests
from bs4 import BeautifulSoup


def get_site(url):
    response = requests.get(url)
    response.encoding = 'UTF-8'
    soup = BeautifulSoup(response.text , 'html.parser')
    return soup


def Department_list():
    # get the home page
    url = 'http://course-query.acad.ncku.edu.tw/qry'
    soup = get_site(url)
    # print(soup)

    #create a dictionary in the form of {department_No. : site_link} for each department
    dept_all = soup.find('ul',id='dept_list')
    dept = dept_all.find_all('div', 'dept')
    dept_link = []
    for i in dept:
        dept_link.append("http://course-query.acad.ncku.edu.tw/qry/" + i.find('a').get('href'))
    dept_text = []
    for i in dept:
        dept_text.append(i.string)
    dept_no = []
    for string in dept_text:
        dept_no.append(string[string.find('(')+2 : string.find(u' ）')])
    dept_dict = dict(zip(dept_no, dept_link))
    # print(dept_dict)
    return dept_dict

	
def Course_list(DeptNo, dept_dict):
    # create a dictionary in the form of {course_No. : [course_name, Space_Available]}
    soup = get_site(dept_dict[DeptNo])
    
    course_tmp = []
    course_all = []
    course_tmp = soup.find_all('td')
    for row in range(1,int(len(course_tmp)/24)+1):
        course_all.append(course_tmp[24*(row-1):24*row-1])
    course_dict = {}
    for i in course_all:
        if i[2].string == None:
            continue
        course_dict.update({i[2].string: [i[10].string, i[15].string]})
    return course_dict