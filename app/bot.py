from telegram import Update
import logging
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes
from secret import API_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
