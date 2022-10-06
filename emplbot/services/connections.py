import psycopg2
import sys
sys.path.append('..')
from services.settings import config_obnullildb


def dec_connection_to_obnullildb(func):
    def wrap_decorator_connection(action: int, sql_command: str, sql_param: tuple):
        try:
            # connect to exist database
            connection = psycopg2.connect(
                host=config_obnullildb['host'],
                user=config_obnullildb['user'],
                password=config_obnullildb['password'],
                dbname=config_obnullildb['db_name']
            )

            func(action, sql_command, sql_param)
            if action == 'add':
                with connection.cursor() as cursor:
                    print(f'command: {sql_command}')
                    cursor.execute(sql_command, sql_param)
                    connection.commit()
                    print(f'[INFO] New entry added to Database')
            elif action == 'del':
                with connection.cursor() as cursor:
                    print(f'command: {sql_command}')
                    cursor.execute(sql_command, sql_param)
                    connection.commit()
                    print(f'[INFO] Entry deleted from Database')
            elif action == 'get':
                with connection.cursor() as cursor:
                    print(f'command: {sql_command}')
                    cursor.execute(sql_command, sql_param)
                    print(f'[INFO] The entry was read from Database')
                    get_info = cursor.fetchall()
                    print(get_info)
                    return get_info
            else:
                print('[INFO] Action not recognised')

        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL', _ex)
        finally:
            if connection:
                connection.close()
                print('[INFO] Connection to PostgreSQL is closed')

    return wrap_decorator_connection


@dec_connection_to_obnullildb
def cursor_command(action, sql_command: str, sql_param: tuple):
    if sql_command[-1] != ';':
        sql_command + ';'

# For Test
# if __name__ == '__main__':
#     cursor_command("SELECT version();")
