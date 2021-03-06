# -*- coding: utf-8 -*-
import logging

from .downloader_base import Downloader
from .scene_info import SceneInfo


logger = logging.getLogger(__name__)


class LandsatDownloader:
    """docstring for LandsatDownloader"""

    @classmethod
    def _validate_scene_id(self, scene_id_list):
        if scene_id_list and type(scene_id_list) == list:
            return True

        return False

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
    def download_scene(
        bands, scene_id=False, product_id=False,
        download_dir=None, metadata=True
    ):

        if scene_id and product_id:
            try:
                bands = LandsatDownloader._create_bands_names(bands)
            except Exception as exc:
                raise(exc)

            scene = SceneInfo(scene_id=scene_id, product_id=product_id)
            scene_downloader = Downloader(scene)
            imgs = scene_downloader.download(
                bands=bands,
                download_dir=download_dir,
                metadata=metadata
            )
            return imgs

        raise ValueError('Expected scene id and product id')
