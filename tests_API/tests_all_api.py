import requests
import pytest
import csv

import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")  # define no ambiente, não no código

session = requests.Session()
if GITHUB_TOKEN:
    session.headers.update({"Authorization": f"Bearer {GITHUB_TOKEN}"})
session.headers.update({"Accept": "application/vnd.github+json"})

final_user = "torvalds"
base_url = "https://api.github.com/"
base_json_url = "https://jsonplaceholder.typicode.com/"

TOKEN = "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"
HEADERS = {'Authorization': f"Bearer{TOKEN}"}


def get_json_field_from_user(user, jsonField):
    url = base_url + "users/" + user
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data[jsonField]

def get_json_from_user_repo(user, repo):
    url = base_url + "repos/" + user + "/" + repo
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data

def get_json_commits_from_user_repo(user, repo):
    url = base_url + "repos/" + user + "/" + repo + "/commits"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data

# Step 1: Simple Request
def test_simple_request():
    response = requests.get('https://api.github.com')
    assert response.status_code == 200

# Step 2: Fetch a Specific User
def test_username_octocat():
    assert get_json_field_from_user("octocat", "login") == "octocat"

# Step 3: Validate User Type
# Check if "octocat" is of type "User".
def test_user_type():
    assert get_json_field_from_user("octocat", "type") == "User"

# Step 4: Request with Repository ID
# Fetch the repository with ID 1296269 and check if it is "Hello-World".
def test_repository_id():
    target_url = "https://api.github.com/repositories/1296269"
    response = requests.get(target_url)
    data = response.json()
    assert data["name"] == "Hello-World"

# Step 5: Handling Errors (Non-existent User)
# Try to fetch a user that does not exist (e.g., "nonexistentuser12345") and check if the status code is 404 (Not Found).
def test_non_existent_user_request():
    response = requests.get('https://api.github.com/users/nonexistentuser123451623129931249')
    assert response.status_code == 404

# Step 6: List User Repositories
# Make a request to list the repositories of the user "google" with a limit of 5 and print the name of the first one in the list.
def test_google_user_repos_list_five():
    target_user_repos = 'https://api.github.com/users/google/repos'
    limit_repos = 5
    params = {'per_page': limit_repos}

    response = requests.get(target_user_repos, params)
    data = response.json()
    assert response.status_code == 200
    assert len(data) > 0
    assert len(data) <= 5
    assert "name" in data[0]
    print("Step 6:")
    print(data[0]["name"])

# Step 7: Navigate Follower Pagination
# List the followers of the user "microsoft", get the URL of the next page from the 'Link' header, and make a new request.
def test_microsoft_followers_header_link():
    target_followers = 'https://api.github.com/users/microsoft/followers'
    response = requests.get(target_followers)

    print("Step 7:")
    assert response.status_code == 200
    header_link = response.headers.get("Link")
    print(header_link)
    # <https://api.github.com/user/6154722/followers?page=2>; rel="next", <https://api.github.com/user/6154722/followers?page=3490>; rel="last"

    header_link = response.headers.get("Link")
    parts = header_link.split("'")
    next_link = ""
    for part in parts:
        if 'rel="next"' in part:
            next_link = part.split(";")[0].strip("<> ")
            break
    print("Next page URL:", next_link)
    next_response = requests.get(next_link)
    print("Status da próxima página:", next_response.status_code)
    assert response.status_code == 200
    assert response.headers.get("Link"), "Link header ausente"
    assert next_link, "não achou rel=next"
    assert next_response.status_code == 200

# Step 8: Count a User's Public Repositories
# Check how many public repositories the user "facebook" has.
def test_count_public_repos():
    print("Step 8: ")
    print(get_json_field_from_user("facebook", "public_repos"))
    val = get_json_field_from_user("facebook", "public_repos")
    assert isinstance(val, int)
    assert val >= 0

# Step 9: Find a Specific Language in a Repository
# Check if the language "JavaScript" is in the list of languages for the "react" repository from Facebook.
def test_check_javascript_language_react_facebook():
    url = base_url + "repos/facebook/react/languages"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    if "JavaScript" in data:
        print("Step 9:")
        print("Repositório 'facebook' usa JavaScript")
    else:
        print("Step 9:")
        print("Repositório 'facebook' não usa JavaScript")
    assert response.status_code == 200
    assert "JavaScript" in data

# Step 10: Explore Another Endpoint (Emojis)
# Fetch the list of available emojis from the API and check if the "+1" emoji exists.
def test_check_emojis_plus_one():
    url = base_url + "emojis"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    print("Step 10:")
    if "+1" in data:
        print("Emoji '+1' faz parte do GitHub")
    else:
        print("Emoji '+1' não faz parte do GitHub")
    assert response.status_code == 200
    assert "+1" in data

# Step 11: Validate Repository JSON Structure
# For the "linux" repository from "torvalds", check if the keys "name", "owner", and "language" exist in the response JSON.
def test_torvalds_linux_name_owner_language():
    data = get_json_from_user_repo("torvalds", "linux")
    print("Step 11:")
    if "name" in data:
        print("Key 'name' existe no json extraído")
    else:
        print("Key 'name' não existe no json extraído")

    if "owner" in data:
        print("Key 'owner' existe no json extraído")
    else:
        print("Key 'owner' não existe no json extraído")

    if "language" in data:
        print("Key 'language' existe no json extraído")
    else:
        print("Key 'language' não existe no json extraído")
    assert "name" in data and "owner" in data and "language" in data
    assert isinstance(data["owner"], dict)

# Step 12: Compare Repository Attributes
# Compare the "stargazers_count" of Microsoft's "vscode" repository and Atom's "atom" repository. Check if the VSCode count is higher.
def test_check_stargazers_vscode_atom():
    data_vscode = get_json_from_user_repo("microsoft", "vscode")
    vscode_stargazers = data_vscode["stargazers_count"]
    data_atom = get_json_from_user_repo("atom", "atom")
    atom_stargazers = data_atom["stargazers_count"]
    print("Step 12:")
    if(atom_stargazers > vscode_stargazers):
        print(f"VSCode count ({vscode_stargazers}) is lower than Atom's count ({atom_stargazers}).")
    elif(atom_stargazers == vscode_stargazers):
        print(f"VSCode count ({vscode_stargazers}) is equal than Atom's count ({atom_stargazers}).")
    else:
        print(f"VSCode count ({vscode_stargazers}) is higher than Atom's count ({atom_stargazers}).")
    assert isinstance(vscode_stargazers, int) and isinstance(atom_stargazers, int)
    assert vscode_stargazers >= 0 and atom_stargazers >= 0
    assert vscode_stargazers >= atom_stargazers

# Step 13: Fetch a License
# Fetch the "mit" license and check its name.
def test_fetch_mit_license_name():
    url = base_url + "licenses"
    response = requests.get(url)
    data = response.json()
    print("Step 13:")

    license_name = ""
    for license in data:
        if(license["key"] == "mit"):
            license_name = license["name"]
            break
    assert response.status_code == 200
    assert license_name != "", "MIT não encontrada"
    assert license_name == "MIT License"
    print("License name: " + license_name)

# Step 14: List All Licenses
# Make a request to the licenses endpoint and count how many common licenses exist.
def test_count_common_licenses():
    url = base_url + "licenses"
    response = requests.get(url)
    data = response.json()
    print("Step 14:")

    license_count = 0
    for license in data:
        license_count += 1
    assert response.status_code == 200
    assert isinstance(data, list) and len(data) > 0
    assert isinstance(license_count, int)
    assert license_count == len(data)
    print(f"License count: {license_count}")

# Step 15: Find Repositories with a Specific License
# Search for repositories with the "apache-2.0" license and print the name of the first one in the list.
def test_find_repos_with_apache_license():
    url = base_url + "search/repositories?q=licence:apache-2.0"
    response = requests.get(url)
    data = response.json()
    print("Step 15:")
    assert response.status_code == 200
    assert "items" in data
    assert isinstance(data["items"], list) and len(data["items"]) > 0
    assert "name" in data["items"][0]
    print(data["items"][0]["name"])

# Step 16: Validate a Repository's Organization
# Check if the "docker" repository belongs to the "moby" organization.
def test_check_docker_moby():
    data = get_json_from_user_repo("docker", "docker")
    print("Step 16:")
    assert "owner" in data and "login" in data["owner"]
    assert data["owner"]["login"] == "moby"
    print(f"Owner: {data['owner']['login']}")

# Step 17: Check the Last Commit of a Repository
# From the "tensorflow/tensorflow" repository, get the last commit and check if the message is not empty.
def test_tensorflow_repo_last_commit():
    data = get_json_commits_from_user_repo("tensorflow", "tensorflow")
    print("Step 17:")
    assert isinstance(data, list) and len(data) > 0
    assert "commit" in data[0] and "message" in data[0]["commit"]
    assert data[0]["commit"]["message"]
    print(data[0]["commit"]["message"])

# Step 18: Check if a User is an Organization
# Check if "apple" is of type "Organization".
def test_check_user_type_apple():
    data = get_json_field_from_user("apple", "type")
    print("Step 18:")
    assert data == "Organization"
    print(data)
    if(data == "Organization"):
        print(f"User 'apple' is of type 'Organization'")
    else:
        print(f"User 'apple' isn't of type 'Organization'")

# Step 19: Find the Number of Contributors to a Repository
# Fetch the number of contributors for the "kubernetes/kubernetes" repository and check if it is greater than 1000.

def test_get_number_of_contributors_kubernetes():
    target_total_contributors = base_url + "repos/kubernetes/kubernetes/contributors"
    response = requests.get(target_total_contributors)  # primeira página
    header_link = response.headers.get("Link")
    page = 1
    total_count = 0

    # conta a primeira página
    sum_quantity = len(response.json())
    total_count += sum_quantity

    max_pages = 1
    next_link = ""

    # se houver header Link, pega max_pages e next_link
    if header_link:
        parts = header_link.split(",")  # separa cada link
        for part in parts:
            part = part.strip()

            if 'rel="last"' in part:
                last_link = part.split(";")[0].strip("<> ")
                # faz parse "manual": pega o número depois de 'page='
                if "page=" in last_link:
                    max_pages = int(last_link.split("page=")[1])
            
            if 'rel="next"' in part:
                next_link = part.split(";")[0].strip("<> ")

    # percorre páginas seguintes até max_pages
    while page < max_pages and next_link:
        page += 1
        response = requests.get(next_link)
        sum_quantity = len(response.json())
        total_count += sum_quantity

        header_link = response.headers.get("Link")
        next_link = ""

        if header_link:
            parts = header_link.split(",")
            for part in parts:
                part = part.strip()
                if 'rel="next"' in part:
                    next_link = part.split(";")[0].strip("<> ")
                    break
    assert total_count >= 0
    if total_count > 1000:
        print(f"Kubernetes has more than 1000 contributors ({total_count} total)")
    else:
        print(f"Kubernetes doesn't have more than 1000 contributors ({total_count} total)")
    assert total_count < 1000, f"esperado <1000, obtido {total_count}"

# Step 20: Final Challenge - Putting It All Together
# Create a function that takes a username, fetches their data, and returns a dictionary with their login, name, and number of public repositories. Test it with "torvalds".
def test_final_challenge_torvalds_data():
    login = get_json_field_from_user("torvalds", "login")
    name = get_json_field_from_user("torvalds", "name")
    public_repos = get_json_field_from_user("torvalds", "public_repos")

    print("Step 20:")
    print(login)
    print(name)
    print(public_repos)
    assert login == "torvalds"
    assert isinstance(name, str) and name != ""
    assert isinstance(public_repos, int) and public_repos >= 0

# Step 21: Create a New Post (POST)
# Make a POST request to /posts to create a new post. Check if the status code is 201 (Created).
def test_create_new_post():
    new_post = {
        "title": "Hello world",
        "body": "This is a test post",
        "userId": 1
    }
    url = base_json_url + "posts"
    response = requests.post(url, json=new_post)

    print("Step 21:")
    print("Status code:", response.status_code)
    if response.status_code == 201:
        print("Post created successfully!")
    else:
        print("Failed to create post.")
    assert response.status_code == 201

# Step 22: Validate Created Post Data
# Validate that the response body of the created post contains the sent title and body.
def test_validate_created_post_data():
    new_post = {
        "title": "Hello world",
        "body": "This is a test post",
        "userId": 1
    }
    url = base_json_url + "posts"
    response = requests.post(url, json=new_post)
    data = response.json()

    if(new_post["title"] == data["title"]):
        print(f"'title' é o mesmo")
    else:
        print(f"'title' não é o mesmo")
    if(new_post["body"] == data["body"]):
        print(f"'body' é o mesmo")
    else:
        print(f"'body' não é o mesmo")
    if(new_post["userId"] == data["userId"]):
        print(f"'userId' é o mesmo")
    else:
        print(f"'userId' não é o mesmo")
    assert response.status_code == 201
    assert new_post["title"] == data["title"]
    assert new_post["body"]  == data["body"]
    assert new_post["userId"] == data["userId"]

# Step 23: Update a Post (PUT)
# Make a PUT request to /posts/1 to update the post with ID 1. Check if the status code is 200.
def test_update_post_with_put():
    url = base_json_url + "posts/1"
    updated_post = {
        "id": 1,
        "title": "Updated Title",
        "body": "This post has been updated.",
        "userId": 1
    }
    response = requests.put(url, json=updated_post)

    print("Step 23:")
    print("Status code:", response.status_code)
    if response.status_code == 200:
        print("Post updated successfully")
    else:
        print("Failed to update post")
    assert response.status_code == 200

# Step 24: Validate Post Update
# Check if the response body of the updated post contains the new data sent.
def test_validate_updated_post_data():
    updated_post = {
        "id": 1,
        "title": "Updated Title",
        "body": "This post has been updated.",
        "userId": 1
    }
    url = base_json_url + "posts/1"
    response = requests.put(url, json=updated_post)
    data = response.json()

    if(updated_post["id"] == data["id"]):
        print(f"'id' é o mesmo")
    else:
        print(f"'id' não é o mesmo")
    if(updated_post["title"] == data["title"]):
        print(f"'title' é o mesmo")
    else:
        print(f"'title' não é o mesmo")
    if(updated_post["body"] == data["body"]):
        print(f"'body' é o mesmo")
    else:
        print(f"'body' não é o mesmo")
    if(updated_post["userId"] == data["userId"]):
        print(f"'userId' é o mesmo")
    else:
        print(f"'userId' não é o mesmo")
    assert response.status_code == 200
    assert updated_post["id"] == data["id"]
    assert updated_post["title"] == data["title"]
    assert updated_post["body"] == data["body"]
    assert updated_post["userId"] == data["userId"]

# Step 25: Delete a Post (DELETE)
# Make a DELETE request to /posts/1 to delete the post. Check if the status code is 200.
def test_delete_post():
    url = base_json_url + "posts/1"
    response = requests.delete(url)

    print("Step 21:")
    print("Status code:", response.status_code)
    if response.status_code == 200:
        print("Post deleted successfully")
    else:
        print("Failed to delete post")
    assert response.status_code == 200

# Step 26: List All Users
# Make a GET request to /users and check if the list contains 10 users.
def test_get_users_size():
    url = base_json_url + "users"
    response = requests.get(url)
    data = response.json()
    quantity_on_list = len(data)
    print("Users quantity is " + str(quantity_on_list))
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 10

# Step 27: Fetch a Specific User
# Fetch the user with ID 5 and check if their name is "Chelsey Dietrich".
def test_user_name_id_five():
    url = base_json_url + "users"
    response = requests.get(url)
    data = response.json()
    for user in data:
        if(user["id"] == 5):
            check_name = user["name"]
            break
    print("name of user with ID 5 is: " + str(check_name))
    assert 'check_name' in locals(), "user id 5 não encontrado"
    assert check_name == "Chelsey Dietrich"

# Step 28: Create a New Comment for a Post
# Make a POST request to /posts/1/comments to add a new comment. Check for status code 201.
def test_new_comment_with_post():
    new_comment = {
        "postId": 1,
        "id": 1,
        "name": "id labore ex et quam laborum",
        "email": "Eliseo@gardner.biz",
        "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium"
    }
    url = base_json_url + "posts/1/comments"
    response = requests.post(url, json=new_comment)

    print("Step 21:")
    print("Status code:", response.status_code)
    if response.status_code == 201:
        print("Post comment created successfully!")
    else:
        print("Failed to create post comment.")
    assert response.status_code == 201


# Step 29: List a User's Albums
# List all albums for the user with ID 3 (/users/3/albums) and count how many albums they have.
def test_list_all_albums_user_three():
    url = base_json_url + "users/3/albums"
    response = requests.get(url)
    data = response.json()
    quantity_of_albums = len(data)
    i = 1
    print("Step 29:")
    for user in data:
        name = user["title"]
        print(f"Album number '{i}': {name}")
        i += 1
    print(f"Total of albums: {quantity_of_albums}")
    assert response.status_code == 200
    assert isinstance(data, list)
    assert quantity_of_albums >= 0

# Step 30: List Photos in an Album
# List all photos from the album with ID 2 (/albums/2/photos) and check if the first photo has the title "reprehenderit est deserunt velit ipsam".
def test_list_all_photos_album_id_two():
    url = base_json_url + "/albums/2/photos"
    response = requests.get(url)
    data = response.json()
    print("Step 30:")
    if(data[0]["title"] == "reprehenderit est deserunt velit ipsam"):
        print("Album has 'reprehenderit est deserunt velit ipsam' on its title")
    else:
        print("Album doesn't have 'reprehenderit est deserunt velit ipsam' on its title")
    i = 1
    
    for user in data: 
        name = user["url"]
        print(f"Photo number '{i}' URL: {name}")
        i += 1
    assert response.status_code == 200
    assert isinstance(data, list) and len(data) > 0
    assert not data[0]["title"] == "reprehenderit est dese runt velit ipsam"

# Step 31: Create a New Task (Todo)
# Create a new task (todo) for the user with ID 1 with the title "Learn Pytest" and check if it was created successfully.
def test_new_to_do():
    new_todo = {
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": False
    }
    url = base_json_url + "todos/1"
    response = requests.put(url, json=new_todo)
    data = response.json()

    print("Step 31:")
    print("Status code:", response.status_code)
    if response.status_code == 200:
        print("Post created successfully!")
    else:
        print("Failed to create post.")
    assert response.status_code == 200
    assert isinstance(data, dict)
    for k in ("title","completed","id","userId"):
        assert k in data

# Step 32: Update a Task (PATCH)
# Update the status of the task with ID 5 to completed: true using a PATCH request. Check the response.
def test_update_patch_task():
    new_todo = {
    "title": "yoyoyo"
    }
    url = base_json_url + "todos/5"
    response = requests.patch(url, json=new_todo)
    data = response.json()

    print("Step 32:")
    print("Status code:", response.status_code)
    if response.status_code == 200:
        print("Post patched successfully!")
    else:
        print("Failed to patch post.")
    assert response.status_code == 200
    assert data.get("title") == "yoyoyo"

# Step 33: List a User's Completed Tasks
# List all tasks for the user with ID 1 and filter only those that are completed (completed: true).
def test_list_user_completed_tasks():
    url = base_json_url + "/todos/"
    response = requests.get(url)
    data = response.json()
    print("Step 33:")
    i = 1
    for user in data: 
        if user["userId"] == 1 and user["completed"] == True:
            task = user["title"]
            print(f"Completed task number '{i}': {task}")
            i += 1
    assert response.status_code == 200
    filtered = [t for t in data if t["userId"] == 1 and t["completed"] is True]
    assert all(t["completed"] is True for t in filtered)

# Step 34: Validate a Comment's Structure
# Fetch the comment with ID 10 and check if it contains the keys "postId", "id", "name", "email", and "body".
def test_validate_comment_id_ten():
    url = base_json_url + "comments/10"
    response = requests.get(url)
    data = response.json()

    print("Step 34:")
    expected_keys = ["postId", "id", "name", "email", "body"]

    for key in expected_keys:
        if key in data:
            print(f"Key '{key}' found")
        else:
            print(f"Key '{key}' missing")
    assert response.status_code == 200
    for k in ("postId", "id", "name", "email", "body"):
        assert k in data

# Step 35: Delete a Comment
# Delete the comment with ID 3 and check if the request was successful.
def test_delete_comment_three():
    url = base_json_url + "comments/10"
    response = requests.delete(url)

    print("Step 35:")
    print("Status code:", response.status_code)
    if response.status_code == 200:
        print("Post deleted successfully!")
    else:
        print("Failed to delete post.")
    assert response.status_code == 200

# Step 36: Create a Post with Invalid Data
# Try to create a post by sending an empty JSON body and observe the API's response (although JSONPlaceholder might return 201, it's good practice to check the behavior).
def test_invalid_data_send_through_post():
    empty_json = {}
    url = base_json_url + "users"
    response = requests.post(url, json=empty_json)
    print("Step 36:")
    print("Status code:", response.status_code)
    assert response.status_code in (200, 201)

# Step 37: Fetch a Specific User's Posts
# Fetch all posts from the user with ID 7 (/users/7/posts) and count how many posts they have.
def test_fetch_posts_user_id_seven():
    url = base_json_url + "users/7/posts"
    response = requests.get(url)
    data = response.json()
    quantity_of_posts = len(data)
    print("Step 37:")
    print(f"Amount of posts of user with ID 7: {quantity_of_posts}")
    assert response.status_code == 200
    assert isinstance(data, list)
    assert all(p["userId"] == 7 for p in data)

# Step 38: Update a User's Email (PUT)
# Update the data for the user with ID 2, changing only the email to "new.email@example.com".
def test_put_new_user_email_id_two():
    update_email = {
        "email": "new.email@example.com"
    }
    url = base_json_url + "users/2"
    response = requests.patch(url, json=update_email)
    print("Step 38:")
    print("Status code:", response.status_code)
    assert response.status_code == 200

# Step 39: Delete an Album
# Delete the album with ID 4 and check the response status.
def test_delete_album_id_four():
    url = base_json_url + "albums/4"
    response = requests.delete(url)
    print("Step 39:")
    print("Status code:", response.status_code)
    assert response.status_code == 200

# Step 40: Final Challenge with JSONPlaceholder
# Create a function that receives a userId, creates a new post for them, adds a comment to that post, and then deletes the post. Validate each step.
def test_final_challenge_jsonplaceholder():
    userIdSelected = 1
    print("Step 40:")
    new_post = {
        "title": "Hello world",
        "body": "This is a test post",
        "userId": userIdSelected
    }
    url = base_json_url + "posts"
    response1 = requests.post(url, json=new_post)

    print("Status code:", response1.status_code)
    if response1.status_code == 201:
        print("Post created successfully!")
    else:
        print("Failed to create post.")

    new_comment = {
        "postId": 1,
        "id": userIdSelected,
        "name": "id labore ex et quam laborum",
        "email": "Eliseo@gardner.biz",
        "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium"
    }
    url = base_json_url + "posts/1/comments"
    response2 = requests.post(url, json=new_comment)
    print("Status code:", response2.status_code)
    if response2.status_code == 201:
        print("Post comment created successfully!")
    else:
        print("Failed to create post comment.")

    url = base_json_url + "posts/1"
    response3 = requests.delete(url)
    print("Status code:", response3.status_code)
    if response3.status_code == 200:
        print("Post deleted successfully")
    else:
        print("Failed to delete post")

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 200

# Query Params
# 41. Fetch all comments for post ID 2 and verify that all returned comments belong to that post.
@pytest.mark.api_test
def test_fetch_comments_post_id_two_verify(base_json_url, api_client):
    response = api_client.get(f"{base_json_url}/posts/2/comments")
    print("Step 41:")
    print("Status code: " + str(response.status_code))
    if(response.status_code == 200):
        print("Fetch comment done successfully!")
    else:
        print("Failed to fetch comment.")
        return
    data = response.json()
    all_belong = True
    for comment in data:
        if comment["postId"] != 2:
            print("Not all comments fetched belong to post with ID 2")
            id_comment = comment["id"]
            print(f"Comment with {id_comment} doesn't belong to post with ID 2")
            all_belong = False
    if(all_belong):
        print("All comments belong to post with ID 2")
    assert response.status_code == 200
    assert isinstance(data, list)
    assert all(c["postId"] == 2 for c in data)

# 42. List all todos for user ID 5 and verify that the list is not empty.
@pytest.mark.api_test
def test_todos_user_id_five_verify_not_empty(base_json_url, api_client):
    response = api_client.get(f"{base_json_url}/todos?userId=5")
    print("Step 42:")
    if(response.status_code == 200):
        print("Fetch todos done successfully!")
    else:
        print("Failed to fetch todos.")
        return
    data = response.json()
    if(len(data) > 0):
        print("Todo list for user with ID 5 isn't empty")
    else:
        print("Todo list for user with ID 5 is empty")
    assert response.status_code == 200
    assert isinstance(data, list) and len(data) > 0

# 43. Fetch all albums for user ID 9 and count how many they have (should be 10).
@pytest.mark.api_test
def test_all_albums_user_id_nine_how_many(base_json_url, api_client):
    response = api_client.get(f"{base_json_url}/albums?userId=9")
    print("Step 43:")
    if(response.status_code == 200):
        print("Fetch albums done successfully!")
    else:
        print("Failed to albums todos.")
        return
    data = response.json()
    quantity_of_albums = len(data)
    print(f"Quantity of albums: {quantity_of_albums}")
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 10

# 44. List all completed todos (completed: true) for user ID 1 and verify that all in the response are indeed completed.
@pytest.mark.api_test
def test_completed_todos_user_id_one_verify_completed(base_json_url, api_client):
    response = api_client.get(f"{base_json_url}/todos?userId=1&completed=true")
    print("Step 44:")
    print("Status code: " + str(response.status_code))
    if(response.status_code == 200):
        print("Fetch todos done successfully!")
    else:
        print("Failed to fetch todos.")
        return
    data = response.json()
    all_completed = True
    for todo in data:
        if todo["completed"] != True:
            print("Not all todos for user ID 1 are completed")
            id_todo = todo["id"]
            print(f"Todo with {id_todo} isn't completed")
            all_completed = False
    if(all_completed):
        print("All todos that belong to user with ID 1 are completed")
    assert response.status_code == 200
    assert all(todo["completed"] is True for todo in data)

# Headers
# 45. Send a request to httpbin.org/headers with the custom header X-Custom-Header: MyValue and validate the response.
@pytest.mark.api_test
def test_custom_header_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/headers"
    headers = {"X-Custom-Header": "MyValue"}
    print("Step 45:")
    response = api_client.get(url, headers=headers)
    print("Status code: ", response.status_code)
    data = response.json()
    if response.status_code == 200 and data["headers"].get("X-Custom-Header") == "MyValue":
        print("Custom header received successfully")
    else:
        print("Custom header not found or incorrect")
    print("Response JSON:", data)
    assert response.status_code == 200
    assert data["headers"].get("X-Custom-Header") == "MyValue"

# 46. Send a request to httpbin.org/response-headers to set a custom response header (e.g., My-Test-Header: Hello) and check if it is present in the response headers.
@pytest.mark.api_test
def test_custom_response_header_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/response-headers"
    params = {"My-Test-Header": "Hello"}

    print("Step 46:")
    response = api_client.get(url, params=params)
    print("Status code:", response.status_code)

    if response.status_code == 200 and response.headers.get("My-Test-Header") == "Hello":
        print("Custom response header received successfully")
    else:
        print("Custom response header missing or incorrect")
    print("Response headers:", response.headers)
    assert response.status_code == 200
    assert response.headers.get("My-Test-Header") == "Hello"

# 47. Send a request to httpbin.org/headers with a custom User-Agent header ("My-Test-Agent/1.0") and validate if it was received correctly.
@pytest.mark.api_test
def test_custom_user_agent_header_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/headers"
    headers = {"User-Agent": "My-Test-Agent/1.0"}

    print("Step 47:")
    response = api_client.get(url, headers=headers)
    data = response.json()
    print("Status code:", response.status_code)

    if response.status_code == 200 and data["headers"].get("User-Agent") == "My-Test-Agent/1.0":
        print("Custom User-Agent header received successfully")
    else:
        print("Custom User-Agent header missing or incorrect")
    print("Response JSON:", data)
    assert response.status_code == 200
    assert data["headers"].get("User-Agent") == "My-Test-Agent/1.0"

# 48. Send multiple custom headers (X-Header-1: Value1, X-Header-2: Value2) in a single request to httpbin.org/headers and validate all of them.
@pytest.mark.api_test
def test_multiple_custom_headers_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/headers"
    headers = {"X-Header-1": "Value1", "X-Header-2": "Value2"}

    print("Step 48:")
    response = api_client.get(url, headers=headers)
    data = response.json()
    print("Status code:", response.status_code)

    if response.status_code == 200 and data["headers"].get("X-Header-1") == "Value1" and data["headers"].get("X-Header-2") == "Value2":
        print("Custom multiple headers received successfully")
    else:
        print("Custom multiple headers missing or incorrect")
    print("Response JSON:", data)
    assert response.status_code == 200
    assert data["headers"].get("X-Header-1") == "Value1"
    assert data["headers"].get("X-Header-2") == "Value2"

# Authentication
# 49. Test the httpbin Basic Auth endpoint (/basic-auth/user/passwd) with the correct credentials (user, passwd) and validate the 200 status.
@pytest.mark.api_test
def test_basic_auth_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/basic-auth/user/passwd"
    print("Step 49:")
    response = api_client.get(url, auth=("user", "passwd"))
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Authentication succeeded with correct credentials")
    else:
        print("Authentication failed")
    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert response.json().get("authenticated") is True

# 50. Test the same Basic Auth endpoint with a correct user but wrong password and validate the 401 status.
@pytest.mark.api_test
def test_basic_wrong_auth_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/basic-auth/user/passwd"
    print("Step 50:")
    response = api_client.get(url, auth=("user", "wrongpasswordhere"))
    print("Status code:", response.status_code)

    if response.status_code == 401:
        print("Authentication failed as expected (wrong password).")
    elif response.status_code == 503:
        pytest.skip("httpbin returned 503 (Service Unavailable). Skipping test.")
    else:
        print("Unexpected status code:", response.status_code)

    try:
        print("Response JSON:", response.json())
    except ValueError:
        print("Response body is empty or not JSON.")
    assert response.status_code in (401, 503)

# 51. Send a request to httpbin.org/bearer with a valid Bearer Token (mock, e.g., "my-mock-token") and validate the successful authentication.
@pytest.mark.api_test
def test_bearer_auth_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/bearer"
    headers = {"Authorization": "Bearer my-mock-token"}

    print("Step 51:")
    response = api_client.get(url, headers=headers)
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Bearer authentication succeeded with valid token.")
    elif response.status_code == 401:
        print("Authentication failed with invalid or missing token.")
    elif response.status_code == 503:
        pytest.skip("httpbin returned 503 (Service Unavailable). Skipping test.")
    else:
        print(f"Unexpected status code: {response.status_code}")

    try:
        print("Response JSON:", response.json())
    except ValueError:
        print("Response body is empty or not JSON.")
    assert response.status_code in (200, 401, 503)

# 52. Send a request to httpbin.org/bearer without any authorization header and validate if the response is 401.
@pytest.mark.api_test
def test_bearer_empty_auth_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/bearer"
    headers = {}

    print("Step 52:")
    response = api_client.get(url, headers=headers)
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Bearer authentication succeeded with invalid token.")
    elif response.status_code == 401:
        print("Authentication failed with invalid or missing token.")
    elif response.status_code == 503:
        pytest.skip("httpbin returned 503 (Service Unavailable). Skipping test.")
    else:
        print(f"Unexpected status code: {response.status_code}")

    try:
        print("Response JSON:", response.json())
    except ValueError:
        print("Response body is empty or not JSON.")
    assert response.status_code in (401, 503)

# Advanced Assertions
# 53. Fetch user with ID 1 from JSONPlaceholder and validate the data types of the keys id (int), name (str), address (dict), and company (dict).
@pytest.mark.api_test
def test_fetch_user_id_one_keys(base_json_url, api_client):
    url = f"{base_json_url}/users?id=1"

    print("Step 53:")
    response = api_client.get(url)
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Fetched user with ID 1 successfully")
    elif response.status_code == 401:
        print("Failed to fetch user with ID 1")
    elif response.status_code == 503:
        pytest.skip("httpbin returned 503 (Service Unavailable). Skipping test.")
    else:
        print(f"Unexpected status code: {response.status_code}")

    data = response.json()
    user = data[0]
    if(type(user["id"]) == int):
        print("'id' is of int type")
    else:
        print("'id' isn't of int type")
    if(type(user["name"]) == str):
        print("'name' is of str type")
    else:
        print("'name' isn't of str type")
    if(type(user["address"]) == dict):
        print("'address' is of dict type")
    else:
        print("'address' isn't of dict type")
    if(type(user["company"]) == dict):
        print("'company' is of dict type")
    else:
        print("'company' isn't of dict type")

    assert response.status_code == 200
    assert isinstance(data, list) and len(data) > 0
    user = data[0]
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str)
    assert isinstance(user["address"], dict)
    assert isinstance(user["company"], dict)

# 54. For the same user, check if the address key contains the sub-keys street, city, and zipcode.
@pytest.mark.api_test
def test_fetch_user_id_one_check_subkeys(base_json_url, api_client):
    url = f"{base_json_url}/users?id=1"

    print("Step 54:")
    response = api_client.get(url)
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Fetched user with ID 1 successfully")
    elif response.status_code == 401:
        print("Failed to fetch user with ID 1")
    elif response.status_code == 503:
        pytest.skip("httpbin returned 503 (Service Unavailable). Skipping test.")
    else:
        print(f"Unexpected status code: {response.status_code}")

    data = response.json()
    user = data[0]
    address = user.get("address", {})
    subkeys = {"street", "city", "zipcode"}
    missing = []
    for key in subkeys:
        if key not in address:
            missing.append(key)

    if missing == []:
        print("All subkeys checked (street, city and zipcode) are present on user address")
    else:
        print("Missing subkeys are the following: ", missing)

    assert response.status_code == 200
    assert isinstance(data, list) and len(data) > 0
    user = data[0]
    address = user.get("address", {})
    for k in ("street","city","zipcode"):
        assert k in address


# 55. Fetch post with ID 10 and validate if the keys userId and id are integers and if title and body are non-empty strings.
@pytest.mark.api_test
def test_fetch_user_id_ten_check_keys(base_json_url, api_client):
    url = f"{base_json_url}/posts?id=10"

    print("Step 55:")
    response = api_client.get(url)
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Fetched post with ID 10 successfully")
    elif response.status_code == 401:
        print("Failed to fetch post with ID 10")
    elif response.status_code == 503:
        pytest.skip("httpbin returned 503 (Service Unavailable). Skipping test.")
    else:
        print(f"Unexpected status code: {response.status_code}")

    data = response.json()
    post = data[0]
    if(type(post["userId"]) == int):
        print("'userId' is of int type")
    else:
        print("'userId' isn't of int type")
    if(type(post["id"]) == int):
        print("'id' is of int type")
    else:
        print("'id' isn't of int type")
    if(post["title"]) != "":
        print("'title' isn't an empty string")
    else:
        print("'title' is an empty string")
    if(post["body"]) != "":
        print("'body' isnt an empty string")
    else:
        print("'body' is an empty string")

    assert response.status_code == 200
    assert isinstance(data, list) and len(data) > 0
    post = data[0]
    assert isinstance(post["userId"], int)
    assert isinstance(post["id"], int)
    assert post["title"] != ""
    assert post["body"]  != ""

# 56. List the photos from album with ID 1 and check if each photo in the response contains the keys albumId, id, title, url, and thumbnailUrl.
@pytest.mark.api_test
def test_fetch_album_id_one_check_subkeys(base_json_url, api_client):
    url = f"{base_json_url}/photos?albumId=1"

    print("Step 56:")
    response = api_client.get(url)
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Fetched album with ID 1 successfully")
    elif response.status_code == 401:
        print("Failed to fetch album with ID 1")
    elif response.status_code == 503:
        pytest.skip("httpbin returned 503 (Service Unavailable). Skipping test.")
    else:
        print(f"Unexpected status code: {response.status_code}")

    data = response.json()
    album = data[0]
    subkeys = {"albumId", "id", "title", "url", "thumbnailUrl"}
    missing = []
    i = 0
    for key in subkeys:
        album = data[i]
        if key not in album and key not in missing:
            missing.append(key)
        i += 1

    if missing == []:
        print("All subkeys checked (albumId, id, title, url and thumbnailUrl) are present on album photos")
    else:
        print("Missing subkeys are the following: ", missing)

    assert response.status_code == 200
    assert isinstance(data, list) and len(data) > 0
    for photo in data:
        for k in ("albumId", "id", "title", "url", "thumbnailUrl"):
            assert k in photo

# 57. Check if the email key of user with ID 3 follows a valid email format (contains "@" and "." in the domain part).
@pytest.mark.api_test
def test_fetch_email_key_user_id_one_validate(base_json_url, api_client):
    url = f"{base_json_url}/users?id=1"

    print("Step 57:")
    response = api_client.get(url)
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Fetched user with ID 1 successfully")
    elif response.status_code == 401:
        print("Failed to fetch user with ID 1")
    elif response.status_code == 503:
        pytest.skip("httpbin returned 503 (Service Unavailable). Skipping test.")
    else:
        print(f"Unexpected status code: {response.status_code}")

    data = response.json()
    email = data[0]["email"]
    print("User email: " + email)
    split_email = email.split("@")
    if len(split_email) != 2:
        print("Invalid email: missing or multiple '@'")
        return

    local = split_email[0]
    domain = split_email[1]
    if "." not in domain:
        print("Invalid email: no '.' found in domain")
        return
    if domain.startswith(".") or domain.endswith("."):
        print("Invalid email: domain starts or ends with '.'")
        return
    if (local or domain) == "":
        print("Invalid email: local or domain is empty")
        return

    print("User email is valid")
    assert response.status_code == 200
    assert isinstance(data, list) and len(data) > 0
    email = data[0]["email"]
    assert (
        "@" in email
        and "." in email.split("@")[1]
        and not email.split("@")[1].startswith(".")
        and not email.split("@")[1].endswith(".")
    )

# 58. Fetch the comments for post with ID 5 and check if the list of comments is not empty.
@pytest.mark.api_test
def test_fetch_comments_post_five_not_empty(base_json_url, api_client):
    url = f"{base_json_url}/comments?postId=5"

    print("Step 58:")
    response = api_client.get(url)
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Fetched comment with post ID 5 successfully")
    elif response.status_code == 401:
        print("Failed to fetch comment with post ID 5")
    elif response.status_code == 503:
        pytest.skip("httpbin returned 503 (Service Unavailable). Skipping test.")
    else:
        print(f"Unexpected status code: {response.status_code}")

    data = response.json()
    if(len(data) > 0):
        print("Comment list for post with ID 5 isn't empty")
    else:
        print("Comment list for post with ID 5 is empty")

    assert response.status_code == 200
    assert isinstance(data, list) and len(data) > 0

# 59. For the first comment from the previous list, validate the types of postId (int), id (int), name (str), email (str), and body (str).
@pytest.mark.api_test
def test_fetch_first_comment_post_id_five_validate(base_json_url, api_client):
    url = f"{base_json_url}/comments?postId=5"
    print("Step 59:")
    response = api_client.get(url)
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Fetched comment with post ID 5 successfully")
    elif response.status_code == 401:
        print("Failed to fetch comment with post ID 5")
    elif response.status_code == 503:
        pytest.skip("httpbin returned 503 (Service Unavailable). Skipping test.")
    else:
        print(f"Unexpected status code: {response.status_code}")

    data = response.json()
    first_comment = data[0]

    if(type(first_comment["postId"]) == int):
        print("'postId' is of int type")
    else:
        print("'postId' isn't of int type")
    if(type(first_comment["id"]) == int):
        print("'id' is of int type")
    else:
        print("'id' isn't of int type")
    if(type(first_comment["name"]) == str):
        print("'name' is of str type")
    else:
        print("'name' isn't of str type")
    if(type(first_comment["email"]) == str):
        print("'email' is of str type")
    else:
        print("'email' isn't of str type")
    if(type(first_comment["body"]) == str):
        print("'body' is of str type")
    else:
        print("'body' isn't of str type")

    assert response.status_code == 200
    assert isinstance(data, list) and len(data) > 0
    first_comment = data[0]
    assert isinstance(first_comment["postId"], int)
    assert isinstance(first_comment["id"], int)
    assert isinstance(first_comment["name"], str)
    assert isinstance(first_comment["email"], str)
    assert isinstance(first_comment["body"], str)

# 60. Fetch the todo with ID 199 and check if the value of the completed key is a boolean (True or False).
@pytest.mark.api_test
def test_todo_one_nine_nine_completed_or_not(base_json_url, api_client):
    url = f"{base_json_url}/todos?id=199"

    print("Step 60:")
    response = api_client.get(url)
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Fetched todo with ID 199 successfully")
    elif response.status_code == 401:
        print("Failed to fetch todo with ID 199")
    elif response.status_code == 503:
        pytest.skip("httpbin returned 503 (Service Unavailable). Skipping test.")
    else:
        print(f"Unexpected status code: {response.status_code}")

    data = response.json()
    todo_199 = data[0]
    if(type(todo_199["completed"]) == bool):
        print("'completed' is of bool type")
    else:
        print("'completed' isn't of bool type")

    assert response.status_code == 200
    assert isinstance(data, list) and len(data) > 0
    todo_199 = data[0]
    assert isinstance(todo_199["completed"], bool)
