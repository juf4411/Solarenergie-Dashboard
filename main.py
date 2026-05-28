"""PyCharm entry point for the solar dashboard API."""

import uvicorn


def main() -> None:
    """Start the FastAPI app with settings that work well from PyCharm."""

    uvicorn.run(
        "solar_server.server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
