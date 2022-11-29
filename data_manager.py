import os
from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


# @database_common.connection_handler
# def get_all_question_data(cursor, table):
#     query = """
#             SELECT *
#             FROM %(table)s
#             """
#     cursor.execute(query, {'table': table})
#     return cursor.fetchall()
@database_common.connection_handler
def get_all_question_data(cursor, table):
    query = f"""
            SELECT *
            FROM {table}
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_question(cursor, submission_time, view_number, vote_number, title, message, image):
    query = """
                INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                VALUES (%s, %s, %s, %s, %s, %s)
                """

    cursor.execute(query, [submission_time, view_number, vote_number, title, message, image])


@database_common.connection_handler
def update_question(cursor, question_id, title, message):
    query = """
                UPDATE question
                SET 
                title = %s,
                message = %s
                WHERE id = %s;
                """
    cursor.execute(query, [title, message, question_id])


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE FROM question
        WHERE id = %s;
        """
    cursor.execute(query, [question_id])


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
                SELECT *
                FROM question
                where id = %s
                """
    cursor.execute(query, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def get_question_id(cursor, time):
    query = """
                SELECT id
                FROM question
                where submission_time = %s
                """
    cursor.execute(query, [time])
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_id_by_time(cursor, time):
    query = """
        SELECT id
        FROM answer
        WHERE submission_time = %s"""
    cursor.execute(query, [time])
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_question_id(cursor, question_id):
    query = """
                    SELECT *
                    FROM answer
                    WHERE question_id = %s
                    ORDER BY vote_number DESC
                    """
    cursor.execute(query, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """
        SELECT question_id
        FROM answer
        WHERE id = %s"""
    cursor.execute(query, [answer_id])
    return cursor.fetchall()


@database_common.connection_handler
def update_image(cursor, table, question_id, image):
    query = f"""
                UPDATE {table}
                SET image = %s
                WHERE id = %s;
                """
    cursor.execute(query, [image, question_id])


@database_common.connection_handler
def increment_view_number(cursor, question_id, table):
    query = f"""
                    UPDATE {table}
                    SET 
                    view_number = view_number + 1
                    WHERE id = %s;
                    """
    cursor.execute(query, [question_id])

@database_common.connection_handler
def new_answer(cursor, time, vote, question_id, message, image):
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, [time, vote, question_id, message, image])


@database_common.connection_handler
def change_vote_number(cursor, question_id, table, number):
    query = f"""
                        UPDATE {table}
                        SET 
                        vote_number = vote_number + %s
                        WHERE id = %s;
                        """
    cursor.execute(query, [number, question_id])


@database_common.connection_handler
def get_sorted_data(cursor, table, sort_by, order_by):
    query = f"""
            SELECT *
            FROM {table}
            ORDER BY {sort_by} {order_by};
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_by_question_id(cursor, question_id):
    query = """
                        SELECT *
                        FROM comment
                        WHERE question_id = %s
                        ORDER BY id DESC
                        """
    cursor.execute(query, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def new_comment(cursor, time, message, edited_count, question_id=None, answer_id=None):
    query = """
            INSERT INTO comment (submission_time, question_id, answer_id, message, edited_count)
            VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, [time, question_id, answer_id, message, edited_count])


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = """
        DELETE FROM answer
        WHERE id = %s"""
    cursor.execute(query, [answer_id])


@database_common.connection_handler
def search_questions(cursor, sentence):
    searching_phrase = f"%{sentence}%"
    query = """
        SELECT DISTINCT question.id, question.title, question.submission_time, question.view_number, question.vote_number
        FROM question
        FULL OUTER JOIN answer ON question.id = answer.question_id
        WHERE title LIKE %s or question.message LIKE %s or answer.message LIKE %s"""
    cursor.execute(query, [searching_phrase, searching_phrase, searching_phrase])
    return cursor.fetchall()


def save_photo(img, id_index, folder):
    way = (os.path.abspath(f"static\\upload\\{folder}\\"))
    img.save(f"{way}\\{id_index}.png")
    return f"{id_index}.png"


def remove_photo(id_index, folder):
    way = (os.path.abspath(f"static\\upload\\{folder}\\"))
    if os.path.exists(f"{way}\\{id_index}.png"):
        os.remove(f"{way}\\{id_index}.png")

@database_common.connection_handler
def update_answer(cursor, answer_id, message):
    query = """
                UPDATE answer
                SET 
                message = %s
                WHERE id = %s;
                """
    cursor.execute(query, [message, answer_id])

@database_common.connection_handler
def get_answer_by_id(cursor, answer_id):
    query = """
                SELECT *
                FROM answer
                where id = %s
                """
    cursor.execute(query, [answer_id])
    return cursor.fetchall()


@database_common.connection_handler
def remove_files(cursor, question_id):
    print(question_id)
    query = """
            SELECT image
            FROM question
            WHERE id = %s;
            """
    cursor.execute(query, [question_id])
    question = cursor.fetchall()
    query = """
                SELECT image
                FROM  answer
                WHERE question_id = %s;
                """
    cursor.execute(query, [question_id])
    answer = cursor.fetchall()
    question_way = (os.path.abspath(f"static\\upload\\question\\"))
    answer_way = (os.path.abspath(f"static\\upload\\answer\\"))
    for item in question:
        if os.path.exists(f"{question_way}\\{item['image']}"):
            os.remove(f"{question_way}\\{item['image']}")
    for item in answer:
        if os.path.exists(f"{answer_way}\\{item['image']}"):
            os.remove(f"{answer_way}\\{item['image']}")


@database_common.connection_handler
def update_question_time(cursor, time, question_id):
    query = """
                UPDATE question
                SET submission_time = %s
                WHERE id = %s;
                """
    cursor.execute(query, [time, question_id])

