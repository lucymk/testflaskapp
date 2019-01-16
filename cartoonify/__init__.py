from app.workflow import Workflow
from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor
from pathlib import Path
from os.path import join


root = Path(__file__).parent


def cartoonify(path, dataset_path, model_path):
    model_name = model_path.split("/")[-2]

    dataset = DrawingDataset(dataset_path, join(
        str(root), 'app', 'label_mapping.jsonl'))

    imageprocessor = ImageProcessor(model_path,
                                    join(str(root), 'app', 'object_detection', 'data',
                                         'mscoco_label_map.pbtxt'),
                                    model_name)

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
