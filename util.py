import data_manager
import time


def increment_view_number(questions, question_id, headers):
    current_question = questions[int(question_id) - 1]
    current_question[headers["view number"]] = int(current_question[headers["view number"]]) + 1
    data_manager.write_file("questions.csv", questions)
    return current_question


def set_new_values(header, data, size, question_id=False):
    new_list = ["" for _ in range(size)]
    new_list[header["id"]] = len(data) + 1
    new_list[header["submission time"]] = int(time.time())
    if question_id:
        new_list[header['question id']] = question_id
    else:
        new_list[header["view number"]] = 0
    new_list[header["vote number"]] = 0
    return new_list


def convert_elements(all_questions, headers):
    for i, item in enumerate(all_questions):
        all_questions[i][headers["view number"]] = int(item[headers["view number"]])
        all_questions[i][headers["vote number"]] = int(item[headers["vote number"]])
        all_questions[i][headers["title"]] = item[headers["title"]].capitalize()
    return all_questions

