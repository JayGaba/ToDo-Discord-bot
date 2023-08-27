import discord
from discord.ext import commands, tasks
import sqlite3
import asyncio
from datetime import datetime, time, timedelta
import pytz
 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)
 
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS user_tasks (
    user_id TEXT,
    task TEXT,
    completed INTEGER
)''')
conn.commit()
 
#add command
@bot.command()
async def add(ctx, *, task: str):
    user_id = str(ctx.author.id)
    cursor.execute('INSERT INTO user_tasks (user_id, task, completed) VALUES (?, ?, ?)', (user_id, task, 0))
    conn.commit()
    await ctx.send(f"Task added: {task}")
 

#show command
@bot.command()
async def show(ctx):
    user_id = str(ctx.author.id)
    cursor.execute('SELECT task, completed FROM user_tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    if tasks:
        tasks_str = "\n".join([f"{index}. {'----------' if completed else ''}{task}{'---------->done' if completed else ''}" for index, (task, completed) in enumerate(tasks, start=1)])
        await ctx.send(f"Your tasks:\n```{tasks_str}```")
    else:
        await ctx.send("No tasks found for you.")

#show command
@bot.command()
async def done(ctx, *task_indices: int):
    user_id = str(ctx.author.id)
    cursor.execute('SELECT task, completed FROM user_tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    completed_tasks = []
    for task_index in task_indices:
        if 1 <= task_index <= len(tasks):
            task, completed = tasks[task_index - 1]
            if not completed:
                cursor.execute('UPDATE user_tasks SET completed = 1 WHERE user_id = ? AND task = ?', (user_id, task))
                conn.commit()
                completed_tasks.append(task)
    if completed_tasks:
        await ctx.send(f"Tasks marked as completed: {', '.join(completed_tasks)}")
    else:
        await ctx.send("No tasks marked as completed.")

#delete command
@bot.command()
async def delete(ctx, task_index: int):
    user_id = str(ctx.author.id)
    cursor.execute('SELECT task FROM user_tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    if 1 <= task_index <= len(tasks):
        task_to_delete = tasks[task_index - 1][0]
        cursor.execute('DELETE FROM user_tasks WHERE user_id = ? AND task = ?', (user_id, task_to_delete))
        conn.commit()
        await ctx.send(f"Task deleted: {task_to_delete}")
    else:
        await ctx.send("Invalid task index.")

#help command 
@bot.command()
async def c_help(ctx):
    """Custom help command"""
    commands_list = [
        ("add [task]", "Add a new task to your list."),
        ("show", "Show your list of tasks."),
        ("done [task a] [task b]...[task x]", "Mark a task as completed."),
        ("summary", "Get a daily summary of your tasks."),
        ("delete", "To delete a task."),
    ]
    help_text = "Commands:\n"
    for command, description in commands_list:
        help_text += f"{command: <15}{description}\n"
    await ctx.send(f"```{help_text}```")
 
class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
         await self.context.invoke(c_help)
 
bot.help_command = CustomHelpCommand()
 
#clear command 
@bot.command()
async def clear(ctx):
    user_id = str(ctx.author.id)
    cursor.execute('DELETE FROM user_tasks WHERE user_id = ?', (user_id,))
    conn.commit()
    await ctx.send("Your to-do list has now been cleared!")

#enter the target channel id for sending summaries
target_channel_id = 

#summary command 
@bot.command()
async def summary(ctx, user=None):
    if isinstance(ctx, commands.Context):
        user = ctx.author
    else:
        user = ctx
    user_id = str(user.id)
 
    cursor.execute('SELECT task, completed FROM user_tasks WHERE user_id = ?', (user_id,))
 
    tasks = cursor.fetchall()
 
    if tasks:
        completed_tasks = [task for task, completed in tasks if completed]
        pending_tasks   = [task for task, completed in tasks if not completed]
 
        completed_str ="```\n" + "\n".join(map(str, completed_tasks)) + "```" if completed_tasks else ""
        pending_str =  "```\n" + "\n".join(map(str, pending_tasks)) + "```" if pending_tasks else ""
        completed_percentage = (len(completed_tasks) / len(tasks)) * 100 if tasks else 0
 
        summary = f"Daily Summary for {user.mention}\n\n" \
                  f"```Completed tasks ({completed_percentage:.2f}%):```{completed_str}\n" \
                  f"```Pending tasks:```{pending_str}"
 
        target_channel = bot.get_channel(target_channel_id)
        await target_channel.send(summary)
 
        if isinstance(ctx, commands.Context):
            await ctx.send("Daily summary has been sent to the target channel.")
    else:
        await ctx.send("No tasks found for you.")
 
async def send_daily_summaries():
    target_channel = bot.get_channel(target_channel_id)
 
    cursor.execute('SELECT DISTINCT user_id FROM user_tasks')
    user_ids = [row[0] for row in cursor.fetchall()]
 
    for user_id in user_ids:
        user = await bot.fetch_user(user_id)
        await summary(user)

#automatically sends summary at 2am  for all users 
@tasks.loop(hours=24)
async def daily_summary_task():
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
 
    if now.time() > time(2, 0):
        now += timedelta(days=1)
 
    target_time = datetime.combine(now.date(), time(2, 0))
    target_time = pytz.timezone('Asia/Kolkata').localize(target_time)
 
    seconds_until_target = (target_time - now).total_seconds()
 
    await asyncio.sleep(seconds_until_target)
    await send_daily_summaries()
 
@daily_summary_task.before_loop
async def before_daily_summary_task():
    await bot.wait_until_ready()
 
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    daily_summary_task.start()
 
@bot.event
async def on_message(message):
    if message.content == '.':
        await bot.process_commands(message)
        return 
    await bot.process_commands(message)

#enter token here 
bot.run(" ")