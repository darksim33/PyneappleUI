from __future__ import annotations
from pathlib import Path

from radimgarray import RadImgArray, SegImgArray
from pyneapple import FitData


class AppData:
    def __init__(self):
        self.app_path = Path(__file__).parent
        self.last_dir: str | Path = Path.home()
        self.img: RadImgArray = None
        self.seg: SegImgArray = None
        self.img_masked: RadImgArray = None
        self.nii_dyn: RadImgArray = None
        self.fit_data = FitData()
        self.plt = dict()
        self.setup_plt_dict()

    def setup_plt_dict(self):
        self.plt["show_plot"] = False  # bool
        self.plt["show_segmentation"] = True  # bool
        self.plt["plt_type"] = "voxel"  # str | None voxel | segmentation
        self.plt["seg_color"] = list()
        self.plt["seg_edge_alpha"] = float()
        self.plt["seg_face_alpha"] = float()
        self.plt["seg_line_width"] = float()
        self.plt["n_slice"] = NSlice(0)
        self.plt["number_points"] = 250  # unused atm


class NSlice:
    def __init__(self, value: int = None):
        if not value:
            self.__value = value
            self.__number = value + 1
        else:
            self.__value = None
            self.__number = None

    @property
    def number(self):
        return self.__number

    @property
    def value(self):
        return self.__value

    @number.setter
    def number(self, value):
        self.__number = value
        self.__value = value - 1

    @value.setter
    def value(self, value):
        self.__number = value + 1
        self.__value = value
