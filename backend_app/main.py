import uvicorn
import socket
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    local_ip = get_local_ip()

    logger.info("=" * 60)
    logger.info("Capacity API Server Starting")
    logger.info("=" * 60)
    logger.info(f"Local:   http://localhost:{port}")
    logger.info(f"Network: http://{local_ip}:{port}")
    logger.info(f"Health:  http://localhost:{port}/health")
    logger.info("=" * 60)
    logger.info("Press CTRL+C to stop the server")
    logger.info("=" * 60)

    uvicorn.run(
        "backend_app.src.asgi:app",
        host=host,
        port=port,
        reload=True
    )
