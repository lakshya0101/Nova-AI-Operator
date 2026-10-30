"""Verification script for Tavily Web Search live integration.

Usage:
    python scripts/verify_tavily_live.py
"""

import os
import sys
import asyncio
import httpx

# Ensure repo root is on sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
BACKEND_DIR = os.path.join(REPO_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.config import get_settings
from app.services.tavily_service import execute_tavily_research
from app.schemas.research import ResearchRequest


async def main():
    print("=" * 65)
    print("NOVA 2.0: TAVILY WEB SEARCH LIVE INTEGRATION AUDIT")
    print("=" * 65)

    settings = get_settings()
    api_key = settings.tavily_api_key or os.getenv("TAVILY_API_KEY")

    if not api_key or not api_key.strip() or api_key.startswith("mock-"):
        print("\n[STATUS: UNVERIFIED - CREDENTIALS MISSING]")
        print("  TAVILY_API_KEY is not configured in the host environment or .env.")
        print("  Live web search queries cannot be dispatched to Tavily.")
        print("  NOVA will use high-fidelity simulated intelligence until an API key is provided.")
        print("\nTo verify live web search:")
        print("  1. Export your Tavily API Key:")
        print("     $env:TAVILY_API_KEY='your_tavily_api_key'")
        print("  2. Re-run this script: python scripts/verify_tavily_live.py")
        sys.exit(0)

    print("\n[Step 1] Dispatching live search query to Tavily API...")
    req = ResearchRequest(
        query="NVIDIA Nemotron AI agent developments 2026",
        max_results=3,
        search_depth="basic",
    )
    try:
        res = await execute_tavily_research(req)
        print(f"       SUCCESS: Received response! (Live Tavily={res.is_live_tavily})")
        print(f"       Answer:  {res.answer[:120]}...")
        print(f"       Sources: {len(res.sources)} references retrieved:")
        for s in res.sources:
            print(f"        - {s.title} ({s.url})")
    except Exception as exc:
        print(f"       ERROR: Tavily live request failed: {exc}")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    asyncio.run(main())

