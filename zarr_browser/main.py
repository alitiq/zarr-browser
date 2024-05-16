""" fastapi wrapper for zarr-browser"""

from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from zarr_browser.app import app as dashboard
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import nest_asyncio

nest_asyncio.apply()

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]
# Define the FastAPI server
app = FastAPI(middleware=middleware)
# Mount the Dash app as a sub-application in the FastAPI server
app.mount("/", WSGIMiddleware(dashboard.server))
