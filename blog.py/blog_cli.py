import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",            # change if you use different user
    password="root",  # 👉 replace with your MySQL password
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
    print("✅ Post created.")

def view_titles():
    cursor.execute("SELECT title FROM posts")
    for (title,) in cursor.fetchall():
        print(f"- {title}")

def view_post():
    title = input("Enter post title: ")
    cursor.execute("SELECT content FROM posts WHERE title = %s", (title,))
    result = cursor.fetchone()
    print(result[0] if result else "❌ Post not found.")

def search_by_tag():
    tag = input("Tag: ").strip().lower()
    cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
    result = cursor.fetchone()
    if not result:
        print("❌ Tag not found.")
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
        else: print("❌ Invalid option.")

menu()
cursor.close()
conn.close()
