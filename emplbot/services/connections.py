import psycopg2
import sys

# sys.path.append('..')
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
            with connection.cursor() as cursor:
                cursor.execute(sql_command, sql_param)
                if action == 'add':
                    connection.commit()
                    print(f'[INFO] New entry added to Database')
                    return True
                elif action == 'del':
                    connection.commit()
                    print(f'[INFO] Entry deleted from Database')
                    return True
                elif action == 'get':
                    print(f'[INFO] The entry was read from Database')
                    get_info = cursor.fetchall()
                    return get_info
                else:
                    print('[INFO] Action not recognised')
                    return False

        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL', _ex)
            return False
        finally:
            if connection:
                connection.close()
                print('[INFO] Connection to PostgreSQL is closed')

    return wrap_decorator_connection


@dec_connection_to_obnullildb
def cursor_command(action, sql_command: str, sql_param: tuple):
    if sql_command[-1] != ';':
        sql_command + ';'
    # TODO: add conditions for data validation

# For Test
# if __name__ == '__main__':
#     cursor_command("SELECT version();")
