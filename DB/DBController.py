'''
DBcontroller.py

@Author: Juan Insuasti

Database controller using RethinkDB, intended to be used with
RaspberryPi

'''

import rethinkdb as r


class DBController(object):
    """
    DBController class.
    Simplifies usage for RethinkDB

    """
    def __init__(self):
        '''
        Constructor Method
        '''


if __name__ == '__main__':
    r.connect( "localhost", 28015).repl()
    print("Test End")
    #r.db("test").table_create("authors").run()
