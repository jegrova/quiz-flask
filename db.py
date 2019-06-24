"""
A "database" created on top of Pandas library.

It has been replaced by the SQL database. Keeping it just as a backup.
"""

import pandas


QUESTIONS_FINAL_COUNT = 50
QUESTIONS_SERIES_COUNT = 10

columns = ['Name', 'Group']
for i in range(QUESTIONS_FINAL_COUNT):
    columns.append(str(i))

data = pandas.DataFrame(columns=columns)


def add_person(name, group):
    df = pandas.DataFrame({'Name': [name], 'Group': [group]})
    global data
    data_new = data.append(df)
    data = data_new
    data = data.reset_index(drop=True)

    print(data)


def add_points(points, name, question_number):
    data.loc[data['Name'] == name, question_number] = points

    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        print(data)


def save_points(question_number):
    data.to_csv('./result_' + question_number + '.csv', ',', encoding='utf-8')


def get_sum():
    col_list = list(data)
    col_list.remove('Group')
    col_list.remove('Name')
    data['Sum'] = 0

    for i in range(int(QUESTIONS_FINAL_COUNT / QUESTIONS_SERIES_COUNT)):
        try:
            col_list.remove('Sum'+str(i))
        except ValueError:
            continue

    data['Sum'] = data[col_list].sum(axis=1)

    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        print(data)


def get_sum_one_series(question_number):
    col_list = list()
    res_modulo = int(int(question_number) / QUESTIONS_SERIES_COUNT)
    for i in range(res_modulo*QUESTIONS_SERIES_COUNT, (res_modulo+1)*QUESTIONS_SERIES_COUNT):
        col_list.append(str(i))

    data['Sum' + str(res_modulo)] = data[col_list].sum(axis=1)

    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        print(data)


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

    for row in range(len(data.index)):
        html_page += "<tr><td>{}</td>".format(data.loc[row, 'Name'])
        html_page += "<td>{}</td>".format(data.loc[row, 'Group'])
        html_page += "<td>{}</td>".format(data.loc[row, 'Sum' + str(int(question_number / QUESTIONS_SERIES_COUNT))])
        html_page += "<td>{}</td>".format(data.loc[row, 'Sum'])
        html_page += "</tr>"
    html_page += "</table>"
    
    return html_page
