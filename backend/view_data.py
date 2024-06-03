import mysql.connector

def fetch_data():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='map_database'
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            
            # Create a cursor object
            cursor = connection.cursor()
            
            # Execute a SQL query
            cursor.execute("SELECT * FROM Map")
            
            # Fetch all rows from the executed query
            records = cursor.fetchall()
            
            # Print the records
            for row in records:
                print(f"id: {row[0]}, place: {row[1]}, date_of_upload: {row[2]}, unique_photo_name: {row[3]}")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Call the function to fetch data
fetch_data()
