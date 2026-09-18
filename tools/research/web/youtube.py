from langchain.tools import tool

import json
import yt_dlp
from config.logging_config import setup_logger, log_tool_call, log_tool_output, log_tool_error

logger = setup_logger("youtube_search")


@tool
def youtube_search(query: str, max_results: int = 5) -> str:
    """
    Search YouTube for videos related to a research query.

    Use this tool when:
    - the user wants YouTube videos
    - tutorials or video explanations are useful
    - technical talks or conference videos are relevant
    - demonstrations or lectures may contain useful information

    This tool performs a free YouTube search and does not require
    a YouTube API key.

    Returns video title, URL, channel, duration and view count.
    """

    try:
        log_tool_call(logger, "youtube_search", query=query, max_results=max_results)

        search_query = f"ytsearch{max_results}:{query}"

        ydl_opts = {
            'quiet' : True,
            'no_warnings' : True,
            'extract_flat' : True,
            'skip_download' : True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                search_query,
                download=False
            )

        videos = []

        for entry in  result.get('entires', []):
            if not entry:
                continue

            video_id = entry.get('id')

            videos.append(
                {
                    'title' : entry.get('title'),
                    'url' : f"https://www.youtube.com/watch?v={video_id}" if video_id else None,
                    'channel' : entry.get('channel') or entry.get('uploader'),
                    'duration' : entry.get('duration'),
                    'view_count' : entry.get('view_count')
                }
            )

        final_result = json.dumps(
            videos,
            indent=4,
            ensure_ascii=False
        )

        log_tool_output(logger, "youtube_search", final_result, success=True)
        return final_result

    except Exception as exc:
        log_tool_error(logger, "youtube_search", exc)
        error_result = json.dumps(
            {"errors" : f"Youtube search failed: {str(exc)}"}
        )
        log_tool_output(logger, "youtube_search", error_result, success=False)
        return error_result