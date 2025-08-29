#!/usr/bin/env python3
"""
Startup script for Render deployment.
This ensures the FastAPI app binds correctly to 0.0.0.0.
"""
import os
import sys
import uvicorn
from main import app

def main():
    """Start the server with explicit configuration."""
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"=== Render Deployment Startup ===")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Environment PORT: {os.environ.get('PORT', 'Not set')}")
    print(f"Python version: {sys.version}")
    print("===================================")
    
    # Start the server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True,
        workers=1
    )

if __name__ == "__main__":
    main()
