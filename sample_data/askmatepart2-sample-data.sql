--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS pk_users_id CASCADE;

DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial NOT NULL,
    user_id integer,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    accepted integer
);

DROP TABLE IF EXISTS public.users;
CREATE TABLE users (
    id serial NOT NULL,
    username varchar(20),
    password text,
    reputation integer,
    questions_no integer,
    answers_no integer,
    comments_no integer,
    registration_date date,
    questions_voted integer ARRAY,
    answers_voted integer ARRAY
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial NOT NULL,
    user_id integer,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial NOT NULL,
    user_id integer,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_users_id PRIMARY KEY (id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE;

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

INSERT INTO users VALUES (1, 'Tomek', '$2b$12$OctARDVbgi/Zuv4lPwZGoOaJi7SzKkbuwQD2H54ii.aju7qm7rQxC', 499, 2, 0, 1, '2022-12-13 14:49:35', array[]::integer[], array[]::integer[]);
INSERT INTO users VALUES (2, 'admin', '$2b$12$5/J3dRnIOPpRjbVnc835muntSETNgiG8b5lGOiXM4npi7nEhpiMpO', 9000, 1, 4, 0, '2022-12-13 14:49:35', array[]::integer[], array[]::integer[]);
INSERT INTO users VALUES (3, 'Marcin', '$2b$12$OctARDVbgi/Zuv4lPwZGoOaJi7SzKkbuwQD2H54ii.aju7qm7rQxC', 999, 1, 1, 1, '2022-12-13 14:49:35', array[]::integer[], array[]::integer[]);
SELECT pg_catalog.setval('users_id_seq', 3, true);
INSERT INTO question VALUES (0, 1, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL, 1);
INSERT INTO question VALUES (1, 2, '2017-04-29 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'question\1.png');
INSERT INTO question VALUES (2, 3, '2017-07-01 13:47:00', 156, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', NULL);
INSERT INTO question VALUES (3, 1, '2017-08-01 10:49:42', 1364, 10, 'How to add new line inside HTML', 'How to do that', NULL, 3);
INSERT INTO question VALUES (4, 1, '2017-09-01 15:41:05', 9427, 253, 'What does if __name__ == "__main__": do?', 'What does this do, and why should one include the if statement?

if __name__ == "__main__":
    print("Hello, World!")', NULL, 4);
INSERT INTO question VALUES (5, 3, '2017-09-01 19:41:30', 1364, 28, 'How do I check if a list is empty?', 'For example, if passed the following:

a = []
How do I check to see if a is empty?', NULL, 5);
SELECT pg_catalog.setval('question_id_seq', 4, true);

INSERT INTO answer VALUES (1, 2, '2017-04-28 16:49:00', 4, 0, 'You need to use brackets: my_list = []', NULL);
INSERT INTO answer VALUES (2, 3, '2017-04-25 14:42:00', 35, 0, 'Look it up in the Python docs', 'answer\2.png');
INSERT INTO answer VALUES (3, 2, '2017-09-25 14:42:00', 35, 3, 'try:', 'answer\1.png');
INSERT INTO answer VALUES (4, 2, '2017-09-02 19:21:00', 900, 4, 'It''s boilerplate code that protects users from accidentally invoking the script when they didn''t intend to. Here are some common problems when the guard is omitted from a script:

If you import the guardless script in another script (e.g. import my_script_without_a_name_eq_main_guard), then the latter script will trigger the former to run at import time and using the second script''s command line arguments. This is almost always a mistake.

If you have a custom class in the guardless script and save it to a pickle file, then unpickling it in another script will trigger an import of the guardless script, with the same problems outlined in the previous bullet.');
INSERT INTO answer VALUES (5, 2, '2017-11-25 14:42:00', 37, 5, 'if not a:
    print("List is empty")
Using the implicit booleanness of the empty list is quite Pythonic.');
SELECT pg_catalog.setval('answer_id_seq', 5, true);

INSERT INTO comment VALUES (1, 1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00');
INSERT INTO comment VALUES (2, 3, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00');
SELECT pg_catalog.setval('comment_id_seq', 2, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'html');
INSERT INTO tag VALUES (4, 'canvas');
INSERT INTO tag VALUES (5, 'wordpress');
SELECT pg_catalog.setval('tag_id_seq', 6, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 5);
INSERT INTO question_tag VALUES (2, 4);
INSERT INTO question_tag VALUES (3, 3);
INSERT INTO question_tag VALUES (4, 1);
INSERT INTO question_tag VALUES (5, 1);
