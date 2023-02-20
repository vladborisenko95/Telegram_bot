import random
import time
from telegram import Update
from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          ContextTypes,
                          MessageHandler,
                          ConversationHandler,
                          filters)

from bot_token import TOKEN


def draw(name_one: str, name_two: str) -> list[str]:
    result = random.randint(1, 2)
    if result == 1:
        first_player = name_one
        second_player = name_two
    else:
        first_player = name_two
        second_player = name_one
    return first_player, second_player


SWEETS_NUMBER = 50
MAXIMUM_MOVE = 12

player_sweets = {}


async def sweets_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f'''Игра в конфеты с ботом.
На столе лежит {SWEETS_NUMBER} конфет. Играют два игрока делая ход друг после друга.
Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем {MAXIMUM_MOVE} конфет.
Все конфеты оппонента достаются сделавшему последний ход. Сколько конфет нужно взять первому игроку,
чтобы забрать все конфеты у своего конкурента?
/cancel - выход из игры
        ''')
    sweets_number = SWEETS_NUMBER
    player_one = update.effective_user.first_name
    player_two = str('Компьютерный Бот')
    emoji_smile = random.choice(['😎', '🤠', '🤓', '🥳', '👽'])
    await update.message.reply_text('Хорошо. бросим жребий!')
    await update.message.reply_text(f'{emoji_smile}')
    time.sleep(3)
    players_list = draw(player_one, player_two)
    print(players_list)

    if players_list[0] != 'Компьютерный Бот':
        await update.message.reply_text('Тебе повезло. Твой ход первый')
        time.sleep(0.5)
        angry_emoji = random.choice(['😉', '🤪', '😝', '😶', '😬', '😔', '😕', '😟',
                                     '🙁', '☹️', '🥺', '😞', '😩', '😫', '😤', '😠'])
        time.sleep(2)
        player_sweets[update.effective_user.id] = sweets_number
        await update.message.reply_text(f"{angry_emoji}")
        await update.message.reply_text("Сколько конфнет забираешь?")
    else:
        await update.message.reply_text('Жребий показал что я буду ходить первый!')
        time.sleep(1)
        fun_emoji = random.choice(
            ['😈', '😜', '🙃', '😆', '😁', '😄', '😃', '😀', '😛'])
        await update.message.reply_text(f'{fun_emoji}')
        time.sleep(2)
        bots_move = random.randint(1, MAXIMUM_MOVE)
        player_sweets[update.effective_user.id] = sweets_number
        player_sweets[update.effective_user.id] -= bots_move
        await update.message.reply_text(
            f"убираем со стола {bots_move} конфет.🍬\n"
            "\n"
            f"на столе остается {player_sweets[update.effective_user.id]} конфет")
        time.sleep(2)
        await update.message.reply_text("Твой ход! Сколько конфнет забираешь?")
    return 1


async def after_move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        sweets = int(update.message.text)
        if sweets <= player_sweets[update.effective_user.id]:
            if 0 < sweets <= MAXIMUM_MOVE:
                player_sweets[update.effective_user.id] -= sweets
            else:
                await update.message.reply_text(f"ты хочешь больше чем можно, попробуй еще раз.")
                return 1
        else:
            await update.message.reply_text(f"ты хочешь больше чем есть на столе, попробуй еще раз.")
            return 1
    except ValueError:
        await update.message.reply_text("🤔")
        time.sleep(2)
        await update.message.reply_text(f"кажется ты ввел не чило, попробуй еще раз.")
        return 1
    if player_sweets[update.effective_user.id] > 0:
        await update.message.reply_text(f"на столе остается {player_sweets[update.effective_user.id]} конфет🍬")
    else:
        await update.message.reply_text("на столе бельше нет конфет🍬")
        sad_emoji = random.choice(
            ['🥴', '🤬', '👿', '😩', '😓', '😣', '😖', '😭', '😢', '🤯', '😡', '🥵'])
        time.sleep(1)
        vin_emoji = random.choice(['🏅', '🥇', '🏆'])
        time.sleep(1)
        await update.message.reply_text(f"ты победил.{sad_emoji}")
        await update.message.reply_text(f"{vin_emoji}")
        return ConversationHandler.END
    time.sleep(2)
    bots_move = random.randint(1, MAXIMUM_MOVE)
    await update.message.reply_text(f"мой ход!")
    if bots_move < player_sweets[update.effective_user.id]:
        player_sweets[update.effective_user.id] -= bots_move
        print(player_sweets[update.effective_user.id])
    else:
        bots_move = player_sweets[update.effective_user.id]
        player_sweets[update.effective_user.id] = 0
    await update.message.reply_text(f"убираем со стола {bots_move} конфет.🍬")
    if player_sweets[update.effective_user.id] > 0:
        await update.message.reply_text(f"на столе остается {player_sweets[update.effective_user.id]} конфет")
        await update.message.reply_text("Твой ход! Сколько конфнет забираешь?")
        return 1
    else:
        await update.message.reply_text("на столе бельше нет конфет")
        time.sleep(1)
        bot_vin_emoji = random.choice(['😀', '😃', '😄', '😆', '🤣', '😂',
                                       '🙂', '😉', '😊', '😇', '🤩', '☺️', '😸', '😼', '😈'])
        await update.message.reply_text(f"Победа моя!!")
        time.sleep(1)
        await update.message.reply_text(f"{bot_vin_emoji}")
        del player_sweets[update.effective_user.id]
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Испугался? Ладно.. я надеюсь мы еще встретимся..")
    time.sleep(1)
    await update.message.reply_text("😸")
    del player_sweets[update.effective_user.id]
    return ConversationHandler.END


handler = ConversationHandler(
    entry_points=[CommandHandler("game", sweets_game)],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, after_move)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)


app = ApplicationBuilder().token(TOKEN).build()


app.add_handler(handler)

app.run_polling()