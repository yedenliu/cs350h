import cs304dbi as dbi
import logging, json

logging.basicConfig(filename='/students/majormatch/queries.log', 
                    filemode='w', format='%(levelname)s:%(message)s', 
                    level=logging.DEBUG)

def get_depts(conn):
    curs = dbi.cursor(conn)
    sql =   ''' select distinct dept 
                from courses 
                where dept <> ""
                order by dept asc 
            '''
    curs.execute(sql)
    deptsTups = curs.fetchall()
    deptsList = [i[0] for i in deptsTups]
    return deptsList

def check_course_exists(conn, dept, cnum):
    curs = dbi.cursor(conn)
    sql = '''   select cid from courses
                where dept = %s and cnum = %s
            '''
    curs.execute(sql, [dept, cnum])
    return len(curs.fetchall()) > 0

def check_rules_exist(conn, dept):
    '''
    Checks if rules for a department exist in the database
    Returns true if exists 
    '''
    curs = dbi.cursor(conn)
    sql =   ''' select count(rules)
                from jsons 
                where dept = %s
            '''
    curs.execute(sql, [dept])
    count = curs.fetchone()
    return count[0]

def get_rules(conn, dept):
    curs = dbi.cursor(conn)
    sql =   ''' select rules
                from jsons 
                where dept = %s
            '''
    curs.execute(sql, [dept])
    return curs.fetchall()


# --- MATCHING FUNCTIONS ----

def ruleCheck(courseList, relevantList, requirementNum):
  '''
  HELPER FOR parseMajor()
  Checks if enough course are taken from a list of applicable courses

  Params - courseList: user's course list
          relevantList: courses that apply to rule
          requirement: how many courses they need to fulfill

  Return - True if requirements are fulfilled. False otherwise
  '''
  courseCount = 0 # how many courses have been fulflled
  countedCourses = []
  for course in courseList:
      if course in relevantList:
          courseCount += 1
          countedCourses.append(course)
          if courseCount == requirementNum:
              return (courseCount, True, countedCourses)
  return (courseCount, False, countedCourses)

def parseMajor(dept, rules, courseList):
    '''
    Takes in a user's course list and a department's major requirement JSON with 
    the relevant rules, giving back the user's major progress

    Param - dept: department abbreviation
            rules: list of rules
            courseList: list of user's taken courses
    Return - matchList (sent to the front-end)
    '''
    totalUnits = 0
    studentUnits = 0
    currentCourses = courseList
    rulesCompleted = []
    rulesLeft = []
    for rule in rules:
        requirementNum = rule['op'].split('-')[1]
        totalUnits += requirementNum
        relevantList = rule['arg']
        courseCount, isFulfilled, countedCourses = ruleCheck(currentCourses, relevantList, requirementNum)
        currentCourses = list(set(currentCourses) ^ set(countedCourses)) # a course can only be counted for one rule 
        studentUnits += courseCount
    
    if isFulfilled:
        rulesCompleted.append(rule)
    else:
        rulesLeft.append(rule)

    unitsLeft = totalUnits - studentUnits
    progress = studentUnits/totalUnits
    if studentUnits >= totalUnits: # student can't be more than 100% complete
        progress = 1
        unitsLeft = 0

    return [dept, progress, unitsLeft, rulesCompleted, rulesLeft]

# --- ARCHIVE ------------------------------------------------------------------
# def get_rules(conn, dept):
#     curs = dbi.cursor(conn)
#     sql =   ''' select rules
#                 from jsons 
#                 where dept = %s
#             '''
#     curs.execute(sql, dept)
#     # rulesTups = curs.fetchall()
#     # logging.debug('TESTING RULES')
#     # logging.debug(type(rulesTups))
#     # rulesList = [i[0][0][0] for i in curs]
#     # logging.debug(rulesList)
#     # rules = ast.literal_eval(rulesList)
#     return curs.fetchall()

# def find_cid(conn, dept, cnum):
#     curs = dbi.cursor(conn)
#     sql = '''   select cid from courses
#                 where dept = %s and cnum = %s
#             '''
#     curs.execute(sql, [dept, cnum])
#     return curs.fetchone()

# def insert_data(conn, dept, cnum):
#     curs = dbi.cursor(conn)
#     if dept != None and cnum != None:
#         cid = find_cid(conn, dept, cnum)
#         sql = '''   insert into form_data(dept, cnum, cid)
#                     values (%s, %s, %s)
#                 ''' 
#         curs.execute(sql, [dept, cnum, cid])
#         conn.commit()

# def major_match(conn):
#     curs = dbi.cursor(conn)
#     sql = '''   select programs.name, 
#                 count(major_pairs.dept_id), 
#                 major_pairs.dept_id from programs
#                 inner join major_pairs using(dept_id)
#                 inner join form_data using(cid)
#                 group by major_pairs.dept_id
#                 order by count(major_pairs.dept_id) DESC
#                 limit 5
#             ''' 
#     curs.execute(sql)
#     return curs.fetchall()

# def matched_courses(conn):
#     curs = dbi.cursor(conn)
#     sql = '''   select courses.name, programs.name
#                 from courses
#                 inner join form_data using(cid)
#                 inner join major_pairs using(cid)
#                 inner join programs using(dept_id)
#                 order by programs.name
#             ''' 
#     curs.execute(sql)
#     return curs.fetchall()

# def delete_form_data(conn):
#     curs = dbi.cursor(conn)
#     sql = 'delete from form_data'
#     curs.execute(sql)
#     conn.commit()

# def get_dept_courses(conn, dept_id):
#     '''
#     Finds the courses that count towards majors in a department 
    
#     Param - connection object, department 
#     Return - list of courses 
#     '''
#     curs = dbi.cursor(conn)
    
#     sql =   ''' select dept, cnum, courses.name, courses.cid,
#                 courses.units, courses.max_enroll,
#                 courses.prereq, courses.instruct,
#                 courses.dr, courses.sem_offered,
#                 courses.year_offered
#                 from courses 
#                 inner join major_pairs using(cid)
#                 inner join programs using (dept_id)
#                 where dept_id = %s
#             '''
#     curs.execute(sql, [dept_id])
#     return curs.fetchall()
