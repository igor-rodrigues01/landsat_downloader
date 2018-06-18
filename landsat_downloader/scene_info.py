# -*- coding: utf-8 -*-
from datetime import datetime
from collections import OrderedDict

from .finder import LandsatFinder

class Product:
    """
    Get info from product as sat info, path, row, acq_date
    colection and category

    Params:
        - product_id as LC08_L1GT_224068_20180310_20180310_01_RT
                     or LC08_L1GT_224068_20180310_20180320_01_T2
                not LC82240682018069LGN00

    Returns:
        OrderedDict with info from product_id

    """

    def __init__(self, product_id=False):

        if not product_id:
            raise ValueError("[Error on Scene Info\n\
                Expected value is scene_id ")

        self.product_id = product_id
        self.info = self.get_info()


    def get_info(self):
        if self.product_id:
            self.get_info_from_product_id(self.product_id)
        else:
            raise ValueError("[Error on Scene Info\n\
                Expected value is product_id")

    def get_info_from_product_id(self, product_id):
        """
        Get info from product as sat info, path, row, acq_date
        colection and category

        Params:
            - product_id as LC08_L1GT_224068_20180310_20180310_01_RT
                         or LC08_L1GT_224068_20180310_20180320_01_T2
                    not LC82240682018069LGN00

        Returns:
            OrderedDict with info from product_id
        """

        product = product_id.split("_")

        self.product_id = product_id
        self.sat = product[0]
        self.correction_level = product[1]
        self.path = int(product[2][:3])
        self.row = int(product[2][3:])
        self.acq_date = datetime.strptime(product[3], "%Y%m%d")
        self.process_date = datetime.strptime(product[4], "%Y%m%d")
        self.collection = product[5]
        self.category = product[6]


class Identifier:
    """
    Class for get info from scene_id as
    path, row, sat info, acquisition date, gsi, version

    Params:
        - scene_id as LC82240682018069LGN00
            not as LC08_L1GT_224068_20180310_20180310_01_RT
                   LC08_L1GT_224068_20180310_20180320_01_T2

    Returns:
        - A instance for Info with attrs for info
    """

    def __init__(self, scene_id=False):
        if not scene_id:
            raise ValueError("[Error on Scene Info\n\
                Expected value is scene_id ")

        self.scene_id = scene_id
        self.get_info()

    def julian_2_date(self, julian_date):
        """ Returns julian date in datetime """
        return datetime.strptime(julian_date, '%Y%j').date()

    def get_info(self):
        """
        Get info from scene id with get_info_from_scene_id
        raising a exception if scene_id doesnt exists
        """

        if self.scene_id:
            self.get_info_from_scene_id(self.scene_id)
        else:
            raise ValueError("[Error on Scene Info\n\
                Expected value is scene_id")

    def get_info_from_scene_id(self, scene_id):
        """
        Get info from scene as sat info, path, row, year, acq_date
        version and gsi info, as attrs for Info class
        """
        if not scene_id:
            return False

        self.scene = scene_id
        self.sat = scene_id[:3]
        self.path = int(scene_id[3:6])
        self.row = int(scene_id[6:9])
        self.year = int(scene_id[9:13])
        self.acq_date = self.julian_2_date(scene_id[9:16])
        self.gsi = scene_id[16:19]
        self.version = scene_id[19:]



class SceneInfo:
    """
    Extract information about scene
    Params:
        - scene_id: Landsat SceneID
        - update_scene: update scene_id with metadata info
    """

    def __repr__(self):
        return "Scene {} - {}".format(self.scene_id, self.product_id)

    def __init__(self, scene_id=False, product_id=False):
        self.scene_id = scene_id
        self.product_id = product_id

        if not scene_id:
            raise ValueError("[Error on Scene Info\n\
                Expected value is scene_id")

        if not product_id:
            raise ValueError("[Error on Scene Info\n\
                Expected value is product_id")

        self.id_info = self.get_scene_info()
        self.product_info = self.get_product_info()

    def __validate_rt_scene_date(self, product_id):
        """
        Internal validation for RT scene, that creates a RT product
        using acq_date for process_date, and returning replaced dates
        Example: LC08_L1GT_224069_20180206_20180301_01_T1 to
                 LC08_L1GT_224069_20180206_20180206_01_RT
        """
        acq_date = datetime.strftime(
            self.product_info.acq_date,  "%Y%m%d")
        process_date = datetime.strftime(
            self.product_info.process_date, "%Y%m%d")

        if acq_date == process_date:
            return self.product_info.product_id

        return self.product_id.replace(process_date, acq_date)

    def make_rt_product_id(self, product_id=False):
        """
        Creates a file with product_id in Real Time category name
        E.g.: LC08_L1GT_224069_20180206_20180301_01_T1 to
              LC08_L1GT_224069_20180206_20180206_01_RT
        """
        if not product_id:
            product_id = self.product_id

        product_id = self.__validate_rt_scene_date(product_id)
        id_parts = product_id.split("_")[:6]
        id_parts.append("RT")

        return '_'.join(id_parts)

    def get_scene_info(self):
        """
        Get Info instance for self.scene_id
        """
        return Identifier(scene_id=self.scene_id)

    def get_product_info(self):
        """
        Get Info instance for self.scene_id
        """
        return Product(product_id=self.product_id)

    # def get_scene_id(self):
    #     """
    #     Get scene id from metadata
    #     """
    #     return self.metadata["sceneID"]

    # def get_product_id(self):
    #     """
    #     Get product id from metadata
    #     """
    #     return self.metadata["LANDSAT_PRODUCT_ID"]

    # def get_metadata(self, scene_info):
    #     """
    #     Get Metadata for scene info with path, row and acquisition date
    #     using LandsatFinder module from finder.py
    #     """
    #     if not hasattr(self, 'metadata'):
    #         return LandsatFinder.search_scenes_metadata(
    #             path_row_list=[(scene_info.path, scene_info.row)],
    #             start_date=scene_info.acq_date,
    #             end_date=scene_info.acq_date,
    #         )[0]
    #     return self.metadata
