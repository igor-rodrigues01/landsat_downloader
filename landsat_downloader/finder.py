# -*- coding: utf-8 -*-
import logging
import requests
import xmltodict

logger = logging.getLogger(__name__)


class LandsatFinder:
    """docstring for LandsatFinder"""

    @classmethod
    def __get_ee_url(self):
        url = "https://earthexplorer.usgs.gov/EE/InventoryStream/pathrow"
        params = "?start_path={path}" + \
            "&end_path={path}" + \
            "&start_row={row}" + \
            "&end_row={row}" + \
            "&sensor={sensor}" + \
            "&start_date={start_date}" + \
            "&end_date={end_date}"

        return url + params

    @classmethod
    def __extract_metadata_info(self, response_metadata):

        try:
            xml = response_metadata.content.decode()
            metadata_list = xmltodict.parse(xml)
            metadata_list = metadata_list['searchResponse']['metaData']

            if type(metadata_list) != list:
                metadata_list = [metadata_list]

            for i, metadata in enumerate(metadata_list):
                for k, v in metadata.items():
                    if v.isdigit():
                        metadata_list[i][k] = int(v)
                    else:
                        try:
                            metadata_list[i][k] = float(v)
                        except Exception as exc:
                            metadata_list[i][k] = str(v)
        except Exception as exc:
            metadata_list = []

        return metadata_list

    @staticmethod
    def search_scenes_metadata(
        path_row_list, start_date, end_date, sensor="LANDSAT_8_C1"
    ):
        """
        Search scenes from EarthExplorer for date range and path row list
        returns a list of scenes with metadata
        params:
            start_date: initial date
            end_date: end date
            path_row_list: must be a list of path and row.
                E.g.: [(50,50),(200,200)]
            sensor: EarthExplorer sensor mode name. default: Landsat_8_C1
        """

        if type(path_row_list) != list:
            raise ValueError(
                "[Error on Search Scenes Metadata] " +
                "Expected value is: [(path, row), (path, row)...]")

        metadata_dict_list = []

        for path_row in path_row_list:

            search_url = LandsatFinder.__get_ee_url().format(
                path=path_row[0],
                row=path_row[1],
                sensor=sensor,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
            )

            r = requests.get(search_url)
            metadata_list = LandsatFinder.__extract_metadata_info(r)

            metadata_dict_list.extend(metadata_list)

        return metadata_dict_list

    @staticmethod
    def search_scenes_id_list(path_row_list, start_date, end_date):
        """
        Search scenes from EarthExplorer for date range and path row list
        returns a list of scenes with metadata
        params:
            start_date: initial date
            end_date: end date
            path_row_list: must be a list of path and row.
                E.g.: [(50,50),(200,200)]
            sensor: EarthExplorer sensor mode name. default: Landsat_8_C1
        """
        scene_list = LandsatFinder.search_scenes_metadata(
            path_row_list, start_date, end_date)
        return [scene['sceneID'] for scene in scene_list]
