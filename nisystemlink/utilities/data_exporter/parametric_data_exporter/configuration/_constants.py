class ColumnGroup:
    PROPERTIES = "properties"
    STATUS_TYPE_SUMMARY = "status_type_summary"
    INPUTS = "inputs"
    OUTPUTS = "outputs"
    DATA = "data"


product_columns = [
    "product_id",
    "product_part_number",
    "product_name",
    "product_family",
    "product_updated_at",
    "product_keywords",
    "product_file_ids",
    "product_workspace",
]
"""
- product columns in the dataframe (prefix added)
- properties won't be here. we can arrange it as per our need in the reorder function
"""

result_columns = [
    "result_started_at",
    "result_updated_at",
    "result_program_name",
    "result_id",
    "result_system_id",
    "result_host_name",
    "result_operator",
    "result_part_number",
    "result_serial_number",
    "result_total_time_in_seconds",
    "result_keywords",
    "result_file_ids",
    "result_workspace",
    "result_status.status_type",
    "result_status.status_name",
]
"""
- result columns in the dataframe (prefix added)
- status_type_summary and properties won't be here. we can arrange them as per our need in the reorder function
"""

step_columns = [
    "step_name",
    "step_step_type",
    "step_step_id",
    "step_parent_id",
    "step_result_id",
    "step_path",
    "step_path_ids",
    "step_status.status_type",
    "step_status.status_name",
    "step_total_time_in_seconds",
    "step_started_at",
    "step_updated_at",
    "step_has_children",
    "step_workspace",
    "step_keywords",
]
"""
- step columns in the dataframe (prefix added)
- properties won't be here. we can arrange it as per our need in the reorder function
"""
