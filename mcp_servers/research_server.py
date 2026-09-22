import sys
from pathlib import Path

# Add parent directory to Python path to import config module
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import json
import requests
import re
import yt_dlp

from fastmcp import FastMCP
from ddgs import DDGS
from bs4 import BeautifulSoup

from youtube_transcript_api import YouTubeTranscriptApi

from langchain_google_community.search import GoogleSearchAPIWrapper
from langchain_community.utilities import ArxivAPIWrapper

from config.settings import Settings
from config.logging_config import setup_logger, log_tool_error, log_tool_output, log_tool_call

logger = setup_logger("Retriever MCP Tools")


mcp = FastMCP("Research Server")

search = GoogleSearchAPIWrapper(
    k=5,
    google_api_key=Settings().google_api_key,
    google_cse_id=Settings().google_cse_id
)

################################################################################################################
#                                                       Web                                                    #
################################################################################################################

@mcp.tool
def duckduckgo_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo.

    Use this tool when you need current information from the internet.
    """
    try:
        results = DDGS().text(
            query,
            max_results=max_results
        )

        if not results:
            return "No search results found."

        formatted_results = []

        for result in results:
            formatted_results.append(
                f"Title: {result.get('title', '')}\n"
                f"URL: {result.get('href', '')}\n"
                f"Snippet: {result.get('body', '')}"
            )

        return "\n\n---\n\n".join(formatted_results)

    except Exception as e:
        return f"Error performing DuckDuckGo search: {str(e)}"


@mcp.tool
def google_search(query: str, num_results: int = 5) -> str:
    """
    Search Google for web results.
    Useful for broad web research and finding official documentation.
    """
    try:
        log_tool_call(logger, "google_search", query=query)

        search = GoogleSearchAPIWrapper(
            k=5,
            google_api_key=Settings().google_api_key,
            google_cse_id=Settings().google_cse_id
        )
        results = search.results(query=query, num_results=num_results)

        formatted_results = []
        for result in results:
            formatted_results.append(
                f"""
Title: {result.get('title', '')}
URL: {result.get("link", '')}
Snippet: {result.get('snippet', '')}
"""
            )

        final_result = "--".join(formatted_results)
        log_tool_output(logger, "google_search", final_result, success=True)
        return final_result

    except Exception as e:
        log_tool_error(logger, "google_search", e)
        error_msg = f"Error performing Google search: {str(e)}"
        log_tool_output(logger, "google_search", error_msg, success=False)
        return error_msg


@mcp.tool
def read_webpage(
    url: str,
    max_characters: int = 5000
) -> str:
    """
    Read and extract textual content from a public webpage.

    Use this tool when:
    - a search result contains a useful URL
    - deeper information is needed from a webpage
    - the search result snippet is insufficient
    - an academic paper HTML page needs to be inspected
    - documentation or technical articles need to be read

    Input must be a complete HTTP or HTTPS URL.

    This tool retrieves publicly accessible webpages and does not
    require a paid API.
    """

    try:
        log_tool_call(logger, "read_webpage", url=url, max_characters=max_characters)

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/140 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=120,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove non-content elements
        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "noscript",
            "svg",
        ]):
            element.decompose()

        # Try to focus on the main content
        main = soup.find("main")

        if main:
            text = main.get_text(
                separator="\n",
                strip=True
            )
        else:
            text = soup.get_text(
                separator="\n",
                strip=True
            )

        # Remove excessive blank lines
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        text = "\n".join(lines)

        result = json.dumps({
            "url": url,
            "content": text[:max_characters],
        }, indent=2, ensure_ascii=False)

        log_tool_output(logger, "read_webpage", result, success=True)
        return result

    except requests.RequestException as exc:
        log_tool_error(logger, "read_webpage", exc)
        error_result = json.dumps({
            "url": url,
            "error": f"Failed to retrieve webpage: {str(exc)}"
        })
        log_tool_output(logger, "read_webpage", error_result, success=False)
        return error_result

    except Exception as exc:
        log_tool_error(logger, "read_webpage", exc)
        error_result = json.dumps({
            "url": url,
            "error": f"Webpage extraction failed: {str(exc)}"
        })
        log_tool_output(logger, "read_webpage", error_result, success=False)
        return error_result


@mcp.tool
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


@mcp.tool
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


################################################################################################################
#                                                    Academic                                                  #
################################################################################################################

@mcp.tool
def arxiv_search(query: str, top_k_results: int = 5, load_max_docs: int = 5) -> str:
    """
    Search academic papers on arXiv.

    Use this tool when:
    - the user asks about research papers or when the google search of duckduckgo search is not enough
    - the user asks about algorithms or academic methods
    - the user asks for recent scientific research
    - evidence from academic literature is useful

    Do not use this tool for general web searches.
    """

    try:
        log_tool_call(logger, "arxiv_search", query=query)
        arxiv = ArxivAPIWrapper(top_k_results=top_k_results, load_max_docs=load_max_docs)

        result = arxiv.run(query)
        log_tool_output(logger, "arxiv_search", result, success=True)
        return result
    except Exception as e:
        log_tool_error(logger, "arxiv_search", e)
        error_msg = f"Error searching arXiv: {str(e)}"
        log_tool_output(logger, "arxiv_search", error_msg, success=False)
        return error_msg

if __name__ == "__main__":
    mcp.run()