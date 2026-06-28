import tools.price_tool
import tools.news_tool
import tools.fundamental_tool
import tools.company_profile_tool
import tools.financial_statement_tool
import tools.compare_tool

from tools.registry import registry
from config.logging_config import logger


def initialize_tools():

    logger.info("===================================")
    logger.info("Initializing Tool Registry")
    logger.info("===================================")

    for tool in registry.list_tools():
        logger.info(f"Registered Tool : {tool}")

    logger.info("===================================")
    logger.info("Tool Initialization Completed")
    logger.info("===================================")