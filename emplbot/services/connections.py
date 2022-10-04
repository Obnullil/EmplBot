import psycopg2
import sys
sys.path.append('..')
from services.settings import config_obnullildb


def dec_connection_to_obnullildb(func):
    def wrap_decorator_connection(command: str):
        try:
            # connect to exist database
            connection = psycopg2.connect(
                host=config_obnullildb['host'],
                user=config_obnullildb['user'],
                password=config_obnullildb['password'],
                dbname=config_obnullildb['db_name']
            )

            func(command)

            with connection.cursor() as cursor:
                cursor.execute(
                    # "SELECT version();"
                    command
                )
                print(f'Server version: {cursor.fetchone()}')

        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL', _ex)
        finally:
            if connection:
                connection.close()
                print('[INFO] Connection to PostgreSQL is closed')

    return wrap_decorator_connection


@dec_connection_to_obnullildb
def cursor_command(command: str):
    print(command)
    if command[-1] != ';':
        command + ';'

# For Test
# if __name__ == '__main__':
#     cursor_command("SELECT version();")
