import requests
from decouple import config,Csv
import json


class GPTRequests:

    def getTopicsToWriteOn(message):
        print("message ======> " + message)
        try : 
            # API endpoint
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + config("GEMINI_API_KEY")
            headers = {"Content-Type": "application/json"}  # Set the Content-Type header
            text = {"text": "Generate a list of titles to write articles on. Use only the topics: "
                + message
                + ". Output the response as a JSON object with a single key called 'titles'. The value of"
                + " 'titles' should be a JSON array of JSON objects. Each object in the array should "
                + "have a single key called 'title' whose value is the generated article title."}
            print(text)
            data = {
                "contents": [{
                    "parts":[
                        text
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.9,
                    "topP": 0.9,
                    "maxOutputTokens": 500
                }
            }
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                response_data = response.json() # First, get the API"s JSON response
                print(response_data)
                # Accessing response structure
                if "candidates" in response_data and len(response_data["candidates"]) > 0 :
                    candidates = response_data["candidates"]
                    if "content" in candidates[0] and "parts" in candidates[0]["content"] and len(candidates[0]["content"]["parts"]) > 0:
                        text_string = candidates[0]["content"]["parts"][0]["text"]
                        # Parse the JSON string
                        try:
                            text = text_string.replace("json", "").replace("```", "")
                            # print(str(text))
                            # json_object1 = json.loads()
                            # print(json.dumps(json_object1, indent=2))
                            json_object = json.loads(text) # Convert JSON String to JSON object
                            # print(json_object)
                            # print(text_string) # Print the parsed JSON object
                            # print(json.dumps(json_object, indent=2))
                            return json.dumps(json_object, indent=2)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                    else:
                        print("invalid response structure")
                else:
                    print("invalid response structure")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except Exception as exception:
            print(f"Error decoding JSON: {exception}")



    def getArticlesToPost(message):
        print("getArticlesToPost -> ()")
        try : 
            # API endpoint
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + config("GEMINI_API_KEY")
            headers = {"Content-Type": "application/json"}  # Set the Content-Type header
            text = {
                "text": "Write an article on the topic '" + message + "' "
                + "to be posted on linkedIn. Write as a social medial handler for a marketting agency and "
                + "draw relations on how your marketting agency fits the narrative in the article. make it unique."
            }
            print(text)
            data = {
                "contents": [{
                    "parts":[
                        text
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "topP": 0.9,
                    "maxOutputTokens": 500
                }
            }
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                response_data = response.json() # First, get the API"s JSON response
                print(response_data)
                # Accessing response structure
                if "candidates" in response_data and len(response_data["candidates"]) > 0 :
                    candidates = response_data["candidates"]
                    if "content" in candidates[0] and "parts" in candidates[0]["content"] and len(candidates[0]["content"]["parts"]) > 0:
                        text_string = candidates[0]["content"]["parts"][0]["text"]
                        # Parse the JSON string
                        try:
                            return text_string
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                    else:
                        print("invalid response structure")
                else:
                    print("invalid response structure")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except Exception as exception:
            print(f"Error decoding JSON: {exception}")