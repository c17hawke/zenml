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
"""Implements a custom model for the Kserve integration."""
from pathlib import Path
from typing import Any, Dict

import click
import kserve

from zenml.logger import get_logger
from zenml.utils.source_utils import import_class_by_path

logger = get_logger(__name__)

ARTIFACT_FILE = "artifact.json"
DEFAULT_MODEL_NAME = "model"
DEFAULT_LOCAL_MODEL_DIR = "/mnt/models"


class ZenMLCustomModel(kserve.Model):  # type: ignore[misc]
    """Custom model class for ZenML and Kserve.

    Attributes:
        name: The name of the model.
        model_uri: The URI of the model.
        predict_func: The predict function of the model.
    """

    def __init__(
        self,
        model_name: str,
        model_uri: str,
        predict_func: str,
    ):
        """Initializes a ZenMLCustomModel object.

        Args:
            model_name: The name of the model.
            model_uri: The URI of the model.
            predict_func: The predict function of the model.
        """
        super().__init__(model_name)
        self.name = model_name
        self.model_uri = model_uri
        self.predict_func = import_class_by_path(predict_func)
        self.model = None
        self.ready = False

    def load(self) -> bool:
        """Load the model.

        Returns:
            True if the model was loaded successfully, False otherwise.

        """
        try:
            from zenml.integrations.kserve.steps.kserve_step_utils import (
                load_from_json_zenml_artifact,
            )

            self.model = load_from_json_zenml_artifact(self.model_dir)
        except Exception as e:
            logger.error("Failed to load model: {}".format(e))
            return False
        self.ready = True
        return self.ready

    def predict(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Predict the given request.

        Args:
            request: The request to predict in a dictionary. e.g. {"instances": []}

        Returns:
            The prediction dictionary.

        Raises:
            Exception: If function could not be called.
            NotImplementedError: If the model is not ready.
        """
        if self.predict_func is not None:
            try:
                prediction = self.predict_func(request)
            except Exception as e:
                raise Exception("Failed to predict: {}".format(e))
            if isinstance(prediction, dict):
                return prediction
            else:
                raise Exception("Prediction is not a dictionary.")
        else:
            raise NotImplementedError("Predict function is not implemented")


@click.command()
@click.option(
    "--model_name",
    default=DEFAULT_MODEL_NAME,
    required=True,
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, path_type=Path
    ),
    help="The directory where the model is stored locally.",
)
@click.option(
    "--model_dir",
    default=DEFAULT_LOCAL_MODEL_DIR,
    required=True,
    type=click.STRING,
    help="The name of the model to deploy.",
)
@click.option(
    "--predict_func",
    required=True,
    type=click.STRING,
    help="The path to the predict function.",
)
def main(model_name: str, model_uri: str, predict_func: str) -> None:
    """Main function for the custom model.

    Args:
        model_name: The name of the model.
        model_uri: The URI of the model.
        predict_func: The path to the predict function.
    """
    model = ZenMLCustomModel(model_name, model_uri, predict_func)
    model.load()
    kserve.ModelServer().start([model])


if __name__ == "__main__":
    main()
