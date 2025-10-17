import pytest
import csv

# Query Params
# 1. Fetch all comments for post ID 2 and verify that all returned comments belong to that post.
@pytest.mark.api_test
def test_fetch_comments_post_id_two_verify(base_json_url, api_client):
    response = api_client.get(f"{base_json_url}/posts/2/comments")
    print("Step 1:")
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

# 2. List all todos for user ID 5 and verify that the list is not empty.
@pytest.mark.api_test
def test_todos_user_id_five_verify_not_empty(base_json_url, api_client):
    response = api_client.get(f"{base_json_url}/todos?userId=5")
    print("Step 2:")
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

# 3. Fetch all albums for user ID 9 and count how many they have (should be 10).
@pytest.mark.api_test
def test_all_albums_user_id_nine_how_many(base_json_url, api_client):
    response = api_client.get(f"{base_json_url}//albums?userId=9")
    print("Step 3:")
    if(response.status_code == 200):
        print("Fetch albums done successfully!")
    else:
        print("Failed to albums todos.")
        return
    data = response.json()
    quantity_of_albums = len(data)
    print(f"Quantity of albums: {quantity_of_albums}")

# 4. List all completed todos (completed: true) for user ID 1 and verify that all in the response are indeed completed.
@pytest.mark.api_test
def test_completed_todos_user_id_one_verify_completed(base_json_url, api_client):
    response = api_client.get(f"{base_json_url}/todos?userId=1&completed=true")
    print("Step 4:")
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

# Headers
# 5. Send a request to httpbin.org/headers with the custom header X-Custom-Header: MyValue and validate the response.
@pytest.mark.api_test
def test_custom_header_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/headers"
    headers = {"X-Custom-Header": "MyValue"}
    print("Step 5:")
    response = api_client.get(url, headers=headers)
    print("Status code: ", response.status_code)
    data = response.json()
    if response.status_code == 200 and data["headers"].get("X-Custom-Header") == "MyValue":
        print("Custom header received successfully")
    else:
        print("Custom header not found or incorrect")
    print("Response JSON:", data)

# 6. Send a request to httpbin.org/response-headers to set a custom response header (e.g., My-Test-Header: Hello) and check if it is present in the response headers.
@pytest.mark.api_test
def test_custom_response_header_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/response-headers"
    params = {"My-Test-Header": "Hello"}

    print("Step 6:")
    response = api_client.get(url, params=params)
    print("Status code:", response.status_code)

    if response.status_code == 200 and response.headers.get("My-Test-Header") == "Hello":
        print("Custom response header received successfully")
    else:
        print("Custom response header missing or incorrect")
    print("Response headers:", response.headers)

# 7. Send a request to httpbin.org/headers with a custom User-Agent header ("My-Test-Agent/1.0") and validate if it was received correctly.
@pytest.mark.api_test
def test_custom_user_agent_header_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/headers"
    headers = {"User-Agent": "My-Test-Agent/1.0"}

    print("Step 7:")
    response = api_client.get(url, headers=headers)
    data = response.json()
    print("Status code:", response.status_code)

    if response.status_code == 200 and data["headers"].get("User-Agent") == "My-Test-Agent/1.0":
        print("Custom User-Agent header received successfully")
    else:
        print("Custom User-Agent header missing or incorrect")
    print("Response JSON:", data)

# 8. Send multiple custom headers (X-Header-1: Value1, X-Header-2: Value2) in a single request to httpbin.org/headers and validate all of them.
@pytest.mark.api_test
def test_multiple_custom_headers_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/headers"
    headers = {"X-Header-1": "Value1", "X-Header-2": "Value2"}

    print("Step 8:")
    response = api_client.get(url, headers=headers)
    data = response.json()
    print("Status code:", response.status_code)

    if response.status_code == 200 and data["headers"].get("X-Header-1") == "Value1" and data["headers"].get("X-Header-2") == "Value2":
        print("Custom multiple headers received successfully")
    else:
        print("Custom multiple headers missing or incorrect")
    print("Response JSON:", data)

# Authentication
# 9. Test the httpbin Basic Auth endpoint (/basic-auth/user/passwd) with the correct credentials (user, passwd) and validate the 200 status.
@pytest.mark.api_test
def test_basic_auth_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/basic-auth/user/passwd"
    print("Step 9:")
    response = api_client.get(url, auth=("user", "passwd"))
    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Authentication succeeded with correct credentials")
    else:
        print("Authentication failed")
    print("Response JSON:", response.json())

# 10. Test the same Basic Auth endpoint with a correct user but wrong password and validate the 401 status.
@pytest.mark.api_test
def test_basic_wrong_auth_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/basic-auth/user/passwd"
    print("Step 10:")
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

# 11. Send a request to httpbin.org/bearer with a valid Bearer Token (mock, e.g., "my-mock-token") and validate the successful authentication.
@pytest.mark.api_test
def test_bearer_auth_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/bearer"
    headers = {"Authorization": "Bearer my-mock-token"}

    print("Step 11:")
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

# 12. Send a request to httpbin.org/bearer without any authorization header and validate if the response is 401.
@pytest.mark.api_test
def test_bearer_empty_auth_httpbin(base_httpbin_url, api_client):
    url = f"{base_httpbin_url}/bearer"
    headers = {}

    print("Step 12:")
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

# Advanced Assertions
# 13. Fetch user with ID 1 from JSONPlaceholder and validate the data types of the keys id (int), name (str), address (dict), and company (dict).
@pytest.mark.api_test
def test_fetch_user_id_one_keys(base_json_url, api_client):
    url = f"{base_json_url}/users?id=1"

    print("Step 13:")
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
    if(type(data["id" == int])):
        print("'id' is of int type")
    else:
        print("'id' isn't of int type")
    if(type(data["name" == str])):
        print("'name' is of str type")
    else:
        print("'name' isn't of str type")
    if(type(data["address" == dict])):
        print("'address' is of dict type")
    else:
        print("'address' isn't of dict type")
    if(type(data["company" == dict])):
        print("'company' is of dict type")
    else:
        print("'company' isn't of dict type")

# 14. For the same user, check if the address key contains the sub-keys street, city, and zipcode.
@pytest.mark.api_test
def test_fetch_user_id_one_check_subkeys(base_json_url, api_client):
    url = f"{base_json_url}/users?id=1"

    print("Step 14:")
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


# 15. Fetch post with ID 10 and validate if the keys userId and id are integers and if title and body are non-empty strings.
@pytest.mark.api_test
def test_fetch_user_id_ten_check_keys(base_json_url, api_client):
    url = f"{base_json_url}/posts?id=10"

    print("Step 15:")
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

# 16. List the photos from album with ID 1 and check if each photo in the response contains the keys albumId, id, title, url, and thumbnailUrl.
@pytest.mark.api_test
def test_fetch_album_id_one_check_subkeys(base_json_url, api_client):
    url = f"{base_json_url}/photos?albumId=1"

    print("Step 16:")
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

# 17. Check if the email key of user with ID 3 follows a valid email format (contains "@" and "." in the domain part).
@pytest.mark.api_test
def test_fetch_email_key_user_id_one_validate(base_json_url, api_client):
    url = f"{base_json_url}/users?id=1"

    print("Step 17:")
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

# 18. Fetch the comments for post with ID 5 and check if the list of comments is not empty.
@pytest.mark.api_test
def test_fetch_comments_post_five_not_empty(base_json_url, api_client):
    url = f"{base_json_url}/comments?postId=5"

    print("Step 18:")
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

# 19. For the first comment from the previous list, validate the types of postId (int), id (int), name (str), email (str), and body (str).
@pytest.mark.api_test
def test_fetch_first_comment_post_id_five_validate(base_json_url, api_client):
    url = f"{base_json_url}/comments?postId=5"
    print("Step 19:")
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
    
# 20. Fetch the todo with ID 199 and check if the value of the completed key is a boolean (True or False).
@pytest.mark.api_test
def test_todo_one_nine_nine_completed_or_not(base_json_url, api_client):
    url = f"{base_json_url}/todos?id=199"

    print("Step 18:")
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