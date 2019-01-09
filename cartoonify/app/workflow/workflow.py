from __future__ import division
import png
import numpy as np
from pathlib import Path
import logging
from ..sketch import SketchGizeh
import subprocess
import time
from csv import writer
from random import randint


class Workflow(object):
    """controls execution of app
    """

    def __init__(self, dataset, imageprocessor):
        self._dataset = dataset
        self._image_processor = imageprocessor
        self._sketcher = None
        self._logger = logging.getLogger(self.__class__.__name__)
        self._image_labels = []
        self._boxes = None
        self._classes = None
        self._scores = None

    def setup(self, setup_gpio=True):
        self._logger.info('loading cartoon dataset...')
        self._dataset.setup()
        self._logger.info('Done')
        self._sketcher = SketchGizeh()
        self._sketcher.setup()
        self._logger.info('loading tensorflow model...')
        self._image_processor.setup()
        self._logger.info('Done')
        self._logger.info('setup finished.')

    def process(self, image_path, threshold=0.3, top_x=None):
        """processes an image. If no path supplied, then capture from camera

        :param top_x: If not none, only the top X results are drawn (overrides threshold)
        :param float threshold: threshold for object detection (0.0 to 1.0)
        :param path: directory to save results to
        :param bool camera_enabled: whether to use raspi camera or not
        :param image_path: image to process, if camera is disabled
        :return:
        """
        self._logger.info('processing image...')
        try:
            self._image_path = Path(image_path)
            img = self._image_processor.load_image_into_numpy_array(image_path)
            # load a scaled version of the image into memory
            img_scaled = self._image_processor.load_image_into_numpy_array(
                image_path, scale=300 / max(img.shape))
            self._boxes, self._scores, self._classes, num = self._image_processor.detect(
                img_scaled)
            # annotate the original image
            self._annotated_image = self._image_processor.annotate_image(
                img, self._boxes, self._classes, self._scores, threshold=threshold)
            self._sketcher = SketchGizeh()
            self._sketcher.setup(img.shape[1], img.shape[0])
            if top_x:
                sorted_scores = sorted(self._scores.flatten())
                threshold = sorted_scores[-min([top_x, self._scores.size])]
            self._image_labels = self._sketcher.draw_object_recognition_results(np.squeeze(self._boxes),
                                                                                np.squeeze(self._classes).astype(
                                                                                    np.int32),
                                                                                np.squeeze(
                                                                                    self._scores),
                                                                                self._image_processor.labels,
                                                                                self._dataset,
                                                                                threshold=threshold)
        except (ValueError, IOError) as e:
            self._logger.exception(e)

    def save_results(self, debug=False):
        """save result images as png and list of detected objects as txt
        if debug is true, save a list of all detected objects and their scores

        :return tuple: (path to annotated image, path to cartoon image)
        """
        self._logger.info('saving results...')
        cartoon_path = self._image_path.with_name(
            'cartoon' + str(int(time.time() * randint(1, 10))) + '.png')
        self._sketcher.save_png(cartoon_path)
        return cartoon_path

    def close(self):
        self._image_processor.close()

    @property
    def image_labels(self):
        return self._image_labels
