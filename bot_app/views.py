
import json
import logging
import datetime
from bot_app.appmodules.message_parser import *
import telepot
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.conf import settings

from bot_app.models import *
from bot_app.appmodules.query_results import *

token = '419939812:AAGbA3ZbJuPa6frIt7blsU6NIIMGmGzKgEg'
TelegramBot = telepot.Bot(token)

logger = logging.getLogger('telegram.bot')

def _start(keys):
    return "Привет! \n" \
           "Команды: " \
           "/task <subject>, /help"

def _help(keys):
    subjects = Subject.objects.all().values();
    result_str = "--- Команды: ---\n" \
                 "/task <subject> - без ключа возвращает все еще действующие задания," \
                 "с ключом, только задания по предмету. subject может принимать следующие значения:\n { "
    for sub in subjects:
        result_str += sub['subject_name']+ ", "
    result_str = result_str[:-2] + " }"
    result_str += "\n----------------------"
    return result_str

def _get_tasks(keys):
    tasks = None
    if keys != []:
        sub_id = Subject.objects.filter(subject_name=keys[0]).values()[0]
        sub_id = sub_id['id']
        tasks = Task.objects.filter(last_date__gte=datetime.datetime.now()).filter(subject_name_id=sub_id).values()
    else:
        tasks = Task.objects.filter(last_date__gte=datetime.datetime.now()).values()

    if not tasks:
        return "Нет заданий"
    subjects = Subject.objects.all().values()
    result_str = ("--- Задани")+ ("я" if tasks.count()>1 else "е") + ": ---\n"
    for task in tasks:
        result_str += QueryResults.get_task(
            subjects[task['subject_name_id']-1]['subject_name'],
            task['type'],
            str(task['last_date']),
            task['task'])
    return result_str+"\n----------------------"

class CommandReceiveView(View):
    commands = {
        '/start': _start,
        '/help': _help,
        '/task': _get_tasks,
    }

    parser = MessageParser(commands.keys())

    def post(self, request, bot_token):
        if bot_token != token:
            return HttpResponseForbidden('Invalid token')

        raw = request.body.decode('utf-8')
        logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')  # command

            task = self.parser.calculate(cmd)
            if task:
                func = self.commands.get(task.get('command'))
                TelegramBot.sendMessage(chat_id, func(task.get('keys')), parse_mode='Markdown')
            else:
                TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)