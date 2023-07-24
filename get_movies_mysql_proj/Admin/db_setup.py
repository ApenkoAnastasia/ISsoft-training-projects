from os import system as sys
import mysql.connector as mc
from mysql.connector.constants import ClientFlag


Delimiter = ', '


def get_config():
    '''Get data to connection.

    Function that return dictionary of config data.
    
    return -- dictionary of config data
   
    '''
    config = {}
    with open('/Admin/config.txt', 'r') as file:
        for line in file.readlines():
            data = line.strip().split(Delimiter)
            config[data[0]] = ''.join(data[1:])

    return config


def get_sql_files():
    '''Get list of sql files.

    Function that return list of sql files to execution.
    
    return -- list of sql files
   
    '''
    sql_files = []
    with open('/Admin/call_sql.txt', 'r') as file:
        for line in file.readlines():
            sql_files.append(line.strip())

    return sql_files


def main():
    """Function that connect to MySQL database, get list of sql files, execute them: create databases, tables, load data to them, transform this data and get table of results."""
    config = get_config()

    sql_files = get_sql_files()

    for i in range(0, len(sql_files)):
        command = """mysql -u %s -p"%s" --host %s --local-infile=1 < %s""" %(config['user'], config['password'], config['host'], '/Admin/sql/'+sql_files[i])
        sys(command)


if __name__ == "__main__":
    main()