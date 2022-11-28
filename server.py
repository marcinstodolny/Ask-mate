from flask import Flask, request, render_template, redirect
import util
import data_manager
import datetime
import time
import os
app = Flask(__name__)


QUESTION_HEADER = ['ID', 'Title', 'Submission time', 'View number', 'Vote number', 'Message', 'Image']


@app.route("/")
@app.route("/list")
def main_page():
    all_questions = data_manager.get_all_question_data("question")[::-1]
    return render_template('index.html',
                           questions=all_questions,
                           QUESTION_HEADER=QUESTION_HEADER)


@app.route("/question/<question_id>")
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)[0]
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template('question.html', question=question, answers=answers)


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.add_new_question(question_time, 0, 0, request.form['title'], request.form['message'], 0)
        question_id = data_manager.get_question_id(question_time)[0]['id']
        if request.files["file"]:
            data_manager.save_photo(request.files["file"], question_id, 'question')
            data_manager.update_image(question_id, f'{question_id}.png')
        return redirect(f"/question/{question_id}")
    return render_template('add_question.html', title="Add question")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)[0]
    if request.method == 'POST':
        data_manager.update_question(question_id, request.form['title'], request.form['message'])
        if request.files["file"]:
            data_manager.save_photo(request.files["file"], question_id, 'question')
            data_manager.update_image(question_id, f'{question_id}.png')
        return redirect(f"/question/{question_id}")
    return render_template('edit_question.html',
                           title="Edit question",
                           question=question)


@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    id_index = int(question_id) - 1
    all_questions = data_manager.get_all_data_from_file("questions.csv")
    all_answers = data_manager.get_all_data_from_file("answers.csv")
    if request.method == 'POST':
        all_answers = data_manager.remove_question_answers(ANSWER_INDEX, question_id, all_answers)
        all_questions = data_manager.remove_photo(all_questions, id_index, Q_WAY)
        data_manager.reindex_items(all_answers, int(question_id), ANSWER_INDEX, rewrite_question_id=True)
        data_manager.reindex_items(all_questions, id_index, HEADERS_INDEX, Q_WAY)
        data_manager.write_file("questions.csv", all_questions)
        data_manager.write_file("answers.csv", all_answers)
    return redirect('/')


@app.route("/question/<question_id>/vote-up", methods=["POST"])
def up_vote(question_id):
    index = int(question_id) - 1
    all_questions = data_manager.get_all_data_from_file("questions.csv")
    all_questions[index][HEADERS_INDEX["vote number"]] = int(
        all_questions[index][HEADERS_INDEX["vote number"]]) + 1
    data_manager.write_file("questions.csv", all_questions)
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/<question_id>/vote-up", methods=["POST"])
def answer_up_vote(answer_id, question_id):
    index = int(answer_id) - 1
    all_answers = data_manager.get_all_data_from_file("answers.csv")
    all_answers[index][ANSWER_INDEX["vote number"]] = int(
        all_answers[index][ANSWER_INDEX["vote number"]]) + 1
    data_manager.write_file("answers.csv", all_answers)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/vote-down", methods=["POST"])
def down_vote(question_id):
    index = int(question_id) - 1
    all_questions = data_manager.get_all_data_from_file("questions.csv")
    all_questions[index][HEADERS_INDEX["vote number"]] = int(
        all_questions[index][HEADERS_INDEX["vote number"]]) - 1
    data_manager.write_file("questions.csv", all_questions)
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/<question_id>/vote-down", methods=["POST"])
def answer_down_vote(answer_id, question_id):
    index = int(answer_id) - 1
    all_answers = data_manager.get_all_data_from_file("answers.csv")
    all_answers[index][ANSWER_INDEX["vote number"]] = int(
        all_answers[index][ANSWER_INDEX["vote number"]]) - 1
    data_manager.write_file("answers.csv", all_answers)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/new-comment", methods=["POST", "GET"])
def add_comment_to_question(question_id):
    all_comments = data_manager.get_all_data_from_file("comments_to_questions.csv")
    if request.method == 'POST':
        new_comment = util.set_new_values(COMMENT_INDEX, all_comments, 5, question_id)
        new_comment[COMMENT_INDEX["message"]] = request.form['message']
        data_manager.write_file("comments_to_questions.csv", all_comments, new_comment)
        return redirect(f"/question/{question_id}")
    return render_template('add_comment.html',
                           title="Add comment",
                           question_id=question_id)


@app.route("/list/sort", methods=["POST"])
def sort_list():
    sort_by = request.form.get('sort_by')
    order_direction = request.form.get('order_by')
    all_questions = data_manager.get_all_data_from_file("questions.csv")
    all_questions = util.convert_elements(all_questions, HEADERS_INDEX)
    sort_by_index = HEADERS_INDEX[sort_by]
    if order_direction == "descending":
        all_questions.sort(key=lambda x: x[sort_by_index], reverse=True)
    elif order_direction == "ascending":
        all_questions.sort(key=lambda x: x[sort_by_index])
    for item in all_questions:
        date = datetime.date.fromtimestamp(int(item[2]))
        item[2] = f"{date.day}-{date.month}-{date.year}"
    return render_template('index.html', all_questions=all_questions, QUESTION_HEADER=QUESTION_HEADER, sort=sort_by, order=order_direction)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    all_answers = data_manager.get_all_data_from_file("answers.csv")
    if request.method == 'POST':
        new_answer = util.set_new_values(ANSWER_INDEX, all_answers, 6, question_id)
        new_answer[ANSWER_INDEX["message"]] = request.form['message']
        new_answer[ANSWER_INDEX["image"]] = data_manager.save_photo(request.files["file"], len(all_answers), "answers")
        data_manager.write_file("answers.csv", all_answers, new_answer)
        return redirect(f"/question/{question_id}")
    return render_template('add_answer.html',
                           title="Add answer",
                           question_id=question_id)


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    id_index = int(answer_id) - 1
    if request.method == 'POST':
        all_answers = data_manager.get_all_data_from_file("answers.csv")
        question_id = int(all_answers[id_index][ANSWER_INDEX['question id']])
        all_answers.pop(id_index)
        if os.path.exists(f"{A_WAY}\\{id_index + 1}.png"):
            os.remove(f"{A_WAY}\\{id_index + 1}.png")
        data_manager.reindex_items(all_answers, id_index, ANSWER_INDEX, A_WAY)
        data_manager.write_file("answers.csv", all_answers)
        return redirect(f"/question/{question_id}")


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=60000,
        debug=True,
    )
