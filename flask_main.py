"""
Definitions of the URL paths available in this app.
"""

from flask import Flask, request, render_template, redirect, url_for, session
import db
from random import shuffle
import questions
import sql_communication as sql

app = Flask(__name__)


def evaluate(question_number):
    user_answer = request.form['Answer']
    list_of_answers_for_question = questions.question_list['q_' + question_number]['options']
    for answer, points in list_of_answers_for_question:
        if answer == user_answer:
            print(user_answer)
            print(points)
            return points


def add_main_button(html_text):
    button = """\n\t\t<form method="post">
          <p class="submit"><input type="submit" name="Button" value="Main"></p>
      </form>
      """

    html_text += button

    html_text += " </body></html>"

    return html_text


@app.route("/results<number>", methods=['GET'])
def print_result(number):
    html_text = sql.html_results(int(number))
    html = add_main_button(html_text)

    return html


@app.route("/results<number>", methods=['POST'])
def go_to_main(number):
    return redirect(url_for('show_form'))


@app.route("/q_<number>")
def question(number):
    answers = questions.question_list['q_' + str(number)]['options']
    shuffle(answers)

    return render_template('template.html', number=number, answers=answers, question=questions.question_list['q_' + str(number)]['text'])


@app.route("/q_<number>", methods=['POST'])
def get_answer(number):
    print(session['Group'])
    print(session['Name'])

    sql.add_entry_to_table(session['Name'], session['Group'], number, evaluate(number))

    db.add_points(evaluate(number), session['Name'], number)

    if int(number)%10 == 9:
        db.save_points(number)
        db.get_sum_one_series(number)
        db.get_sum()

        sql.sum_one_series(session['Name'], number)
        sql.sum_all(session['Name'])

        return redirect(url_for('print_result', number=str(number)))
    else:
        new_number = int(number)+1
        return redirect(url_for('question', number=str(new_number)))


@app.route("/data")
def data_form():
    return render_template('get_data.html')


@app.route("/data", methods=['POST'])
def get_data():
    try:
        group = int(request.form['Group'])
    except ValueError:
        return 'Wrong group'

    name = request.form['Name']

    session['Name'] = name
    session['Group'] = group
    db.add_person(name, group)

    return redirect(url_for('question', number='0'))


@app.route("/", methods=['GET'])
def show_form():
    return render_template('basic.html')


@app.route("/", methods=['POST'])
def run_quiz():
    if 'First Button' in request.form:
        return redirect(url_for('data_form'))
    elif 'Second Button' in request.form:
        return redirect(url_for('question', number=str(10)))
    elif 'Third Button' in request.form:
        return redirect(url_for('question', number=str(20)))
    elif 'Fourth Button' in request.form:
        return redirect(url_for('question', number=str(30)))
    elif 'Fifth Button' in request.form:
        return redirect(url_for('question', number=str(40)))
    else:
        return 'Something is wrong.'


if __name__ == "__main__":
    """For local testing."""
    app.secret_key = "hYVqiysprdPKq3LsuWhqJUJM4zXwkMkxg4yVXLrgEKmFNNcAWEx4PnrEhyecPpXhp93nniMJVwvntqedWdNn4FY7Pgye4ffEchfPLJqghJ4R7mKbFoCf9Ppw"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0')
    app.run(debug=True, port=80)


def create_app(test_config=None):
    """For application deployment using gunicorn."""
    app.secret_key = "hYVqiysprdPKq3LsuWhqJUJM4zXwkMkxg4yVXLrgEKmFNNcAWEx4PnrEhyecPpXhp93nniMJVwvntqedWdNn4FY7Pgye4ffEchfPLJqghJ4R7mKbFoCf9Ppw"
    app.config['SESSION_TYPE'] = 'filesystem'
    return app
