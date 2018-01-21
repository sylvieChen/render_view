import sys
from PySide import QtGui, QtCore
from main import RenderViewer


class RenderViewerUI(QtGui.QWidget):
    def __init__(self):
        super(RenderViewerUI, self).__init__()
        self.title = 'Render View'
        self.render_viewer = RenderViewer()

        self.setup_ui()
        self.setup_signal()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setMaximumSize(800, 600)

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.image_label = QtGui.QLabel()
        self.image_label.setMinimumSize(512, 512)
        self.image_label.setAutoFillBackground(True)
        self.image_label.setPalette(palette)

        info_str = ''
        info_str += 'Output Directory: {}\n'.format(self.render_viewer.output_dir)
        info_str += 'Image FileName: {}\n'.format(self.render_viewer.image_full_path)
        info_str += 'Image Size: {0} x {1}\n'.format(self.render_viewer.image_wsize, self.render_viewer.image_hsize)
        self.render_info_label = QtGui.QLabel()
        self.render_info_label.setText(info_str)
        self.render_info_label.setEnabled(False)

        self.render_log_label = QtGui.QLabel('Render Log:')
        self.render_log_textedit = QtGui.QTextEdit()
        self.render_log_textedit.setMinimumWidth(280)

        self.render_log_vbox_layout = QtGui.QVBoxLayout()
        self.render_log_vbox_layout.addWidget(self.render_info_label)
        self.render_log_vbox_layout.addWidget(self.render_log_label)
        self.render_log_vbox_layout.addWidget(self.render_log_textedit)

        self.color_button = QtGui.QPushButton('Color')
        self.color_button.setToolTip('Select Object Color.')
        self.color_button.setStyleSheet("QPushButton { background-color: rgb(125, 125, 125)}")
        self.color_button.setMaximumWidth(50)

        self.render_button = QtGui.QPushButton('Render')
        self.render_button.setToolTip('Render to disk.')
        self.render_button.setStyleSheet("QPushButton { background-color: rgb(125, 125, 125)}")

        self.render_hbox_layout = QtGui.QHBoxLayout()

        self.render_hbox_layout.addWidget(self.color_button)
        self.render_hbox_layout.addWidget(self.render_button)

        self.hbox_layout = QtGui.QHBoxLayout()
        self.hbox_layout.addWidget(self.image_label)
        self.hbox_layout.addLayout(self.render_log_vbox_layout)

        self.main_vbox_layout = QtGui.QVBoxLayout()
        self.main_vbox_layout.addLayout(self.hbox_layout)
        self.main_vbox_layout.addStretch(1)
        self.main_vbox_layout.addLayout(self.render_hbox_layout)

        self.setLayout(self.main_vbox_layout)

    def setup_signal(self):
        self.color_button.clicked.connect(self.select_color)
        self.render_button.clicked.connect(self.render)

    def select_color(self):
        color = QtGui.QColorDialog.getColor()
        if color.isValid():
            rgb_color = color.getRgb()
            r = float(rgb_color[0]) / 255.0
            g = float(rgb_color[1]) / 255.0
            b = float(rgb_color[2]) / 255.0
            self.render_viewer.set_render_colr(color=[r, g, b])
            bg = "background-color: rgb({r}, {g}, {b})".format(r=rgb_color[0], g=rgb_color[1], b=rgb_color[2])
            self.color_button.setStyleSheet("QPushButton " + "{" + bg + "}")

    def render(self):
        #   Generate rib file.
        self.render_viewer.generate_rib_file()

        #   Render to disk.
        self.render_viewer.render_to_disk()

        #   Display render log to the UI.
        self.render_log = self.render_viewer.get_render_log_data()
        render_log = '\n'.join(self.render_log)
        self.render_log_textedit.setText(render_log)

        #   Display render image to the UI.
        image_file_path = self.render_viewer.image_full_path
        self.image_label.clear()
        pixmap = QtGui.QPixmap(image_file_path)
        scaled_pixmap = pixmap.scaled(512, 512)
        self.image_label.setPixmap(scaled_pixmap)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = RenderViewerUI()
    win.show()
    sys.exit(app.exec_())
