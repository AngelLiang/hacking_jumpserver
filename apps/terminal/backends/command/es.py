# -*- coding: utf-8 -*-
#

from jms_es_sdk import ESStore
from .base import CommandBase
from .models import AbstractSessionCommand


class CommandStore(CommandBase, ESStore):
    def __init__(self, params):
        hosts = params.get('HOSTS', ['http://localhost'])
        ESStore.__init__(self, hosts=hosts)

    def save(self, command):
        return ESStore.save(self, command)

    def bulk_save(self, commands):
        """批量保存"""
        return ESStore.bulk_save(self, commands)

    def filter(self, date_from=None, date_to=None,
               user=None, asset=None, system_user=None,
               input=None, session=None):
        """过滤"""
        data = ESStore.filter(
            self, date_from=date_from, date_to=date_to,
            user=user, asset=asset, system_user=system_user,
            input=input, session=session
        )
        # 从多键字典从提取数据并返回
        return AbstractSessionCommand.from_multi_dict(
            [item["_source"] for item in data["hits"] if item]
        )

    def count(self, date_from=None, date_to=None,
              user=None, asset=None, system_user=None,
              input=None, session=None):
        """统计"""
        amount = ESStore.count(
            self, date_from=date_from, date_to=date_to,
            user=user, asset=asset, system_user=system_user,
            input=input, session=session
        )
        return amount
