import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont


class DompetKu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DompetKu - Manajemen Pengeluaran")
        self.setGeometry(100, 100, 750, 500)
        self.setStyleSheet("background-color: white;")

        # Form input
        self.input_no = QLineEdit()
        self.input_ket = QLineEdit()
        self.input_nominal = QLineEdit()
        self.input_tanggal = QLineEdit()
        self.input_kategori = QLineEdit()

        for widget in [self.input_no, self.input_ket, self.input_nominal, self.input_tanggal, self.input_kategori]:
            widget.setStyleSheet("""
                background-color: #ecf0f1;
                color: #2c3e50;
                padding: 6px;
                border-radius: 4px;
                font-size: 14px;
            """)

        self.input_no.setPlaceholderText("No")
        self.input_ket.setPlaceholderText("Keterangan")
        self.input_nominal.setPlaceholderText("Nominal")
        self.input_tanggal.setPlaceholderText("Tanggal (cth: 2025-06-11)")
        self.input_kategori.setPlaceholderText("Kategori")

        # Tombol aksi
        self.btn_simpan = QPushButton("Simpan")
        self.btn_edit = QPushButton("Edit")
        self.btn_hapus = QPushButton("Hapus")
        self.btn_clear = QPushButton("Clear")
        self.btn_keluar = QPushButton("Keluar")

        # Style tombol
        tombol_style = {
            self.btn_simpan: "#27ae60",
            self.btn_edit: "#f39c12",
            self.btn_hapus: "#e74c3c",
            self.btn_clear: "#2980b9",
            self.btn_keluar: "#7f8c8d"
        }

        for btn, color in tombol_style.items():
            btn.setStyleSheet(f"""
                background-color: {color};
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 8px;
                border-radius: 4px;
            """)

        self.btn_simpan.clicked.connect(self.simpan_data)
        self.btn_edit.clicked.connect(self.edit_data)
        self.btn_hapus.clicked.connect(self.hapus_data)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_keluar.clicked.connect(self.close)

        # Tabel pengeluaran
        self.tabel = QTableWidget()
        self.tabel.setColumnCount(5)
        self.tabel.setHorizontalHeaderLabels(["No", "Keterangan", "Nominal", "Tanggal", "Kategori"])
        self.tabel.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabel.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabel.setAlternatingRowColors(True)
        self.tabel.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f9f9f9;
                border: 1px solid #ccc;
                border-radius: 5px;
                gridline-color: #eee;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: white;
                padding: 6px;
                border: 1px solid #ddd;
                font-weight: bold;
                color: black;
            }
        """)
        self.tabel.cellClicked.connect(self.load_data_ke_form)

        header = self.tabel.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Label total pengeluaran
        self.label_total = QLabel("Total Pengeluaran: Rp 0")
        self.label_total.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #c0392b;
            margin-top: 10px;
        """)

        # Layout form
        form_layout = QVBoxLayout()
        label_judul = QLabel("📒 DompetKu - Catatan Pengeluaran Harian")
        label_judul.setStyleSheet("font-size: 18px; font-weight: bold; color: black; margin-bottom: 10px;")
        form_layout.addWidget(label_judul)

        form_layout.addWidget(self.input_no)
        form_layout.addWidget(self.input_ket)
        form_layout.addWidget(self.input_nominal)
        form_layout.addWidget(self.input_tanggal)
        form_layout.addWidget(self.input_kategori)

        tombol_layout = QHBoxLayout()
        tombol_layout.addWidget(self.btn_simpan)
        tombol_layout.addWidget(self.btn_edit)
        tombol_layout.addWidget(self.btn_hapus)
        tombol_layout.addWidget(self.btn_clear)
        tombol_layout.addWidget(self.btn_keluar)

        # Layout utama
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(tombol_layout)
        layout.addWidget(self.tabel)
        layout.addWidget(self.label_total)

        self.setLayout(layout)

    def simpan_data(self):
        no = self.input_no.text().strip()
        ket = self.input_ket.text().strip()
        nominal = self.input_nominal.text().strip()
        tanggal = self.input_tanggal.text().strip()
        kategori = self.input_kategori.text().strip()

        if not (no and ket and nominal and tanggal and kategori):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Harap isi semua kolom.")
            msg.setWindowTitle("Peringatan")
            msg.setStyleSheet("QLabel { color: red; font-size: 13px; }")
            msg.exec()
            return

        try:
            int(nominal)
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Nominal harus berupa angka.")
            msg.setWindowTitle("Input Tidak Valid")
            msg.setStyleSheet("QLabel { color: red; font-size: 13px; }")
            msg.exec()
            return

        row = self.tabel.rowCount()
        self.tabel.insertRow(row)
        items = [no, ket, nominal, tanggal, kategori]
        for col, val in enumerate(items):
            item = QTableWidgetItem(val)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tabel.setItem(row, col, item)
        self.clear_form()
        self.format_tabel_row(row)
        self.hitung_total_pengeluaran()

    def edit_data(self):
        selected_row = self.tabel.currentRow()
        if selected_row < 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Pilih data yang ingin diedit.")
            msg.setWindowTitle("Peringatan")
            msg.setStyleSheet("QLabel { color: red; font-size: 13px; }")
            msg.exec()
            return

        no = self.input_no.text().strip()
        ket = self.input_ket.text().strip()
        nominal = self.input_nominal.text().strip()
        tanggal = self.input_tanggal.text().strip()
        kategori = self.input_kategori.text().strip()

        items = [no, ket, nominal, tanggal, kategori]
        for col, val in enumerate(items):
            item = QTableWidgetItem(val)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tabel.setItem(selected_row, col, item)
        self.clear_form()
        self.format_tabel_row(selected_row)
        self.hitung_total_pengeluaran()

    def hapus_data(self):
        selected_row = self.tabel.currentRow()
        if selected_row >= 0:
            self.tabel.removeRow(selected_row)
            self.clear_form()
            self.hitung_total_pengeluaran()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Pilih data yang ingin dihapus.")
            msg.setWindowTitle("Peringatan")
            msg.setStyleSheet("QLabel { color: red; font-size: 13px; }")
            msg.exec()

    def clear_form(self):
        self.input_no.clear()
        self.input_ket.clear()
        self.input_nominal.clear()
        self.input_tanggal.clear()
        self.input_kategori.clear()

    def format_tabel_row(self, row):
        for col in range(self.tabel.columnCount()):
            item = self.tabel.item(row, col)
            item.setForeground(QColor("#2c3e50"))
            if col == 2:
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            else:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

    def load_data_ke_form(self, row, column):
        self.input_no.setText(self.tabel.item(row, 0).text())
        self.input_ket.setText(self.tabel.item(row, 1).text())
        self.input_nominal.setText(self.tabel.item(row, 2).text())
        self.input_tanggal.setText(self.tabel.item(row, 3).text())
        self.input_kategori.setText(self.tabel.item(row, 4).text())

    def hitung_total_pengeluaran(self):
        total = 0
        for row in range(self.tabel.rowCount()):
            try:
                nominal = int(self.tabel.item(row, 2).text())
                total += nominal
            except ValueError:
                continue
        self.label_total.setText(f"Total Pengeluaran: Rp {total:,}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = DompetKu()
    window.show()
    sys.exit(app.exec())
