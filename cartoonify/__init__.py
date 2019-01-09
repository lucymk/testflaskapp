# TODO: TRIM DEPENDENCIES

from __future__ import division
import click
from app.workflow import Workflow
from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor, tensorflow_model_name
from app.sketch import SketchGizeh
from pathlib import Path
from os.path import join
import datetime
from remi import start
import importlib
import sys
import time


root = Path(__file__).parent


def cartoonify(path, dataset_path, model_path):
    dataset = DrawingDataset(
        str(dataset_path), str(root / 'app/label_mapping.jsonl'))
    imageprocessor = ImageProcessor(str(model_path),
                                    str(root / 'app' / 'object_detection' /
                                        'data' / 'mscoco_label_map.pbtxt'),
                                    tensorflow_model_name)
    app = Workflow(dataset, imageprocessor)
    app.setup()
    path = Path(path)
    if str(path) != '.' or 'exit':
        app.process(str(path), top_x=3)
        path = app.save_results()
        app.close()
        return path
    else:
        app.close()
        return "Error"
