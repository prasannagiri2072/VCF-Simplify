import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QFileDialog, QRadioButton, 
                             QCheckBox, QGroupBox, QFormLayout, QTextEdit, 
                             QScrollArea, QSizePolicy)

class VcfSimplifyGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create the main layout
        main_layout = QVBoxLayout()

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a container widget for the scroll area
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)

        # Input VCF File
        self.input_label = QLabel("Input VCF File:")
        self.input_btn = QPushButton("Browse")
        self.input_btn.clicked.connect(self.browse_input_vcf)
        container_layout.addWidget(self.input_label)
        container_layout.addWidget(self.input_btn)

        # Output File
        self.output_label = QLabel("Output File Name:")
        self.output_input = QLineEdit()
        self.output_btn = QPushButton("Browse Output")
        self.output_btn.clicked.connect(self.browse_output_file)
        container_layout.addWidget(self.output_label)
        container_layout.addWidget(self.output_input)
        container_layout.addWidget(self.output_btn)

        # Output Type
        self.output_type_group = QGroupBox("Output Type")
        self.haplotype_radio = QRadioButton("Haplotype")
        self.table_radio = QRadioButton("Table")
        self.output_type_layout = QVBoxLayout()
        self.output_type_layout.addWidget(self.haplotype_radio)
        self.output_type_layout.addWidget(self.table_radio)
        self.output_type_group.setLayout(self.output_type_layout)
        container_layout.addWidget(self.output_type_group)

        # Header Options
        self.header_checkbox = QCheckBox("Output Header")
        self.header_input = QLineEdit()
        self.header_input.setEnabled(False)  # Disabled by default
        self.header_checkbox.toggled.connect(lambda: self.header_input.setEnabled(self.header_checkbox.isChecked()))
        container_layout.addWidget(self.header_checkbox)
        container_layout.addWidget(self.header_input)

        # GTbase Options
        self.gtbase_group = QGroupBox("GTbase Options")
        self.gtbase_layout = QVBoxLayout()
        for option in ["GT:numeric", "GT:iupac", "PG:iupac"]:
            cb = QCheckBox(option)
            self.gtbase_layout.addWidget(cb)
        self.gtbase_group.setLayout(self.gtbase_layout)
        container_layout.addWidget(self.gtbase_group)

        # Haplotype Options
        self.pg_group = QGroupBox("PG Options")
        self.pg_layout = QVBoxLayout()
        for option in ["PG", "PG:iupac"]:
            cb = QCheckBox(option)
            self.pg_layout.addWidget(cb)
        self.pg_group.setLayout(self.pg_layout)
        container_layout.addWidget(self.pg_group)

        self.pi_group = QGroupBox("PI Options")
        self.pi_layout = QVBoxLayout()
        for option in ["PI", "CHROM"]:
            cb = QCheckBox(option)
            self.pi_layout.addWidget(cb)
        self.pi_group.setLayout(self.pi_layout)
        container_layout.addWidget(self.pi_group)

        self.include_unphased_checkbox = QCheckBox("Include Unphased (yes/no)")
        container_layout.addWidget(self.include_unphased_checkbox)

        # Table Options
        self.samples_group = QGroupBox("Samples Options")
        self.samples_layout = QVBoxLayout()
        for option in ["Sample A", "Sample B", "match:XXX", "all"]:
            cb = QCheckBox(option)
            self.samples_layout.addWidget(cb)
        self.samples_group.setLayout(self.samples_layout)
        container_layout.addWidget(self.samples_group)

        # PreHeader Options
        self.preheader_group = QGroupBox("PreHeader Options")
        self.preheader_layout = QVBoxLayout()
        for option in ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "all"]:
            cb = QCheckBox(option)
            self.preheader_layout.addWidget(cb)
        self.preheader_group.setLayout(self.preheader_layout)
        container_layout.addWidget(self.preheader_group)

        # Infos Options
        self.infos_group = QGroupBox("INFO Tags Options")
        self.infos_layout = QVBoxLayout()
        for option in ["AC", "AF", "AN", "all"]:
            cb = QCheckBox(option)
            self.infos_layout.addWidget(cb)
        self.infos_group.setLayout(self.infos_layout)
        container_layout.addWidget(self.infos_group)

        # Formats Options
        self.formats_group = QGroupBox("FORMAT Tags Options")
        self.formats_layout = QVBoxLayout()
        for option in ["GT", "PG", "PI", "all"]:
            cb = QCheckBox(option)
            self.formats_layout.addWidget(cb)
        self.formats_group.setLayout(self.formats_layout)
        container_layout.addWidget(self.formats_group)

        # Mode Options
        self.mode_group = QGroupBox("Mode Options")
        self.wide_radio = QRadioButton("Wide")
        self.long_radio = QRadioButton("Long")
        self.mode_layout = QVBoxLayout()
        self.mode_layout.addWidget(self.wide_radio)
        self.mode_layout.addWidget(self.long_radio)
        self.mode_group.setLayout(self.mode_layout)
        container_layout.addWidget(self.mode_group)

        # Execution Button
        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run_vcf_simplify)
        container_layout.addWidget(self.run_btn)

        # Output Status
        self.output_status = QTextEdit()
        self.output_status.setReadOnly(True)  # Make it read-only
        container_layout.addWidget(self.output_status)

        # Set the layout of the container and add it to the scroll area
        scroll_area.setWidget(container_widget)
        main_layout.addWidget(scroll_area)

        # Set the main layout for the widget
        self.setLayout(main_layout)
        self.setWindowTitle("VCF Simplify GUI")
        self.setMinimumSize(400, 800)  # Set a minimum size for better usability
        self.show()

    def browse_input_vcf(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select VCF File")
        if filename:
            self.input_label.setText(filename)

    def browse_output_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Select Output File")
        if filename:
            self.output_input.setText(filename)

    def run_vcf_simplify(self):
        # Collect all input values and construct the command
        vcf_input = self.input_label.text()
        output_file = self.output_input.text()
        output_type = "haplotype" if self.haplotype_radio.isChecked() else "table"
        header_file = self.header_input.text() if self.header_checkbox.isChecked() else ""
        
        # Example output, add the real implementation here
        self.output_status.setPlainText(f"Running VCF Simplify on {vcf_input} with output {output_file}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VcfSimplifyGUI()
    sys.exit(app.exec_())
