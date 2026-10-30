"""Verification script for Nebius Token Factory and NVIDIA Nemotron live integration.

Usage:
    python scripts/verify_nebius_live.py
"""

import os
import sys
import time
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
from app.core.nebius_client import NebiusClient


async def main():
    print("=" * 65)
    print("NOVA 2.0: NEBIUS TOKEN FACTORY & NVIDIA NEMOTRON AUDIT")
    print("=" * 65)

    settings = get_settings()
    api_key = settings.nebius_api_key or os.getenv("NEBIUS_API_KEY")
    base_url = (settings.nebius_base_url or os.getenv("NEBIUS_BASE_URL", "https://api.studio.nebius.ai/v1")).rstrip("/")
    super_model = settings.nebius_model_super
    lightning_model = settings.nebius_model_lightning

    print(f"Base URL:            {base_url}")
    print(f"Configured Super:    {super_model}")
    print(f"Configured Lightning:{lightning_model}")

    if not api_key or not api_key.strip() or api_key.startswith("mock-"):
        print("\n[STATUS: UNVERIFIED - CREDENTIALS MISSING]")
        print("  NEBIUS_API_KEY is not configured in the host environment or .env.")
        print("  Live inference cannot be executed against Nebius Token Factory.")
        print("  NOVA will run in high-fidelity local simulation mode until an API key is provided.")
        print("\nTo verify live inference:")
        print("  1. Export your Nebius API Key:")
        print("     $env:NEBIUS_API_KEY='your_nebius_api_key'")
        print("  2. Re-run this script: python scripts/verify_nebius_live.py")
        sys.exit(0)

    print(f"\n[Step 1] Connecting to Nebius Token Factory: {base_url}/models...")
    headers = {"Authorization": f"Bearer {api_key}"}
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(f"{base_url}/models", headers=headers)
            if resp.status_code == 200:
                models_data = resp.json()
                model_ids = [m["id"] for m in models_data.get("data", [])]
                print(f"       SUCCESS: Connected! Available models ({len(model_ids)}):")
                for mid in model_ids[:10]:
                    print(f"        - {mid}")
            else:
                print(f"       WARNING: /models returned HTTP {resp.status_code}: {resp.text}")
        except Exception as exc:
            print(f"       ERROR: Failed to query /models: {exc}")

    print(f"\n[Step 2] Testing Chat Completion with {lightning_model}...")
    nebius = NebiusClient(api_key=api_key, base_url=base_url)
    try:
        t0 = time.perf_counter()
        res = await nebius.chat_completion(
            messages=[
                {"role": "system", "content": "You are the NOVA AI Operator."},
                {"role": "user", "content": "Respond with 'NOVA ONLINE' and report system status."},
            ],
            model=lightning_model,
        )
        latency = (time.perf_counter() - t0) * 1000
        print(f"       SUCCESS: Response received in {latency:.1f}ms!")
        print(f"       Model:   {res.model}")
        print(f"       Tokens:  Prompt={res.usage.prompt_tokens}, Completion={res.usage.completion_tokens}")
        print(f"       Content: {res.content[:100]}...")
    except Exception as exc:
        print(f"       ERROR: Chat completion failed: {exc}")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    asyncio.run(main())

