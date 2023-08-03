# Path: django-api\response\response_handlers\personal_response.py
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from django.core.mail import send_mail
from accounts.models import  UserProfile
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import json, os, openai, time

load_dotenv()

def get_personalised_transcript(request):

    # Get the url from the request body, request body is the 
    data = json.loads(request.body.decode('utf-8'))
    url = data.get('url')
    user_prompt = data.get('prompt')
    

    # Get the user profile and goal
    user_profile = UserProfile.objects.get(user=request.user)
    user_goal = user_profile.goal 
    print(f"USER GOAL: {user_goal}")

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

    start_time = time.time()
    # Get the transcript for the video
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Extract the sentences from the transcript
    sentences = [entry['text'] for entry in transcript]

    chunks = []
    chunk = []
    chunk_size = 0
    # For each sentence in the transcript
    for text in sentences:
        # If the chunk size is less than or equal the maximum chunk size, append it to chunk list
        if chunk_size + len(text.split()) <= 3000:
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

    summary = []
    for i, chunk in enumerate(chunks):
        res = openai.ChatCompletion.create(
            model = "gpt-4",
            messages = [
                {"role": "system", "content": f"Start of loop {i+1}"},
                {"role": "system", "content": f"""
                                                You are an AI personal doctor who has been asked to extract specific information from a YouTube video transcript.
                                                The transcript has been divided into multiple chunks, and you must process each chunk individually. 
                                                Your task is to follow these steps:
                                                - Review each chunk of the transcript and identify every piece of information that aligns with the given user prompt.
                                                - After processing all chunks, summarize all the relevant pieces of information you have found in a single response.
                                                - User's goal: {user_goal}

                                                Your guiding rule, as defined by the user, is: {user_prompt}
                                            """},
                {"role": "system", "content": f"""You are iterating over each chunk of single entire youtube video transcript,
                                                  you are interpreting chunk {i+1} out of {len(chunks)} chunks of the entire video
                                                  You must give notes about this chunk in regard to the users prompt: ({user_prompt}).
                                                  The next message contains the chunk content."""},
                {"role": "system", "content": f"CHUNK {i+1}: {chunk}"},
                {"role": "system", "content": f"End of loop {i+1}"},
            ]
        )
        response = res['choices'][0]['message']['content']
        summary.append(response)
        # Join the summaries with a newline separator
        summary_text = "\n".join(summary)
    
    res2 = openai.ChatCompletion.create(
        model = "gpt-4",
        messages = [
            {"role": "system", "content": f"""Your task is now to summarize all the relevant pieces
                                              of information you have found in a single response.
             
                                              Listed summary information: {summary_text}
                                              Users prompt: {user_prompt}"""},
        ]   
    )

    print(f"TIME TAKEN TO GENERATE RESPONSE: {time.time() - start_time} seconds")
    final_response = res2['choices'][0]['message']['content']
    print(f"FINAL RESPONSE: {final_response}")
    return final_response