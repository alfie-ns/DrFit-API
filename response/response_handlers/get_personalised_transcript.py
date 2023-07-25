# Path: django-api\response\response_handlers\personal_response.py
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import json, os, openai

load_dotenv()

personal_prompt = """
                  You a knowledgable doctor. You are given the transcript 
                  of a youtube video and must make a list of the different brain nutrients 
                  that are mentioned in the video. You are given the entire transcript in chunks 
                  and must generate a list of every single brain nutrient listed in the video transcript.
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

    responses = []
    for i, chunk in enumerate(chunks):
        res = openai.ChatCompletion.create(
            model = "gpt-4",
            messages = [
                {"role": "system", "content": personal_prompt},
                {"role": "system", "content": f"""You are iterating over chunks of one entire youtube video transcript,
                                                  you are interpreting chunk {i+1} out of {len(chunks)} chunks of the entire video.
                                                  The next message contains the chunk content."""},
                {"role": "system", "content": chunk}
            ]
        )
        response = res['choices'][0]['message']['content']
        responses.append(response)
    
    res2 = openai.ChatCompletion.create(
        model = "gpt-4",
        messages = [
            {"role": "system", "content": """You are now generating a list of all the brain nutrients you have
                                             found in the last response where you iterated of the chunks of the video transcript."""},
        ]   
    )
    final_response = res2['choices'][0]['message']['content']
    print(f"FINAL RESPONSE: {final_response}")
    return final_response