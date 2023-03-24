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

# ==============================================================================
#   Routing functions
# ==============================================================================
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', page_title='Add Rule')

@app.route('/200levels/<dept>', methods=['GET'])
def add200(dept):
    '''
    Routing function for 200-level quick add
    '''
    conn = dbi.connect()
    two_levels = get_two_level(conn, dept) 
    return jsonify(two_levels = two_levels)
   
@app.route('/300levels/<dept>', methods=['GET'])
def add300(dept):
    '''
    Routing function for 300-level quick add
    '''
    conn = dbi.connect()
    three_levels = get_three_level(conn, dept) 
    return jsonify(three_levels = three_levels)
   
# @app.route('/add', methods=['POST'])
# def add(dept_json):
#     return null

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
