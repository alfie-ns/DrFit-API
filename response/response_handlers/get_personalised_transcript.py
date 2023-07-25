# # Path: django-api\response\response_handlers\personal_response.py
# from ..models import Conversation
# from googleapiclient.discovery import build
# from youtube_transcript_api import YouTubeTranscriptApi
# from urllib.parse import urlparse, parse_qs
# from dotenv import load_dotenv
# import json, os, openai

# load_dotenv()

# test_prompt = """
#                   You a knowledgable doctor. You are given the transcript 
#                   of a youtube video and must make a list of the different brain nutrients 
#                   that are mentioned in the video. You are given the entire transcript in chunks 
#                   and must generate a list of every single brain nutrient listed in the video transcript.
#                   """

# def get_personalised_transcript(request):
#     '''This function takes in a youtube video url and a wish
#        from the user and returns a response'''

#     # Get JSON data from the request body
#     data = json.loads(request.body.decode('utf-8'))
#     url = data.get('url')
#     prompt_wish = data.get('wish')




#     # Extract video Id from url
#     query = urlparse(url)
#     video_id = parse_qs(query.query).get('v')[0]

#     # Initialize the Youtube API
#     api_service_name = "youtube"
#     api_version = "v3"
#     DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")
#     youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

#     # Get the English captions
#     caption_request = youtube.captions().list(
#         part="snippet", 
#         videoId=video_id 
#     )
#     response = caption_request.execute()
#     english_captions = [item['id'] for item in response['items'] if item['snippet']['language'] == 'en-US']

#     # Get the transcript for the video
#     transcript = YouTubeTranscriptApi.get_transcript(video_id)

#     # Extract the sentences from the transcript
#     sentences = [entry['text'] for entry in transcript]

#     # Split the sentences into chunks of approximately {insight_num000 tokens each
#     chunks = []
#     chunk = []
#     chunk_size = 0
#     # For each sentence in the transcript
#     for text in sentences:
#         # If the chunk size is less than or equal the maximum chunk size, append it to chunk list
#         if chunk_size + len(text.split()) <= 7500:
#             chunk.append(text)
#             chunk_size += len(text.split()) # Update the chunk size
#         else:
#             # If the chunk size is greater than the maximum chunk size, append the chunks to the chunks list
#             chunks.append(" ".join(chunk))
#             chunk = [text]
#             chunk_size = len(text.split())
#         print(f"CHUNK: {chunk}")
#         print(f"CHUNK SIZE: {chunk_size}")
#     if chunk:  # For the last chunk
#         chunks.append(" ".join(chunk))





#     # Try to get the existing conversation from the database
#     conversation, created = Conversation.objects.get_or_create(user=request.user)

#     summary_responses = []

#     for i, chunk in enumerate(chunks):
#         res = openai.ChatCompletion.create(
#             model = "gpt-3.5-turbo-16k",
#             messages = [
#                 {"role": "system", "content":   f"""
#                                                 In this AI prompt, you are an AI with medical expertise.
#                                                 You are provided with a transcript from a YouTube video.
#                                                 Your task is to follow the user's instructions regarding
#                                                 what to do with the given transcript: {prompt_wish}
#                                                 """},

#                 {"role": "system", "content": f"""You are iterating over chunks of one entire youtube video transcript,
#                                                   you are interpreting chunk {i+1} out of {len(chunks)} chunks of the entire video.
#                                                   The next message contains the chunk content. Your job is to extract things for the wish of {prompt_wish}."""},

#                 {"role": "system", "content": chunk}
#             ] + conversation.history
#         )
#         response = res['choices'][0]['message']['content']
#         conversation.history.append({'role': 'assistant', 'content': response})
#         summary_responses.append(response)
#         conversation.save()
#         print(f"RESPONSE {i+1}: {response}")

#     for i, summary in enumerate(summary_responses):
#         conversation.history.append({"role": "system", "content": f"Info {i+1}: {summary}"})

#     res2 = openai.ChatCompletion.create(
#         model = "gpt-3.5-turbo-16k",
#         messages = [
#             {"role": "system", "content": f"""Now format the response to be easy to read and understand
#                                               and remember to use your entire memory of the youtube transcript when formulating your response."""},
#         ] + conversation.history  
#     )
#     final_response = res2['choices'][0]['message']['content']
#     print(f"FINAL RESPONSE: {final_response}")

#     return final_response


# from googleapiclient.discovery import build
# from youtube_transcript_api import YouTubeTranscriptApi
# from urllib.parse import urlparse, parse_qs
# from dotenv import load_dotenv
# import json, os, openai

# load_dotenv()

# personal_prompt = """
#                   You a knowledgable doctor. You are given the transcript 
#                   of a youtube video and must make a list of the different brain nutrients 
#                   that are mentioned in the video. You are given the entire transcript in chunks 
#                   and must generate a list of every single brain nutrient listed in the video transcript.
#                   """

# def get_personalised_transcript(request):

#     data = json.loads(request.body.decode('utf-8'))
#     url = data.get('url')

#     # Extract video Id from url
#     query = urlparse(url)
#     video_id = parse_qs(query.query).get('v')[0]

#     # Initialize the Youtube API
#     api_service_name = "youtube"
#     api_version = "v3"
#     DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")
#     youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

#     # Get the English captions
#     caption_request = youtube.captions().list(
#         part="snippet", 
#         videoId=video_id 
#     )
#     response = caption_request.execute()
#     english_captions = [item['id'] for item in response['items'] if item['snippet']['language'] == 'en-US']

#     # Get the transcript for the video
#     transcript = YouTubeTranscriptApi.get_transcript(video_id)

#     # Extract the sentences from the transcript
#     sentences = [entry['text'] for entry in transcript]

#     # Split the sentences into chunks of approximately {insight_num000 tokens each
#     chunks = []
#     chunk = []
#     chunk_size = 0
#     # For each sentence in the transcript
#     for text in sentences:
#         # If the chunk size is less than or equal the maximum chunk size, append it to chunk list
#         if chunk_size + len(text.split()) <= 3000:
#             chunk.append(text)
#             chunk_size += len(text.split()) # Update the chunk size
#         else:
#             # If the chunk size is greater than the maximum chunk size, append the chunks to the chunks list
#             chunks.append(" ".join(chunk))
#             chunk = [text]
#             chunk_size = len(text.split())
#         print(f"CHUNK: {chunk}")
#         print(f"CHUNK SIZE: {chunk_size}")
#     if chunk:  # For the last chunk
#         chunks.append(" ".join(chunk))

#     responses = []
#     for i, chunk in enumerate(chunks):
#         res = openai.ChatCompletion.create(
#             model = "gpt-4",
#             messages = [
#                 {"role": "system", "content": personal_prompt},
#                 {"role": "system", "content": f"""You are iterating over chunks of one entire youtube video transcript,
#                                                   you are interpreting chunk {i+1} out of {len(chunks)} chunks of the entire video.
#                                                   The next message contains the chunk content."""},
#                 {"role": "system", "content": chunk}
#             ]
#         )
#         response = res['choices'][0]['message']['content']
#         responses.append(response)
    
#     res2 = openai.ChatCompletion.create(
#         model = "gpt-4",
#         messages = [
#             {"role": "system", "content": """You are now generating a list of all the brain nutrients you are 
#                                              found in the last response where you iterate of the chunks of the video transcript."""},
#         ]   
#     )
#     response2 = res2['choices'][0]['message']['content']

#     final_response = response2

#     return final_response

# Path: django-api\response\response_handlers\personal_response.py
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import json, os, openai

load_dotenv()

personal_prompt = """
                  You are ChatGPT, an AI developed by OpenAI. You are given the transcript 
                  of a youtube video and must make a list of the different brain nutrients 
                  that are mentioned in the video.
                  """

def get_personalised_transcript(request):

    data = json.loads(request.body.decode('utf-8'))
    url = data.get('url')

    # Extract video Id from url
    query = urlparse(url)
    video_id = parse_qs(query.query).get('v')[0]

    # Initialize the Youtube API
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")
    youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # Get the English captions
    caption_request = youtube.captions().list(
        part="snippet", 
        videoId=video_id 
    )
    response = caption_request.execute()
    english_captions = [item['id'] for item in response['items'] if item['snippet']['language'] == 'en-US']

    # Get the transcript for the video
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Extract the sentences from the transcript
    sentences = [entry['text'] for entry in transcript]

    # Split the sentences into chunks of approximately {insight_num000 tokens each
    chunks = []
    chunk = []
    chunk_size = 0
    # For each sentence in the transcript
    for text in sentences:
        # If the chunk size is less than or equal the maximum chunk size, append it to chunk list
        if chunk_size + len(text.split()) <= 10000:
            chunk.append(text)
            chunk_size += len(text.split()) # Update the chunk size
        else:
            # If the chunk size is greater than the maximum chunk size, append the chunks to the chunks list
            chunks.append(" ".join(chunk))
            chunk = [text]
            chunk_size = len(text.split())
        print(f"CHUNK: {chunk}")
        print(f"CHUNK SIZE: {chunk_size}")
    if chunk:  # For the last chunk
        chunks.append(" ".join(chunk))

    responses = []
    for i, chunk in enumerate(chunks):
        res = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-16k",
            messages = [
                {"role": "system", "content": personal_prompt},
                {"role": "system", "content": f"You are now interpreting chunk {i+1} out of {len(chunks)}. The next message contains the chunk content."},
                {"role": "system", "content": chunk}
            ]
        )
        response = res['choices'][0]['message']['content']
        responses.append(response)
    final_response = "<br><br>".join(responses)

    return final_response