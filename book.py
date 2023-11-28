# for Bret Craig's extra feature

import requests
import random

api_key = "AIzaSyBcPiCpOtR4bQwtdvuXLMX2hsbrg3TDfQs"

def recommend_book(query):

    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            item = random.choice(data["items"])
            volume_info = item.get("volumeInfo", {})
            title = volume_info.get("title", "Title not available")
            authors = ", ".join(volume_info.get("authors", ["Author not available"]))
            return f"{title} by {authors}"
        else:
            return "No books found matching your request."
    else:
        return f"Unable to get a book recommendation. Returned status code {response.status_code}."

