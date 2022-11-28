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


def delete_question(cursor, question_id):
    query = """
        DELETE FROM question
        WHERE id = %s;
        DELETE FROM comment
        WHERE question_id = %s;
        DELETE FROM answer
        WHERE question_id = %s;"""
    cursor.execute(query, [question_id, question_id, question_id])


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
def get_answers_by_question_id(cursor, question_id):
    query = """
                    SELECT *
                    FROM answer
                    where question_id = %s
                    """
    cursor.execute(query, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def update_image(cursor, question_id, image):
    query = """
                UPDATE question
                SET 
                image = %s
                WHERE id = %s;
                """
    cursor.execute(query, [image, question_id])


def save_photo(img, id_index, folder):
    way = (os.path.abspath(f"static\\upload\\{folder}\\"))
    img.save(f"{way}\\{id_index}.png")
    return f"{id_index}.png"


def remove_question_answers(header, question_id, all_answers):
    way = (os.path.abspath("static\\upload\\answers\\"))
    for answer in reversed(all_answers):
        if answer[header['question id']] == question_id:
            all_answers.pop(int(answer[header['id']]) - 1)
            if os.path.exists(f"{way}\\{int(answer[header['id']])}.png"):
                os.remove(f"{way}\\{int(answer[header['id']])}.png")
    return all_answers


def remove_photo(all_questions, id_index, way):
    if os.path.exists(f"{way}\\{id_index + 1}.png"):
        os.remove(f"{way}\\{id_index + 1}.png")
    all_questions.pop(id_index)
    return all_questions
