# skyBot

# dotenv file
Any implementation should store the following in a .env file colocated with runtime.
- the Discord bot token as "discordToken" 
- the Tomorrow API Key as "tomorrowAPIKey"

# tomorrow API
Needed to get API token
Setup a location UMBC Observatory and grabbed ID for the queries

# Requirements
discord
xmltodict (or write your own parser)
python-dotenv (for dotenv)

# Non-git changelog
Make bot
 1. Log in to discord website
 2. Navigate to applications page
 3. Click "New Application"
 4. Give name
 5. Copy token
 6. OAuth2: Set bot permissions and generate invite link
 7. Drop link into browser and confirm server/perms
 8. Ensure discord library is available to python3 interp.
 ```
[proutyr1@/Users/proutyr1/Documents/git/skyBot]
python3 -c "import discord"
[proutyr1@/Users/proutyr1/Documents/git/skyBot]
```
9. Bot needed Privileged Gateway Intents in developer settings online


