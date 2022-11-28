import os
from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

# @database_common.connection_handler
# def get_mentors_by_last_name(cursor, last_name):
#     query = """
#         SELECT first_name, last_name, city
#         FROM mentor
#         WHERE last_name = %(last_name)s
#         ORDER BY first_name"""
#     cursor.execute(query, {'last_name': last_name})
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
    query = f"""
                INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                VALUES ('{submission_time}', '{view_number}', '{vote_number}', '{title}', '{message}', {image})
                """
    cursor.execute(query)


@database_common.connection_handler
def remove_question(cursor, question_id):
    query = f"""
                DELETE FROM question
                WHERE id = {question_id}
                DELETE FROM comment
                WHERE question_id = {question_id}
                DELETE FROM answer
                WHERE question_id = {question_id}"""

    cursor.execute(query)


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = f"""
                SELECT *
                FROM question
                where id = '{question_id}'
                """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_question_id(cursor, time):
    query = f"""
                SELECT id
                FROM question
                where submission_time = '{time}'
                """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_question_id(cursor, question_id):
    query = f"""
                    SELECT *
                    FROM answer
                    where question_id = '{question_id}'
                    """
    cursor.execute(query)
    return cursor.fetchall()


def save_photo(img, id_index, folder):
    way = (os.path.abspath(f"static\\upload\\{folder}\\"))
    img.save(f"{way}\\{id_index + 1}.png")
    return f"{id_index + 1}.png"


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


