"""
Test script to demonstrate the logging functionality for all research tools.

This script tests each tool individually to show how logging works.
Run this to verify that all tools are properly logging their calls and outputs.
"""

from tools.research.web.duckduckgo_search import duckduckgo_search
from tools.research.web.google_search import google_search
from tools.research.web.webpage import read_webpage
from tools.research.web.youtube import youtube_search
from tools.research.web.youtube_transcripts import youtube_transcript
from tools.research.code.github import github_search
from tools.research.academic.arxiv import arxiv_search


def test_all_tools():
    """Test all tools to demonstrate logging functionality."""
    
    print("\n" + "="*70)
    print("TESTING RESEARCH TOOLS WITH LOGGING")
    print("="*70 + "\n")
    
    print("Check the logs/ directory for detailed log files!")
    print("Console output shows INFO level, files contain DEBUG level.\n")
    
    # Test 1: DuckDuckGo Search
    print("\n[TEST 1] Testing DuckDuckGo Search...")
    try:
        result = duckduckgo_search.invoke({"query": "Python programming tutorial"})
        print(f"✓ DuckDuckGo search completed")
    except Exception as e:
        print(f"✗ DuckDuckGo search failed: {e}")
    
    # Test 2: Google Search (may fail if API keys not configured)
    print("\n[TEST 2] Testing Google Search...")
    try:
        result = google_search.invoke({"query": "machine learning basics"})
        print(f"✓ Google search completed")
    except Exception as e:
        print(f"✗ Google search failed (API key may be missing): {e}")
    
    # Test 3: Web Page Reading
    print("\n[TEST 3] Testing Webpage Reading...")
    try:
        result = read_webpage.invoke({
            "url": "https://www.python.org",
            "max_characters": 500
        })
        print(f"✓ Webpage reading completed")
    except Exception as e:
        print(f"✗ Webpage reading failed: {e}")
    
    # Test 4: GitHub Search
    print("\n[TEST 4] Testing GitHub Search...")
    try:
        result = github_search.invoke({
            "query": "python web scraping",
            "max_results": 3
        })
        print(f"✓ GitHub search completed")
    except Exception as e:
        print(f"✗ GitHub search failed: {e}")
    
    # Test 5: arXiv Search
    print("\n[TEST 5] Testing arXiv Search...")
    try:
        result = arxiv_search.invoke({"query": "neural networks"})
        print(f"✓ arXiv search completed")
    except Exception as e:
        print(f"✗ arXiv search failed: {e}")
    
    # Test 6: YouTube Search
    print("\n[TEST 6] Testing YouTube Search...")
    try:
        result = youtube_search.invoke({
            "query": "python tutorial for beginners",
            "max_results": 3
        })
        print(f"✓ YouTube search completed")
    except Exception as e:
        print(f"✗ YouTube search failed: {e}")
    
    # Test 7: YouTube Transcript (will likely fail without valid video)
    print("\n[TEST 7] Testing YouTube Transcript...")
    try:
        result = youtube_transcript.invoke({
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "max_characters": 500
        })
        print(f"✓ YouTube transcript completed")
    except Exception as e:
        print(f"✗ YouTube transcript failed (expected if video unavailable): {e}")
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print("="*70)
    print("\nAll tool calls and outputs have been logged!")
    print("Check the logs/ directory for the complete log file.")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_all_tools()
