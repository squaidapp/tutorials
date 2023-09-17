import requests

llama2_url = "http://localhost:8000/streaming"

while True:
    # Get user input for the question
    question = input("Type your question: ")
    
    # Check if the user wants to exit the loop
    if question.lower() == "exit":
        break

    author = 'Squaid'
    body = {'author': author, 'question': question}

    try:
        # Make a POST request to the web service
        with requests.post(llama2_url, json=body, stream=True) as r:
            r.raise_for_status()  # Raise an exception if the request was not successful

            # Process and print the streaming response
            for chunk in r.iter_content(1024):
                print(chunk.decode('utf-8'))

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

print("Exiting the program.")