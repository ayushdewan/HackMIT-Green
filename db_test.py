import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='35.238.255.61',
                             user='root',
                             password='claimcart',
                             db='claims',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    f = open("dummy.txt", "r")
    for i in f.readlines():
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `board` (`name`, `bolts`, `carbon`, `os`) VALUES (%s, %s, %s, %s)"
            print(tuple(i.split(", ")))
            cursor.execute(sql, tuple(i.split(", ")))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
finally:
    connection.close()