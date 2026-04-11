import os
from ms_oforms.form import Form
from ms_oforms.Views import ViewBase
from typing import TypeVar


T = TypeVar('T', bound='ExportController')


class ExportController:
    """
    The Controller: Orchestrates the flow between Model and View.
    """
    def __init__(self: T, model: Form, view: ViewBase) -> None:
        self.model = model
        self.view = view

    def execute_export(self: T, output_path: str) -> None:
        """Coordinates the export process."""
        print(f"Validating {self.model.name} for MS-OFORMS specs...")
        
        # 1. Validation Logic
        if self.model.width > 32767 or self.model.height > 32767:
            raise ValueError("Form dimensions exceed MS-OFORMS limits.")

        # 2. Extract data from Model
        form_data = self.model.get_form_data()
        controls = self.model.controls

        # 3. Command the View to generate the binary file
        try:
            self.view.write_to_file(form_data, controls, output_path)
            print(f"Successfully generated: {output_path}")
        except Exception as e:
            print(f"Export failed: {str(e)}")
