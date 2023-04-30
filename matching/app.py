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
    conn = dbi.connect()
    depts = get_depts(conn)
    if request.method == 'GET':
        return render_template('index.html', page_title='Home', depts=depts)
    else:
        # STEP 1: Create courseList of user's inputted courses
        courseList = []
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
                courseList.append(dept + ' ' + cnum)
        
        # STEP 2: Get progress of each major
        progress_list = []
        for d in depts: # For each dept, get the rules
            rules = None
            if check_rules_exist(conn, d)!=0:
                rulesTups = get_rules(conn, d)
                # logging.debug(rulesTups)
                try: 
                    rules = json.loads(rulesTups[0][0])          
                except:
                    logging.debug('Prepared query output is weirdly formatted')
                    logging.debug(rulesTups)
            # logging.debug(rules)
        
            major_progress = parseMajor(d, rules, courseList)
            progress_list.append(major_progress)
        
        progress_list.sort(key=lambda x: x[1])
        # What is in each major's list: [dept, progress, unitsLeft, rulesCompleted, rulesLeft]
        matchList = progress_list[:2]
        return jsonify(matchList = matchList)

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
