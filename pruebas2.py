import settings
import random
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs
import json
from letterboxdpy import movie


logger = settings.logging.getLogger("bot")
