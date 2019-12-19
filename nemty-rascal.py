#!/bin/env python3

import time, asyncio, os, sys, psutil
import json, argparse

import telepot
from telepot.aio.loop import MessageLoop

config_file_key = 'CONFIG_FILE'

class NemtyRascalBot(telepot.aio.Bot):
    def __init__(self, config_file=''):
        if (config_file == '') and (config_file_key in os.environ):
            config_file = os.environ[config_file_key]
        self.__allowed_ids = []
        print ("Using config file %s" % (config_file), file=sys.stderr)
        with open(config_file, 'r') as f:
            bot_data = json.load(f)['bot']
            access_token = bot_data['access_token']
            self.__allowed_ids.extend(bot_data['allowed_ids'])
        super(NemtyRascalBot, self).__init__(access_token)

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print ("%s,%s,%s,%s" % (chat_type, chat_id, content_type, msg['text']),
                                file=sys.stderr)

        from_data = msg['from']
        if from_data['id'] in self.__allowed_ids:
            await self.__process_message(msg)
        else:
            # Not in allowed list!
            print ("Not replying to %s-%s-%s message %s"
                   % (from_data['first_name'], from_data['last_name'],
                      from_data['id'], msg), file=sys.stderr)

    async def __process_message(self, msg):
        content_type, _, chat_id = telepot.glance(msg)
        response_msg = ""
        if content_type == 'text':
            if msg['text'].lower() == "wassup":
                for p in psutil.process_iter():
                    if "ssh" in p.name():
                        response_msg += ("%s, %s, %s, %s\n" % (p.pid, p.name(),
                                          p.username(), p.cmdline()))
                response_msg += "\nDone"
        else:
            response_msg = "Cannot respond to non-text message"

        await bot.sendMessage(chat_id, response_msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', type=str, default="",
                        help="JSON config file")
    args = parser.parse_args()

    bot = NemtyRascalBot(config_file=args.config_file)
    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot).run_forever())

    print ("Starting NemtyRascalBot service...", file=sys.stderr)
    loop.run_forever()

print ("NemtyRascalBot service terminated", file=sys.stderr)
