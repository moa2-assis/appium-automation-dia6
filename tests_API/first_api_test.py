# Example of a basic GET request
import requests
import pytest

final_user = "torvalds"
base_url = "https://api.github.com/"
base_json_url = "https://jsonplaceholder.typicode.com/"


def get_json_field_from_user(user, jsonField):
    url = base_url + "users/" + user
    response = requests.get(url)
    data = response.json()
    return data[jsonField]

def get_json_from_user_repo(user, repo):
    url = base_url + "repos/" + user + "/" + repo
    response = requests.get(url)
    data = response.json()
    return data

def get_json_commits_from_user_repo(user, repo):
    url = base_url + "repos/" + user + "/" + repo + "/commits"
    response = requests.get(url)
    data = response.json()
    return data

# # Step 1: Simple Request
# def test_simple_request():
#     response = requests.get('https://api.github.com')
#     assert response.status_code == 200

# # Step 2: Fetch a Specific User
# def test_username_octocat():
#     assert get_json_field_from_user("octocat", "login") == "octocat"

# # Step 3: Validate User Type
# # Check if "octocat" is of type "User".
# def test_user_type():
#     assert get_json_field_from_user("octocat", "type") == "User"

# # Step 4: Request with Repository ID
# # Fetch the repository with ID 1296269 and check if it is "Hello-World".
# def test_repository_id():
#     target_url = "https://api.github.com/repositories/1296269"
#     response = requests.get(target_url)
#     data = response.json()
#     assert data["name"] == "Hello-World"

# # Step 5: Handling Errors (Non-existent User)
# # Try to fetch a user that does not exist (e.g., "nonexistentuser12345") and check if the status code is 404 (Not Found).
# def test_non_existent_user_request():
#     response = requests.get('https://api.github.com/users/nonexistentuser123451623129931249')
#     assert response.status_code == 404

# # Step 6: List User Repositories
# # Make a request to list the repositories of the user "google" with a limit of 5 and print the name of the first one in the list.
# def test_google_user_repos_list_five():
#     target_user_repos = 'https://api.github.com/users/google/repos'
#     limit_repos = 5
#     params = {'per_page': limit_repos}

#     response = requests.get(target_user_repos, params)
#     assert response.status_code == 200
#     data = response.json()

#     print("Step 6:")
#     print(data[0]["name"])

# # Step 7: Navigate Follower Pagination
# # List the followers of the user "microsoft", get the URL of the next page from the 'Link' header, and make a new request.
# def test_microsoft_followers_header_link():
#     target_followers = 'https://api.github.com/users/microsoft/followers'
#     response = requests.get(target_followers)

#     print("Step 7:")
#     assert response.status_code == 200
#     header_link = response.headers.get("Link")
#     print(header_link)
#     # <https://api.github.com/user/6154722/followers?page=2>; rel="next", <https://api.github.com/user/6154722/followers?page=3490>; rel="last"

#     header_link = response.headers.get("Link")
#     parts = header_link.split("'")
#     next_link = ""
#     for part in parts:
#         if 'rel="next"' in part:
#             next_link = part.split(";")[0].strip("<> ")
#             break
#     print("Next page URL:", next_link)
#     next_response = requests.get(next_link)
#     print("Status da próxima página:", next_response.status_code)

# # Step 8: Count a User's Public Repositories
# # Check how many public repositories the user "facebook" has.
# def test_count_public_repos():
#     print("Step 8: ")
#     print(get_json_field_from_user("facebook", "public_repos"))

# # Step 9: Find a Specific Language in a Repository
# # Check if the language "JavaScript" is in the list of languages for the "react" repository from Facebook.
# def test_check_javascript_language_react_facebook():
#     url = base_url + "repos/facebook/react/languages"
#     response = requests.get(url)
#     assert response.status_code == 200
#     data = response.json()
#     if "JavaScript" in data:
#         print("Step 9:")
#         print("Repositório 'facebook' usa JavaScript")
#     else:
#         print("Step 9:")
#         print("Repositório 'facebook' não usa JavaScript")

# # Step 10: Explore Another Endpoint (Emojis)
# # Fetch the list of available emojis from the API and check if the "+1" emoji exists.
# def test_check_emojis_plus_one():
#     url = base_url + "emojis"
#     response = requests.get(url)
#     assert response.status_code == 200
#     data = response.json()
#     print("Step 10:")
#     if "+1" in data:
#         print("Emoji '+1' faz parte do GitHub")
#     else:
#         print("Emoji '+1' não faz parte do GitHub")

# # Step 11: Validate Repository JSON Structure
# # For the "linux" repository from "torvalds", check if the keys "name", "owner", and "language" exist in the response JSON.
# def test_torvalds_linux_name_owner_language():
#     data = get_json_from_user_repo("torvalds", "linux")
#     print("Step 11:")
#     if "name" in data:
#         print("Key 'name' existe no json extraído")
#     else:
#         print("Key 'name' não existe no json extraído")

#     if "owner" in data:
#         print("Key 'owner' existe no json extraído")
#     else:
#         print("Key 'owner' não existe no json extraído")

#     if "language" in data:
#         print("Key 'language' existe no json extraído")
#     else:
#         print("Key 'language' não existe no json extraído")

# # Step 12: Compare Repository Attributes
# # Compare the "stargazers_count" of Microsoft's "vscode" repository and Atom's "atom" repository. Check if the VSCode count is higher.
# def test_check_stargazers_vscode_atom():
#     data_vscode = get_json_from_user_repo("microsoft", "vscode")
#     vscode_stargazers = data_vscode["stargazers_count"]
#     data_atom = get_json_from_user_repo("atom", "atom")
#     atom_stargazers = data_atom["stargazers_count"]
#     print("Step 12:")
#     if(atom_stargazers > vscode_stargazers):
#         print(f"VSCode count ({vscode_stargazers}) is lower than Atom's count ({atom_stargazers}).")
#     elif(atom_stargazers == vscode_stargazers):
#         print(f"VSCode count ({vscode_stargazers}) is equal than Atom's count ({atom_stargazers}).")
#     else:
#         print(f"VSCode count ({vscode_stargazers}) is higher than Atom's count ({atom_stargazers}).")

# # Step 13: Fetch a License
# # Fetch the "mit" license and check its name.
# def test_fetch_mit_license_name():
#     url = base_url + "licenses"
#     response = requests.get(url)
#     data = response.json()
#     print("Step 13:")

#     license_name = ""
#     for license in data:
#         if(license["key"] == "mit"):
#             license_name = license["name"]
#             break

#     print("License name: " + license_name)

# # Step 14: List All Licenses
# # Make a request to the licenses endpoint and count how many common licenses exist.
# def test_count_common_licenses():
#     url = base_url + "licenses"
#     response = requests.get(url)
#     data = response.json()
#     print("Step 14:")

#     license_count = 0
#     for license in data:
#         license_count += 1

#     print(f"License count: {license_count}")

# # Step 15: Find Repositories with a Specific License
# # Search for repositories with the "apache-2.0" license and print the name of the first one in the list.
# def test_find_repos_with_apache_license():
#     url = base_url + "search/repositories?q=licence:apache-2.0"
#     response = requests.get(url)
#     data = response.json()
#     print("Step 15:")
#     print(data["items"][0]["name"])

# # Step 16: Validate a Repository's Organization
# # Check if the "docker" repository belongs to the "moby" organization.
# def test_check_docker_moby():
#     data = get_json_from_user_repo("docker", "docker")
#     print("Step 16:")
#     print(f"Owner: {data['owner']['login']}")

# # Step 17: Check the Last Commit of a Repository
# # From the "tensorflow/tensorflow" repository, get the last commit and check if the message is not empty.
# def test_tensorflow_repo_last_commit():
#     data = get_json_commits_from_user_repo("tensorflow", "tensorflow")
#     print("Step 17:")
#     print(data[0]["commit"]["message"])

# # Step 18: Check if a User is an Organization
# # Check if "apple" is of type "Organization".
# def test_check_user_type_apple():
#     data = get_json_field_from_user("apple", "type")
#     print("Step 18:")
#     print(data)
#     if(data == "Organization"):
#         print(f"User 'apple' is of type 'Organization'")
#     else:
#         print(f"User 'apple' isn't of type 'Organization'")

# # Step 19: Find the Number of Contributors to a Repository
# # Fetch the number of contributors for the "kubernetes/kubernetes" repository and check if it is greater than 1000.

# def test_get_number_of_contributors_kubernetes():
#     target_total_contributors = base_url + "repos/kubernetes/kubernetes/contributors"
#     response = requests.get(target_total_contributors)  # primeira página
#     header_link = response.headers.get("Link")
#     page = 1
#     total_count = 0

#     # conta a primeira página
#     sum_quantity = len(response.json())
#     total_count += sum_quantity

#     max_pages = 1
#     next_link = ""

#     # se houver header Link, pega max_pages e next_link
#     if header_link:
#         parts = header_link.split(",")  # separa cada link
#         for part in parts:
#             part = part.strip()

#             if 'rel="last"' in part:
#                 last_link = part.split(";")[0].strip("<> ")
#                 # faz parse "manual": pega o número depois de 'page='
#                 if "page=" in last_link:
#                     max_pages = int(last_link.split("page=")[1])
            
#             if 'rel="next"' in part:
#                 next_link = part.split(";")[0].strip("<> ")

#     # percorre páginas seguintes até max_pages
#     while page < max_pages and next_link:
#         page += 1
#         response = requests.get(next_link)
#         sum_quantity = len(response.json())
#         total_count += sum_quantity

#         header_link = response.headers.get("Link")
#         next_link = ""

#         if header_link:
#             parts = header_link.split(",")
#             for part in parts:
#                 part = part.strip()
#                 if 'rel="next"' in part:
#                     next_link = part.split(";")[0].strip("<> ")
#                     break

#     if total_count > 1000:
#         print(f"Kubernetes has more than 1000 contributors ({total_count} total)")
#     else:
#         print(f"Kubernetes doesn't have more than 1000 contributors ({total_count} total)")

# # Step 20: Final Challenge - Putting It All Together
# # Create a function that takes a username, fetches their data, and returns a dictionary with their login, name, and number of public repositories. Test it with "torvalds".
# def test_final_challenge_torvalds_data():
#     login = get_json_field_from_user("torvalds", "login")
#     name = get_json_field_from_user("torvalds", "name")
#     public_repos = get_json_field_from_user("torvalds", "public_repos")

#     print("Step 20:")
#     print(login)
#     print(name)
#     print(public_repos)

# # Step 21: Create a New Post (POST)
# # Make a POST request to /posts to create a new post. Check if the status code is 201 (Created).
# def test_post():
#     new_post = {
#         "title": "Hello world",
#         "body": "This is a test post",
#         "userId": 1
#     }
#     url = base_json_url + "posts"
#     response = requests.post(url, json=new_post)

#     print("Step 21:")
#     print("Status code:", response.status_code)
#     if response.status_code == 201:
#         print("Post created successfully!")
#     else:
#         print("Failed to create post.")

# # Step 22: Validate Created Post Data
# # Validate that the response body of the created post contains the sent title and body.
# def test_validate_created_post_data():
#     new_post = {
#         "title": "Hello world",
#         "body": "This is a test post",
#         "userId": 1
#     }
#     url = base_json_url + "posts"
#     response = requests.post(url, json=new_post)
#     data = response.json()

#     if(new_post["title"] == data["title"]):
#         print(f"'title' é o mesmo")
#     else:
#         print(f"'title' não é o mesmo")
#     if(new_post["body"] == data["body"]):
#         print(f"'body' é o mesmo")
#     else:
#         print(f"'body' não é o mesmo")
#     if(new_post["userId"] == data["userId"]):
#         print(f"'userId' é o mesmo")
#     else:
#         print(f"'userId' não é o mesmo")

# # Step 23: Update a Post (PUT)
# # Make a PUT request to /posts/1 to update the post with ID 1. Check if the status code is 200.
# def test_update_post_with_put():
#     url = base_json_url + "posts/1"
#     updated_post = {
#         "id": 1,
#         "title": "Updated Title",
#         "body": "This post has been updated.",
#         "userId": 1
#     }
#     response = requests.put(url, json=updated_post)

#     print("Step 23:")
#     print("Status code:", response.status_code)
#     if response.status_code == 200:
#         print("Post updated successfully")
#     else:
#         print("Failed to update post")

# # Step 24: Validate Post Update
# # Check if the response body of the updated post contains the new data sent.
# def test_validate_updated_post_data():
#     updated_post = {
#         "id": 1,
#         "title": "Updated Title",
#         "body": "This post has been updated.",
#         "userId": 1
#     }
#     url = base_json_url + "posts/1"
#     response = requests.put(url, json=updated_post)
#     data = response.json()

#     if(updated_post["id"] == data["id"]):
#         print(f"'id' é o mesmo")
#     else:
#         print(f"'id' não é o mesmo")
#     if(updated_post["title"] == data["title"]):
#         print(f"'title' é o mesmo")
#     else:
#         print(f"'title' não é o mesmo")
#     if(updated_post["body"] == data["body"]):
#         print(f"'body' é o mesmo")
#     else:
#         print(f"'body' não é o mesmo")
#     if(updated_post["userId"] == data["userId"]):
#         print(f"'userId' é o mesmo")
#     else:
#         print(f"'userId' não é o mesmo")

# # Step 25: Delete a Post (DELETE)
# # Make a DELETE request to /posts/1 to delete the post. Check if the status code is 200.
# def test_delete_post():
#     url = base_json_url + "posts/1"
#     response = requests.delete(url)

#     print("Step 21:")
#     print("Status code:", response.status_code)
#     if response.status_code == 200:
#         print("Post deleted successfully")
#     else:
#         print("Failed to delete post")

# # Step 26: List All Users
# # Make a GET request to /users and check if the list contains 10 users.
# def test_get_users_size():
#     url = base_json_url + "users"
#     response = requests.get(url)
#     data = response.json()
#     quantity_on_list = len(data)
#     print("Users quantity is " + str(quantity_on_list))

# # Step 27: Fetch a Specific User
# # Fetch the user with ID 5 and check if their name is "Chelsey Dietrich".
# def test_user_name_id_five():
#     url = base_json_url + "users"
#     response = requests.get(url)
#     data = response.json()
#     for user in data:
#         if(user["id"] == 5):
#             check_name = user["name"]
#             break
#     print("name of user with ID 5 is: " + str(check_name))

# # Step 28: Create a New Comment for a Post
# # Make a POST request to /posts/1/comments to add a new comment. Check for status code 201.
# def test_new_comment_with_post():
#     new_comment = {
#         "postId": 1,
#         "id": 1,
#         "name": "id labore ex et quam laborum",
#         "email": "Eliseo@gardner.biz",
#         "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium"
#     }
#     url = base_json_url + "posts/1/comments"
#     response = requests.post(url, json=new_comment)

#     print("Step 21:")
#     print("Status code:", response.status_code)
#     if response.status_code == 201:
#         print("Post comment created successfully!")
#     else:
#         print("Failed to create post comment.")

# # Step 29: List a User's Albums
# # List all albums for the user with ID 3 (/users/3/albums) and count how many albums they have.
# def test_list_all_albums_user_three():
#     url = base_json_url + "users/3/albums"
#     response = requests.get(url)
#     data = response.json()
#     quantity_of_albums = len(data)
#     i = 1
#     print("Step 29:")
#     for user in data:
#         name = user["title"]
#         print(f"Album number '{i}': {name}")
#         i += 1
#     print(f"Total of albums: {quantity_of_albums}")
    
# # Step 30: List Photos in an Album
# # List all photos from the album with ID 2 (/albums/2/photos) and check if the first photo has the title "reprehenderit est deserunt velit ipsam".
# def test_list_all_albums_user_three():
#     url = base_json_url + "/albums/2/photos"
#     response = requests.get(url)
#     data = response.json()
#     print("Step 30:")
#     if(data[0]["title"] == "reprehenderit est deserunt velit ipsam"):
#         print("Album has 'reprehenderit est deserunt velit ipsam' on its title")
#     else:
#         print("Album doesn't have 'reprehenderit est deserunt velit ipsam' on its title")
#     i = 1
    
#     for user in data: 
#         name = user["url"]
#         print(f"Photo number '{i}' URL: {name}")
#         i += 1

# # Step 31: Create a New Task (Todo)
# # Create a new task (todo) for the user with ID 1 with the title "Learn Pytest" and check if it was created successfully.
# def test_new_to_do():
#     new_todo = {
#     "userId": 1,
#     "id": 1,
#     "title": "delectus aut autem",
#     "completed": False
#     }
#     url = base_json_url + "todos/1"
#     response = requests.put(url, json=new_todo)
#     data = response.json()

#     print("Step 31:")
#     print("Status code:", response.status_code)
#     if response.status_code == 200:
#         print("Post created successfully!")
#     else:
#         print("Failed to create post.")

# # Step 32: Update a Task (PATCH)
# # Update the status of the task with ID 5 to completed: true using a PATCH request. Check the response.
# def test_update_patch_task():
#     new_todo = {
#     "title": "yoyoyo"
#     }
#     url = base_json_url + "todos/5"
#     response = requests.patch(url, json=new_todo)
#     data = response.json()

#     print("Step 32:")
#     print("Status code:", response.status_code)
#     if response.status_code == 200:
#         print("Post patched successfully!")
#     else:
#         print("Failed to patch post.")

# # Step 33: List a User's Completed Tasks
# # List all tasks for the user with ID 1 and filter only those that are completed (completed: true).
# def test_list_user_completed_tasks():
#     url = base_json_url + "/todos/"
#     response = requests.get(url)
#     data = response.json()
#     print("Step 33:")
#     i = 1
#     for user in data: 
#         if user["userId"] == 1 and user["completed"] == True:
#             task = user["title"]
#             print(f"Completed task number '{i}': {task}")
#             i += 1

# # Step 34: Validate a Comment's Structure
# # Fetch the comment with ID 10 and check if it contains the keys "postId", "id", "name", "email", and "body".
# def test_validate_comment_id_ten():
#     url = base_json_url + "comments/10"
#     response = requests.get(url)
#     data = response.json()

#     print("Step 34:")
#     expected_keys = ["postId", "id", "name", "email", "body"]

#     for key in expected_keys:
#         if key in data:
#             print(f"Key '{key}' found")
#         else:
#             print(f"Key '{key}' missing")

# # Step 35: Delete a Comment
# # Delete the comment with ID 3 and check if the request was successful.
# def test_delete_comment_three():
#     url = base_json_url + "comments/10"
#     response = requests.delete(url)

#     print("Step 35:")
#     print("Status code:", response.status_code)
#     if response.status_code == 200:
#         print("Post deleted successfully!")
#     else:
#         print("Failed to delete post.")

# # Step 36: Create a Post with Invalid Data
# # Try to create a post by sending an empty JSON body and observe the API's response (although JSONPlaceholder might return 201, it's good practice to check the behavior).
# def test_invalid_data_send_through_post():
#     empty_json = {}
#     url = base_json_url + "users"
#     response = requests.post(url, json=empty_json)
#     print("Step 36:")
#     print("Status code:", response.status_code)

# # Step 37: Fetch a Specific User's Posts
# # Fetch all posts from the user with ID 7 (/users/7/posts) and count how many posts they have.
# def test_fetch_posts_user_id_seven():
#     url = base_json_url + "users/7/posts"
#     response = requests.get(url)
#     data = response.json()
#     quantity_of_posts = len(data)
#     print("Step 37:")
#     print(f"Amount of posts of user with ID 7: {quantity_of_posts}")

# # Step 38: Update a User's Email (PUT)
# # Update the data for the user with ID 2, changing only the email to "new.email@example.com".
# def test_put_new_user_email_id_two():
#     update_email = {
#         "email": "new.email@example.com"
#     }
#     url = base_json_url + "users/2"
#     response = requests.patch(url, json=update_email)
#     print("Step 38:")
#     print("Status code:", response.status_code)

# # Step 39: Delete an Album
# # Delete the album with ID 4 and check the response status.
# def test_delete_album_id_four():
#     url = base_json_url + "albums/4"
#     response = requests.delete(url)
#     print("Step 39:")
#     print("Status code:", response.status_code)

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