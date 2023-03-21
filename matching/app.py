################################################################################
#   Import Modules
################################################################################
from pdb import find_function
from re import split
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# import pymysql
import cs304dbi as dbi
import random
from prepared_queries import *

################################################################################
app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True


################################################################################
#   Routing functions
################################################################################
@app.route('/', methods=['GET','POST'])
def index():
    # conn = pymysql.connect(read_default_file='~/.my.cnf', database='wmdb')
    conn = dbi.connect()
    if request.method == 'GET':
        depts = get_depts(conn)
        return render_template('index.html', page_title='Home', depts=depts)
    else:
        for n in range(0, 32): # range is the n# of total courses they can input
            dept = request.form.get('dept-'+str(n))
            cnum = request.form.get('cnum-'+str(n))
            if dept not in [None, ''] and cnum not in [None, '']:
                cnum = cnum.upper().strip()
                
                # if course doesnt exist
                if not check_course_exists(conn, dept, cnum):
                    flash(str(dept) + ' ' + str(cnum) + 
                          " doesn't exist in our database")
                # if course does exist
                insert_data(conn, dept, cnum)
        results = major_match(conn)
        course_matches = matched_courses(conn)        
        delete_form_data(conn)
        
        # get all the courses in each department
        dept_courses = (
        [(get_dept_courses(conn, results[i][2])) for i in range(len(results))]
        )

        courses_to_take_dict = {
            results[i][0]: dept_courses[i] for i in range(len(results))
        }

        # find the % of courses that have been taken for each matched major
        percentage = [
            format((results[i][1] / len(dept_courses[i])), '.0') 
            for i in range(len(results))
            ]
        p = [(int((float(x)*100)),'') for x in percentage]
        # results = (major, 
        #            count matched courses, 
        #            dept_id, percent courses taken,
        #            empty string)
        results = [results[i]+ tuple(p[i]) for i in range(len(results))]

        # put the courses with the majors they fulfill 
        courses_taken_dict = {
            course_matches[i][1]:[] for i in range(len(course_matches))
        }
        for i in range(len(course_matches)):
            courses_taken_dict[course_matches[i][1]].append(
                course_matches[i][0]
            )

        # (-) courses taken from dept courses and put still needed into dict
        for major in courses_to_take_dict:
            # get the taken courses and subtract from the dept courses
            courses_to_take_dict[major] = list(
                set(courses_to_take_dict[major])-set(courses_taken_dict[major])
                )
        return render_template('results.html',
                                page_title='Results',
                                results = results,
                                course_matches = course_matches,
                                courses_to_take_dict = courses_to_take_dict
                                )

@app.route('/contact/')
def contact():
    return render_template('contact.html',
                            page_title='Contact Us!')

################################################################################
@app.before_first_request
def init_db():
    dbi.cache_cnf()
    db_to_use = 'majormatch_db' 
    dbi.use(db_to_use)
    # pymysql.select_db(db)
    print('will connect to {}'.format(db_to_use))

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
