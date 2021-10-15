#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/24 下午9:16
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.models.hook_strategy import HookStrategy
from dongtai.models.hook_type import HookType
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request

from dongtai.utils import const
from dongtai.endpoint import OpenApiEndPoint, R

# note: 当前依赖必须保留，否则无法通过hooktype反向查找策略
from apiserver.api_schema import DongTaiParameter

logger = logging.getLogger("django")


class HookProfilesEndPoint(OpenApiEndPoint):
    name = "api-v1-profiles"
    description = "获取HOOK策略"

    @staticmethod
    def get_profiles(user=None):
        profiles = list()
        hook_types = HookType.objects.all()
        for hook_type in hook_types:
            strategy_details = list()
            profiles.append({
                'type': hook_type.type,
                'enable': hook_type.enable,
                'value': hook_type.value,
                'details': strategy_details
            })
            strategies = hook_type.strategies.filter(created_by__in=[1, user.id] if user else [1],
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

    @extend_schema(
        description='Pull Agent Engine Hook Rule',
        parameters=[
            DongTaiParameter.LANGUAGE,
        ],
        responses=R,
        methods=['GET']
    )
    def get(self, request):
        user = request.user
        language = request.query_params.get('language')
        profiles = self.get_profiles(user)

        return R.success(data=profiles)

    def put(self, request):
        pass

    def post(self):
        pass


if __name__ == '__main__':
    strategy_count = HookStrategy.objects.count()
