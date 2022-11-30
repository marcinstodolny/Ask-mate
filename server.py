from flask import Flask, request, render_template, redirect
import util
import data_manager
import datetime
import time
app = Flask(__name__)


@app.route("/list", methods=['POST', 'GET'])
def all_questions():
    sort_by = request.form.get('sort_by')
    order_by = request.form.get('order_by')
    if sort_by is None:
        questions = sort_list('question')
    else:
        questions = sort_list('question', sort_by, order_by)
    return render_template('index.html', questions=questions, sort=sort_by, order=order_by, link="/list")


@app.route("/", methods=['POST', 'GET'])
def main_page():
    sort_by = request.form.get('sort_by')
    order_by = request.form.get('order_by')
    if sort_by is None:
        questions = sort_list('question', limit='LIMIT 5')
    else:
        questions = sort_list('question', sort_by, order_by, limit='LIMIT 5')
    return render_template('index.html', questions=questions, sort=sort_by, order=order_by, link="/")


@app.route("/question/<question_id>")
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)[0]
    answers = data_manager.get_answers_by_question_id(question_id)
    comments = data_manager.get_comments_by_question_id(question_id)
    question['submission_time'] = (datetime.datetime.now().replace(microsecond=0)) - question['submission_time']
    data_manager.increment_view_number(question_id, 'question')
    return render_template('question.html', question=question, answers=answers, comments=comments)


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    if request.method != 'POST':
        return render_template('add_question.html', title="Add question")
    question_time = datetime.datetime.now()
    data_manager.add_new_question(question_time, 0, 0, request.form['title'], request.form['message'], None)
    question_id = data_manager.get_question_id(question_time)[0]['id']
    data_manager.update_question_time(question_time.strftime("%Y-%m-%d %H:%M:%S"), question_id)
    if request.files["file"]:
        data_manager.save_photo(request.files["file"], question_id, 'question')
        data_manager.update_image('question', question_id, f'{question_id}.png')
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method != 'POST':
        question = data_manager.get_question_by_id(question_id)[0]
        return render_template('edit_question.html', title="Edit question", question=question)
    data_manager.update_question(question_id, request.form['title'], request.form['message'])
    if request.files["file"]:
        data_manager.save_photo(request.files["file"], question_id, 'question')
        data_manager.update_image('question', question_id, f'{question_id}.png')
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/delete", methods=['POST'])
def delete_question(question_id):
    if request.method == 'POST':
        data_manager.remove_files(question_id)
        data_manager.delete_question(question_id)
        return redirect('/')


@app.route("/question/<question_id>/vote-up", methods=["POST"])
@app.route("/answer/<answer_id>/<question_id>/vote-up", methods=["POST"])
def up_vote(question_id, answer_id=None):
    if answer_id:
        data_manager.change_vote_number(answer_id, 'answer', 1)
    else:
        data_manager.change_vote_number(question_id, 'question', 1)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/vote-down", methods=["POST"])
@app.route("/answer/<answer_id>/<question_id>/vote-down", methods=["POST"])
def down_vote(question_id, answer_id=None):
    if answer_id:
        data_manager.change_vote_number(answer_id, 'answer', -1)
    else:
        data_manager.change_vote_number(question_id, 'question', -1)
    return redirect(f"/question/{question_id}")


@app.route("/question/<answer_id>/new-comment", methods=["POST", "GET"])
@app.route("/question/<question_id>/new-comment", methods=["POST", "GET"])
def add_comment(question_id=None, answer_id=None):
    if request.method == 'POST':
        submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.new_comment(submission_time, request.form['message'], 0, question_id=question_id, answer_id=answer_id)
        return redirect(f"/question/{question_id}")
    return render_template('add_comment.html', title="Add comment", question_id=question_id)


def sort_list(table, sort_by='submission_time', order_direction='DESC', limit=''):
    return data_manager.get_sorted_data(table, sort_by, order_direction, limit)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method != 'POST':
        return render_template('add_answer.html',
                               title="Add answer",
                               question_id=question_id)
    submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = request.form['message']
    data_manager.new_answer(submission_time, 0, question_id, message, None)
    answer_id = data_manager.get_answer_id_by_time(submission_time)[0]['id']
    if request.files["file"]:
        data_manager.save_photo(request.files["file"], answer_id, 'answer')
        data_manager.update_image('answer', answer_id, f'{answer_id}.png')
    return redirect(f"/question/{question_id}")


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    if request.method == 'POST':
        question_id = data_manager.get_question_id_by_answer_id(answer_id)[0]['question_id']
        data_manager.delete_answer(answer_id)
        data_manager.remove_photo(answer_id, 'answer')
        return redirect(f"/question/{question_id}")


@app.route('/answer/<answer_id>/edit', methods=['GET','POST'])
def edit_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)[0]
    if request.method != 'POST':
        return render_template('edit_answer.html', title="Edit answer", answer=answer)
    data_manager.update_answer(answer_id, request.form['message'])
    if request.files["file"]:
        data_manager.save_photo(request.files["file"], answer_id, 'answer')
        data_manager.update_image('answer', answer_id, f'{answer_id}.png')
    return redirect(f"/question/{answer['question_id']}")


@app.route('/search')
def searching():
    search_phrases = request.args.get('q')
    questions = data_manager.search_questions(search_phrases)
    return render_template('index.html', questions=questions)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=60000,
        debug=True,
    )
