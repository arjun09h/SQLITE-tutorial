import sqlite3
from icecream import ic as print
# creating a connection 
def create_connection(db_name):
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        print (f"Error {e}")
        raise
# creating a table
def create_table(connection):
    query = """
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT UNIQUE
            )
            """
    try:
        with connection:
            connection.execute(query)
        print("Table is Created.")
    except Exception as e:
        print(e)
# adding user
def insert_data(connection,name:str,age:int,email:str):
    query = 'INSERT INTO users (name, age, email) VALUES (?, ?, ?)'
    try:
        with connection:
            connection.execute(query,(name,age,email))
            print(f"{name} is Added to your Database")
    except Exception as e:
        print(e)
# display user
def display_data(connection, condition: str = None) -> list[tuple]:
    query = 'SELECT * FROM users'
    if condition:
        query += f'WHERE {condition}'
    try:
        with connection:
            rows = connection.execute(query).fetchall()
            return rows
    except Exception as e:
        print(e)
# delete user
def delete_data(connection,user_id:int):
    query = 'DELETE FROM users WHERE id = ?'
    try:
        with connection:
            connection.execute(query,(user_id,))
        print(f"Data with ID {user_id} is Deleted.")
    except Exception as e:
        print(e)
# update user email
def update_data(connection,user_id:int,email:str):
    query = 'UPDATE users SET email = ? WHERE id = ?'
    try:
        with connection:
            connection.execute(query,(email,user_id))
        print(f"Email with ID {user_id} is Updated.")
    except Exception as e:
        print(e)
# add multiple users
def add_many(connection,users:list[tuple[str,int,str]]):
    query = 'INSERT INTO users (name,age,email) VALUES (?, ?, ?)'
    try:
        with connection:
            connection.executemany(query,users)
        print(f"{len(users)} users were Added to the Database.")
    except Exception as e:
        print(e)

# main
def main():
    connection = create_connection("first.db")
    try:
        create_table(connection)
        choice = int(input("Press 1 for Activate Press 2 for Freeze : "))
        while choice != 2:
            options = input("Enter your choice(add,delete,update,search,add multiple) : ").lower()
            match options:
                case "add":
                    name = input("Enter your name : ")
                    age = int(input("Enter your age : "))
                    email = input("Enter your email : ")
                    insert_data(connection,name,age,email )
                case "search":
                    print("All Users : ")
                    for user in display_data(connection):
                        print(user)
                case "delete":
                    user_id = int(input("Enter the data id you want to delete : "))
                    delete_data(connection, user_id)
                case "update":
                    user_id = int(input("Enter the data id you want to update : "))
                    new_email = input("Enter The Updated Email : ")
                    update_data(connection,user_id,new_email)
                case "add multiple":
                    users = [("Karan", 20, "karan01@gmail.com"),
                             ("Rohit", 19, "rohit01@gmail.com")]
                    add_many(connection,users)    
                case _ :
                    print("UNKNOWN CHOICE")
            choice = int(input("Press 1 for Activate Press 2 for Freeze : "))
    finally:
        connection.close()
if __name__ == "__main__":
    main()