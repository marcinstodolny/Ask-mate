from flask import Flask, request, render_template, redirect
import util
import data_manager
import datetime
import time
import os
app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
@app.route("/list")
def main_page():
    sort_by = request.form.get('sort_by')
    order_by = request.form.get('order_by')
    if sort_by is None:
        all_questions = sort_list('question')
    else:
        all_questions = sort_list('question', sort_by, order_by)
    return render_template('index.html', questions=all_questions, sort=sort_by, order=order_by)


@app.route("/question/<question_id>")
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)[0]
    answers = data_manager.get_answers_by_question_id(question_id)
    question['submission_time'] = (datetime.datetime.now().replace(microsecond=0)) - question['submission_time']
    data_manager.increment_view_number(question_id, 'question')
    return render_template('question.html', question=question, answers=answers)


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.add_new_question(question_time, 0, 0, request.form['title'], request.form['message'], '')
        question_id = data_manager.get_question_id(question_time)[0]['id']
        if request.files["file"]:
            data_manager.save_photo(request.files["file"], question_id, 'question')
            data_manager.update_image('question', question_id, f'{question_id}.png')
        return redirect(f"/question/{question_id}")
    return render_template('add_question.html', title="Add question")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        data_manager.update_question(question_id, request.form['title'], request.form['message'])
        if request.files["file"]:
            data_manager.save_photo(request.files["file"], question_id, 'question')
            data_manager.update_image(question_id, f'{question_id}.png')
        return redirect(f"/question/{question_id}")
    question = data_manager.get_question_by_id(question_id)[0]
    return render_template('edit_question.html',
                           title="Edit question",
                           question=question)


@app.route("/question/<question_id>/delete", methods=['POST'])
def delete_question(question_id):
    if request.method == 'POST':
        data_manager.delete_question(question_id)
        return redirect('/')


@app.route("/question/<question_id>/vote-up", methods=["POST"])
def up_vote(question_id):
    data_manager.increment_vote_number(question_id, 'question')
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/<question_id>/vote-up", methods=["POST"])
def answer_up_vote(answer_id, question_id):
    data_manager.increment_vote_number(answer_id, 'answer')
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/vote-down", methods=["POST"])
def down_vote(question_id):
    data_manager.decrement_vote_number(question_id, 'question')
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/<question_id>/vote-down", methods=["POST"])
def answer_down_vote(answer_id, question_id):
    data_manager.decrement_vote_number(answer_id, 'answer')
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


def sort_list(table, sort_by='submission_time', order_direction='DESC'):
    return data_manager.get_sorted_data(table, sort_by, order_direction)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'POST':
        submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = request.form['message']
        data_manager.new_answer(submission_time, 0, question_id, message, '')
        answer_id = data_manager.get_answer_id_by_time(submission_time)[0]['id']
        if request.files["file"]:
            data_manager.save_photo(request.files["file"], answer_id, 'answer')
            data_manager.update_image('answer', answer_id, f'{answer_id}.png')
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
