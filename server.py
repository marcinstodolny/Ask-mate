from flask import Flask, request, render_template, redirect
import util
import data_manager
import datetime
import time
app = Flask(__name__)


@app.route("/list", methods=['POST', 'GET'])
def all_questions():
    sort_by = request.args.get('sort_by')
    order_by = request.args.get('order_by')
    questions = sort_list() if sort_by is None else sort_list(sort_by, order_by)
    return render_template('index.html', questions=questions, sort=sort_by, order=order_by)


@app.route("/", methods=['POST', 'GET'])
def main_page():
    questions = sort_list(limit='LIMIT 5')
    return render_template('index.html', questions=questions)


@app.route("/question/<question_id>")
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)[0]
    answers = data_manager.get_answers_by_question_id(question_id)
    comments = data_manager.get_comments()
    question['submission_time'] = (datetime.datetime.now().replace(microsecond=0)) - question['submission_time']
    data_manager.increment_view_number(question_id)
    return render_template('question.html', question=question, answers=answers, comments=comments)


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    if request.method != 'POST':
        return render_template('add_question.html', title="Add question")
    question_time = datetime.datetime.now()
    data_manager.add_new_question(question_time, 0, 0, request.form['title'], request.form['message'], None)
    question_id = data_manager.get_question_id_by_time(question_time)[0]['id']
    data_manager.update_question_time(question_time.strftime("%Y-%m-%d %H:%M:%S"), question_id)
    if request.files["file"]:
        data_manager.save_photo(request.files["file"], question_id, 'question')
        data_manager.update_image('question', question_id, f'question\\{question_id}.png')
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method != 'POST':
        question = data_manager.get_question_by_id(question_id)[0]
        return render_template('edit_question.html', title="Edit question", question=question)
    data_manager.update_question(question_id, request.form['title'], request.form['message'])
    if request.files["file"]:
        data_manager.save_photo(request.files["file"], question_id, 'question')
        data_manager.update_image('question', question_id, f'question\\{question_id}.png')
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/delete", methods=['POST'])
def delete_question(question_id):
    if request.method == 'POST':
        data_manager.remove_images(question_id)
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
def add_comment_to_question(question_id=None, answer_id=None):
    if request.method == 'POST':
        submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.new_comment(submission_time, request.form['message'], 0, question_id=question_id, answer_id=answer_id)
        return redirect(f"/question/{question_id}")
    return render_template('add_comment_q.html', title="Add comment", question_id=question_id)


@app.route('/comments/<comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    if request.method == 'POST':
        comment = data_manager.get_comment_by_id(comment_id)[0]
        if comment['answer_id']:
            question_id = data_manager.get_question_id_by_answer_id(comment['answer_id'])[0]['question_id']
        else:
            question_id = comment['question_id']
        data_manager.delete_comment(comment_id)
        return redirect(f'/question/{question_id}')


def sort_list(sort_by='submission_time', order_direction='DESC', limit=''):
    return data_manager.get_sorted_data(sort_by, order_direction, limit)


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
        data_manager.update_image('answer', answer_id, f'answer\\{answer_id}.png')
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
        data_manager.update_image('answer', answer_id, f'answer\\{answer_id}.png')
    return redirect(f"/question/{answer['question_id']}")


@app.route('/search')
def searching():
    search_phrases = request.args.get('q')
    questions = data_manager.search_questions(search_phrases)
    return render_template('index.html', questions=questions)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def new_tag(question_id):
    if request.method == 'POST':
        data_manager.add_new_tag(request.form['message'])
        return redirect(f"/question/{question_id}")
    return render_template('add_tag.html', title="Add new tag", question_id=question_id)


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)[0]
    if request.method != 'POST':
        return render_template('edit_comment.html', title="Edit comment", comment=comment)
    submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if comment['answer_id']:
        question_id = data_manager.get_question_id_by_answer_id(comment['answer_id'])[0]['question_id']
    else:
        question_id = comment['question_id']
    data_manager.update_comment(comment_id, request.form['message'], submission_time)
    return redirect(f"/question/{question_id}")


@app.route("/answer/<question_id>/new-comment", methods=["POST", "GET"])
@app.route("/answer/<answer_id>/new-comment", methods=["POST", "GET"])
def add_comment_to_answer(question_id=None, answer_id=None):
    if request.method == 'POST':
        submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.new_comment(submission_time, request.form['message'], 0, question_id=question_id, answer_id=answer_id)
        return redirect(f"/question/{data_manager.get_question_id_by_answer_id(answer_id)[0]['question_id']}")
    return render_template('add_comment_a.html', title="Add comment", answer_id=answer_id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=60000,
        debug=True,
    )
