# ==============================================================================
#   Import Modules
# ==============================================================================
from pdb import find_function
from re import split
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

import cs304dbi as dbi
from prepared_queries import *

import logging 
logging.basicConfig(filename='/students/majormatch/app.log', filemode='w', format='%(levelname)s:%(message)s', level=logging.DEBUG)

import json
import unicodedata

# ==============================================================================
#   Routing functions
# ==============================================================================
@app.route('/', methods=['GET','POST'])
def index():
    conn = dbi.connect()
    if request.method == 'GET':
        depts = get_abbrev(conn)
        return render_template('index.html', page_title='Major Requirements',
                           depts = depts)
    else:
        deptName = request.form['deptName']
        return redirect(url_for('deptPage', deptName = deptName))

@app.route('/<deptName>')
def deptPage(deptName):
    conn = dbi.connect()
    depts = get_abbrev(conn)
    courses = get_courses(conn)
    rules = None
    if check_rules_exist(conn, deptName)!=0:
        rulesTups = get_rules(conn, deptName)
        logging.debug(rulesTups)
        try: 
            rules = json.loads(rulesTups[0][0])          
        except:
            logging.debug('Prepared query output is weirdly formatted')
            logging.debug(rulesTups)
    logging.debug(rules)
    return render_template('rules.html', page_title='Add Rules',
                           depts = depts,
                           courses = courses,
                           rules = rules)

@app.route('/200levels/<dept>')
def add200(dept):
    '''
    Routing function for 200-level quick add
    '''
    conn = dbi.connect()
    level200 = get_two_level(conn, dept) 
    return jsonify(level200 = level200)
   
@app.route('/300levels/<dept>')
def add300(dept):
    '''
    Routing function for 300-level quick add
    '''
    conn = dbi.connect()
    level300 = get_three_level(conn, dept) 
    return jsonify(level300 = level300)


@app.route('/rules/<dept>')
def getRules(dept):
    '''
    Routing function for rules refresh
    '''
    conn = dbi.connect()
    rules = None
    if check_rules_exist(conn, dept)!=0:
        rulesTups = get_rules(conn, dept)
        logging.debug(rulesTups)
        try: 
            rules = json.loads(rulesTups[0][0])          
        except:
            logging.debug('Prepared query output is weirdly formatted')
            logging.debug(rulesTups)
    logging.debug(rules)
    return jsonify(rules = rules)

@app.route('/submit/<dept>', methods=['POST'])
def submit(dept):
    '''
    Routing function for submitting a major into the database
    '''
    conn = dbi.connect()

    # Getting rules in form of string that needs to be converted
    string = request.form['majorJSON']

    # Convert string to JSON
    majorJSON = json.loads(str(string))

    # Getting deptName and rules from JSON
    deptName = majorJSON['deptName']
    deptName = str(deptName)
    rules = json.dumps(majorJSON['rules'])
    
    add_major(conn, deptName, rules)
    return redirect(url_for('deptPage', deptName = dept))

################################################################################
@app.before_first_request
def init_db():
    dbi.cache_cnf()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'majormatch_db' 
    dbi.use(db_to_use)
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
 