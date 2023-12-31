# ToDo Bot

ToDo Bot is a Discord bot designed to help users manage their tasks efficiently, providing commands for adding, tracking, and summarizing tasks on a daily basis.

## Features

- **Add Tasks:** Use the `.add` command to add new tasks to your list.
- **Mark as Done:** Use the `.done` command to mark tasks as completed.
- **Delete Tasks:** Remove unwanted tasks using the `.delete` command.
- **Show Tasks:** Display your current list of tasks using the `.show` command.
- **Summary:** Receive a daily summary of your tasks with the `.summary` command.
- **Help Command:** Access bot commands and their descriptions with `.help`.

## Bot Commands

- `.add [task]`: Add a new task to your list.
- `.done [task indices]`: Mark tasks as completed.
- `.delete [task index]`: Delete a task from your list.
- `.show`: Display your current list of tasks.
- `.summary`: Receive a summary of your tasks.
- `.clear`: Clear your entire task list at EOD.
- `.help`: Display custom help for available commands.

## Setup

1. Clone this repository: `git clone https://github.com/JayGaba/ToDo-Discord-Bot.git`
2. Install required dependencies.
3. Configure the bot token in `bot.py`.
4. Set up a SQLite database using `sqlite3` and create the necessary table.
5. Customize the bot's behavior as needed.
6. Run the bot: `python bot.py`


## Issues and Suggestions

If you encounter any issues or have suggestions for improvements, please feel free to open an issue or contribute to the project.

## Preview

![image](https://github.com/JayGaba/ToDo-Discord-bot/assets/111695826/83144d71-3197-422d-9d2d-70df85aae12b)

In my server i have implemented it in a way such that each user has a seperate channel where they add, show, mark tasks complete and there is a common summary channel where summary of all users is sent.

![image](https://github.com/JayGaba/ToDo-Discord-bot/assets/111695826/9a3d41ba-8558-4f6e-bef1-b5db6e5153e2)


