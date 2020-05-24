from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)

import logging

from client import Client

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)

logger = logging.getLogger(__name__)

authorized_users = [232197557]

AGENT_LOC = 'Agent location'
PORTAL_LOC = 'Portal location'
STATS = 'Stats'
SETTINGS = 'Settings'
main_keyboard = [
    [AGENT_LOC, PORTAL_LOC],
    [STATS, SETTINGS]
]
main_markup = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True)

client = Client('+380507691229', None)



def start(update, context):
    if update.message.chat.id not in authorized_users:
        reply_text = "Hi! Please, authorize first"
        update.message.reply_text(reply_text)
        return

    update.message.reply_text('Welcome', reply_markup=main_markup)


def authorize_client(update, context):
    if update.message.chat.username != 'danasemaniv':
        return
    bot_data = context.bot_data.get('authorized_users', set())
    for user in context.args:
        bot_data.add(user)

    update.message.reply_text('Added some users')


def add_agent_to_list(update, context):
    if update.message.chat.id not in authorized_users:
        reply_text = "Hi! Please, authorize first"
        update.message.reply_text(reply_text)
        return

    if not context.args:
        update.message.reply_text('Please, specify agent username')
    user_list = context.user_data.get('agent_list', [])
    for agent in context.args:
        if agent not in user_list:
            user_list.append(agent)
            update.message.reply_text(f'Agent {agent} was added successfully.')

    context.user_data['agent_list'] = user_list


def remove_agent_from_list(update, context):
    if update.message.chat.id not in authorized_users:
        reply_text = "Hi! Please, authorize first"
        update.message.reply_text(reply_text)
        return

    user_list = context.user_data.get('agent_list', [])
    for agent in context.args:
        if agent in user_list:
            user_list.remove(agent)
            update.message.reply_text(f'Agent {agent} was removed successfully.')

    context.user_data['agent_list'] = user_list


def agent_loc_choice(update, context):
    if update.message.chat.id not in authorized_users:
        reply_text = "Hi! Please, authorize first"
        update.message.reply_text(reply_text)
        return

    user_agent_list = [[f'{AGENT_LOC} {value}'] for value in context.user_data.get('agent_list', [])] + [['Back']]
    agent_list_markup = ReplyKeyboardMarkup(user_agent_list)
    update.message.reply_text('Choose the agent', reply_markup=agent_list_markup)


def agent_loc_request(update, context):
    if update.message.chat.id not in authorized_users:
        reply_text = "Hi! Please, authorize first"
        update.message.reply_text(reply_text)
        return

    text = update.message.text.replace(AGENT_LOC, '').strip()
    update.message.reply_text('Loading friends list')
    message = f'Бот где {text}'
    client.send_message(text=message)


def add_portal_to_list(update, context):
    if update.message.chat.id not in authorized_users:
        reply_text = "Hi! Please, authorize first"
        update.message.reply_text(reply_text)
        return

    if not context.args:
        update.message.reply_text('Please, specify portal')
    portals = context.user_data.get('portal_list', {})
    portal_name, command = context.args

    if command not in portals:
        portals[command] = portal_name
        update.message.reply_text(f'Portal {portal_name} was added successfully.')
    else:
        update.message.reply_text(f'Already in list.')

    context.user_data['portal_list'] = portals


def remove_portal_from_list(update, context):
    if update.message.chat.id not in authorized_users:
        reply_text = "Hi! Please, authorize first"
        update.message.reply_text(reply_text)
        return

    portal_list = context.user_data.get('portal_list', [])
    for portal in context.args:
        for key, value in context.user_data['portal_list'].items():
            if value == portal:
                del portal_list[key]
                break

    context.user_data['portal_list'] = portal_list


def portal_loc_choice(update, context):
    if update.message.chat.id not in authorized_users:
        reply_text = "Hi! Please, authorize first"
        update.message.reply_text(reply_text)
        return

    user_portal_list = [[f'{PORTAL_LOC} {value}'] for key, value in context.user_data.get('portal_list', {}).items()] \
                       + [['Back']]
    portal_list_markup = ReplyKeyboardMarkup(user_portal_list)
    update.message.reply_text('Choose the portal', reply_markup=portal_list_markup)


def portal_loc_request(update, context):
    if update.message.chat.id not in authorized_users:
        reply_text = "Hi! Please, authorize first"
        update.message.reply_text(reply_text)
        return

    text = update.message.text.replace(PORTAL_LOC, '').strip()
    message = None
    for key, value in context.user_data['portal_list'].items():
        if value == text:
            message = key
            break
    if message:
        client.send_message(text=message)
    update.message.reply_text(f'Loading events list')


def back(update, context):
    update.message.reply_text('Choose menu', reply_markup=main_markup)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    pp = PicklePersistence(filename='conversationbot')
    updater = Updater("457267588:AAHDi4858egbTTTHGSQz4iEu-Hljx-b9ZPk", persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)

    # agent location
    add_agent_to_list_handler = CommandHandler('add_agent', add_agent_to_list)
    dp.add_handler(add_agent_to_list_handler)

    remove_agent_from_list_handler = CommandHandler('remove_agent', remove_agent_from_list)
    dp.add_handler(remove_agent_from_list_handler)

    agent_loc_menu_handler = MessageHandler(Filters.text(AGENT_LOC), agent_loc_choice)
    dp.add_handler(agent_loc_menu_handler)

    agent_loc_request_handler = MessageHandler(Filters.regex(f'{AGENT_LOC} .+'), agent_loc_request)
    dp.add_handler(agent_loc_request_handler)

    # portal location
    add_portal_to_list_handler = CommandHandler('add_portal', add_portal_to_list)
    dp.add_handler(add_portal_to_list_handler)

    remove_portal_from_list_handler = CommandHandler('remove_portal', remove_portal_from_list)
    dp.add_handler(remove_portal_from_list_handler)

    portal_loc_menu_handler = MessageHandler(Filters.text(PORTAL_LOC), portal_loc_choice)
    dp.add_handler(portal_loc_menu_handler)

    portal_loc_request_handler = MessageHandler(Filters.regex(f'{PORTAL_LOC} .+'), portal_loc_request)
    dp.add_handler(portal_loc_request_handler)

    # back
    back_handler = MessageHandler(Filters.text('Back'), back)
    dp.add_handler(back_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
