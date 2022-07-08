#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

from typing import List, Tuple

from zenml.enums import AnnotationTasks
from zenml.logger import get_logger

logger = get_logger(__name__)


TASK_TO_FILENAME_REFERENCE_MAPPING = {
    AnnotationTasks.IMAGE_CLASSIFICATION: "image",
    AnnotationTasks.OBJECT_DETECTION_BOUNDING_BOXES: "image",
}


def generate_image_classification_label_config(
    labels: List[str],
) -> Tuple[str, str]:
    """Generates a Label Studio label config for image classification.

    This is based on the basig config example shown at https://labelstud.io/templates/image_classification.html.
    """
    label_config_type = AnnotationTasks.IMAGE_CLASSIFICATION

    label_config_start = f"""<View>
    <Image name="image" value="$image"/>
    <Choices name="choice" toName="image">
    """
    label_config_choices = "".join(
        f"<Choice value='{label}' />\n" for label in labels
    )
    label_config_end = "</Choices>\n</View>"

    return (
        label_config_start + label_config_choices + label_config_end,
        label_config_type,
    )


def generate_basic_object_detection_bounding_boxes_label_config(
    labels: List[str],
) -> Tuple[str, str]:
    """Generates a Label Studio config for object detection with bounding boxes.

    This is based on the basic config example shown at https://labelstud.io/templates/image_bbox.html.
    """
    label_config_type = AnnotationTasks.OBJECT_DETECTION_BOUNDING_BOXES

    label_config_start = f"""<View>
    <Image name="image" value="$image"/>
    <RectangleLabels name="label" toName="image">
    """
    label_config_choices = "".join(
        f"<Label value='{label}' />\n" for label in labels
    )
    label_config_end = "</RectangleLabels>\n</View>"

    return (
        label_config_start + label_config_choices + label_config_end,
        label_config_type,
    )