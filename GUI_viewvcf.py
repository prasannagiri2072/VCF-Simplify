import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QTextEdit, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout
from VcfSimplify import vcf_solver
from io import StringIO
import contextlib

class VcfSimplifyGUI(QWidget):
    class Args:
        def __init__(self, inVCF, outFile=None, outType=None, metadata=None):
            self.inVCF = inVCF
            self.outFile = outFile
            self.outType = outType
            self.metadata = metadata

    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("VCF Simplify Tool")
        self.setGeometry(200, 200, 1000, 1000)

        # Input fields and buttons
        self.input_vcf_label = QLabel("Input VCF File:")
        self.input_vcf = QLineEdit(self)
        self.browse_input_btn = QPushButton("Browse")
        self.browse_input_btn.clicked.connect(self.browse_input_vcf)

        self.output_file_label = QLabel("Output File:")
        self.output_file = QLineEdit(self)
        self.browse_output_btn = QPushButton("Browse")
        self.browse_output_btn.clicked.connect(self.browse_output_file)

        # Output format checkboxes
        self.table_checkbox = QCheckBox("Table")
        self.json_checkbox = QCheckBox("JSON")
        self.dict_checkbox = QCheckBox("Dict")

        # Layout for output format checkboxes
        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.addWidget(self.table_checkbox)
        self.checkbox_layout.addWidget(self.json_checkbox)
        self.checkbox_layout.addWidget(self.dict_checkbox)

        # Metadata selection group box
        self.metadata_group_box = self.create_metadata_group()

        # Separate buttons for viewing metadata and running the full process
        self.view_metadata_btn = QPushButton("View Metadata")
        self.view_metadata_btn.clicked.connect(self.view_metadata)

        self.run_view_vcf_btn = QPushButton("Run ViewVCF")
        self.run_view_vcf_btn.clicked.connect(self.run_view_vcf)

        self.output_display = QTextEdit()

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.input_vcf_label)
        layout.addWidget(self.input_vcf)
        layout.addWidget(self.browse_input_btn)
        layout.addWidget(self.output_file_label)
        layout.addWidget(self.output_file)
        layout.addWidget(self.browse_output_btn)
        layout.addLayout(self.checkbox_layout)
        layout.addWidget(self.metadata_group_box)
        layout.addWidget(self.view_metadata_btn)
        layout.addWidget(self.run_view_vcf_btn)
        layout.addWidget(self.output_display)
        self.setLayout(layout)

    def create_metadata_group(self):
        group_box = QGroupBox("Select Metadata")

        # Create metadata checkboxes
        self.vcfspec_checkbox = QCheckBox("VCFspec")
        self.reference_checkbox = QCheckBox("Reference")
        self.contig_checkbox = QCheckBox("Contig")
        self.samples_checkbox = QCheckBox("Samples")
        self.info_checkbox = QCheckBox("INFO")
        self.format_checkbox = QCheckBox("FORMAT")
        self.filter_checkbox = QCheckBox("FILTER")
        self.gatk_command_checkbox = QCheckBox("GATKCommandLine")
        self.gvcf_block_checkbox = QCheckBox("GVCFBlock")

        # Arrange checkboxes in a grid layout
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.vcfspec_checkbox, 0, 0)
        grid_layout.addWidget(self.reference_checkbox, 0, 1)
        grid_layout.addWidget(self.contig_checkbox, 1, 0)
        grid_layout.addWidget(self.samples_checkbox, 1, 1)
        grid_layout.addWidget(self.info_checkbox, 2, 0)
        grid_layout.addWidget(self.format_checkbox, 2, 1)
        grid_layout.addWidget(self.filter_checkbox, 3, 0)
        grid_layout.addWidget(self.gatk_command_checkbox, 3, 1)
        grid_layout.addWidget(self.gvcf_block_checkbox, 4, 0)

        group_box.setLayout(grid_layout)
        return group_box

    def browse_input_vcf(self):
        vcf_file, _ = QFileDialog.getOpenFileName(self, "Select VCF File", "", "VCF Files (*.vcf)")
        if vcf_file:
            self.input_vcf.setText(vcf_file)

    def browse_output_file(self):
    # Remove the file type filter (e.g., "Text Files (*.txt)")
        output_file, _ = QFileDialog.getSaveFileName(self, "Save Output", "")
        if output_file:
            # Set the chosen file path without enforcing any extension
            self.output_file.setText(output_file)

    def view_metadata(self):
        input_vcf = self.input_vcf.text()
        metadata = self.get_selected_metadata()

        if not input_vcf or not metadata:
            self.output_display.setText("Please specify input VCF file and at least one metadata option.")
            return

        args = self.Args(inVCF=input_vcf, metadata=metadata)

        # Capture stdout to get printed output
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            try:
                # Execute metadata display
                vcf_solver("ViewVCF", args)  # Change to correct command if necessary
                output = buf.getvalue()  # Get the printed output
                self.output_display.setText(f"Metadata Output:\n{output}")
            except Exception as e:
                self.output_display.setText(f"Error: {str(e)}")

    def run_view_vcf(self):
        input_vcf = self.input_vcf.text()
        output_file = self.output_file.text()

        # Get selected formats and metadata
        output_formats = self.get_selected_formats()
        metadata = self.get_selected_metadata()

        if not input_vcf or not output_file or not output_formats or not metadata:
            self.output_display.setText("Please specify input VCF file, output file, at least one output format, and at least one metadata option.")
            return

        # Manually set up arguments for running ViewVCF
        args = self.Args(inVCF=input_vcf, outFile=output_file, outType=output_formats, metadata=metadata)

        try:
            start_time = time.time()
            vcf_solver("ViewVCF", args)
            run_time = time.time() - start_time
            self.output_display.setText(f"ViewVCF executed successfully\nOutput file location: {output_file}\nRun time: {run_time:.4f} seconds")
        except Exception as e:
            self.output_display.setText(f"Error: {str(e)}")

    def get_selected_metadata(self):
        metadata = []
        if self.vcfspec_checkbox.isChecked():
            metadata.append('VCFspec')
        if self.reference_checkbox.isChecked():
            metadata.append('reference')
        if self.contig_checkbox.isChecked():
            metadata.append('contig')
        if self.samples_checkbox.isChecked():
            metadata.append('samples')
        if self.info_checkbox.isChecked():
            metadata.append('INFO')
        if self.format_checkbox.isChecked():
            metadata.append('FORMAT')
        if self.filter_checkbox.isChecked():
            metadata.append('FILTER')
        if self.gatk_command_checkbox.isChecked():
            metadata.append('GATKCommandLine')
        if self.gvcf_block_checkbox.isChecked():
            metadata.append('GVCFBlock')
        return metadata

    def get_selected_formats(self):
        output_formats = []
        if self.table_checkbox.isChecked():
            output_formats.append('table')
        if self.json_checkbox.isChecked():
            output_formats.append('json')
        if self.dict_checkbox.isChecked():
            output_formats.append('dict')
        return output_formats

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VcfSimplifyGUI()
    gui.show()
    sys.exit(app.exec_())
