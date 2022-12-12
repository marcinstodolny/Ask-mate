# AskMate (sprint 3)

## Story

Last week you made great progress improving your web application.
We need some more features to make it more usable and more appealing to users.

The users requested new features, such as the ability to register and login.
There are a few other feature requests which you can find in the user stories.

The management wants you to separate the already working features from
the upcoming ones, so your development team need to **start using branching
workflow and open new branches for the features you start in this sprint**.
Just like last week, the ownership is in your hands. There are no compulsory stories,
but of course, management would prefer if all stories were implemented.
So first, choose the stories, then ask a mentor to validate your choice.

Just like last week, you have a **prioritized list** of new user stories that you should
add to the unfinished stories from last week on your product backlog. Try to
estimate these new stories as well, and, based on the estimations, decide how many
your team can finish until the demo. As the order is important, you choose
from the beginning of the list as much as you can.

## What are you going to learn?

- Web routing and redirects
- Gitflow workflow
- Advanced SQL commands (`JOIN`, `GROUP BY`, and aggregate functions)
- User authentication with sessions
- Hashed passwords
- HTML and the Jinja2 templating engine
- Javascript basics DOM manipulation

## Tasks

1. Since you work in a new repository, but also need the code from the previous sprint, add the `ask-mate-3` repository as a new remote to the repository of the previous sprint, then pull (merge) and push your changes into it.
    - There is a merge commit in the project repository that contains code from the previous sprint.

2. As a user, I would like to be able to register a new account in the system.
    - There is a `/registration` page.
    - The page is linked from the front page.
    - There is a form on the `/registration` page when a request is issued with the `GET` method.
    - The form ask for a username (or email address) and a password, then issues a `POST` request to `/registration` on submitting.
    - After submitting, the page redirects to the main page and the new user account is saved in the database.
    - A user account consists of an email address stored as a username, a password stored as a password hash, and a registration date.

3. As a registered user, I would like to be able to log in to the system with my previously saved username and password.
    - There is a `/login` page.
    - The page is linked from the front page.
    - Theres is a form on the `/login` page when a request is issued with `GET` method.
    - The form asks for the username (email address) and password, then issues a `POST` request to `/login` on submit.
    - After submitting the page redirects to the main page and the user is logged in.
    - It is only possible to ask or answer a question when logged in.

4. There should be a page where I can list all the registered users with all their attributes.
    - There is a `/users` page.
    - The page is linked from the front page when logged in.
    - The page is not accessible without logging in.
    - Theres is a `<table>` with user data in it. The table contains the following details of a user.
  - Username (with a link to the user page if implemented)
  - Registration date
  - Number of asked questions (if binding is implemented)
  - Number of answers (if binding is implemented)
  - Number of comments (if binding is implemented)
  - Reputation (if implemented)

5. As a user, when I add a new question, I would like to be saved as the user who created the new question.
    - The user ID of the logged in user is saved when a new question is added.

6. As a user, when I add a new answer, I would like to be saved as the user who created the new answer.
    - The user ID of the logged in user is saved when a new answer is added.

7. As a user, when I add a new comment, I would like to be saved as the user who created the new comment.
    - The user ID of the logged in user is saved when a new comment is added.

8. There should be a page where we can see all details and activities of a user.
    - There is a `/user/<user_id>` page.
    - The user page of a logged in user is linked from the front page.
    - The page of every user is linked from the users list page.
    - Theres is a list with the following deatils about the user.
  - User ID
  - Username (link to user page if implemented)
  - Registration date
  - Number of asked questions (if binding is implemented)
  - Number of answers (if binding is implemented)
  - Number of comments (if binding is implemented)
  - Reputation (if implemented)
    - There is a separate table where every **question** is listed that the user created. The related question is linked in every line.
    - There is a separate table where every **answer** is listed that the user created. The related question is linked in every line.
    - There is a separate table where every **comment** is listed that the user created. The related question is linked in every line.

9. As a user, I would like to have the possibility to mark an answer as accepted.
    - There is a clickable element for every answer on the question page, that can be used for marking an answer as accepted.
    - There is an option to remove the accepted state from an answer.
    - Only the user who asked the question can change the accepted state of answers.
    - An accepted answer has some visual distinction from other answers.

10. As a user, I would like to see a reputation system to strengthen the community. Reputation is a rough measurement of how much the community trusts a user.
    - **A user gains reputation when:**
- their question is voted up: +5
- their answer is voted up: +10
- their answer is marked "accepted": +15

11. As a user, I would like to see a small drop in reputation when a user's question or answer is voted down.
    - **A user loses reputation when:**
- their question is voted down: −2
- their answer is voted down: −2

12. As a user, I would like to see a page that lists all existing tags and the number of questions marked with those tags.
    - There is a `/tags` page.
    - The page is linked from the front page and a question page.
    - The page is accessible whithout logging in.

13. When the user navigates to the `bonus-questions` route and types in the input box, the displayed questions are filtered to match the criteria. This must be done without page reload.
    - When typing `life`, the only question displayed is the one titled `What is the meaning of life ?`.
    - When typing `!life`, questions are filtered to the ones that do NOT include the word `life`. (That is nine questions in this scenario.)
    - When typing `Description:life`, questions are filtered to those that include the word `life` in the `Description` column. (No question is displayed in this scenario.)
    - When typing `!Description:life`, questions are filtered to those that do NOT include the word `life` in the `Description column. (All ten questions are displayed in this scenario)

14. When the user navigates to the `bonus-questions` route and clicks on any table header, the items are sorted based on the column. This must be done without page reload.
    - When clicking the `Description` column, the questions are sorted in alphabetical order, based on the values from the `Description` column.
    - When clicking the `Description` column a second time, the questions are sorted in reverse alphabetical order, based on the values from the `Description` column.

15. [OPTIONAL] When the user navigates to the `bonus-questions` and clicks the `Decrease page font` or `Increase page font` button, the font size is decreased or increased in the page, respectively. This must be done without page reload.
    - Clicking the `Increase page font` button increases the font in the page.
    - Clicking the `Increase page font` button multiple times increases the font size to a maximum of 15. Further clicks do not result in an increase.
    - Clicking the `Decrease page font` button decreases the font the page.
    - Clicking the `Decrease page font` button multiple times decreases the font size to a minimum of 3. Further clicks do not result in an decrease.

## General requirements

- Use gitflow workflow in your team projects from now on.

## Hints

- Use the `CREATE` and `ALTER TABLE` statements to extend and change the database. For more information, see
  [this link](https://www.w3schools.com/sql/sql_alter.asp).
  (Do not forget to set up the foreign keys if you need them.)
- Use one of the following methods to add a value to the timestamp column of a database.
    - Use strings in the following format `'1999-01-08 04:05:06'`,
    - Pass a `datetime` object to the SQL query as a parameter if you use `psycopg2` and the `datetime` module. For more information on date and time handling in psycopg2, see the Background section.
- Insert data into the tables in the appropriate order to avoid violating foreign
key constraints (for example, if you insert data into the `question_tag` before inserting
  the corresponding tag ID in the tag table, the tag you refer to does not exist yet).
  This is especially important after changing the database structure with new foreign keys.
  Consider modifying the sample data based on your changes.
- Optimize your previous queries by applying your knowledge of complex queries and joined tables.
- Remeber that some user stories have prerequisites.

## Background materials

### Git

- <i class="far fa-exclamation"></i> [Working with the `git remote` command](https://git-scm.com/docs/git-remote)
- <i class="far fa-book-open"></i> [Merge vs rebase](project/curriculum/materials/pages/git/merge-vs-rebase.md)
- <i class="far fa-book-open"></i> [Mastering git](project/curriculum/materials/pages/git/mastering-git.md)

### SQL

- <i class="far fa-exclamation"></i> [Working with more complex data](project/curriculum/materials/pages/sql/sql-working-with-data.md)
- [SQL injection](project/curriculum/materials/pages/web-security/sql-injection.md)
- [Best practices for Python/Psycopg/Postgres](project/curriculum/materials/pages/python/tips-python-psycopg-postgres.md)
- [Date/Time handling in psycopg2](https://www.psycopg.org/docs/usage.html?highlight=gunpoint#date-time-objects-adaptation)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page on Queries](https://www.postgresql.org/docs/current/queries.html)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page Data Manipulation](https://www.postgresql.org/docs/current/dml.html)

### Workflow

- <i class="far fa-exclamation"></i> [Gitflow workflow](project/curriculum/materials/pages/git/git-branching.md)

### Web basics (Sessions/Flask)

- <i class="far fa-exclamation"></i> [Sessions](project/curriculum/materials/pages/web/authentication-sessions.md)
- <i class="far fa-exclamation"></i> [Salted password hashing](project/curriculum/materials/pages/web-security/salted-password-hashing.md)
- <i class="far fa-exclamation"></i> [Flask documentation](http://flask.palletsprojects.com/) (especially the quickstart#the-request-object and quickstart#sessions part)
- [Flask/Jinja Tips & Tricks](project/curriculum/materials/pages/web/web-with-python-tips.md)
- [Passing data from browser](project/curriculum/materials/pages/web/passing-data-from-browser.md)
- <i class="far fa-book-open"></i> [HTTP is stateless](project/curriculum/materials/pages/web/authentication-http-stateless.md)
- <i class="far fa-book-open"></i> [Cookies](project/curriculum/materials/pages/web/authentication-cookies.md)
- <i class="far fa-book-open"></i> [Jinja2 documentation](https://jinja.palletsprojects.com/en/2.10.x/templates/)
- <i class="far fa-book-open"></i> [Collection of web resources](project/curriculum/materials/pages/web/resources.md)
