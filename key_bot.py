import discord
from discord import app_commands
import hashlib
from keep_alive import keep_alive
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# ID de votre serveur Discord
GUILD_ID = 1212131820938731631

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        pass

client = MyClient()

def generate_license_key(username: str) -> str:
    # Créer un hash SHA256 du nom d'utilisateur
    sha256 = hashlib.sha256()
    sha256.update(username.encode('utf-8'))
    # Convertir le hash en hexadécimal et prendre les 16 premiers caractères
    return sha256.hexdigest().upper()[:16]

@client.tree.command(
    name="key",
    description="Get your license key privately"
)
async def velocekey(interaction: discord.Interaction):
    username = interaction.user.name
    license_key = generate_license_key(username)
    message = (
        f"Hello {interaction.user.name}!\n"
        f"Here is your license key:\n"
        f"Username: `{username}`\n"
        f"License Key: `{license_key}`\n"
        "Thank you for using ArkeonProject!"
    )
    try:
        await interaction.user.send(message)
        await interaction.response.send_message("I have sent you a private message with your license key.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I couldn't send you a private message. Please check your privacy settings.", ephemeral=True)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    
    # Afficher les serveurs où le bot est présent
    print("Connected to servers:")
    for guild in client.guilds:
        print(f"- {guild.name} (ID: {guild.id})")
    
    # Synchroniser les commandes avec le serveur spécifique
    try:
        guild = client.get_guild(GUILD_ID)
        if guild:
            client.tree.copy_global_to(guild=guild)
            await client.tree.sync(guild=guild)
            print(f"Commands synced to server: {guild.name}")
        else:
            print(f"Could not find guild with ID {GUILD_ID}")
            print("Available guilds:")
            for g in client.guilds:
                print(f"- {g.name} (ID: {g.id})")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

if __name__ == '__main__':
    print("Starting bot...")
    # Récupérer le token depuis les variables d'environnement
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: No token found in environment variables!")
        print("Please make sure to set DISCORD_TOKEN in your .env file or environment variables.")
        exit(1)
    
    # Démarrer le serveur web keep alive
    keep_alive()
    # Démarrer le bot
    client.run(token)