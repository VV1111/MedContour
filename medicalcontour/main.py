import cv2
import numpy as np
import nibabel as nib
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QSlider, QLineEdit, QMessageBox, QWidget,QInputDialog,QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QMouseEvent

import os

import utils
from matplotlib import pyplot as plt
from scipy import ndimage as ndi

# set parameters
SIZES = {
    "window_size": (1600, 600),  # window_size
    "button_size": (150, 30),   # button_size
    "text_size": (250, 30),  # text_size
    "img_size": (450, 400),  # img_size
    "coordinate_box_size": (160, 400),  # coordinate_box_size
    "slider_size":(450,),
}


class ImageSegmentationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_para()
        # self.image_data = None
        # self.result_data = None



    def init_para(self):
        self.is_keypoint_active =False
        self.current_key_point = 0  # 当前点击计数
        self.current_slice = 0
        self.current_result_slice = 0
        self.key_points = []
        self.dim = 2
        self.gray = 1
        self.height = 450
        self.weight = 450
        self.scaled_width  = 450
        self.scaled_height = 450
        self.scale = 1.0
        self.num = 1
        self.selected_mode = "point"  # Default to point mode for keypoints/area
        self.centerpoint = []
        self.selected_color = (255, 0, 0) 

    def init_ui(self):
        """initial window"""
        self.setWindowTitle("Medical Image Segmentation")
        self.setGeometry(200, 200,*SIZES["window_size"])

        # main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # first line: control button
        control_layout = QHBoxLayout()
        self.open_button = QPushButton("Open File")
        self.open_button.setFixedSize(*SIZES["button_size"])
        self.open_button.clicked.connect(self.open_image)

        # Mode selection (Point/rectangle)
        self.mode_selector = QComboBox()
        self.mode_selector.addItem("Point")
        self.mode_selector.addItem("rectangle")
        self.mode_selector.addItem("ellipse")
        self.mode_selector.currentTextChanged.connect(self.update_mode)
        self.mode_selector.setFixedSize(*SIZES["text_size"])



        self.keypoint_input = QLineEdit()
        self.keypoint_input.setPlaceholderText("Enter keypoint count (>=0)")
        self.keypoint_input.setFixedSize(*SIZES["text_size"])

        self.keypoint_button = QPushButton("Select Keypoints")
        self.keypoint_button.clicked.connect(self.select_keypoints)
        self.keypoint_button.setFixedSize(*SIZES["button_size"])

        self.color_selector = QComboBox()
        self.color_selector.addItems(["Red", "Green", "Blue", "Yellow", "Cyan", "Magenta"])
        self.color_selector.currentTextChanged.connect(self.select_color)
  

        self.edge_button = QPushButton("Centerline Detection")
        self.edge_button.clicked.connect(self.medcontour)
        self.edge_button.setFixedSize(*SIZES["button_size"])

        self.save_button = QPushButton("Save Result")
        self.save_button.clicked.connect(self.save_result)
        self.save_button.setFixedSize(*SIZES["button_size"])
        
        control_layout.addWidget(self.open_button)
        control_layout.addWidget(self.mode_selector)
        control_layout.addWidget(self.keypoint_input)
        control_layout.addWidget(self.keypoint_button)
        control_layout.addWidget(self.color_selector)
        control_layout.addWidget(self.edge_button)
        control_layout.addWidget(self.save_button)
        main_layout.addLayout(control_layout)

        # secoond line show images
        display_layout = QHBoxLayout()
        self.original_label = QLabel("Original Image")
        self.original_label.setFixedSize(*SIZES["img_size"])
        self.original_label.setStyleSheet("background-color: lightgray;")
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.mousePressEvent = self.select_point_on_image

        self.keypoints_label = QLabel("Keypoints Coordinates")
        self.keypoints_label.setFixedSize(*SIZES["coordinate_box_size"])
        self.keypoints_label.setStyleSheet("background-color: white;")
        self.keypoints_label.setAlignment(Qt.AlignTop)

        self.result_label = QLabel("Result Image")
        self.result_label.setFixedSize(*SIZES["img_size"])
        self.result_label.setStyleSheet("background-color: lightgray;")
        self.result_label.setAlignment(Qt.AlignCenter)

        display_layout.addWidget(self.original_label)
        display_layout.addWidget(self.keypoints_label)
        display_layout.addWidget(self.result_label)
        main_layout.addLayout(display_layout)

        # third line：sliders
        slider_layout = QHBoxLayout()
        self.image_slider = QSlider(Qt.Horizontal)
        self.image_slider.setEnabled(False)
        self.image_slider.setFixedWidth(*SIZES["slider_size"])
        self.image_slider.valueChanged.connect(self.update_image_slice)
        self.image_slice_info = QLabel("Slice: 0/0")

        self.result_slider = QSlider(Qt.Horizontal)
        self.result_slider.setEnabled(False)
        self.result_slider.setFixedWidth(*SIZES["slider_size"])
        self.result_slider.valueChanged.connect(self.update_result_slice)
        self.result_slice_info = QLabel("Result Slice: 0/0")

        slider_layout.addWidget(self.image_slider)
        slider_layout.addWidget(self.image_slice_info)
        slider_layout.addWidget(self.result_slider)
        slider_layout.addWidget(self.result_slice_info)
        main_layout.addLayout(slider_layout)

        self.setCentralWidget(central_widget)

    def open_image(self):
        """Open and load an image file, determining its type (2D or 3D) based on the file extension."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", 
            "All Files (*);;Images (*.jpg *.png *.bmp);;NIfTI Files (*.nii *.nii.gz)"
        )
        if file_path:
            reply = QMessageBox.warning(self, "Confirm Image", f"Are you sure you want to use this image?\n{file_path}",
                                          QMessageBox.No | QMessageBox.Yes)
            if reply == QMessageBox.Yes:                        
                self.init_para()
                if file_path.endswith(('.jpg', '.png', '.bmp')):
                    self.dim =2
                    self.load_2d_image(file_path)
                elif file_path.endswith(('.nii', '.nii.gz')):
                    self.dim =2
                    self.load_3d_image(file_path)

    def load_2d_image(self, file_path):
        """ Load a 2D medical image and preprocess it for display and interaction."""
        
        self.image = cv2.imread(file_path)
        if self.image is None:
            QMessageBox.warning(self, "Error", "Failed to load image.")
            return
        if len(self.image.shape) == 2:  # self.gray
            self.image_data = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_data =cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_result = self.display_data.copy()
            self.gray =1
        elif len(self.image.shape) == 3:
            self.image_data = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_data =cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_result = self.display_data.copy()
            self.gray = 0

        self.result = np.expand_dims(self.image_data, axis=-1)

        self.current_slice = 0
        self.image_slider.setEnabled(False)
        self.result_slider.setEnabled(False)
        self.update_display(self.display_data,self.original_label)
        self.update_display(self.display_result,self.result_label)

    def load_3d_image(self, file_path):
        """ Load a 3D medical image and preprocess it for display and interaction."""
            
        self.dim =3
        nii_img = nib.load(file_path)
        self.image = nii_img.get_fdata()
        self.image = utils.normalize(self.image)
        if len(self.image.shape)==3:
            self.gray = 1 
            # print(self.image.shape) # (432, 104, 432)
            
            # self.image = np.transpose(self.image,(0,2,1))
            self.image = np.transpose(self.image,(1,0,2))
            self.image = np.flip(self.image, axis=0) 
            # print(self.image.shape)

            self.result = np.stack([self.image] * 3, axis=2)
            self.image_data = cv2.cvtColor(self.image[:, :, self.current_slice], cv2.COLOR_GRAY2RGB)
            self.display_data = cv2.cvtColor(self.image[:, :, self.current_slice], cv2.COLOR_GRAY2RGB)
            self.display_result = self.display_data.copy()
            self.current_slice = 0

            self.image_slider.setEnabled(True)
            self.result_slider.setEnabled(True)
            self.image_slider.setMinimum(0)
            self.image_slider.setMaximum(self.image.shape[2] - 1)
            self.result_slider.setMinimum(0)
            self.result_slider.setMaximum(self.image.shape[2] - 1)
            # self.update_display()
            self.image_slider.valueChanged.connect(self.update_image_slice)
            self.result_slider.valueChanged.connect(self.update_result_slice)

            self.update_display(self.display_data,self.original_label)
            self.update_display(self.display_result ,self.result_label)

    def update_image_slice(self, value):
        """Update the display for the selected image slice."""
        self.current_slice = value
        self.image_data = cv2.cvtColor(self.image[:, :, self.current_slice], cv2.COLOR_GRAY2RGB)
        self.display_data = cv2.cvtColor(self.image[:, :, self.current_slice], cv2.COLOR_GRAY2RGB)
        self.image_slice_info.setText(f"slice: {self.current_slice + 1}/{self.image.shape[-1]}")
        self.update_display(self.display_data,self.original_label)

    def update_result_slice(self, value):
        """Update the result display for the selected slice index"""

        self.current_result_slice = value
        self.display_result =self.result[..., self.current_result_slice]
        self.result_slice_info.setText(f"slice: {self.current_result_slice + 1}/{self.image.shape[-1]}")
        self.update_display(self.display_result ,self.result_label)

    def update_display(self,display_input,label):
        if display_input is not None:
            # For 2D Image-gray
            if self.dim == 2 and self.gray ==1:
                self.display_image(display_input, label)
            # For 2D-RGB 
            elif self.dim ==2 and self.gray ==0:

                self.display_image(display_input, label)
            # For 3D Image
            elif self.dim ==3 and self.gray ==1:
               self.display_image(display_input, label)

    def display_image(self, img, label):
        if len(img.shape) == 2:  # Grayscale image
            self.height, self.width = img.shape
            q_image = QImage(img.data.tobytes(), self.width, self.height, self.width, QImage.Format_Grayscale8)
        else:  # RGB image
            self.height, self.width, _ = img.shape
            # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            q_image = QImage(img.data.tobytes(), self.width, self.height, 3 * self.width, QImage.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio))


    def update_mode(self, mode):
        """ Update the mode based on the selection (Point or rectangle) """
        self.selected_mode = mode

    def select_color(self, color_name):
        """Update the contour color based on the user's selected choice"""
        color_map = {
            "Red": (255, 0, 0),
            "Green": (0, 255, 0),
            "Blue": (0, 0, 255),
            "Yellow": (255, 255, 0),
            "Cyan": (0, 255, 255),
            "Magenta": (255, 0, 255),
        }
        self.selected_color = color_map.get(color_name, (255, 0, 0))


    def select_keypoints(self):
        """Clears all selected key points and re-enables the selection process"""
        try:
            self.num_points = int(self.keypoint_input.text())

            if self.num_points < 0:
                raise ValueError("Key Point count must be greater than or equal to 0.")

            self.is_keypoint_active = True
            self.current_key_point = 0
            self.key_points = []



        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid number of keypoints.")
            return

        
    def select_point_on_image(self, event: QMouseEvent):
        """Updates the display of key points on the image."""
        if not self.image_data.any():
            return
        if not self.is_keypoint_active:
            QMessageBox.warning(self, "Not Ready", "Set the Key Point count first!")
            # return
        if self.current_key_point < int(self.keypoint_input.text()):

            x = event.pos().x()
            y = event.pos().y()
            x_ratio = self.original_label.width()/self.width
            y_ratio = self.original_label.height()/self.height
            scale = min(x_ratio, y_ratio)
            self.scale = scale

            self.scaled_width = int(self.width * scale)
            self.scaled_height = int(self.height* scale)

            offset_x = (self.original_label.width()-self.scaled_width)//2
            offset_y = (self.original_label.height()-self.scaled_height)//2

            if offset_x <= x <= offset_x + self.scaled_width and offset_y <= y <= offset_y + self.scaled_height:
                image_x = int((x - offset_x) / scale)
                image_y = int((y - offset_y) / scale)
                self.key_points.append((image_x, image_y))
                self.update_keypoints_display()   
                self.current_key_point += 1
                if self.current_key_point == int(self.keypoint_input.text()):
                    self.is_keypoint_active = False
                    QMessageBox.information(self, "Selection Complete", "You have selected all key points.")
                    if self.selected_mode == "rectangle" or self.selected_mode == "ellipse":  
                        self.update_area_display()
            else:
                QMessageBox.warning(self, "Error", "The clicked point is outside the bounds!")
                return   

        else:
            QMessageBox.information(self, "Selection Complete", "You have already selected all key points.")


    def update_area_display(self):
        """Update the display of key area"""
        masked = self.display_data.copy()
    
        assert len(self.key_points)==2
        [(x1, y1),(x2,y2)] = self.key_points
        top_left = (x1, y1)
        bottom_right = (x2,y2)
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        center = (center_x,center_y)   

        self.centerpoint.append(center)

        if self.selected_mode == "rectangle":
            masked = cv2.rectangle(masked, top_left, bottom_right, (255, 0, 0), 2)  # Green rectangle
        elif self.selected_mode == "ellipse":
            axes_length = (int(abs(x2 - x1) / 2) , 
                            int(abs(y2 - y1) / 2))

            masked = cv2.ellipse(masked, center, axes_length, angle=0, startAngle=0, endAngle=360, color=(0, 255, 0), thickness=2)
        cv2.circle(masked, center, 5, (255, 0, 0), -1)  # Red point for center
        self.update_display(masked,self.original_label)

    def update_keypoints_display(self):
        """Update the display of key points"""
        self.keypoints_label.setText("\n".join([f"({x}, {y})" for x, y in self.key_points]))       

        masked = self.display_data.copy()
        for point in self.key_points:
            cv2.circle(masked, point, 5, (255, 0, 0), -1)
        self.update_display(masked,self.original_label)



    def visual_result(self,levelset):
        self.display_result = self.result[..., self.current_slice]

        self.display_image(self.display_result, self.result_label) 

        edge_overlay = self.display_result.copy()
        if levelset is None or levelset.size == 0:
            print("Received invalid levelset.")
            return
        # Update the edge overlay
        edges =levelset > 0.5
        # edges = ndi.binary_dilation(edges)
        edges = edges ^ ndi.binary_erosion(edges)
        # Highlight the edges in red
        # edge_overlay[edges] = [255, 0, 0]
        edge_overlay[edges] = self.selected_color
        # Update the QLabel display
        self.display_image(edge_overlay, self.result_label)

        QApplication.processEvents()  # Ensure the GUI updates immediately

        return edge_overlay

    def morphological_geodesic_active_contour(self,gimage, iterations,
                                            init_level_set, smoothing=1,
                                            threshold=0.5, balloon=0):


        image = gimage
        init_level_set = init_level_set
        utils._check_input(image, init_level_set)

        structure = np.ones((3,) * len(image.shape), dtype=np.int8)
        dimage = np.gradient(image)
        # threshold_mask = image > threshold
        if balloon != 0:
            threshold_mask_balloon = image > threshold / np.abs(balloon)
        u = np.int8(init_level_set > 0)
        self.visual_result(u)
        for _ in range(iterations):
            # Balloon
            if balloon > 0:
                aux = ndi.binary_dilation(u, structure)
            elif balloon < 0:
                aux = ndi.binary_erosion(u, structure)
            if balloon != 0:
                u[threshold_mask_balloon] = aux[threshold_mask_balloon]

            # Image attachment
            aux = np.zeros_like(image)
            du = np.gradient(u)
            for el1, el2 in zip(dimage, du):
                aux += el1 * el2
            u[aux > 0] = 1
            u[aux < 0] = 0
            # Smoothing
            for _ in range(smoothing):
                u = utils._curvop(u)

            self.visual_result(u)
        return u


    def medcontour(self):
        if not self.key_points:
            QMessageBox.warning(self, "Error", "Please select keypoints before edge detection.")
            return
        if self.image_data is not None:
            slice_data = cv2.cvtColor(self.image_data.copy(), cv2.COLOR_RGB2GRAY) 
            img = slice_data/255.0
            # g(I)
            gimg = utils.inverse_gaussian_gradient(img, alpha=1000, sigma=5.48)
            # Initialization of the level-set and threshold.
            init_ls,mean_roi = utils.generate_Initial_mask(img, self.selected_mode, self.key_points)

            mask = self.morphological_geodesic_active_contour(gimg, iterations=10,
                                                    init_level_set=init_ls,
                                                    smoothing=2, threshold=0.8*mean_roi,
                                                    balloon=-1)  

            edge_overlay = self.visual_result(mask)
            self.display_result = cv2.addWeighted(self.display_data, 1, edge_overlay, 0.5, 0)
            self.result[..., self.current_slice] = self.display_result

    def save_result(self):
        # 弹出对话框让用户选择保存选项
        response, ok = QInputDialog.getItem(
            self, "Save Options", "Choose an option:", ["Save current slice", "Save all slices"], 0, False
        )
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Result", "", "NIfTI Files (*.nii);;Images (*.jpg *.png)")
        if not file_path:
            return
        
        if ok:
            if response == "Save current slice":
                # self.save_image(self.result[:, :, :, self.current_slice], f"slice_{self.current_slice}.nii")
                image_data = self.result[:, :, :, self.current_slice]
                cv2.imwrite(file_path, cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR))  # 转换为 BGR 格式，OpenCV 使用 BGR
                QMessageBox.information(self, "Save", f"Image saved as {file_path}")            
            elif response == "Save all slices":
                nii_image = nib.Nifti1Image(self.result, affine=np.eye(4))
                nib.save(nii_image, file_path)
                QMessageBox.information(self, "Save", f"Image saved as {file_path}")



if __name__ == "__main__":
    app = QApplication([])
    window = ImageSegmentationApp()
    window.show()
    app.exec_()
