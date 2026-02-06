"""Store server process management utilities."""

import subprocess
import time
import atexit


# Global store process for cleanup
_store_process = None


def cleanup_store():
    """Cleanup store server on exit."""
    global _store_process
    if _store_process:
        print("\n🛑 Shutting down store server...")
        _store_process.terminate()
        try:
            _store_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _store_process.kill()
        _store_process = None


def start_store_server(store_url: str = None) -> bool:
    """Start store server in background.
    
    Args:
        store_url: Store server URL (e.g., "http://localhost:4747").
                   If None or empty, no server is started (returns True).
        
    Returns:
        bool: True if server started successfully or not needed, False on failure
    """
    import os
    global _store_process
    
    # No store URL provided - no server needed
    if not store_url:
        return True
    
    # Tell agentlightning NOT to start its own internal server wrapper
    # This avoids binding conflicts and timeout issues
    os.environ["AGL_MANAGED_STORE"] = "false"
    
    # Extract port from URL
    try:
        port = int(store_url.split(":")[-1])
    except (ValueError, IndexError):
        port = 4747
        print(f"⚠️ Could not parse port from URL '{store_url}', using default port {port}")
    
    print(f"🚀 Starting store server on port {port}...")
    _store_process = subprocess.Popen(
        ["agl", "store", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Register cleanup handler
    atexit.register(cleanup_store)
    
    # Wait for server to be ready
    print("⏳ Waiting for store server to start...")
    time.sleep(3)  # Give it time to start
    
    if _store_process.poll() is not None:
        # Process died
        stdout, stderr = _store_process.communicate()
        print(f"❌ Store server failed to start:\n{stderr}")
        return False
    
    print(f"✅ Store server running (PID: {_store_process.pid})")
    print(f"🔗 Using external store: {store_url}")
    return True
