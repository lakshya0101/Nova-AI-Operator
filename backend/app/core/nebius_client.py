"""NVIDIA Nemotron & Nebius Token Factory LLM Provider Client for NOVA.

Provides an OpenAI-compatible interface to Nebius Token Factory for NVIDIA Nemotron models.
Includes model routing, structured output decoding, tool-calling support, retry logic,
neural embeddings, latency and token usage recording, and a realistic fallback mode for offline/test environments.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, List, Optional, Union
import httpx
from pydantic import BaseModel, Field

from ..config import get_settings

logger = logging.getLogger("nova.nebius")


class ModelUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0


class LLMResponse(BaseModel):
    content: str
    model: str
    usage: ModelUsage = Field(default_factory=ModelUsage)
    tool_calls: Optional[List[Dict[str, Any]]] = None
    structured_data: Optional[Dict[str, Any]] = None
    finish_reason: str = "stop"


class NebiusClient:
    """Client for Nebius Token Factory running NVIDIA Nemotron models."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ):
        settings = get_settings()
        self.api_key = api_key or settings.nebius_api_key
        self.base_url = (base_url or settings.nebius_base_url).rstrip("/")
        self.timeout = timeout or settings.llm_timeout_seconds
        self.max_retries = max_retries or settings.llm_max_retries
        self.lightning_model = settings.nebius_model_lightning
        self.super_model = settings.nebius_model_super
        self.embedding_model = "BAAI/bge-en-icl"
        self.mock_if_no_key = settings.mock_llm_if_no_key

    @property
    def is_live(self) -> bool:
        """Returns True if a real Nebius API key is configured."""
        return bool(self.api_key and self.api_key.strip() and not self.api_key.startswith("mock-"))

    def select_model(self, tier: str = "lightning") -> str:
        """Route to appropriate NVIDIA Nemotron model based on required capability."""
        if tier == "super":
            return self.super_model
        return self.lightning_model

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        tier: str = "lightning",
        temperature: float = 0.2,
        max_tokens: int = 2048,
        tools: Optional[List[Dict[str, Any]]] = None,
        response_format: Optional[Dict[str, str]] = None,
    ) -> LLMResponse:
        """Execute chat completion using Nebius Token Factory or intelligent simulation."""
        target_model = model or self.select_model(tier)
        start_time = time.perf_counter()

        if not self.is_live:
            if self.mock_if_no_key:
                logger.info("Executing simulated NVIDIA Nemotron response (model=%s, tier=%s)", target_model, tier)
                return self._simulate_response(messages, target_model, start_time, tools)
            raise ValueError(
                "NEBIUS_API_KEY is not configured and offline fallback is disabled. "
                "Please configure NEBIUS_API_KEY in your environment."
            )

        endpoint = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: Dict[str, Any] = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            payload["tools"] = tools
        if response_format:
            payload["response_format"] = response_format

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.post(endpoint, json=payload, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        latency_ms = (time.perf_counter() - start_time) * 1000
                        choice = data["choices"][0]
                        msg = choice.get("message", {})
                        content = msg.get("content") or ""
                        tool_calls = msg.get("tool_calls")
                        raw_usage = data.get("usage", {})
                        usage = ModelUsage(
                            prompt_tokens=raw_usage.get("prompt_tokens", 0),
                            completion_tokens=raw_usage.get("completion_tokens", 0),
                            total_tokens=raw_usage.get("total_tokens", 0),
                            latency_ms=round(latency_ms, 2),
                        )

                        # Try to parse structured data if expected or contained within markdown code blocks
                        structured = None
                        if response_format and response_format.get("type") == "json_object":
                            try:
                                structured = json.loads(content)
                            except Exception:
                                pass
                        if structured is None and ("{" in content and "}" in content):
                            try:
                                # Extract JSON from markdown if wrapped in ```json ... ```
                                start_idx = content.find("{")
                                end_idx = content.rfind("}")
                                if start_idx != -1 and end_idx != -1:
                                    structured = json.loads(content[start_idx : end_idx + 1])
                            except Exception:
                                pass

                        return LLMResponse(
                            content=content,
                            model=target_model,
                            usage=usage,
                            tool_calls=tool_calls,
                            structured_data=structured,
                            finish_reason=choice.get("finish_reason", "stop"),
                        )
                    elif resp.status_code in (429, 500, 502, 503, 504):
                        logger.warning(
                            "Nebius API attempt %d returned HTTP %d: %s. Retrying...",
                            attempt, resp.status_code, resp.text
                        )
                        last_error = f"HTTP {resp.status_code}: {resp.text}"
                    else:
                        raise RuntimeError(f"Nebius API failed with HTTP {resp.status_code}: {resp.text}")
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                logger.warning("Nebius network/timeout on attempt %d: %s", attempt, exc)
                last_error = str(exc)

            time.sleep(0.5 * (2 ** (attempt - 1)))

        raise RuntimeError(f"Nebius API request failed after {self.max_retries} attempts: {last_error}")

    async def create_embeddings(
        self,
        texts: List[str],
        model: Optional[str] = None,
    ) -> List[List[float]]:
        """Generate neural embeddings via Nebius Token Factory /v1/embeddings endpoint."""
        target_model = model or self.embedding_model

        if not self.is_live:
            # Fallback to local deterministic normalized embedding
            from ..services.memory_service import compute_embedding
            return [compute_embedding(t) for t in texts]

        endpoint = f"{self.base_url}/embeddings"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": target_model,
            "input": texts,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(endpoint, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                return [item["embedding"] for item in data["data"]]
            logger.warning("Nebius embeddings failed with HTTP %d: %s. Using local embeddings.", resp.status_code, resp.text)
            from ..services.memory_service import compute_embedding
            return [compute_embedding(t) for t in texts]

    def _simulate_response(
        self,
        messages: List[Dict[str, str]],
        model: str,
        start_time: float,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> LLMResponse:
        """Intelligent simulator for NVIDIA Nemotron when running locally without active API tokens."""
        last_message = messages[-1]["content"] if messages else ""
        system_prompt = next((m["content"] for m in messages if m.get("role") == "system"), "")
        latency_ms = (time.perf_counter() - start_time) * 1000 + 12.5

        # If system prompt asks for planner JSON
        if "planner" in system_prompt.lower() or "plan" in system_prompt.lower():
            is_evening = "evening" in last_message.lower() or "interview" in last_message.lower()
            if is_evening:
                plan_obj = {
                    "goal": last_message,
                    "strategy": "Deconstruct evening organization into task retrieval, priority scheduling, web research, and action generation.",
                    "subtasks": [
                        {
                            "step_id": 1,
                            "agent": "execution",
                            "action": "get_tasks",
                            "description": "Retrieve existing tasks",
                            "requires_approval": False,
                        },
                        {
                            "step_id": 2,
                            "agent": "planner",
                            "action": "get_tasks",
                            "description": "Propose ordered task list",
                            "requires_approval": False,
                        },
                        {
                            "step_id": 3,
                            "agent": "execution",
                            "action": "create_task",
                            "description": "Create interview preparation task",
                            "requires_approval": True,
                        },
                    ],
                }
            else:
                plan_obj = {
                    "goal": last_message,
                    "strategy": "Deconstruct goal into tasks, context retrieval, and state mutations.",
                    "subtasks": [
                        {
                            "step_id": 1,
                            "agent": "execution",
                            "action": "get_tasks",
                            "description": "Retrieve active tasks from storage",
                            "requires_approval": False,
                        },
                        {
                            "step_id": 2,
                            "agent": "execution",
                            "action": "create_task",
                            "description": f"Register action item for '{last_message[:35]}'",
                            "requires_approval": True,
                        },
                    ],
                }
            content = json.dumps(plan_obj)
            return LLMResponse(
                content=content,
                model=model,
                usage=ModelUsage(prompt_tokens=180, completion_tokens=140, total_tokens=320, latency_ms=latency_ms),
                structured_data=plan_obj,
            )

        # Critic simulator
        if "critic" in system_prompt.lower():
            critic_obj = {
                "status": "approved",
                "critique": "Plan is logically sound, observes human approval constraints for state mutations, and addresses all facets of the prompt.",
                "confidence_score": 0.98,
                "recommendations": ["Execute read-only steps first, then await user approval for task creation."],
            }
            return LLMResponse(
                content=json.dumps(critic_obj),
                model=model,
                usage=ModelUsage(prompt_tokens=120, completion_tokens=70, total_tokens=190, latency_ms=latency_ms),
                structured_data=critic_obj,
            )

        # Reflection simulator
        if "reflection" in system_prompt.lower():
            reflection_obj = {
                "summary": "Workflow completed with verified execution steps and security checkpoints.",
                "insights": "User goals successfully planned and executed with human confirmation where required.",
                "memory_updates": [
                    {
                        "category": "workflow",
                        "content": f"Completed execution for instruction: '{last_message[:80]}'",
                    }
                ],
            }
            return LLMResponse(
                content=json.dumps(reflection_obj),
                model=model,
                usage=ModelUsage(prompt_tokens=150, completion_tokens=85, total_tokens=235, latency_ms=latency_ms),
                structured_data=reflection_obj,
            )

        # Generic Nemotron response
        content = f"NOVA Nemotron Operator processed input: {last_message[:100]}."
        return LLMResponse(
            content=content,
            model=model,
            usage=ModelUsage(prompt_tokens=50, completion_tokens=30, total_tokens=80, latency_ms=latency_ms),
        )


# Global singleton instance
_nebius_client: Optional[NebiusClient] = None


def get_nebius_client() -> NebiusClient:
    """Return configured NebiusClient instance."""
    global _nebius_client
    if _nebius_client is None:
        _nebius_client = NebiusClient()
    return _nebius_client
