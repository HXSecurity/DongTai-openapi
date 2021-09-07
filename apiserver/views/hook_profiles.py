#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/24 下午9:16
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.models.hook_strategy import HookStrategy
from dongtai.models.hook_type import HookType
from rest_framework.request import Request

from dongtai.utils import const
from dongtai.endpoint import OpenApiEndPoint, R

# note: 当前依赖必须保留，否则无法通过hooktype反向查找策略

logger = logging.getLogger("django")
JAVA = 1


class HookProfilesEndPoint(OpenApiEndPoint):
    name = "api-v1-profiles"
    description = "获取HOOK策略"

    @staticmethod
    def get_profiles(user=None, language_id=JAVA):
        profiles = list()
        hook_types = HookType.objects.filter(language_id=language_id).all()
        for hook_type in hook_types:
            strategy_details = list()
            profiles.append({
                'type': hook_type.type,
                'enable': hook_type.enable,
                'value': hook_type.value,
                'details': strategy_details
            })
            strategies = hook_type.strategies.filter(
                created_by__in=[1, user.id] if user else [1],
                enable=const.HOOK_TYPE_ENABLE)
            for strategy in strategies:
                strategy_details.append({
                    "source": strategy.source,
                    "track": strategy.track,
                    "target": strategy.target,
                    "value": strategy.value,
                    "inherit": strategy.inherit
                })
        return profiles

    def get(self, request: Request):
        """
        IAST 检测引擎 agent接口
        :param request:
        :return:
        """
        user = request.user
        language_id = request.query_params.get('language_id', None)
        language_id = JAVA if language_id is None else language_id
        profiles = self.get_profiles(user, language_id)

        return R.success(data=profiles)

    def put(self, request):
        pass

    def post(self):
        pass


if __name__ == '__main__':
    strategy_count = HookStrategy.objects.count()
