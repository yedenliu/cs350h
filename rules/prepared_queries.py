import cs304dbi as dbi

def get_courses(conn):
    curs = dbi.cursor(conn)
    sql =   ''' select distinct dept, cnum 
                from courses 
                where dept <> ""
                and cnum <> ""
                order by dept asc 
            '''
    curs.execute(sql)
    courseTups = curs.fetchall()
    courseList = [i[0] + i[1] for i in courseTups]
    return courseList


def get_abbrev(conn):
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


def get_dept_courses(conn, abbrev):
    '''
    Finds courses given an department abbreviation
    
    Param - connection object, department abbreviation 
    Return - list of courses (in form CS 111)
    '''
    curs = dbi.cursor(conn)
    
    sql =   ''' select dept, cnum from courses 
                where dept = %s
            '''
    curs.execute(sql, [abbrev])
    return curs.fetchall()

def get_dept_courses(conn, abbrev):
    '''
    Finds courses given an department abbreviation
    
    Param - connection object, department abbreviation 
    Return - list of courses
    '''
    curs = dbi.cursor(conn)
    
    sql =   ''' select dept, cnum from courses 
                where dept = %s and cnum =%s
            '''
    curs.execute(sql, [abbrev])
    return curs.fetchall()

def get_two_level(conn, abbrev):
    '''
    Finds courses given an department abbreviation at the 200-level
    
    Param - connection object, department abbreviation 
    Return - list of courses
    '''
    curs = dbi.cursor(conn)
    level = '2%'
    sql =   ''' select dept, cnum
                from courses 
                where dept = %s
                and cnum like %s
            '''
    curs.execute(sql, [abbrev, level])
    return curs.fetchall()

def get_three_level(conn, abbrev):
    '''
    Finds courses given an department abbreviation at the 300-level
    
    Param - connection object, department abbreviation 
    Return - list of courses
    '''
    curs = dbi.cursor(conn)
    level = '3%'
    sql =   ''' select dept, cnum
                from courses 
                where dept = %s
                and cnum like %s
            '''
    curs.execute(sql, [abbrev, level])
    return curs.fetchall()
