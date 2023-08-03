from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from django.core.mail import send_mail
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
    insight_count = data.get('insight_count')

    if insight_count == None: # If not insight number is specified, default to 5
        insight_count = 5

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

    # Split the sentences into chunks of approximately {insight_count000 tokens each
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

    # Start the timer
    start_time1 = time.time()
    # Get the AI's interpretations of the chunks
    summary = []
    for i, chunk in enumerate(chunks):
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": """You are a very knowledgeable doctor. You have been tasked with interpreting 
                                                 and summarizing a YouTube video and extracting summarized insights from each chunk  it."""},

                {"role": "system", "content": f"""You are iterating over chunks of one entire youtube video transcript,
                                                  you are interpreting chunk {i+1} out of {len(chunks)} chunks of the entire video.
                                                  The next message contains the chunk content."""},

                {"role": "system", "content": f"Chunk {i+1}: {chunk}"}
            ]
        )
        response = res['choices'][0]['message']['content']
        summary.append(response)
        # Join the summaries with a newline separator
        summary_text = "\n".join(summary)
        conversation.history.append({'role': 'assistant', 'content': response})
    print(f"TIME TAKEN FOR VIDEO TRANSCRIPT GENERATION: {time.time() - start_time1}") # End the timer

    # Start the second timer
    start_time2 = time.time()
    final_res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"""
                You are ChatGPT, an AI developed by OpenAI. You are given many insights and must generate a list of {insight_count} insights. 

                Please format your output as follows:

                <b>{insight_count} Insights for achieving your personal goal of: {user_goal}:</b>
                [ 
                - Insight 1 
                ...
                ]

                Be sure to generate exactly {insight_count} insights that are relevant to the video content. After you finish listing the {insight_count} insights, do not generate any more text. STOP AFTER THE LIST.
                """
            },
            {"role": "system", "content": summary_text}
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


