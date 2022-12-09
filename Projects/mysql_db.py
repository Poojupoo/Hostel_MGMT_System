import pymysql


class DBConnect:

    def connect(self):
        try:
            return pymysql.connect("localhost", "root", "admin", "hostel_management")
        except Exception as e:
            print("Unable to connect to database " + str(e))
            return False


class DBQueryEngine:

    __table_name = "loginuser";

    __create_user = "register";

    @staticmethod
    def is_user_exists(user_name):
        is_exist = False
        conn = DBConnect().connect()
        print("User will be checked for user_name {}".format(user_name))
        try:
            cursor = conn.cursor()
            sql = "SELECT count(*) from {} where user_name = '{}'".format(DBQueryEngine.__table_name, user_name)
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result is not None:
                if result[0][0] > 0:
                    is_exist = True
        except Exception as e:
            print("Caught exception while getting the user " + str(e))
        finally:
            conn.close()
        return is_exist

    @staticmethod
    def check_password(user_name, password):
        print("password will be check for the username {}".format(user_name))
        conn = DBConnect().connect()
        try:
            if DBQueryEngine.is_user_exists(user_name):
                cursor = conn.cursor()
                sql = "SELECT password from {} where user_name= '{}'".format(DBQueryEngine.__table_name, user_name)
                print(sql)
                cursor.execute(sql)
                result = cursor.fetchall()
                if result is not None:
                    pwd = result[0][0]
                    if password == str(pwd):
                        return ""
                    else:
                        return "Password is invalid"
            else:
                return "Username doesn't exist"
        except Exception as e:
            print("Caught Exception is : " + str(e))
        finally:
            conn.close()

    @staticmethod
    def create_user(id, student_name, father_name, dob, phno, email, Gender, Roomno, Address, Amount):
        conn = DBConnect().connect()
        try:
                cursor = conn.cursor()
                fields = "'" + id + "', '" + student_name + "', '" + father_name + "' ,'" + dob + "', '" + phno + "','" + email + "','" + Gender + "','" + Roomno + "','" + Address + "','" + Amount + "'"
                sql = "INSERT INTO {} (id, student_name, father_name, dob, phno, email, Gender, Roomno, Address, Amount) VALUES ({})".format( DBQueryEngine. __create_user, fields)
                print(sql)
                cursor.execute(sql)
                conn.commit()
                return "User added successfully"
        except Exception as e:
            print("Caught exception while adding users " + str(e))
            return "Failed to register new user [ username = {} ]".format(id)
        finally:
            conn.close()

    @staticmethod
    def del_user(id):
        conn = DBConnect().connect()
        try:
                cursor = conn.cursor()
                sql="delete from register where id = id"
                print(sql)
                cursor.execute(sql)
                conn.commit()
                return "Successfully deleted"
        except Exception as e:
            print("Caught exception while adding users " + str(e))
            return "Unsuccessful".format(id)
        finally:
            conn.close()

    @staticmethod
    def update_user(id):
        conn = DBConnect().connect()
        try:
            cursor = conn.cursor()
            sql="UPDATE register SET Roomno = 301 where id=id"
            print(sql)
            cursor.execute(sql)
            conn.commit()
            return "Successfully updated"
        except Exception as e:
            print("Caught exception while updating users " +str(e))
            return "Unsuccessful".format(id)
        finally:
            conn.close()


""" @staticmethod
    def get_questions():
        questions = []
        conn = DBConnect().connect()
        try:
            cursor = conn.cursor()
            sql = "select * from questionaire"
            cursor.execute(sql)
            column_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            for row in rows:
                questions.append(dict(zip(column_names, row)))
            print(questions)
        except Exception as e:
            print("Caught Exception while getting all the questions " + str(e))
        finally:
            conn.close()
        return questions"""
