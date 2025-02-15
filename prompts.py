class Prompts:
    SYSTEM_PROMPT = """You are an assistant that will be given a meeting transcript, and you will be required to perform the following tasks:
1. Summarize the meeting
2. Extract the action items
3. Extract the meeting minutes

{format_instructions}

Here is the meeting transcript:
{transcript}
"""

    SPAM_DETECTOR_PROMPT = """You are an assistant that will be given a meeting transcript, and you will be required to determine if the transcript is spam.
A transcript is considered spam if it contains any of the following:
1. Invalid format (e.g., gibberish, random characters, no speaker identification)
2. Inappropriate content (e.g., hate speech, harassment, threats)

{format_instructions}

Here is the meeting transcript:
{transcript}
"""