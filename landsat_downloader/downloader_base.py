# -*- coding: utf-8 -*-
import os
import requests
import logging

from homura import download as fetch

from .exceptions import (
    InvalidBandError, RemoteFileDoesntExist, DownloaderErrors
)
from .scene_info import SceneInfo

DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'landsat')

logger = logging.getLogger(__name__)


class DownloaderBase:
    """Base class to download Landsat imagery from AWS or Google servers."""

    def __init__(self, scene_info):
        if not isinstance(scene_info, SceneInfo):
            raise TypeError('scene_info must be a instance of SceneInfo')

        self.scene_info = scene_info

    def check_create_folder(self, folder_path):
        """Check whether a folder exists, if not the folder is created.
        Always return folder_path.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        return folder_path

    def fetch(self, url, path, filename):
        """Verify if the file is already downloaded and complete. If they don't
        exists or if are not complete, use homura download function to fetch
        files. Return a list with the path of the downloaded file and the size
        of the remote file.
        """
        print('\nDownloading file:\t{}'.format(filename))

        remote_file_size = self.get_remote_file_size(url)
        file_path = os.path.join(path, filename)

        if os.path.exists(os.path.join(path, filename)):
            size = os.path.getsize(file_path)
            if size == remote_file_size:
                print('File already exists')
                values = {
                    "name": filename,
                    "path": file_path,
                    "type": filename.split("_")[-1].split(".")[0],
                    "size": size
                }
                return values

        fetch(url, path)
        print('stored at {}'.format(path))
        values = {
            "name": filename,
            "path": file_path,
            "type": filename.split("_")[-1].split(".")[0],
            "size": remote_file_size
        }

        return values

    def remote_file_exists(self, url):
        """Check whether the remote file exists on Storage"""
        return requests.head(url).status_code == 200

    def get_remote_file_size(self, url):
        """Gets the filesize of a remote file """
        headers = requests.head(url).headers
        return int(headers['content-length'])

    def _get_valid_bands(self):
        bands = ["B{}".format(i) for i in range(1, 12)]
        bands.append('BQA')
        return bands

    def validate_bands(self, bands):
        """Validate bands parameter."""
        valid_bands = self._get_valid_bands()
        if not isinstance(bands, list):
            logger.error('Parameter bands must be a "list"')
            raise TypeError('Parameter bands must be a "list"')
        for band in bands:
            if band not in valid_bands:
                logger.error('{} is not a valid band'.format(band))
                raise InvalidBandError('{} is not a valid band'.format(band))


class AWSDownloaderBase(DownloaderBase):
    """Download Landsat 8 imagery from AWS Storage."""

    __remote_file_ext = 'TIF'

    def __init__(self, scene_info, considered_id, url):
        self.scene_info = scene_info
        self.considered_id = considered_id
        self.base_url = os.path.join(
            url,
            '{0:03d}'.format(scene_info.info.get('path')),
            '{0:03d}'.format(scene_info.info.get('row')),
            considered_id
        )
        self.check_remote_file()

    def check_remote_file(self):
        if not self.remote_file_exists():
            msg = '{} is not available on AWS Storage'.format(
                self.considered_id)
            raise RemoteFileDoesntExist(msg)

    def remote_file_exists(self):
        """Verify whether the file (scene) exists on AWS Storage."""
        url = os.path.join(self.base_url, 'index.html')
        return super(AWSDownloaderBase, self).remote_file_exists(url)

    def download(self, bands=[], download_dir=None, metadata=True):
        """Download each specified band and metadata."""
        super(AWSDownloaderBase, self).validate_bands(bands)

        if download_dir is None:
            download_dir = DOWNLOAD_DIR

        dest_dir = self.check_create_folder(
            os.path.join(download_dir, self.considered_id))

        downloaded = []
        if len(bands) > 0:
            for band in bands:
                filename = '{id}_{band}.{extension}'.format(
                    id=self.considered_id,
                    band=band,
                    extension=self.__remote_file_ext
                )
                band_url = os.path.join(self.base_url, filename)
                downloaded.append(self.fetch(band_url, dest_dir, filename))

        if metadata:
            filename = '{}_MTL.txt'.format(self.considered_id)
            url = os.path.join(self.base_url, filename)
            downloaded.append(self.fetch(url, dest_dir, filename))

        return downloaded


class AWSDownloaderCollection1T1(AWSDownloaderBase):
    """docstring for AWSDownloaderCollection1."""

    def __init__(self, scene_info):
        url = 'http://landsat-pds.s3.amazonaws.com/c1/L8/'
        super().__init__(scene_info, scene_info.product_id, url)

    def __repr__(self):
        return "AWS - T1/T2: Scene {}".format(self.considered_id)


class AWSDownloaderCollection1RT(AWSDownloaderBase):
    """docstring for AWSDownloaderCollection1."""

    def __init__(self, scene_info):
        url = 'http://landsat-pds.s3.amazonaws.com/c1/L8/'
        super().__init__(scene_info, scene_info.make_rt_product_id(), url)

    def __repr__(self):
        return "AWS - RT: Scene {}".format(self.considered_id)


class Downloader:
    """
    Class that calls
        AWSDownloaderCollection1
        GoogleDownloader
    to download Landsat imagery.
    """

    def __init__(self, scene_info=False):
        self.downloader = None
        self.scene_info = scene_info

        print('\nScene-ID:\t' + str(self.scene_info.product_id))
        print('Path:\t\t' + str(self.scene_info.info.get('path')))
        print('Row:\t\t' + str(self.scene_info.info.get('row')))
        print('Acq. date:\t' + str(self.scene_info.info.get('acq_date')))

        t1_available = True
        rt_available = True

        try:
            self.downloader = AWSDownloaderCollection1RT(self.scene_info)
        except Exception as exc:
            rt_available = False
            pass
        try:
            self.downloader = AWSDownloaderCollection1T1(self.scene_info)
        except Exception as exc:
            t1_available = False
            pass

        t1_t2_msg = 'scene is available on AWS:\t{}\t({})'.format(
            t1_available, self.scene_info.product_id)
        rt_msg = 'scene is available on AWS:\t{}\t({})'.format(
            rt_available, self.scene_info.make_rt_product_id())

        print('\nT1/T2\t\t{}'.format(t1_t2_msg))
        print('Real-Time\t{}'.format(rt_msg))

        if self.downloader is None:
            raise DownloaderErrors([])

    def download(self, *args, **kwargs):
        print("\nUsing {}".format(self.downloader))
        return self.downloader.download(*args, **kwargs)
