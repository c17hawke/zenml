#  Copyright (c) ZenML GmbH 2021. All Rights Reserved.
#
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
from sklearn.preprocessing import StandardScaler

from zenml.artifacts import SchemaArtifact, StatisticsArtifact
from zenml.logger import get_logger
from zenml.steps import Output
from zenml.steps.step_interfaces.base_preprocesser_step import (
    BasePreprocesserConfig,
    BasePreprocesserStep,
)

logger = get_logger(__name__)


class SklearnStandardScalerConfig(BasePreprocesserConfig):
    ignore_columns = []
    exclude_columns = []


class SklearnStandardScaler(BasePreprocesserStep):
    def entrypoint(
        self,
        train_dataset: pd.DataFrame,
        test_dataset: pd.DataFrame,
        validation_dataset: pd.DataFrame,
        statistics: StatisticsArtifact,
        schema: SchemaArtifact,
        config: SklearnStandardScalerConfig,
    ) -> Output(
        train_transformed=pd.DataFrame,
        test_transformed=pd.DataFrame,
        valdation_transformed=pd.DataFrame,
    ):
        schema_dict = {k: v[0] for k, v in schema.to_dict().items()}

        feature_set = set(train_dataset.columns) - set(config.exclude_columns)
        for feature, feature_type in schema_dict.items():
            if feature_type != "int64" and feature_type != "float64":
                feature_set.remove(feature)
                logger.warning(
                    f"{feature} column is a not numeric, thus it is excluded "
                    f"from the standard scaling."
                )

        transform_feature_set = feature_set - set(config.ignore_columns)

        scaler = StandardScaler()
        scaler.mean_ = statistics["mean"][transform_feature_set]
        scaler.scale_ = statistics["std"][transform_feature_set]

        train_dataset[list(transform_feature_set)] = scaler.transform(
            train_dataset[transform_feature_set]
        )
        test_dataset[list(transform_feature_set)] = scaler.transform(
            test_dataset[transform_feature_set]
        )
        validation_dataset[list(transform_feature_set)] = scaler.transform(
            validation_dataset[transform_feature_set]
        )

        return train_dataset, test_dataset, validation_dataset
