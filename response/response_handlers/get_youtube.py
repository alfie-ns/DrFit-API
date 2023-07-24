from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from accounts.models import UserProfile
from response.models import Conversation
from dotenv import load_dotenv
import os, openai, json, time

# OpenAI API configuation
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
model="gpt-4"

def get_youtube(request):
    print("ENTERED GET_YOUTUBE FUNCTION")

    # Parse JSON data from the request body
    data = json.loads(request.body.decode('utf-8'))
    url = data.get('url')
    insight_num = data.get('insight_num')

    if insight_num == None: # If not insight number is specified, default to 5
        insight_num = 5

    # Extract video ID from URL
    query = urlparse(url)
    video_id = parse_qs(query.query).get('v')[0]

    # Initialize the YouTube API service
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

    # Get the user profile and goal
    user_profile = UserProfile.objects.get(user=request.user)
    user_goal = user_profile.goal 
    print(f"USER GOAL: {user_goal}")

    # Initialize the conversation
    conversation, created = Conversation.objects.get_or_create(user=user_profile.user)


    transcript_prompt = f"""
    You are ChatGPT, an AI developed by OpenAI. You are given many Youtube insights and must generate a list of {insight_num} insights that are beneficial for achieving the specific personal goal of: {user_goal}. 

    Please format your output as follows:

    <b>{insight_num} Insights for achieving your personal goal of: {user_goal}:</b>
    [ 
    - Insight 1 
    ...
    ]

    Be sure to generate exactly {insight_num} insights that are relevant to the video content. After you finish listing the {insight_num} insights, do not generate any more text. STOP AFTER THE LIST.
    """

    # Start the timer
    start_time1 = time.time()
    # Get the AI's interpretations of the chunks
    responses = []
    for i, chunk in enumerate(chunks):
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are ChatGPT, an AI developed by OpenAI. You have been tasked with interpreting a YouTube video and extracting insights from it."},
                {"role": "system", "content": f"You are now interpreting chunk {i+1} out of {len(chunks)}. The next message contains the chunk content."},
                {"role": "system", "content": chunk}
            ]
        )
        response = res['choices'][0]['message']['content']
        responses.append(response)
    responses = "<br><br>".join(responses)
    print(f"TIME TAKEN FOR VIDEO TRANSCRIPT GENERATION: {time.time() - start_time1}") # End the timer

    # Start the second timer
    start_time2 = time.time()
    final_res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": transcript_prompt},
            {"role": "system", "content": responses}
        ]
    )
    final_response = final_res['choices'][0]['message']['content']
    print(f"TIME TAKEN FOR FINAL RESPONSE GENERATION: {time.time() - start_time2}") # End the second timer
    print(f"TOTAL TIME TAKEN: {time.time() - start_time1}")
    print(f"FINAL RESPONSE: {final_response}")

    # Append the insights to the conversation history
    conversation.history.append({'role': 'assistant', 'content': final_response})
    conversation.save()

    return final_response


