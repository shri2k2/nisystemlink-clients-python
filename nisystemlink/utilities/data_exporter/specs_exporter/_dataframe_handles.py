from typing import Dict, List

import pandas as pd
from nisystemlink.clients.spec.models import Condition
from nisystemlink.clients.spec.models._condition import NumericConditionValue


def __serialize_conditions(conditions: List[Condition]) -> Dict:
    """Seriazlize conditions into desired format.

    Args:
        conditions: List of all conditions in a spec.

    Returns:
        Conditions as a dictionary in specific format for the dataframe.
    """
    condition_dict = {}

    for condition in conditions:
        column_header = (
            "condition_" + condition.name
            if condition.name
            else ""
            + (
                f"({condition.value.unit})"
                if type(condition.value) == NumericConditionValue
                else ""
            )
        )

        condition_dict[column_header] = ""

        values = []

        if condition.value:
            if type(condition.value) == NumericConditionValue:
                for range in condition.value.range or []:
                    values.append(
                        f"[{'; '.join([f'{k}: {v}' for k, v in vars(range).items() if v is not None])}]"
                    )

            values.extend(
                [str(discrete) for discrete in condition.value.discrete or []]
            )

        condition_dict[column_header] = ", ".join(values)

    return condition_dict


def serialize_specs(
    specs: pd.DataFrame,
    product_part_number: str,
    workspaces: dict[str, str],
    users: dict[str, str],
) -> pd.DataFrame:
    """Serialize specs into a dataframe with specific format.

    Args:
        specs: Specs dataframe.
        product_part_number: Part number of the product to which the specs belong to.
        workspaces: Dictionary of workspaces {workspace_id: workspace_name}.
        users: Dictionary of users {user_id: first_name + last_name}.

    Returns:
        Serialized dataframe of specs.
    """
    limit_fields = ["min", "max", "typical"]
    specs_dict = []

    for spec in specs:
        spec_dict = vars(spec)

        product_dict = {"product_part_number": product_part_number}

        condition_dict = __serialize_conditions(spec.conditions)

        spec_dict["workspace"] = workspaces[spec_dict["workspace"]]
        spec_dict["updated_by"] = users[spec_dict["updated_by"]]
        spec_dict["created_by"] = users[spec_dict["created_by"]]

        # Converting SpecificationType enum into string value.
        spec_dict["type"] = spec_dict["type"].name

        # Extracting min, max and typical from the limits.
        limit_dict = {
            field: getattr(spec.limit, field, None) if spec.limit else None
            for field in limit_fields
        }

        # Merging the dictionaries.
        result_dict = {**spec_dict, **product_dict, **limit_dict, **condition_dict}

        # Removing limit Column.
        result_dict.pop("limit", None)
        # Removing product id Column.
        result_dict.pop("product_id", None)
        # Removing conditions Column.
        result_dict.pop("conditions", None)

        specs_dict.append(result_dict)

    specs_df = pd.json_normalize(specs_dict, sep="_")

    return specs_df
