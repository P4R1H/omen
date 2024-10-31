

# OMEN Official Discord Bot

This bot is designed for the official OMEN Discord server, helping users select roles, express gratitude, stay informed, and manage community interaction.

## Features

- **Role Selection**:
  - Assign roles based on CPU, GPU, and device type with `!setup`, `!setup2`, and `!setup3`.
  - Supports role selection and removal with organized interactive menus.

- **Thank System**:
  - `/thank` command to appreciate server members helping in troubleshooting, recorded with MongoDB.
  - **Leaderboard** feature to highlight the most thanked members.

- **Sticky Messages**:
  - Automated sticky messages in designated channels for announcements.
  - Regularly deletes old sticky messages and replaces them with updated ones every hour.

- **Embed Creation**:
  - Customizable embed messages for channels with the `!embed` command.
  
## Commands and Usage

1. **Role Selection**:
   - Use these commands to open role selection interfaces:
     - `!setup` - Select CPU roles.
     - `!setup2` - Select GPU roles.
     - `!setup3` - Select device roles.

2. **Thank System**:
   - `/thank @user` - Thank a user for their help.
   - `/leaderboard` - View the top 10 most thanked members.

3. **Sticky Messages**:
   - Automatic sticky messages in the specified channels, updated hourly.

4. **Embed Creation**:
   - `!embed` - Command for creating a customizable embed message:
     - Waits for user input on channel, title, description, thumbnail, and image.
     - Uses `none` if a field should be empty.

## Installation

1. **Clone Repository**:
   ```bash
   git clone https://github.com/your-username/omen-discord-bot.git
   cd omen-discord-bot
   ```

2. **Environment Variables**:
   Create a `.env` file and add your Discord bot token and MongoDB URI:
   ```env
   token=YOUR_DISCORD_TOKEN
   URI=YOUR_MONGODB_URI
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Bot**:
   ```bash
   python bot.py
   ```

## Dependencies

- `pycord`: Core library for Discord bot development.
- `pymongo`: MongoDB driver.
- `dotenv`: For loading environment variables.

## Permissions

Ensure your bot has the following permissions:

- Manage Roles
- Send Messages
- Embed Links
- Manage Messages (for sticky messages)

## Notes

This bot is configured for the OMEN Official Discord server. Make sure to update `guild_ids` for slash commands to match your server’s ID. 
