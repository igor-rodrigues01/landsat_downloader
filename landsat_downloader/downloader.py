# -*- coding: utf-8 -*-
import logging
import os

from .downloader_base import Downloader
from .scene_info import SceneInfo


logger = logging.getLogger(__name__)


class LandsatDownloader:
    """docstring for LandsatDownloader"""

    @classmethod
    def _create_bands_names(self, bands):
        if type(bands) != list:
            raise ValueError(
                "[Error on Bands] Expected value is: [1,2,3,4,5...]")

        _bands = ["B{}".format(band)
                  for band in bands if isinstance(band, int)]
        _bands.extend([band for band in bands if isinstance(band, str)])

        return _bands

    @staticmethod
    def download_scenes(bands, scene_id_list=False, product_id_list=False, download_dir=None, metadata=True):

        downloaded = []

        if scene_id_list and type(scene_id_list) != list:
            raise ValueError("[Error on Download Scenes\n\
                Expected value is: [scene_id, scene_id...]")

        if product_id_list and type(product_id_list) != list:
            raise ValueError("[Error on Download Scenes\n\
                Expected value is: [scene_id, scene_id...]")

        try:
            bands = LandsatDownloader._create_bands_names(bands)
        except Exception as exc:
            raise(exc)

        if product_id_list:

            for scene_id in scene_id_list:
                scene = SceneInfo(product_id=scene_id)
                scene_downloader = Downloader(scene)
                imgs = scene_downloader.download(bands=bands,
                                          download_dir=download_dir,
                                          metadata=metadata)
                downloaded.extend(imgs)

        if scene_id_list:

            for scene_id in scene_id_list:
                scene = SceneInfo(scene_id=scene_id)
                scene_downloader = Downloader(scene)
                imgs = scene_downloader.download(bands=bands,
                                          download_dir=download_dir,
                                          metadata=metadata)
                downloaded.extend(imgs)

        return downloaded