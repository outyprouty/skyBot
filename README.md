# skyBot

General: `skyBot` uses NOAA and TomorrowAPI to gather some sky data and organize it for 'easy' viewing.

Usage as discord bot: `skyBot summary | details | obstimes | help`

`summary`: Gives three-day sun/moon information along with estimates of number of hours before and after sunset with clear skies
`details`: Gives three-day 'score' (see below) for each hour along with average of NOAA and Tomorrow API cloud cover forecast.
`obstimes`: Same as details, but only for hours with scores above a certain threshold, currently set to {:0.2f}
What does 'clear' mean? NOAA and Tomorrow API agree forecast less than 30\% cloud cover over a three-hour rolling window centered on the hour in question.
The time of day along with the cloud cover calculation above are bundled together into a score ranging from 0 to 1 with 1 being the best score.




# dotenv file
Any implementation should store the following in a .env file colocated with runtime.
- the Discord bot token as "discordToken" 
- the Tomorrow API Key as "tomorrowAPIKey"
TODO: Roy can distill more of the random 

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


