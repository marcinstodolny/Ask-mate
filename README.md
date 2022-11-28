# AskMate (sprint 2)

## Story

Last week you created a pretty good site from scratch. It already has some features but it's a bit difficult to maintain due to the fact that the data is stored in CSV files. Some new features are also needed, to make the site more usable and more appealing to users.

The management decided to move further as users requested new features, such as the ability to comment on answers and tag questions (and of course the issue with CSV files). There are several other feature requests which you can find in the user stories.

Just like last week, management is handing out a **prioritized list** of new user stories that you must add to the unfinished stories from last week on your product backlog. Try to estimate these new stories as well, and, based on the estimations, decide how many of them your team can finish until the demo. As the order is important, you must choose from the beginning of the list as much as you can.

## What are you going to learn?

- Use `psycopg2` to connect to a PostgreSQL database from Python.
- Understand basic SQL commands (`SELECT`, `UPDATE`, `DELETE`, `INSERT`).
- Understand CSS basics.
- Work according to the Scrum framework,
- Create a _sprint plan_.

## Tasks

1. Since you work in a new repository, but also need the code from the previous sprint, add the `ask-mate-2` repository as a new remote to the repository of the previous sprint, then pull (merge) and push your changes into it.
    - There is a merge commit in the project repository that contains code from the previous sprint.

2. Make the application use a database instead of CSV files.
    - The application uses a PostgreSQL database instead of CSV files.
    - The application respects the `PSQL_USER_NAME`, `PSQL_PASSWORD`, `PSQL_HOST` and `PSQL_DB_NAME` environment variables.
    - The database structure (tables) is the same as in the provided SQL file (`sample_data/askmatepart2-sample-data.sql`).

3. Allow the user to add comments to a question.
    - There is a `/question/<question_id>/new-comment` page.
    - The page is linked from the question page.
    - There is a form with a `message` field, and it issues `POST` requests.
    - After submitting, the page redirects to the question detail page, and the new comment appears together with its submission time.

4. Allow the user to add comments to an answer.
    - There is a `/answer/<answer_id>/new-comment` page.
    - The page is linked from the question page, next to or below the answer.
    - There is a form with a `message` field, and it issues `POST` requests.
    - After submitting, the page redirects to the question detail page, and the new comment appears together with its submission time.

5. Implement searching in questions and answers. (Hint: [Passing data from browser](https://learn.code.cool/web-python/#/../pages/web/passing-data-from-browser))

    - There is a search box and "Search" button on the main page.
    - When writing something and pressing the button, a results list of questions is displayed (with the same data as in the list page).
    - The results list contains questions for which the title or description contain the searched phrase.
    - The results list also contains questions which have answers for which the message contains the searched phrase.
    - The results list URL is `/search?q=<search phrase>`.

6. Allow the user to edit the posted answers.
    - There is a `/answer/<answer_id>/edit` page.
    - The page is linked from the answer page.
    - There is a form with a `message` field, and it issues a `POST` request.
    - The field is pre-filled with existing answer data.
    - After submitting, the page redirects to the question detail page, and the answer is updated.

7. Allow the user to edit comments.
    - The page URL is `/comment/<comment_id>/edit`.
    - There is a link to the edit page next to each comment.
    - The page contains a `POST` form with a `message` field.
    - The field pre-filled with current comment message.
    - After submitting, the page redirects to the question detail page, and the new comment appears.
    - The submission time is updated.
    - There is a message that says "Edited `<number_of_editions>` times." next to or below the comment.

8. Allow the user to delete comments.
    - There is a recycle bin icon next to the comment.
    - Clicking the icon asks the user to confirm the deletion.
    - The deletion itself is implemented by the `/comments/<comment_id>/delete` endpoint (which does not ask for confirmation anymore).
    - After deleting, the page redirects to the question detail page, and the comment is not shown anymore.

9. Display five latest questions on the main page (`/`).
    - The main page (`/`) displays the five latest submitted questions.
    - The main page contains a link to all of the questions (`/list`).

10. Implement sorting for the question list. [If you did this user story in the previous sprint, now you only have to rewrite it to use SQL.]
    - The question list can be sorted by title, submission time, message, number of views, and number of votes.
    - The list can be sorted in ascending and descending order.
    - The order is passed as query string parameters, for example `/list?order_by=title&order_direction=desc`.

11. Add tags to questions.
    - The tags are displayed on the question detail page.
    - There is an "add tag" link which leads to the page for adding a tag.
    - The URL for the page for adding a tag has is `/question/<question_id>/new-tag`.
    - The page allows to choose from existing tags or define a new one.

12. Highlight the search phrase in the search results.
    - On the search results page, the searched phrase is highlighted.
    - If the phrase is found in an answer, the answer is also displayed (slightly indented).
    - The search phrase is also highlighted in the answers.

13. Allow the user to delete tags from questions.
    - There is an X link next to each tag.
    - Clicking that link deletes the tag and reloads the question page.
    - The deletion is implemented as `/question/<question_id>/tag/<tag_id>/delete` endpoint.

## General requirements

None

## Hints

- It's important that if the database table has a timestamp column then you cannot insert a UNIX timestamp value directly into that table, you should use:
    - either strings in the following format '1999-01-08 04&colon;05&colon;06',
    - or if you use psycopg2 and the datetime module, you can pass a datetime object to the SQL query as parameter (details in the background materials: [Date/Time handling in psycopg2](https://www.psycopg.org/docs/usage.html?highlight=gunpoint#date-time-objects-adaptation))
- Pay attention on the order of inserting data into the tables, because you may violate foreign key constraints (that means e.g. if you insert data into the question_tag before you insert into the tag table the corresponding tag id you want to refer to then it won't exist yet)!
- You can import the sample data file into `psql` with the `\i` command or run it via the Database tool in PyCharm.
- Some user stories may require to deal with CSS as well, but do not deal with CSS too much. It's more important that you write proper queries, have a working connection with psycopg2, have a clean Python code than create an amazingly beautiful web application (although if you have time, of course it's not forbidden to do so :smiley:).

### Data models

All data should be persisted in a PostgreSQL database in the following tables (you can ignore data in the not implemented fields):

![AskMate data model part 2](media/web-python/askmate-data-model-part-2.png)

**question table**<br>
*id:* A unique identifier for the question<br>
*submission_time:* The date and time when the question was posted<br>
*view_number:* How many times this question was displayed in the single question view<br>
*vote_number:* The sum of votes this question has received<br>
*title:* The title of the question<br>
*message:* The question text<br>
*image:* the path to the image for this question<br>

**answer table**<br>
*id:* A unique identifier for the answer<br>
*submission_time:* The date and time when the answer was posted<br>
*vote_number:* The sum of votes this answer has received<br>
*question_id:* The id of the question this answer belongs to<br>
*message:* The answer text<br>
*image:* The path to the image for this answer<br>

**tag table**<br>
*id:* A unique identifier for the tag<br>
*name:* The name of the tag<br>

**question_tag table**<br>
*question\_id:* The id of the question the tag belongs to<br>
*tag\_id:* The id of the tag belongs to the question<br>

**comment table**<br>
*id:* A unique identifier for the comment<br>
*question\_id:* The id of the question this comment belongs to (if the comment belongs to an answer, the value of this field should be NULL)<br>
*answer\_id:* The id of the answer this comment belongs to (if the comment belongs to a question, the value of this field should be NULL)<br>
*message:* The comment text<br>
*submission\_time:* The date and time the comment was posted or updated<br>
*edited\_number::* How many times this comment was edited<br>

### Database and sample data

To init the database use the `sample_data/askmatepart2-sample-data.sql` file in your repository.

## Background materials

### Git

- <i class="far fa-exclamation"></i> [Working with the `git remote` command](https://git-scm.com/docs/git-remote)
- <i class="far fa-book-open"></i> [Merge vs rebase](project/curriculum/materials/pages/git/merge-vs-rebase.md)
- <i class="far fa-book-open"></i> [Mastering git](project/curriculum/materials/pages/git/mastering-git.md)

### SQL

- <i class="far fa-exclamation"></i> [Installing and setting up PostgreSQL](project/curriculum/materials/pages/tools/installing-postgresql.md)
- <i class="far fa-exclamation"></i> [Installing psycopg2](project/curriculum/materials/pages/tools/installing-psycopg2.md)
- <i class="far fa-exclamation"></i> [Best practices for Python/Psycopg/Postgres](project/curriculum/materials/pages/python/tips-python-psycopg-postgres.md)
- [Setting up a database connection in PyCharm](project/curriculum/materials/pages/tools/pycharm-database.md)
- [Date/Time handling in psycopg2](https://www.psycopg.org/docs/usage.html?highlight=gunpoint#date-time-objects-adaptation)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page on Queries](https://www.postgresql.org/docs/current/queries.html)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page Data Manipulation](https://www.postgresql.org/docs/current/dml.html)

### Agile/SCRUM

- [Agile project management](project/curriculum/materials/pages/methodology/agile-project-management.md)
- <i class="far fa-book-open"></i> [Planning poker](https://en.wikipedia.org/wiki/Planning_poker)

### Web basics (Flask/Jinja/HTML/CSS)

- <i class="far fa-exclamation"></i> [Flask/Jinja Tips & Tricks](project/curriculum/materials/pages/web/web-with-python-tips.md)
- <i class="far fa-exclamation"></i> [Passing data from browser](project/curriculum/materials/pages/web/passing-data-from-browser.md)
- [Collection of web resources](project/curriculum/materials/pages/web/resources.md)
- <i class="far fa-book-open"></i> [Pip and VirtualEnv](project/curriculum/materials/pages/python/pip-and-virtualenv.md)
- <i class="far fa-book-open"></i> [A web-framework for Python: Flask](project/curriculum/materials/pages/python/python-flask.md)
- <i class="far fa-book-open"></i> [Flask documentation](http://flask.palletsprojects.com/) (the Quickstart gives a good overview)
- <i class="far fa-book-open"></i> [Jinja2 documentation](https://jinja.palletsprojects.com/en/2.10.x/templates/)
