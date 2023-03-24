'''Module to read MySQL database credentials and access databases as the
MySQL user.

This module is designed to work with the pymysql package and make it
easier to read the database credentials from the standard ~/.my.cnf file,
or any file of similar format.  Doing so avoids putting those credentials
in the source code and removes that dependency from the code.

EXAMPLE USAGE

import cs304dbi as dbi

dbi.conf(db='some_db')
conn = dbi.connect()
curs = dbi.cursor(conn)                    # or dbi.dictCursor(conn) 
                                           # or dbi.dict_cursor(conn)

curs.execute('select * from table where id = %s',[some_id])
vals = curs.fetchall()
curs.execute('insert into table values(%s,%s)',[col1,col2])
conn.commit()                              # necessary after insert/update/delete

USAGE DETAIL

import cs304dbi as dbi

Use one of the following to read the credentials (DSN) file

dsn = dbi.read_cnf(db=some_db)
dsn = dbi.read_cnf('~/.my.cnf',db=some_db)
dsn = dbi.read_cnf('/path/to/any/dsn_file',db=some_db)

Or use dbi.cache_cnf() in the same way.

Your credentials file typically specify a database to connect to in
the [mysql] section. You can optionally assign or modify that value in
either of these functions (which will apply to subsequent connections)
or use the select_db() method on the connection, like this:

dsn['database'] = 'wmdb'     # the database we want to connect to every time

or

conn = dbi.connect(dsn)
conn.select_db('wmdb')       # switch to this database for this connection

Use the DSN (credentials dictionary) to connect to the database. From here
on, mostly use the PyMySQL API.

conn = dbi.connect(dsn)
conn.select_db('wmdb')
curs = db.dict_cursor(conn)
curs.execute('select name,birthdate from person')
curs.execute('select name,birthdate from person where name like %s',
             ['%george%'])
curs.fetchall()
curs.fetchone()

curs.execute('insert into person values(%s,%s)',[123,'George Clooney'])
conn.commit()

PROVISOS and CONFIGURATION

The database connection is set to auto_commit(), but you can modify that
by using the conn.autocommit() method on the database connection:

conn=connect()
conn.autocommit(False)

INSTALLATION

It's usually easiest to install this module into your virtual
environment. Here's how to do that: 

(1) activate your virtual environment, and 
(2) execute the following Unix command:

cp ~cs304/pub/downloads/pymysql/cs304dbi.py $VIRTUAL_ENV/lib/python3.6/site-packages/

REPL

If you load this file using the Python REPL, you can get a read-eval-print
loop to the database with the repl() function:

repl(conn)
dbi> select user()
1
('cs304guest@localhost')
dbi> select database()
1
('wmdb')
dbi> select * from person limit 10;
10
(0, 'Alan Smithee', None, 1)
(1, 'Fred Astaire', datetime.date(1899, 5, 10), 167)
(2, 'Lauren Bacall', datetime.date(1924, 9, 16), 1207)
(3, 'Brigitte Bardot', datetime.date(1934, 9, 28), 1)
(4, 'John Belushi', datetime.date(1949, 3, 5), None)
(5, 'Ingmar Bergman', datetime.date(1918, 7, 14), 1)
(6, 'Ingrid Bergman', datetime.date(1915, 8, 29), 1)
(7, 'Humphrey Bogart', datetime.date(1899, 12, 25), 1247)
(8, 'Marlon Brando', datetime.date(1924, 4, 3), 1)
(9, 'Richard Burton', datetime.date(1925, 11, 10), 64)
dbi> quit
>>>

'''

import pymysql
import configparser
import os

DEBUG = False

# got this code from pymsql/optionfile.py

class Parser(configparser.RawConfigParser):

    def __remove_quotes(self, value):
        quotes = ["'", "\""]
        for quote in quotes:
            if len(value) >= 2 and value[0] == value[-1] == quote:
                return value[1:-1]
        return value

    def get(self, section, option):
        value = configparser.RawConfigParser.get(self, section, option)
        return self.__remove_quotes(value)

def read_cnf(cnf_file='~/.my.cnf',db=None):
    '''Read a file formatted like ~/.my.cnf file; defaulting to that
    file. Return a dictionary with the necessary information to connect to
    a database. See the connect() function. If 'db' given, replace the 
    value from the cnf_file. '''
    abs_cnf_file = os.path.expanduser(cnf_file)
    if not os.path.exists(abs_cnf_file):
        raise FileNotFoundError(cnf_file)

    # this code is from pymysql/connections.py
    read_default_group = "client"
    cfg = Parser()
    cfg.read(abs_cnf_file)

    def _config(key):
        return cfg.get(read_default_group, key)

    user = _config("user")
    password = _config("password")
    host = _config("host")
    # on Tempest, we put the database in the mysql group
    database = cfg.get("mysql","database")
    if db is not None:
        database = db
    if DEBUG:
        print('read_cnf: {} {}'.format(user,database))
    return {'user': user,
            'password': password,
            'host': host,
            'database': database}

DSN_CACHE = None

def cache_cnf(cnf_file='~/.my.cnf',db=None):
    '''Like read_cnf but reads the CNF file only once and caches the
results. You can override the default database with the second
argument.'''
    global DSN_CACHE
    if DSN_CACHE is None:
        DSN_CACHE = read_cnf(cnf_file,db=db)
    return DSN_CACHE

def conf(db=None):
    '''In practice, we rarely choose a different cnf file, but we often
    choose a different database, so I should have switched the
    arguments above.  Instead of redefining that, I'll define this
    new, better function. It also doesn't return the CNF data, since
    we rarely need it, and we can always get it from cache_cnf if we
    want it.

    '''
    cache_cnf(db=db)

# ================================================================

def use(database):

    '''Like the 'use' statement, but modifies the cached cnf. Then connect()'''
    if DSN_CACHE is None:
        raise Exception('You have to invoke cache_cnf first')
    DSN_CACHE['database'] = database

def connect(dsn=None):
    '''Returns a new database connection given the dsn (a dictionary). The
default is to use cache_cnf('~/.my.cnf')

    The database connection is not set to automatically commit.

    '''
    if dsn is None:
        dsn = cache_cnf('~/.my.cnf')
    check_DSN(dsn)
    try:
        # have no idea why this unix_socket thing is necessary, but
        # only for deployed apps, not in development mode
        # see stackoverflow.com/questions/6885164/pymysql-cant-connect-to-mysql-on-localhost
        conn = pymysql.connect( use_unicode=True,
                                autocommit=False,
                                charset='utf8',
                                unix_socket='/var/lib/mysql/mysql.sock',
                                **dsn )
    except pymysql.Error as e:
        print("Couldn't connect to database. PyMySQL error {}: {}"
              .format(e.args[0], e.args[1]))
        raise
    return conn

def check_DSN(dsn):
    '''Raises a comprehensible error message if the DSN is missing
    some necessary info'''
    for key in ('host', 'user', 'password', 'database' ):
        if not key in dsn:
            raise KeyError('''DSN lacks necessary '{k}' key'''.format(k=key))
    return True

def cache_select_db(db_name):
    '''Stores given db_name in DSN, so that subsequent connections use it.'''
    DSN_CACHE['database'] = db_name
    return DSN_CACHE

def select_db(conn,db):
    '''This function isn't necessary; just use the select_db() method
on the connection.'''
    conn.select_db(db)

def cursor(conn):
    '''Returns a cursor where rows are represented as tuples.'''
    return conn.cursor()

# for those who prefer snake_case

def dict_cursor(conn):
    '''Returns a cursor where rows are represented as dictionaries.'''
    return conn.cursor(pymysql.cursors.DictCursor)

# for those who prefer camelCase

def dictCursor(conn):
    '''Returns a cursor where rows are represented as dictionaries.'''
    return conn.cursor(pymysql.cursors.DictCursor)

## ================================================================
## testing and help functions

def usage():
    '''Prints a usage message.'''
    print('''How to use the cs304dbi python module:

''')

def repl(conn):
    '''Read SQL statements, Execute them, and print the results. Use 'quit' to quit.'''
    curs = cursor(conn)
    while True:
        expr = input('dbi> ')
        if expr == 'quit':
            break
        val = curs.execute(expr)
        print(val)
        for row in curs.fetchall():
            print(row)

def _testing_changed_cache(cnf_file):
    '''Testing that changing the db in the cache changes future connections'''
    # checking modification of DSN. But students can't switch to scottdb, so
    # this is just for scott
    scottdsn = cache_cnf(cnf_file)
    # we will use scottdb from now on
    scottdsn['database'] = 'scottdb'
    conn2 = connect()           # don't even have to supply it as an argment
    curs2 = cursor(conn2)
    curs2.execute('select database()')
    db = curs2.fetchone()[0]
    if db == 'scottdb':
        print('Successfully changed the database to scottdb')
    else:
        raise Error('did not successfully change database')
    return conn2

def _testing_commit(cnf_file):
    '''For Scott to test the behavior of commit()'''
    def drevil(should_be_there):
        conn = connect()
        curs = conn.cursor()
        curs.execute('select database()')
        db = curs.fetchone()[0]
        if db != 'scottdb':
            raise Exception('did not connect to scottdb')
        curs.execute('select name from person where nm = 666')
        row = curs.fetchone()
        name = None if row is None else row[0]
        if should_be_there and name is None:
            raise Exception('name is not there and it should be there')
        else:
            print('name is correctly there')
        if not should_be_there and name is not None:
            raise Exception('name is there and it should not be there')
        else:
            print('name is correctly not there')

    # series of checks about behavior of commit
    conn2 = _testing_changed_cache(cnf_file)
    curs2 = conn2.cursor()
    # set up by removing dr evil
    curs2.execute('delete from person where nm = 666')
    conn2.commit()
    # it should not be there
    drevil(False)

    # since autocommit is false, this won't stick
    curs2.execute('''insert into person(nm,name) values(666, 'dr evil')
                     on duplicate key update name='dr evil' ''')
    drevil(False)

    # now, commit the insert/update in connection 2
    conn2.commit()
    drevil(True)

    # clean up by removing dr evil
    curs2.execute('delete from person where nm = 666')
    conn2.commit()
    # last check, to make sure it's gone
    drevil(False)


if __name__ == '__main__':
    print('starting test code')
    import sys
    import os
    if len(sys.argv) < 2:
        print('''Usage: {cmd} cnf_file
test this module by giving the name of a cnf_file on the command line'''
              .format(cmd=sys.argv[0]))
        sys.exit(1)
    cnf_file = sys.argv[1]
    DSN = cache_cnf(cnf_file)
    print('Your DSN / CNF file should connect you as user {}@{} to database {}'
          .format(DSN['user'],DSN['host'],DSN['database']))
    conn = connect(DSN)
    print('successfully connected')
    DSN = cache_cnf(cnf_file,db='wmdb')
    print('Override DB to be wmdb')
    conn = connect(DSN)
    print('successfully connected')
    print('switching to wmdb')
    conn.select_db('wmdb')
    curs = cursor(conn)
    curs.execute('select user() as user, database() as db')
    row = curs.fetchone()
    print('connected to {db} as {user}'
          .format(db=row[1],user=row[0]))
    curs = dict_cursor(conn)
    # example of a simple query
    curs.execute('select nm,name,birthdate from person limit 3')
    print('first three people')
    for row in curs.fetchall():
        print(row)
    # example of a prepared query
    curs.execute('select nm,name,birthdate from person where name like %s',
                 ['%george%'])
    print('names like george')
    for row in curs.fetchall():
        print(row)

    # the following is just for scott (1942 is the cs304 course account)
    if os.getuid() == 1942:
        print('testing code for Scott/ CS304 course account')
        _testing_commit(cnf_file)
