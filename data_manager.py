import csv
import os


def get_all_data_from_file(data_file_path):
    all_lines = []
    with open(data_file_path, 'r') as f:
        all_lines.extend(iter(csv.reader(f)))
    return all_lines


def write_file(data_file_path, data, new_element=False):
    if new_element:
        data.append(new_element)
    with open(data_file_path, 'w', newline='') as file:
        for line in data:
            csv.writer(file).writerow(line)


def save_photo(img, id_index, folder):
    way = (os.path.abspath(f"static\\upload\\{folder}\\"))
    img.save(f"{way}\\{id_index + 1}.png")
    return f"{id_index + 1}.png"


def reindex_items(all_items, question_id, headers, way=False, rewrite_question_id=False):
    for i in range(len(all_items)):
        all_items[i][headers["id"]] = i + 1
        all_items[i][headers["image"]] = f"{i + 1}.png"
        if rewrite_question_id and int(all_items[i][headers['question id']]) > question_id:
            all_items[i][headers['question id']] = int(all_items[i][headers['question id']]) - 1
    if way:
        rename_files(way)


def remove_question_answers(header, question_id, all_answers):
    way = (os.path.abspath("static\\upload\\answers\\"))
    for answer in reversed(all_answers):
        if answer[header['question id']] == question_id:
            all_answers.pop(int(answer[header['id']]) - 1)
            if os.path.exists(f"{way}\\{int(answer[header['id']])}.png"):
                os.remove(f"{way}\\{int(answer[header['id']])}.png")
    rename_files(way)
    return all_answers


def rename_files(way):
    all_files = os.listdir(way)
    test = sorted([int(item.split(".")[0]) for item in all_files])
    for i, item in enumerate(test, start=1):
        os.rename(f"{way}\\{item}.png", f"{way}\\{i}.png")


def remove_photo(all_questions, id_index, way):
    if os.path.exists(f"{way}\\{id_index + 1}.png"):
        os.remove(f"{way}\\{id_index + 1}.png")
    all_questions.pop(id_index)
    return all_questions
