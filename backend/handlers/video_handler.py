import datetime
from typing import List

from tornado_request_mapping import request_mapping

from dao.type_dao import TypeDao
from dao.vod_dao import VodDao
from mixins.video_handler_mixin import VideoHandlerMixin
from utils.base_handler import BaseHandler
from utils.entity_utils import EntityUtils
from utils.logger_factory import LoggerFactory
from utils.redis_cache import RedisCache
from utils.response import Response, NotFoundResponse, FuckYouResponse
from vo.type_vo import TypeVo
from vo.video_detail_vo import Url, VideoDetailVo
from vo.video_list_vo import VodListVo


@request_mapping("/api/video")
class VideoHandler(BaseHandler, VideoHandlerMixin):
    logger = LoggerFactory.get_logger()

    @request_mapping('/get_list', 'get')
    async def get_list(self):
        type_en = self.get_argument('type_en', '')
        page = int(self.get_argument('page') or 1)
        per_page = int(self.get_argument('per_page') or 36)
        kw = self.get_argument('kw', '')
        self.logger.info(f'视频列表: ip: {self.get_remote_ip()}, type_en: {type_en}, page: {page}, per_page: {per_page}, kw: {kw}')
        if per_page > 60:
            return self.send_response(FuckYouResponse())
        start = (page - 1) * per_page
        type_id = 0
        if type_en:
            type_by_en = await TypeDao.get_by_type_en(type_en)
            if type_by_en:
                type_id = type_by_en['type_id']
        vod_list = await VodDao.get_by_query(type_id, kw, start, per_page)
        total = await VodDao.count_by_query(type_id, kw)
        return_list = list()  # type: List[VodListVo]
        for video in vod_list:
            vod_vo = EntityUtils.convert(video, VodListVo)
            vod_vo['vod_time'] = datetime.datetime.fromtimestamp(video['vod_time'])
            return_list.append(vod_vo)
        self.send_response(Response({
            'total': total,
            'data': return_list
        }))

    @request_mapping('/get_by_id', 'get')
    async def get_by_id(self):

        vod_id = self.get_argument('vod_id')
        if not vod_id:
            return self.send_response(NotFoundResponse())
        key = 'video_by_id::{}'.format(vod_id)
        response_cache = RedisCache.get(key)
        if response_cache:
            self.logger.info(f'视频详情: ip:{self.get_remote_ip()}, vod_id: {vod_id}, 名称: {response_cache.data.get("vod_name")}')
            return self.send_response(response_cache)

        vod = await VodDao.get_by_vod_id(int(vod_id))
        return_dict = EntityUtils.convert(vod, VideoDetailVo)
        return_dict.update({
            'urls': self._parse_vod_play_url(vod['vod_play_url'], vod['vod_play_from'])
        })
        response = Response(return_dict)
        RedisCache.set(key, response)
        self.logger.info(f'视频详情: ip:{self.get_remote_ip()}, vod_id: {vod_id}, 视频名称: {return_dict["vod_name"]}')
        self.send_response(response)

    @request_mapping("/get_type_list", 'get')
    async def get_type_list(self):
        key = 'type_list'
        response_cache = RedisCache.get(key)
        if response_cache:
            return self.send_response(response_cache)
        all_type = await TypeDao.get_all_type()
        response = Response(EntityUtils.list_convert(all_type, TypeVo))
        RedisCache.set(key, response)
        self.send_response(response)

