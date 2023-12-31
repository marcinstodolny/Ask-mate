from bonus_questions import SAMPLE_QUESTIONS
import datetime
import data_manager
import util
import password_management
import bonus_questions

from flask import Flask, request, render_template, redirect, session, url_for, escape


app = Flask(__name__)
app.secret_key = b'ask-mate-3'


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route("/list")
def all_questions():
    sort_by = request.args.get('sort_by')
    order_by = request.args.get('order_by')
    questions = util.sort_list() if sort_by is None else util.sort_list(sort_by, order_by)
    if is_login():
        user_reputation = data_manager.get_user_data(session['id'])[0]['reputation']
        return render_template('index.html',
                               message=f"Logged in as {escape(session['username'])}",
                               questions=questions,
                               sort=sort_by,
                               order=order_by,
                               reputation=user_reputation)
    return render_template('index.html', questions=questions, sort=sort_by, order=order_by)


@app.route("/", methods=['POST', 'GET'])
def main_page():
    questions = util.sort_list(limit='LIMIT 5')
    if is_login():
        user_reputation = data_manager.get_user_data(session['id'])[0]['reputation']
        return render_template('index.html', message=f"Logged in as {escape(session['username'])}", questions=questions, reputation=user_reputation)
    return render_template('index.html', questions=questions)


def is_login():
    return 'username' in session


def is_registered(username):
    return data_manager.is_user_exist(username)


@app.route("/login", methods=['POST', 'GET'])
def login_page():
    return render_template('login.html')


@app.route("/login_attempt", methods=['POST', 'GET'])
def login_attempt():
    if request.method == 'POST':
        username = request.form['username']
        if is_registered(username) and password_management.verify_password(request.form.get('password'),
                                                                           data_manager.get_user_password(username)[0]['password']):
            session['username'] = username
            session['id'] = data_manager.get_user_id(session['username'])[0]['id']
            return redirect(url_for('main_page'))
    return render_template('login.html', message='Invalid login attempt')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('main_page'))


@app.route("/question/<question_id>", methods=['GET', 'POST'])
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)[0]
    question['submission_time'] = (datetime.datetime.now().replace(microsecond=0)) - question['submission_time']
    answers = data_manager.get_answers_by_question_id(question_id)
    comments = data_manager.get_comments()
    data_manager.increment_view_number(question_id)
    util.exchange_newlines(question, answers, comments)
    if is_login():
        user_reputation = data_manager.get_user_data(session['id'])[0]['reputation']
        return render_template('question.html',
                               question=question,
                               answers=answers,
                               comments=comments,
                               tags=data_manager.get_tags_name_and_id_by_question_id(question_id),
                               message=f"Logged in as {escape(session['username'])}",
                               user_id=session['id'],
                               reputation=user_reputation,
                               all_users=data_manager.get_users_list())

    return render_template('question.html',
                           question=question,
                           answers=answers,
                           comments=comments,
                           tags=data_manager.get_tags_name_and_id_by_question_id(question_id),
                           all_users=data_manager.get_users_list())


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    if request.method != 'POST':
        return render_template('add_question.html', title="Add question", login=is_login())
    if is_login():
        question_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.add_new_question(session['id'], question_time, 0, 0, request.form['title'], request.form['message'], None)
        question_id = data_manager.get_question_id_by_time(question_time)[0]['id']
        if request.files["file"]:
            data_manager.save_photo(request.files["file"], question_id, 'question')
            data_manager.update_image('question', question_id, f'question\\{question_id}.png')
        return redirect(f"/question/{question_id}")
    return redirect('/')


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method != 'POST':
        return render_template('edit_question.html', title="Edit question",
                               question=data_manager.get_question_by_id(question_id)[0], login=is_login())
    if is_login():
        data_manager.update_question(question_id, request.form['title'], request.form['message'])
        if request.files["file"]:
            data_manager.save_photo(request.files["file"], question_id, 'question')
            data_manager.update_image('question', question_id, f'question\\{question_id}.png')
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/delete", methods=['POST'])
def delete_question(question_id):
    if request.method == 'POST' and is_login() and session['id'] == data_manager.get_question_by_id(question_id)[0]['user_id']:
        data_manager.remove_images(question_id)
        data_manager.delete_question(question_id)
        return redirect('/')


@app.route("/question/<question_id>/vote-up", methods=["POST"])
@app.route("/answer/<answer_id>/<question_id>/vote-up", methods=["POST"])
def up_vote(question_id, answer_id=None):
    vote_gain = 1
    if answer_id and is_login():
        vote_update(answer_id, 'answer', vote_gain, reputation=10)
    elif is_login():
        vote_update(question_id, 'question', vote_gain, reputation=5)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/vote-down", methods=["POST"])
@app.route("/answer/<answer_id>/<question_id>/vote-down", methods=["POST"])
def down_vote(question_id, answer_id=None):
    vote_decrease = -1
    reputation_decrease = -2
    if answer_id and is_login():
        vote_update(answer_id, 'answer', vote_decrease, reputation_decrease)
    elif is_login():
        vote_update(question_id, 'question', vote_decrease, reputation_decrease)
    return redirect(f"/question/{question_id}")


def vote_update(item_id, table, vote, reputation):
    data_manager.change_vote_number(item_id, table, vote, session['id'])
    data_manager.change_reputation(item_id, table, reputation, session['id'])


@app.route("/question/<question_id>/new-comment", methods=["POST", "GET"])
def add_comment_to_question(question_id=None):
    if request.method != 'POST':
        return render_template('add_comment_q.html', title="Add comment", question_id=question_id, login=is_login())
    if is_login():
        data_manager.new_comment(session['id'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 request.form['message'], 0, question_id=question_id)
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/new-comment", methods=["POST", "GET"])
def add_comment_to_answer(answer_id=None):
    if request.method != 'POST':
        return render_template('add_comment_a.html', title="Add comment", answer_id=answer_id, login=is_login())
    if is_login():
        data_manager.new_comment(session['id'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), request.form['message'], 0,
                                 answer_id=answer_id)
    return redirect(f"/question/{data_manager.get_question_id_by_answer_id(answer_id)[0]['question_id']}")


@app.route('/comment/<comment_id>/<question_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id, question_id):
    comment = data_manager.get_comment_by_id(comment_id)[0]
    if request.method != 'POST':
        return render_template('edit_comment.html', title="Edit comment", comment=comment, question=question_id, login=is_login())
    if is_login():
        submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.update_comment(comment_id, request.form['message'], submission_time)
    return redirect(f"/question/{question_id}")


@app.route('/comments/<comment_id>/<question_id>/delete', methods=['POST'])
def delete_comment(comment_id, question_id):
    if request.method == 'POST' and is_login():
        data_manager.delete_comment(comment_id)
        return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method != 'POST':
        return render_template('add_answer.html',
                               title="Add answer",
                               question_id=question_id,
                               login=is_login())
    submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if is_login():
        data_manager.new_answer(session['id'], submission_time, 0, question_id, request.form['message'], None)
        answer_id = data_manager.get_answer_id_by_time(submission_time)[0]['id']
        if request.files["file"]:
            data_manager.save_photo(request.files["file"], answer_id, 'answer')
            data_manager.update_image('answer', answer_id, f'answer\\{answer_id}.png')
    return redirect(f"/question/{question_id}")


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)[0]
    if request.method != 'POST':
        return render_template('edit_answer.html', title="Edit answer", answer=answer, login=is_login())
    if is_login():
        data_manager.update_answer(answer_id, request.form['message'])
        if request.files["file"]:
            data_manager.save_photo(request.files["file"], answer_id, 'answer')
            data_manager.update_image('answer', answer_id, f'answer\\{answer_id}.png')
    return redirect(f"/question/{answer['question_id']}")


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    if request.method == 'POST' and is_login():
        question_id = data_manager.get_question_id_by_answer_id(answer_id)[0]['question_id']
        data_manager.delete_answer(answer_id)
        data_manager.remove_photo(answer_id, 'answer')
        return redirect(f"/question/{question_id}")


@app.route('/search')
def searching():
    search_phrases = request.args.get('q')
    if search_phrases[0] == '\\':
        search_phrases = search_phrases[1:]
    titles = data_manager.search_question_title(search_phrases)
    answers = data_manager.search_answer(search_phrases)
    question_messages = data_manager.search_question_message(search_phrases)
    util.exchange_search_phrases(titles, answers, question_messages, search_phrases)
    message = ""
    user_reputation = 0
    if is_login():
        message = f"Logged in as {escape(session['username'])}"
        user_reputation = data_manager.get_user_data(session['id'])[0]['reputation']
    return render_template('search.html',
                           titles=titles,
                           question_messages=question_messages,
                           answers=answers,
                           search=search_phrases,
                           message=message,
                           reputation=user_reputation)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def new_tag(question_id):
    if request.method != 'POST':
        return render_template('add_tag.html', title="Add new tag", question_id=question_id, login=is_login())
    if is_login():
        tag_id = data_manager.get_tag_id_by_tag_name(request.form['message'])
        if not tag_id:
            data_manager.add_new_tag(request.form['message'])
        tag_id = data_manager.get_tag_id_by_tag_name(request.form['message'])[0]['id']
        if not data_manager.check_tag_id_with_question_id(question_id, tag_id):
            data_manager.link_tag_id_with_question_id(question_id, tag_id)
    return redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    if is_login():
        data_manager.delete_tag_from_question(question_id, tag_id)
    return redirect(f"/question/{question_id}")


@app.route('/tags')
def tags():
    tags_list = data_manager.get_tag_names_and_tags_occurs()
    return render_template('tags_list.html', tags_list=tags_list)


@app.route('/users')
def list_users():
    if not is_login():
        return redirect("/")
    users_list = data_manager.get_users_list()
    return render_template('users_list.html',
                           users=users_list,
                           reputation=data_manager.get_user_data(session['id'])[0]['reputation'],
                           message=f"Logged in as {escape(session['username'])}")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method != 'POST':
        return render_template('registration.html')
    user_name = request.form.get('user-name')
    if data_manager.is_user_exist(user_name):
        message = "This user name exist!"
    elif request.form.get('password') == request.form.get('confirm-password'):
        hashed_password = password_management.hash_password(request.form.get('password'))
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.insert_new_user(user_name, hashed_password, time)
        return redirect('/')
    else:
        message = "Entered password are not the same!"
    return render_template('registration.html', message=message)


@app.route('/user/<user_id>', methods=['GET', 'POST'])
def user_page(user_id):
    if not is_login():
        return redirect("/")
    user_data = data_manager.get_user_data(user_id)
    questions = data_manager.get_user_questions(user_id)
    answers = data_manager.get_user_answers(user_id)
    comments = data_manager.get_user_comments(user_id)
    answer_id_to_question_id = data_manager.get_question_id_to_bypass_lack_of_question_id_in_comments()
    return render_template('user_page.html', users=user_data, questions=questions, answers=answers, comments=comments,answer_id_to_question_id=answer_id_to_question_id)

@app.route('/bonus-questions', methods=['GET', 'POST'])
def bonus_questions():
    questions = bonus_questions.SAMPLE_QUESTIONS
    return render_template('bonus_questions.html', questions=questions)


@app.route('/question/<question_id>/<answer_id>/accept', methods=['POST'])
def accept_answer(question_id, answer_id):
    if not is_login():
        return redirect("/")
    data_manager.save_accepted_answer(question_id, answer_id)
    return redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/<answer_id>/remove_accept', methods=['POST'])
def remove_accepted_answer(question_id, answer_id):
    if not is_login():
        return redirect("/")
    data_manager.remove_accepted_answer(question_id, answer_id)
    return redirect(f"/question/{question_id}")



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=60000,
        debug=True,
    )
