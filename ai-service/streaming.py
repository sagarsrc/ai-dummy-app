from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import anthropic

async def stream_response(prompt: str):
    """Stream LLM responses using SSE"""
    client = anthropic.Anthropic()

    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield f"data: {text}\n\n"
