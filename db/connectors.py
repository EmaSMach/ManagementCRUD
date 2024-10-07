import mysql.connector
from decouple import config
from mysql.connector import errorcode

from loggers import logger


class InvalidCredentialsError(Exception):
    pass


class NonExistingDatabaseError(Exception):
    pass


class MySqlConnector:
    def __init__(self, conf, table_definitions=None):
        self.__connection = None
        self.__cursor = None
        if table_definitions is None:
            table_definitions = {}
        self.host = conf("DB_HOST")
        self.user = conf("DB_USER")
        self.password = conf("DB_PASSWORD")
        self.database = conf("DB_NAME")
        self.port = conf("DB_PORT")
        self.table_definitions = table_definitions

        print("HOST:", self.host)
        print("USER:", self.user)
        print("PASSWORD:", self.password)
        print("DATABASE:", self.database)

    def get_existing_connection_and_cursor(self):
        """Return the existing connection object"""
        return self.__connection, self.__cursor

    def get_connection(self):
        """Try to connect to the database and return the connection object"""
        try:
            if self.__connection and self.__connection.is_connected():
                return self.__connection
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            self.__connection = conn
            return conn
        except (mysql.connector.Error, IOError) as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Invalid credentials")
                raise InvalidCredentialsError from err
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                raise NonExistingDatabaseError from err
            else:
                print(str(err))
                raise err
        except Exception as ex:
            print("Unexpected error connecting to database: ", str(ex))
            raise ex

    def run_query(self, query, *args, commit=True, **kwargs):
        conn = self.get_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor(dictionary=True)
        else:
            return None

        try:
            cursor.execute("USE " + self.database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            return None

        try:
            cursor.execute(query, *args, **kwargs)
        except mysql.connector.Error as ex:
            print("Error executing query: ", ex)
            return None
        else:
            if query.startswith(("SELECT", "select", "SHOW", "show")):
                return cursor.fetchall()
            elif query.startswith(("INSERT", "insert")):
                if commit:
                    conn.commit()
                    return cursor.lastrowid
            elif query.startswith(("UPDATE", "update", "DELETE", "delete")):
                if commit:
                    conn.commit()
                    return cursor.rowcount
            elif query.startswith(("CREATE", "create")):
                return True
        finally:
            if not commit:
                self.__cursor = cursor
                self.__connection = conn
            else:
                cursor.close()
                if conn.is_connected():
                    conn.close()
                self.__cursor = None
                self.__connection = None
        return None

    def create_database(self, database_name):
        query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
        conn = mysql.connector.connect(
            host=self.host, user=self.user, password=self.password, port=self.port
        )
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.close()

    def create_tables(self, table_definitions=None):
        if table_definitions is None:
            table_definitions = self.table_definitions
        for table_name, table_definition in table_definitions.items():
            self.run_query(table_definition)

    def start_transaction(self):
        conn = self.get_connection()
        if conn and conn.is_connected():
            conn.start_transaction()
        return None

    def commit(self, close=True):
        if self.__connection and self.__connection.is_connected():
            self.__connection.commit()
        if close:
            if self.__cursor:
                self.__cursor.close()
            if self.__connection:
                self.__connection.close()
        return None

    def rollback(self, close=True):
        conn = self.get_connection()
        if conn and conn.is_connected():
            conn.rollback()
        if not close:
            return None
        if self.__cursor:
            self.__cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    import sys

    from db.table_definitions import TABLES

    connector = MySqlConnector(config, table_definitions=TABLES)
    try:
        connection = connector.get_connection()
    except InvalidCredentialsError:
        logger.error("Invalid credentials")
        sys.exit(1)
    except NonExistingDatabaseError:
        logger.error("Database does not exist")
        try:
            connector.create_database(config("DB_NAME"))
            connection = connector.get_connection()
            logger.info("Database created")
        except Exception as ex:
            logger.error("Unexpected error: %s", ex)
            sys.exit(1)
    except Exception as ex:
        logger.error("Unexpected error: %s", ex)
        sys.exit(1)

    if connection and connection.is_connected():
        connector.create_tables()
        print("Connected to database")
    else:
        print("Failed to connect to database")
    if connection and connection.is_connected():
        print("Closing...")
        connection.close()
