from __future__ import annotations
from typing import TYPE_CHECKING
from PyQt6 import QtWidgets
from scipy import ndimage

from radimgarray import RadImgArray, SegImgArray
from pyneapple import Parameters, NNLSParams, IVIMParams, IDEALParams, NNLSCVParams

if TYPE_CHECKING:
    pass


class BasicMessageBox(QtWidgets.QMessageBox):
    def __init__(
        self, title: str, message: str, info_text: str | None = None, **kwargs
    ):
        super().__init__()

        self.setWindowTitle(title)
        self.setText(message)
        if info_text is not None:
            self.setInformativeText(info_text)
        self.setWindowIcon(
            self.style().standardIcon(
                QtWidgets.QStyle.StandardPixmap.SP_MessageBoxWarning
            )
        )
        self.setIcon(kwargs.get("icon", QtWidgets.QMessageBox.Icon.Warning))

        self.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No
        )

        if kwargs.get("debug", False):
            self.close()

    def closeEvent(self, event):
        self.accept()


class AlreadyLoadedSegMessageBox(BasicMessageBox):
    def __init__(self, **kwargs):
        super().__init__(
            "Segmentation already loaded:",
            "There is already a Segmentation loaded.\n"
            "Do you want to keep this segmentation?",
            **kwargs,
        )


class ReshapeSegMessageBox(BasicMessageBox):
    def __init__(self, **kwargs):
        super().__init__(
            "Segmentation Shape Mismatch:",
            "The shape of the segmentation does not match the image shape.",
            "Do you want to scale the segmentation shape to the image shape?",
            **kwargs,
        )

    @staticmethod
    def reshape(*args):
        img: RadImgArray = args[0]
        seg: SegImgArray = args[1]
        new_array = ndimage.zoom(
            seg,
            (
                img.shape[0] / seg.shape[0],
                img.shape[1] / seg.shape[1],
                img.shape[2] / seg.shape[2],
                1,
            ),
            order=0,
        )
        print(f"Seg.shape from {seg.shape} to {new_array.shape}")
        return SegImgArray(new_array, seg.info)


class MissingSegmentationMessageBox(BasicMessageBox):
    def __init__(self, **kwargs):
        super().__init__(
            "Missing Segmentation:",
            "There is no Segmentation loaded at the moment.\n"
            "Do you want to fit every Pixel in the image?",
            **kwargs,
        )


class StillLoadedSegMessageBox(BasicMessageBox):
    def __init__(self, **kwargs):
        super().__init__(
            "Segmentation still loaded:",
            "Another Segmentation is still loaded.\n"
            "Do you want to keep this segmentation?",
            **kwargs,
        )


class ZeroPaddingMissmatchMessageBox(BasicMessageBox):
    def __init__(self, **kwargs):
        super().__init__(
            "Zero-Padding Error:",
            "Segmentation of same shape loaded.",
            "The loaded Segmentation has the same shape as the loaded image.\nDo you want to perform Zero-padding on both?",
            **kwargs,
        )


class FitParametersMessageBox(BasicMessageBox):
    def __init__(
        self, params: Parameters | IVIMParams | NNLSParams | NNLSCVParams, **kwargs
    ):
        title = "Parameter missmatch:"
        if isinstance(params, IVIMParams):
            message = (
                "Currently IVIM parameters are loaded.\nDo you want to overwrite them?"
            )
        elif isinstance(params, IDEALParams):
            message = (
                "Currently IDEAL parameters are loaded.\nDo you want to overwrite them?"
            )
        elif isinstance(params, (NNLSParams, NNLSCVParams)):
            message = (
                "Currently NNLS parameters are loaded.\nDo you want to overwrite them?"
            )
        else:
            message = "Unknown parameters detected.\nDo you want to overwrite them?"
        super().__init__(title, message, **kwargs)


class IDEALSquarePlaneMessageBox(BasicMessageBox):
    def __init__(self, **kwargs):
        super().__init__(
            "Matrix Shape Error",
            "The Image Matrix is not square!",
            "The Image Matrix should be square to perform proper IDEAL fitting.\n"
            "Do you want to make the image and the segmentation square?",
            **kwargs,
        )


class IDEALFinalDimensionStepMessageBox(BasicMessageBox):
    def __init__(self, **kwargs):
        super().__init__(
            "Dimension Step missmatch detected",
            "Dimension of Image does not match final dimension step of IDEAL!\n"
            "The last step will be replaced by the image dimensions!",
            **kwargs,
        )


class RepeatedFitMessageBox(BasicMessageBox):
    def __init__(self, **kwargs) -> None:
        self.title = "Repeated Fit detected"
        self.message = "Found a already processed fit!"
        self.info_text = (
            "Do you want to aboard or continue and discard the previous fit results?"
        )

        super().__init__(self.title, self.message, self.info_text, kwargs=kwargs)

        self.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        self.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Abort
            | QtWidgets.QMessageBox.StandardButton.Discard
        )
