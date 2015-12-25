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
    def __init__(self, host="localhost",port=28015):
        '''
        Constructor Method
        creates database an tables schema
        '''
        self.DB_NAME = "IoT"
        self.HOST    = host
        self.PORT    = port

        try:
            #Connection to DB
            self.conn = r.connect( self.HOST, self.PORT).repl()
            print("Connected to RethinkDB.")

            #Database Veridication
            if self.DB_NAME in r.db_list().run(self.conn):
                self.conn.use(self.DB_NAME)
                print("Using IoT Database.")
            else:
                r.db_create(self.DB_NAME).run(self.conn)
                print("IoT Database created.")
                self.conn.use(self.DB_NAME)
                print("Using IoT Database.")


            #Table Verification
            if "SENSOR_DATA" not in r.table_list().run(self.conn):
                r.table_create("SENSOR_DATA").run(self.conn)
                print("Table created: SENSOR_DATA.")
            if "ACTUATOR_DATA" not in r.table_list().run(self.conn):
                r.table_create("ACTUATOR_DATA").run(self.conn)
                print("Table created: ACTUATOR_DATA.")


        except r.ReqlDriverError as err:
            print(err)

        except r.ReqlRuntimeError as err:
            print(err)

        except:
            Print("Unknown Error Initializing DB")


    def append(self, table, data):
        '''
        Appends data to a table
        '''
        r.table(table).insert(data).run(self.conn)

    def time(self):
        time_data = [time.strftime("%Y"),time.strftime("%m"),time.strftime("%d"),time.strftime("%H:%M:%S")]

        return time_data


if __name__ == '__main__':
    import random
    import time
    DB = DBController()
    data = {}
    data["device"]      = "A"
    data["light"]       = random.random()
    data["temperature"] = random.random()
    data["humidity"]    = random.random()
    data["timestamp"]        = DB.time()
    DB.append("SENSOR_DATA",data)
    table = r.table("SENSOR_DATA").run(DB.conn)
    for document in table:
        print document










