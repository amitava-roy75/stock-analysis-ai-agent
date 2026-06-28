from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.analyze import router as analyze_router
from api.price_history import router as price_history_router
from api.company import router as company_router
from api.chat import router as chat_router
from api.stock import router as stock_router

from config.logging_config import logger
from tools.bootstrap import initialize_tools
from tools.registry import registry


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("==============================================")
    logger.info("Starting Stock Analyzer AI Agent")
    logger.info("Version : 1.0.0")
    logger.info("==============================================")

    initialize_tools()

    logger.info("Registered Tools:")

    for tool in registry.list_tools():
        logger.info("   %s", tool)

    logger.info("==============================================")
    logger.info("Application Started Successfully")
    logger.info("==============================================")

    yield

    logger.info("==============================================")
    logger.info("Stopping Stock Analyzer AI Agent")
    logger.info("==============================================")


app = FastAPI(
    title="Stock Analyzer AI Agent",
    description="Enterprise AI Stock Analysis Platform powered by Amazon Bedrock and LangGraph",
    version="1.0.0",
    lifespan=lifespan,
)

# ----------------------------------------------------
# CORS
# ----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------


@app.get("/")
async def home():
    return {
        "application": "Stock Analyzer AI Agent",
        "version": "1.0.0",
        "status": "UP",
        "framework": "FastAPI",
        "llm": "Amazon Bedrock - Nova Lite",
    }


@app.get("/health")
async def health():
    return {
        "status": "UP"
    }


@app.get("/tools")
async def list_tools():
    return {
        "registeredTools": registry.list_tools(),
        "count": len(registry.list_tools())
    }


app.include_router(chat_router)
app.include_router(analyze_router)
app.include_router(stock_router)
app.include_router(price_history_router)
app.include_router(company_router)