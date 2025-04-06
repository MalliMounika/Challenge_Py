# Challenge_py(AIVOA)

## Challenge 1 - Backend Application: Enhanced Blog Post Management with Tagging (Python & MySQL). 

## Problem Description:
Build a command-line interface for managing blog posts, storing data in a MySQL database with tables for posts, tags, and a linking table post_tags. The application should allow users to:

- Create new posts with comma-separated tags.
  
- View all post titles.
 
- View specific post content by title.
  
- Search posts by a given tag.

## MySQL Database Requirements:

Create posts (id, title, content), tags (id, name), and post_tags (post_id, tag_id) tables with appropriate primary and foreign keys.
Python Application Requirements:
Use mysql.connector to create a command-line interface for the described features.

## Features
- Add new posts with tags
- View all post titles
- View content by title
- Search posts by tag

-------------------------------------------

## Code

    import mysql.connector

    conn = mysql.connector.connect(
    host="localhost",
    user="root",                       # change if you use different user
    password="replace your password",  # replace with your MySQL password
    database="blog_db"
    )
    cursor = conn.cursor()

    def create_post():
    title = input("Title: ")
    content = input("Content: ")
    tags = input("Tags (comma separated): ").split(',')
    cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
    post_id = cursor.lastrowid
    for tag in tags:
        tag = tag.strip().lower()
        cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
        tag_result = cursor.fetchone()
        tag_id = tag_result[0] if tag_result else (
            cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag,)) or cursor.lastrowid
        )
        cursor.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (%s, %s)", (post_id, tag_id))
    conn.commit()
    print("Post created.")

    def view_titles():
    cursor.execute("SELECT title FROM posts")
    for (title,) in cursor.fetchall():
        print(f"- {title}")

    def view_post():
    title = input("Enter post title: ")
    cursor.execute("SELECT content FROM posts WHERE title = %s", (title,))
    result = cursor.fetchone()
    print(result[0] if result else " Post not found.")

    def search_by_tag():
    tag = input("Tag: ").strip().lower()
    cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
    result = cursor.fetchone()
    if not result:
        print(" Tag not found.")
        return
    tag_id = result[0]
    cursor.execute("""
        SELECT title FROM posts
        JOIN post_tags ON posts.id = post_tags.post_id
        WHERE tag_id = %s
    """, (tag_id,))
    posts = cursor.fetchall()
    for (title,) in posts:
        print(f"- {title}")

    def menu():
    while True:
        print("\n1. New Post\n2. View Titles\n3. View Post by Title\n4. Search by Tag\n5. Exit")
        choice = input("Choose: ")
        if choice == '1': create_post()
        elif choice == '2': view_titles()
        elif choice == '3': view_post()
        elif choice == '4': search_by_tag()
        elif choice == '5': break
        else: print("Invalid option.")

    menu()
    cursor.close()
    conn.close()

##  ✅ STEP-BY-STEP GUIDE: Blog Post Manager (Python + MySQL) 

***PART 1: Setup MySQL Database**

   🔹 Step 1:  Open MySQL Workbench
          
   👉 Open MySQL Workbench

   👉 Click your Local Instance to connect

   👉 Open a new SQL tab

   🔹 Step 2: Run the following SQL code:

# SQL 

    CREATE DATABASE IF NOT EXISTS blog_db;
    USE blog_db;

    //Table to store blog posts

    CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL
    );

    //Table to store tags

    CREATE TABLE IF NOT EXISTS tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
    );

    //Linking table between posts and tags (many-to-many relationship)

    CREATE TABLE IF NOT EXISTS post_tags (
    post_id INT,
    tag_id INT,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
    );



***PART 2: Write the Python Code**

  🔹 Step 3: Install MySQL Connector for Python

Open CMD and run:

    pip install mysql-connector-python

  🔹 Step 4: Create a file named blog_cli.py


    import mysql.connector

    conn = mysql.connector.connect(
    host="localhost",
    user="root",                       # change if you use different user
    password="replace your password",  # replace with your MySQL password
    database="blog_db"
    )
    cursor = conn.cursor()

    def create_post():
    title = input("Title: ")
    content = input("Content: ")
    tags = input("Tags (comma separated): ").split(',')
    cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
    post_id = cursor.lastrowid
    for tag in tags:
        tag = tag.strip().lower()
        cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
        tag_result = cursor.fetchone()
        tag_id = tag_result[0] if tag_result else (
            cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag,)) or cursor.lastrowid
        )
        cursor.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (%s, %s)", (post_id, tag_id))
    conn.commit()
    print("Post created.")

    def view_titles():
    cursor.execute("SELECT title FROM posts")
    for (title,) in cursor.fetchall():
        print(f"- {title}")

    def view_post():
    title = input("Enter post title: ")
    cursor.execute("SELECT content FROM posts WHERE title = %s", (title,))
    result = cursor.fetchone()
    print(result[0] if result else " Post not found.")

    def search_by_tag():
    tag = input("Tag: ").strip().lower()
    cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
    result = cursor.fetchone()
    if not result:
        print(" Tag not found.")
        return
    tag_id = result[0]
    cursor.execute("""
        SELECT title FROM posts
        JOIN post_tags ON posts.id = post_tags.post_id
        WHERE tag_id = %s
    """, (tag_id,))
    posts = cursor.fetchall()
    for (title,) in posts:
        print(f"- {title}")

    def menu():
    while True:
        print("\n1. New Post\n2. View Titles\n3. View Post by Title\n4. Search by Tag\n5. Exit")
        choice = input("Choose: ")
        if choice == '1': create_post()
        elif choice == '2': view_titles()
        elif choice == '3': view_post()
        elif choice == '4': search_by_tag()
        elif choice == '5': break
        else: print("Invalid option.")

    menu()
    cursor.close()
    conn.close()


👇 Replace:

    password="your_password"

with your real MySQL password (e.g., "1234").

-----------------------------------------------

🔹STEP 5: Run the Python File

Open VS Code Terminal or CMD, go to the folder where your blog_cli.py file is, and run:
     
    python blog_cli.py

**🎉 Final Result**
You now have a CLI app that can:

✅ Add blog posts

✅ Store tags automatically

✅ Show all post titles

✅ View content by title

✅ Search by tag

-----------------------------------------


## ⭐ 1. Briefly explain your database schema design?
The database has three tables:

Posts to store blog post details,
tags to store unique tag names,
post_tags to link posts and tags using their IDs.
This design uses a many-to-many relationship so that each post can have multiple tags, 
and each tag can belong to multiple posts. It ensures clean data handling using primary and foreign keys.

(or)

## 🧩 Database Schema Design Explanation
The database consists of three tables: posts, tags, and post_tags, designed to manage blog posts and their associated tags using a many-to-many relationship.

## 1. Posts
Stores information about each blog post.

Fields:

Id (Primary Key): Unique identifier for each post.

Title: Title of the post (must be unique).

Content: Full content of the blog post.

## 2. Tags
Stores each unique tag that can be assigned to blog posts.

Fields:
id (Primary Key): Unique identifier for each tag.

name: The name of the tag (must be unique).

## 3. Post_tags
Linking table to create a many-to-many relationship between posts and tags.

Fields:
post_id: References the id of the posts table.

tag_id: References the id of the tags table.

Constraints:
Primary Key on (post_id, tag_id) to prevent duplicates.

Foreign Keys with ON DELETE CASCADE to ensure data integrity when a post or tag is deleted.

------------------------------

## ✅ Summary
This schema allows:

A post to have multiple tags

A tag to belong to multiple posts

It is normalized, efficient, and supports scalable tag-based filtering.


## ✅ Database Schema Design (Simplified)

The database has three tables:

posts – Stores each blog post with id, title, and content.

tags – Stores unique tag names with id and name.

post_tags – Links posts and tags using their IDs to support many-to-many relationships.

## This design allows:

Each post to have multiple tags.

Each tag to be used in multiple posts.

Foreign keys and primary keys ensure data is linked properly and kept clean.


-------------------------------

## 💡 What This Does:

✅ posts: Stores each blog post (title + content)

✅ tags: Stores tag names (unique)

✅ post_tags: Connects posts to tags using foreign keys

-------------------------------


## ⭐ 2. How I implemented the search by tag feature:

To search posts by a tag, I first join the posts, tags, and post_tags tables using SQL joins. When a user enters a tag name, I run a query that finds all post titles linked to that tag. This way, the user can easily view posts related to a specific tag.

I used mysql.connector in Python to connect to the database and execute the query, then printed the matching post titles in the command-line interface.

----------------------------------

## ⭐ 3. If you used an LLM, describe how:
I used a Large Language Model (LLM) like ChatGPT to assist me in understanding the problem, generating SQL queries, and writing clean Python code. It helped me clarify my logic, fix errors quickly, and learn best practices. However, I made sure to understand and customize the code myself to ensure it met the exact project requirements.

----------------------------------

## ⭐ 4. Briefly discuss one alternative approach to tagging:
- An alternative approach to tagging is to store tags as a comma-separated string in a single column within the posts table. For example, a post might have a tags field like "python, mysql, backend".

- This method is easier to implement but has limitations—it's harder to search, filter, or prevent duplicates. That’s why the many-to-many relationship using a separate tags table and post_tags linking table is a more flexible and scalable solution.

---------------------------------

## ⭐ 5. Instructions to run my application:
"To run my application, first I installed Python and MySQL on my system. Then I created the required tables by running the SQL script in MySQL Workbench. I used mysql.connector, so I installed that package using pip. After updating the database connection details in my Python file, I ran the script using the command python blog_cli.py. The application runs in the terminal with a simple menu where the user can create posts, view titles, or search by tag."
