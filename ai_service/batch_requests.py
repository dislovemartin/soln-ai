
import asyncio
import httpx
from typing import List, Dict
from fastapi import HTTPException

async def fetch_url(client: httpx.AsyncClient, url: str) -> Dict:
    """
    Fetches a single URL using an asynchronous HTTP client.
    
    Arguments:
    client: httpx.AsyncClient -- The async HTTP client.
    url: str -- The URL to fetch.
    
    Returns:
    Dict -- The JSON response from the service.
    """
    try:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Error connecting to external service: {exc}")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"Error response from service: {exc.response.text}")

async def batch_requests(urls: List[str]) -> List[Dict]:
    """
    Fetches multiple URLs asynchronously in a batch.
    
    Arguments:
    urls: List[str] -- A list of URLs to fetch.
    
    Returns:
    List[Dict] -- A list of JSON responses from the services.
    """
    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(client, url) for url in urls]
        return await asyncio.gather(*tasks)

# Example usage in your API
@app.get("/batch-vr-ar-object-detection")
async def batch_vr_ar_object_detection() -> List[Dict]:
    """
    Calls multiple VR/AR object detection services in a batch.
    
    Returns:
    List[Dict] -- The JSON responses from the services.
    """
    urls = ["http://vr-ar-service1/object-detection", "http://vr-ar-service2/object-detection"]
    return await batch_requests(urls)
