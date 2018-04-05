# -*- coding: utf-8 -*-
from datetime import datetime
from collections import OrderedDict

from .finder import LandsatFinder


class SceneInfo:
    """Extract information about scene from sceneName"""

    def __init__(self, scene_id=False, product_id=False):
        self.scene_id = scene_id
        self.product_id = product_id

        if scene_id and product_id:
            raise ValueError("[Error on Scene Info\n\
                Expected value is only scene_id or product_id")

        self.info = self.__validate_scene_id()

    def __validate_scene_id(self):
        if self.scene_id:
            info = self.get_info_from_scene_id(self.scene_id)
            metadata = self.get_product_id(info)
            data = self.get_info_from_product_id(metadata)

            self.product_id = data.get("product")

        if self.product_id:
            data = self.get_info_from_product_id(self.product_id)

        return data

    def __validate_rt_scene_date(self, product_id):
        info = self.get_info_from_product_id(product_id)

        acq_date = datetime.strftime(
            info.get("acq_date"),  "%Y%m%d")
        process_date = datetime.strftime(
            info.get("process_date"), "%Y%m%d")

        if acq_date == process_date:
            return info.get("product")

        return info.get("product").replace(process_date, acq_date)

    def julian_2_date(self, julian_date):
        """ Returns julian date in datetime """
        return datetime.strptime(julian_date, '%Y%j').date()

    def make_rt_product_id(self, product_id=False):
        """ 
        Creates a file with product_id in Real Time category name
        E.g.: LC08_L1GT_224069_20180206_20180301_01_T1 ->
              LC08_L1GT_224069_20180206_20180206_01_RT
        """
        if not product_id:
            product_id = self.product_id

        product_id = self.__validate_rt_scene_date(product_id)
        id_parts = product_id.split("_")[:6]
        id_parts.append("RT")

        return '_'.join(id_parts)

    def get_product_id(self, scene_info):
        """ Returns product id for """
        return self.get_metadata(scene_info)["LANDSAT_PRODUCT_ID"]

    def get_metadata(self, scene_info):
        return LandsatFinder.search_scenes_metadata(
            path_row_list=[(scene_info.get("path"), scene_info.get("row"))],
            start_date=scene_info.get("acq_date"),
            end_date=scene_info.get("acq_date")
        )[0]

    def get_info_from_product_id(self, product_id):
        product = product_id.split("_")

        return OrderedDict([
            ('product', product_id),
            ('sat', product[0]),
            ('path', int(product[2][:3])),
            ('row', int(product[2][3:])),
            ('correction_level', product[1]),
            ('acq_date', datetime.strptime(product[3], "%Y%m%d")),
            ('process_date', datetime.strptime(product[4], "%Y%m%d")),
            ('collection', product[5]),
            ('category', product[6]),
        ])

    def get_info_from_scene_id(self, scene_id):
        return OrderedDict([
            ('sat', scene_id[:3]),
            ('path', int(scene_id[3:6])),
            ('row', int(scene_id[6:9])),
            ('year', int(scene_id[9:13])),
            ('acq_date', self.julian_2_date(scene_id[9:16])),
            ('gsi', scene_id[16:19]),
            ('version', scene_id[19:]),
        ])

    def __repr__(self):
        return "Scene %s" % self.product_id
