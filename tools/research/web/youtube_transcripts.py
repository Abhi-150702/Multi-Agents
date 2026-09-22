import json
import re

from langchain.tools import tool
from youtube_transcript_api import YouTubeTranscriptApi
from config.logging_config import setup_logger, log_tool_call, log_tool_output, log_tool_error

logger = setup_logger("youtube_transcript")


def extract_video_id(url : str) -> str | None:
    """
    Extract YouTube video ID from common YouTube URL formats.
    """

    patterns = [
        r"(?:youtube\.com/watch\?v=)([^&]+)",
        r"(?:youtu\.be/)([^?&]+)",
        r"(?:youtube\.com/embed/)([^?&]+)",
        r"(?:youtube\.com/shorts/)([^?&]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)


    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url
    return None


@tool
def youtube_transcript(video_url: str, max_characters: int = 5000) -> str:
    """
    Retrieve the transcript of a YouTube video.

    Use this tool when:
    - a YouTube video contains information relevant to the research
    - the user wants the content of a video summarized
    - the user asks about what was said in a YouTube video
    - deeper research is required after youtube_search

    Provide either a YouTube URL or an 11-character YouTube video ID.

    This tool uses publicly available YouTube transcript data and
    does not require a paid API.
    """
    try:
        log_tool_call(logger, "youtube_transcript", video_url=video_url, max_characters=max_characters)

        video_id = extract_video_id(url=video_url)
        if not video_id:
            error_result = json.dumps({
                "error" : "Could not extract Youtube video ID"
            })
            log_tool_output(logger, "youtube_transcript", error_result, success=False)
            return error_result

        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        segments = []

        for item in transcript:
            segments.append(
                {
                    'start': item.start,
                    'duration' : item.duration,
                    'text' : item.text
                }
            )

        full_text = " ".join(item['text'] for item in segments)

        result = json.dumps(
            {
                "video_id" : video_id,
                "transcript" : full_text,
                "segments" : segments[:500]
            },
            indent=4,
            ensure_ascii=False
        )

        log_tool_output(logger, "youtube_transcript", result, success=True)
        return result

    except Exception as exc:
        log_tool_error(logger, "youtube_transcript", exc)
        error_result = json.dumps({
            "error" : f"Transcript extraction failed: {str(exc)}"
        })
        log_tool_output(logger, "youtube_transcript", error_result, success=False)
        return error_result
