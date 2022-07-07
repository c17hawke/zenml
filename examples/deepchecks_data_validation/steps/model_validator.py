#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

import pandas as pd
from deepchecks.core.suite import SuiteResult
from sklearn.base import ClassifierMixin

from zenml.integrations.deepchecks.data_validators.deepchecks_data_validator import (
    DeepchecksDataValidator,
)
from zenml.steps import step

LABEL_COL = "target"


@step
def model_validator(
    dataset: pd.DataFrame,
    model: ClassifierMixin,
) -> SuiteResult:
    """Run model validation checks using Deepchecks"""
    data_validator = DeepchecksDataValidator.get_active_data_validator()

    return data_validator.model_validation(
        dataset=dataset,
        model=model,
        dataset_kwargs=dict(label=LABEL_COL, cat_features=[]),
    )