from typing import Iterable
import mysql.connector
import bcrypt


class database:
    def __init__(
        self,
        database_name: str,
        username: str,
        password: str,
        host: str = "localhost",
    ) -> None:
        self.database_name = database_name
        self.username = username
        self.password = password
        self.host = host

        self.connect()

    def set_database_name(self, database_name: str) -> None:
        self.database_name = database_name
        self.connect()

        # return self.conn, self.cur

    def set_username(self, username: str) -> None:
        self.username = username
        self.connect()

    def set_password(self, password: str) -> None:
        self.password = password
        self.connect()

    def set_host(self, host: str) -> None:
        self.host = host
        self.connect()

    def connect(self) -> None:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                passwd=self.password,
                database=self.database_name,
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            self.connection = None
            self.cursor = None
            raise e

    def add_record(
        self, table_name: str, data: Iterable, columns: Iterable = None
    ) -> None:
        table_name = "".join(table_name.split())
        if not columns:
            columns = self.__get_columns_name(table_name=table_name)
        cols = ""
        for col in columns:
            cols += col + ","
        cols = cols[:-1]
        cols = "(" + cols + ")"
        s = "%s," * len(columns)
        s = s[:-1]
        s = "(" + s + ")"

        query = """INSERT INTO {} {} 
                    VALUES 
                    {} """.format(
            table_name, cols, s
        )
        self.cursor.execute(query, data)
        self.connection.commit()

    def update_record(
        self, table_name: str, col_name: str, value: str, id_name: str, id_value: str
    ) -> None:
        table_name = "".join(table_name.split())
        query = """UPDATE {} 
                    SET {} = {}
                    WHERE {} ={} """.format(
            table_name,
            col_name,
            ("'" + str(value) + "'"),
            id_name,
            ("'" + str(id_value) + "'"),
        )
        self.cursor.execute(query)
        self.connection.commit()

    def remove_record(self, table_name: str, col_name: str, value: str) -> None:
        table_name = "".join(table_name.split())
        query = """DELETE 
                    FROM {} 
                    WHERE {}={}
                    """.format(
            table_name, col_name, "'" + str(value) + "'"
        )
        self.cursor.execute(query)
        self.connection.commit()

    def search(self, table_name: str, col_name: str = None, value: str = None) -> dict:
        table_name = "".join(table_name.split())
        if not col_name or not value:
            query = "SELECT * FROM {}".format(table_name)
        else:
            query = """SELECT * FROM {} WHERE {} = {}""".format(
                table_name, col_name, ("'" + str(value) + "'")
            )

        self.cursor.execute(query)
        records = self.cursor.fetchall()

        columns = [column[0] for column in self.cursor.description]
        res = []

        for record in records:
            record_dict = {}
            for i in range(len(columns)):
                record_dict[columns[i]] = record[i]

            res.append(record_dict)

        return res

    def search_mail(
        self, table_name: str, col_name: str = None, value: str = None
    ) -> dict:
        table_name = "".join(table_name.split())
        if not col_name or not value:
            query = "SELECT * FROM {}".format(table_name)
        else:
            query = """SELECT * FROM {} WHERE {} = {}""".format(
                table_name, col_name, ("'" + str(value) + "'")
            )

        self.cursor.execute(query)
        records = self.cursor.fetchall()

        columns = [column[0] for column in self.cursor.description]
        res = []

        for record in records:
            record_dict = {}
            for i in range(len(columns)):
                record_dict[columns[i]] = record[i]

            res.append(record_dict)

        return res

    def __get_columns_name(self, table_name):
        table_name = "".join(table_name.split())
        query = f"SHOW COLUMNS FROM {table_name} WHERE Extra != 'auto_increment'"
        self.cursor.execute(query)
        columns = [column[0] for column in self.cursor.fetchall()]

        return columns

    def update_record(self, table_name, col_name, value, id_name, id_value):
        """this function used to update a row with input parms

        Args:
            table_name (str): name of that table we want to change data
            col_name (str): column name of table
            value (str): new vlaue
            id_name (str): name of column for selecting the row
            id_value (str): Row specifier
        """

        # try:
        # if self.check_connection():
        mySql_insert_query = """UPDATE {} 
                                        SET {} = {}
                                        WHERE {} ={} """.format(
            table_name,
            col_name,
            ("'" + value + "'"),
            id_name,
            ("'" + id_value + "'"),
        )
        self.cursor.execute(mySql_insert_query)
        self.connection.commit()
        # self.show_message(
        #     (self.cursor.rowcount, "Record Updated successfully "), level=1
        # )
        self.cursor.close()
        return True
        # else:
        #  return False

        # except mysql.connector.Error as e:
        #   self.show_message(("Error Update Record ", e))

    def show_message(self, error, level=0):
        """this function print errors or messages

        Args:
            error (_type_): _description_
            level (int, optional): _description_. Defaults to 0.
        """
        # if self.log_level == 1:
        print(error)


class hasher:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())


class login:
    def __init__(
        self,
        database_name: str = None,
        database_username: str = None,
        database_password: str = None,
        database_host: str = None,
        db_obj: object = None,
        users_table: str = "Users",
        username_field: str = "user",
        password_field: str = "pass",
        hash_password: bool = False,
        hasher_obj: object = None,
    ) -> None:
        if database_name and database_username and database_password and database_host:
            db_obj = database(
                database_name=database_name,
                username=database_username,
                password=database_password,
                host=database_host,
            )
            self.set_database(db_obj)
        elif db_obj:
            self.set_database(db_obj)
        else:
            self.database = None

        self.set_users_table(users_table)
        self.set_username_field(username_field)
        self.set_password_field(password_field)
        self.set_hash_password(hash_password)

        if hasher_obj:
            self.set_hasher(hasher_obj)
        else:
            hasher_obj = hasher()
            self.set_hasher(hasher_obj)

    def set_database(self, database_obj: object) -> None:
        self.database = database_obj

    def set_users_table(self, table_name: str):
        self.users_table = table_name

    def set_username_field(self, username_field):
        self.username_field = username_field

    def set_password_field(self, password_filed):
        self.password_filed = password_filed

    def set_hash_password(self, hash_password):
        self.hash_password = hash_password

    def set_hasher(self, hash_obj):
        self.hasher = hash_obj

    def login(self, username: str, password: str):
        res = False
        users = self.database.search(self.users_table, self.username_field, username)
        if not users:
            return "The Invalid User Name", res

        if len(users) != 1:
            return "The Invalid User Name", res

        users = users[0]
        if self.hash_password:
            res = self.hasher.verify_password(password, users[self.password_filed])
        else:
            res = users[self.password_filed] == password

        if res:
            return "Successful login", res

        else:
            return "Invalid Password", res

    def signup(
        self, tablename: str, username: str, family: str, password: str, email: str
    ):
        users = self.database.search(self.users_table, self.username_field, username)
        if not users:
            self.database.add_record(tablename, (username, family, password, email))
            return "This user has been added successfully"
        else:
            return "This user already exists"

    def change_password(
        self, tablename: str, username: str, oldpassword: str, newpassword: str
    ):
        users = self.database.search(self.users_table, self.username_field, username)

        if not users:
            return "Invalid Username"
        else:
            users = users[0]
            if self.hash_password:
                res = self.hasher.verify_password(
                    oldpassword, users[self.password_filed]
                )
            else:
                res = users[self.password_filed] == oldpassword

        if res:
            self.database.update_record(
                tablename, "pass", newpassword, "user", username
            )
            return "Successful change the password", res

        else:
            return "Invalid Oldpassword", res

    def forgot_password(self, tablename: str, username: str, password: str):
        users = self.database.search(self.users_table, self.username_field, username)
        if not users:
            return "Invalid Username"
        else:
            ## self.login.search_email(email)
            pass


if __name__ == "__main__":
    db = database(database_name="test_database", username="root", password="dorsa-co")

    lo = login(
        database_name="test_database",
        database_username="root",
        database_password="dorsa-co",
        database_host="localhost",
        users_table="Users",
    )
    answer = lo.signup(
        "Users", "Elham", "Hatefi", "12345", "daniz.ai2022@gmail.com"
    )  #  It is okkkkkkkkkkkkkkkkkkkkkkkk
    print(answer)
    answer = lo.change_password(
        "Users", "Elham", "12345", "12345678"
    )  #  It is okkkkkkkkkkkkkkkkkkkkkkkk
    print(answer)
    ans = answer = lo.login("Elham", "12345678")  #  It is okkkkkkkkkkkkkkkkkkkkkkkk
    print(ans)
