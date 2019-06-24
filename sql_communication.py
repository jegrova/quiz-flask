"""
Module encapsulating communication with the SQL DB.
"""

import pymysql

QUESTIONS_FINAL_COUNT = 50
QUESTIONS_SERIES_COUNT = 10

# Used to initialize DB when used for the first time.
# FIXME: Create DB migrations properly.
# conn.cursor().execute('create database quiz')

# sqlQuery = "CREATE TABLE `user_points` (`name` varchar(32), `group` int, `question_id` int, `points` int)"
#
# conn.cursor().execute(sqlQuery)

# cursor = conn.cursor()
#
# cursor.execute("show tables")
#
# tables = cursor.fetchall()
#
# for (table_name,) in tables:
#     print(table_name)
#


# insertStatement = "INSERT INTO user_points (`name`, `group`, `question_id`, `points`) VALUES ('Eva', 2, 10, 10)"
#
# conn.cursor().execute(insertStatement)
# conn.commit()
#
#
# cursorObject = conn.cursor()
# sqlQuery = "select * from user_points"
# cursorObject.execute(sqlQuery)
#
# rows = cursorObject.fetchall()
# for row in rows:
#     print(row)
#


def connect_to_db():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           database='quiz',
                           )
    return conn


def add_entry_to_table(name, group, question_id, points):
    insert_statement = "INSERT INTO user_points (`name`, `group`, `question_id`, `points`) VALUES " \
                       "('" + name + "', " + str(group) + ", " + str(question_id) + ", " + str(points) + ")"

    connection = connect_to_db()
    connection.cursor().execute(insert_statement)
    connection.commit()


def get_all_users():
    select_statement = "SELECT DISTINCT name FROM user_points;"

    connection = connect_to_db()
    cursorObject = connection.cursor()
    cursorObject.execute(select_statement)

    rows = cursorObject.fetchall()

    users = list()

    for (row,) in rows:
        users.append(row)

    return users


def get_group_of_user(name):
    select_statement = "select `group` from user_points where name = '" + name + "';"

    connection = connect_to_db()

    cursorObject = connection.cursor()
    cursorObject.execute(select_statement)

    rows = cursorObject.fetchall()
    for (row,) in rows:
        group = row
        return group


def sum_one_series(name, number):
    sum = 0
    res_modulo = int(int(number) / QUESTIONS_SERIES_COUNT)

    for i in range(res_modulo*QUESTIONS_SERIES_COUNT, (res_modulo+1)*QUESTIONS_SERIES_COUNT):

        select_statement = "select points from user_points where (name = '" + name + "' AND question_id =" + str(i) + ");"

        connection = connect_to_db()

        cursorObject = connection.cursor()
        cursorObject.execute(select_statement)

        rows = cursorObject.fetchall()
        for (row,) in rows:
            sum += row
            print(sum)
            break

    return sum


def sum_all(name):
    select_statement = "select points from user_points where name = '" + name + "';"

    connection = connect_to_db()

    cursorObject = connection.cursor()
    cursorObject.execute(select_statement)

    rows = cursorObject.fetchall()
    sum = 0
    for (row,) in rows:
        sum += row
        print(row)
        print(sum)

    return sum


def html_results(question_number):
    if question_number < 10:
        series = 1
    elif question_number < 20:
        series = 2
    elif question_number < 30:
        series = 3
    elif question_number < 40:
        series = 4
    elif question_number < 50:
        series = 5
    else:
        print('Wrong question number, can not compute series.')

    html_page = """<!DOCTYPE html >
    <html lang = "en" >
    <head>
    <meta charset = "UTF-8" >
    <title> Results </title>

    </head>
    <body>"""

    html_page += str(series) + '. '

    html_page += """ kolo
        <table>
            <tr>
                <th>Kdo</th>
                <th>Skupina</th>
                <th>Počet bodů za kolo</th>
                <th>Počet bodů celkem</th>
            </tr>
    """

    users = get_all_users()

    for entry in users:
        html_page += "<tr><td>{}</td>".format(entry)
        html_page += "<td>{}</td>".format(get_group_of_user(entry))
        html_page += "<td>{}</td>".format(sum_one_series(entry, question_number))
        html_page += "<td>{}</td>".format(sum_all(entry))
        html_page += "</tr>"
    html_page += "</table>"

    return html_page
