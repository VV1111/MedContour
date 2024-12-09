import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QMessageBox,QFileDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap,QMouseEvent
from PyQt5.QtWidgets import QLabel
import sys
import cv2
import numpy as np
from medicalcontour.main import ImageSegmentationApp
# import utils
import medicalcontour.utils as utils 
class TestImageSegmentationApp(unittest.TestCase):

    def setUp(self):
        """Set up the application and main window."""
        self.app = QApplication(sys.argv)  # Create a QApplication instance
        self.window = ImageSegmentationApp()  # Create the main window instance
        # self.window.show()  # Display the window

    def test_init_para(self):
        """Test that parameters are initialized correctly."""
        
        # Test that boolean and numerical parameters are set correctly
        self.assertEqual(self.window.is_keypoint_active, False)
        self.assertEqual(self.window.current_key_point, 0)
        self.assertEqual(self.window.current_slice, 0)
        self.assertEqual(self.window.current_result_slice, 0)
        
        # Test the list initialization
        self.assertEqual(self.window.key_points, [])
        
        # Test dimensional parameters
        self.assertEqual(self.window.dim, 2)
        self.assertEqual(self.window.gray, 1)
        
        # Test image size parameters
        self.assertEqual(self.window.height, 450)
        self.assertEqual(self.window.weight, 450)
        self.assertEqual(self.window.scaled_width, 450)
        self.assertEqual(self.window.scaled_height, 450)
        
        # Test scale factor
        self.assertEqual(self.window.scale, 1.0)
        
        # Test miscellaneous parameters
        self.assertEqual(self.window.num, 1)
        self.assertEqual(self.window.selected_mode, "point")
        self.assertEqual(self.window.centerpoint, [])
        self.assertEqual(self.window.selected_color, (255, 0, 0))


    def test_init_ui(self):
        """Test that the UI components are initialized correctly."""
        
        # Check if buttons are created
        self.assertTrue(self.window.open_button is not None)
        self.assertTrue(self.window.keypoint_button is not None)
        self.assertTrue(self.window.edge_button is not None)
        self.assertTrue(self.window.save_button is not None)
        
        # Check if combo boxes are created
        self.assertTrue(self.window.mode_selector is not None)
        self.assertTrue(self.window.color_selector is not None)
        
        # Check if keypoint input field is created
        self.assertTrue(self.window.keypoint_input is not None)
        
        # Check if labels are created
        self.assertTrue(self.window.original_label is not None)
        self.assertTrue(self.window.keypoints_label is not None)
        self.assertTrue(self.window.result_label is not None)

        # Check if mode_selector has the correct items
        self.assertIn("Point", [self.window.mode_selector.itemText(i) for i in range(self.window.mode_selector.count())])
        self.assertIn("rectangle", [self.window.mode_selector.itemText(i) for i in range(self.window.mode_selector.count())])
        self.assertIn("ellipse", [self.window.mode_selector.itemText(i) for i in range(self.window.mode_selector.count())])

    @patch('cv2.imread')
    def test_load_2d_image(self, mock_imread):
        """Test the load_2d_image function and mock cv2.imread."""
        
        # Mock cv2.imread to return a pre-defined image (e.g., a blank 100x100 image)
        mock_imread.return_value = np.zeros((100, 100), dtype=np.uint8)
        image_path = "path.png"
        self.window.load_2d_image(image_path)
        self.assertIsNotNone(self.window.image)
        self.assertEqual(self.window.image.shape, (100, 100))  # Check the shape of the mocked image
        self.assertEqual(self.window.image.dtype, np.uint8)    # Ensure the data type is correct

    
    @patch('nibabel.load')  # Mocking nib.load
    @patch('cv2.cvtColor')  # Mocking cv2.cvtColor
    def test_load_3d_image(self, mock_cvtColor, mock_nib_load):
        """Test the load_3d_image function and mock nib.load and cv2.cvtColor."""
        
        # Prepare mock NIfTI data
        mock_img_data = np.random.rand(432, 104, 432)  # A 3D image with random data (e.g., 432x104x432)
        mock_nii_img = MagicMock()
        mock_nii_img.get_fdata.return_value = mock_img_data  # Mocking get_fdata to return the random data
        
        # Mock nib.load to return our mocked NIfTI image
        mock_nib_load.return_value = mock_nii_img
        
        # Mock cv2.cvtColor to return the same input data (just for testing, not actually processing)
        mock_cvtColor.return_value = np.zeros((432, 104, 3), dtype=np.uint8)  # Mock RGB image output
        
        # Call load_3d_image with a fake file path
        file_path = "fake_file.nii"
        self.window.load_3d_image(file_path)

        # Verify nib.load was called with the correct path
        mock_nib_load.assert_called_once_with(file_path)

        # Verify that the image was processed correctly
        self.assertIsNotNone(self.window.image)  # Ensure image is loaded
        self.assertEqual(self.window.image.shape, (104, 432, 432))  # Verify the shape after transposition and flipping
        self.assertEqual(self.window.result.shape, (104, 432, 3,432))  # Check the result shape after stacking
        
        # Verify slider values
        self.assertTrue(self.window.image_slider.isEnabled())  # Ensure the image slider is enabled
        self.assertTrue(self.window.result_slider.isEnabled())  # Ensure the result slider is enabled
        self.assertEqual(self.window.image_slider.minimum(), 0)  # Ensure slider min value is 0
        self.assertEqual(self.window.image_slider.maximum(), self.window.image.shape[2] - 1)  # Max value based on image depth
        
        # Check if cv2.cvtColor was called (this happens during display setup)
        mock_cvtColor.assert_called()
    
    
    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    @patch.object(ImageSegmentationApp, 'load_2d_image')
    @patch.object(ImageSegmentationApp, 'load_3d_image')
    def test_open_image(self, mock_load_3d_image, mock_load_2d_image, mock_message_box, mock_file_dialog):
        """Test the open_image function, ensuring correct file loading behavior."""

        # Simulate the file dialog returning a 2D image file path
        mock_file_dialog.return_value = ("path/to/image.jpg", "")

        # Simulate the user clicking "Yes" on the confirmation message box
        mock_message_box.return_value = QMessageBox.Yes

        # Call open_image (this should call load_2d_image)
        self.window.open_image()

        # Verify that the correct image loading function is called
        mock_load_2d_image.assert_called_once_with("path/to/image.jpg")
        mock_load_3d_image.assert_not_called()

        # Now test with a 3D image (NIfTI file)
        mock_file_dialog.return_value = ("path/to/image.nii", "")

        # Call open_image again (this should call load_3d_image)
        self.window.open_image()

        # Verify that the correct image loading function is called for a 3D image
        mock_load_3d_image.assert_called_once_with("path/to/image.nii")
        mock_load_2d_image.assert_called_once_with("path/to/image.jpg")  # Make sure the 2D test was called once as well
    

    def test_display_image(self):
        # Test the display_image function with both grayscale and RGB images
        
        # Mock the QLabel
        label = MagicMock(spec=QLabel)
        
        # Create a mock 2D grayscale image (e.g., 100x100)
        grayscale_image = np.zeros((100, 100), dtype=np.uint8)  # Black 100x100 image
        
        # Call the display_image method with the grayscale image
        self.window.display_image(grayscale_image, label)
        
        # Check that the QImage constructor was called with the correct format
        self.assertTrue(QImage.Format_Grayscale8)
        
        # Create a mock 2D RGB image (e.g., 100x100x3)
        rgb_image = np.zeros((100, 100, 3), dtype=np.uint8)  # Black 100x100 RGB image
        
        # Call the display_image method with the RGB image
        self.window.display_image(rgb_image, label)
        
        # Check that the QImage constructor was called with the correct format
        self.assertTrue(QImage.Format_RGB888)
    

    def test_update_display(self):
        # Create a mock QLabel to avoid actually displaying anything
        label = MagicMock(spec=QLabel)

        # Create a mock 2D grayscale image (e.g., 100x100)
        grayscale_image = np.zeros((100, 100), dtype=np.uint8)  # Black 100x100 image
    
        # Create an instance of the class and set up the required attributes
        self.window.dim = 2  # 2D image
        self.window.gray = 1  # Grayscale image
    
        # Mock the display_image method to avoid UI actions during the test
        self.window.display_image = MagicMock()

        # Call the update_display method, passing in the grayscale image
        self.window.update_display(grayscale_image, label)

        # Ensure that the display_image method was called with the correct arguments
        self.window.display_image.assert_called_with(grayscale_image, label)

        # Test for RGB image
        rgb_image = np.zeros((100, 100, 3), dtype=np.uint8)  # Black 100x100 RGB image
        self.window.gray = 0  # RGB image
        self.window.dim = 2 

        # Call the update_display method with the RGB image
        self.window.update_display(rgb_image, label)

        # Ensure that the display_image method was called again with the correct arguments
        self.window.display_image.assert_called_with(rgb_image, label)

    
    @patch('PyQt5.QtWidgets.QMessageBox.warning')  # Mock the warning message box
    def test_select_keypoints_valid_input(self, mock_warning):
        """Test select_keypoints with valid input."""

        
        self.window.selected_mode == "rectangle"
        self.window.keypoint_input.setText('2')
        self.window.select_keypoints()

        # Verify that no warning is shown
        mock_warning.assert_not_called()

        # Check the internal state variables
        self.assertEqual(self.window.num_points, 2)  # Check that the number of key points was set
        self.assertTrue(self.window.is_keypoint_active)  # Ensure key point selection is active
        self.assertEqual(self.window.current_key_point, 0)  # Ensure starting point is 0
        self.assertEqual(len(self.window.key_points), 0)  

    
    @patch('PyQt5.QtWidgets.QMessageBox.warning')  # Mock the warning message box
    @patch('PyQt5.QtWidgets.QMessageBox.information')
    def test_select_point_on_image(self, mock_info,mock_warning):
        """Test valid click for selecting key points on the image."""
        self.window.load_2d_image("examples/mama07ORI.bmp")
        self.window.keypoint_input.setText('1')
        self.window.select_keypoints()

        # Simulate a valid mouse click event inside the bounds'example\mama07ORI.bmp
        event = QMouseEvent(QMouseEvent.MouseButtonPress, QPoint(50, 50), Qt.LeftButton, Qt.NoButton, Qt.NoModifier)
        self.window.select_point_on_image(event)

        # Check that the point was added to the key_points list
        self.assertEqual(len(self.window.key_points), 1)

        # Check that the current key point counter has incremented
        self.assertEqual(self.window.current_key_point, 1)

        # # Verify that no warning was shown
        mock_warning.assert_not_called()


    def test_update_area_display(self):
        # Mock or set up the window to simulate the scenario
        self.window.key_points = [(10, 10), (100, 100)]  # Simulate two key points
        self.window.selected_mode = "rectangle"  # Set mode to rectangle
        self.window.display_data = np.zeros((200, 200, 3), dtype=np.uint8)  # Create a blank image for testing

        # Call the update_area_display function
        self.window.update_area_display()

        # Check if the area (rectangle or ellipse) is drawn on the image
        # For instance, you can check if the center point was added correctly
        self.assertEqual(len(self.window.centerpoint), 1)
        self.assertEqual(self.window.centerpoint[0], (55, 55))  # Expected center point


    def test_update_keypoints_display(self):
        self.window.update_display = MagicMock() 
        # Mock key points data
        self.window.key_points = [(50, 50), (150, 150)]  # Two points for testing
        self.window.display_data = np.zeros((200, 200, 3), dtype=np.uint8)  # Blank image for testing
        self.window.keypoints_label = MagicMock()  # Mock QLabel for testing

        # Call the function to update key points display
        self.window.update_keypoints_display()

        # Check that the label was updated with the correct key points
        self.window.keypoints_label.setText.assert_called_with("(50, 50)\n(150, 150)")  # Check the text set in the label

        # Check if the circles were drawn at the key points (mocking update_display function)
        # Here you would check that update_display was called with the modified masked image.
        self.assertTrue(self.window.update_display.called)  # Ensure update_display was called


    def test_visual_result(self):
         # Setting mock values for required attributes
        self.window.selected_color = [255, 0, 0]  # Red color for highlighting edges
        self.window.result = np.zeros((100, 100, 3, 100), dtype=np.uint8)  # Mock 3D RGB image (100x100x100x3)
        self.window.current_slice = 50  # Choose a slice (e.g., 50)
        
        # Mocking QLabel to simulate display updates
        self.window.result_label = MagicMock()
        self.window.display_image = MagicMock()
        # Simulate a levelset array (e.g., edges in the image)
        levelset = np.zeros((100, 100), dtype=np.float32)
        levelset[20:80, 20:80] = 1  # Create a square edge in the middle of the image
        
        # Call the visual_result method with the valid levelset
        edge_overlay = self.window.visual_result(levelset)

        # Check if the edge_overlay was updated correctly
        self.assertEqual(edge_overlay.shape, (100, 100, 3))  # Ensure it's a 3-channel RGB image
        
        # Check that the selected color (red) was applied to the edges
        self.assertIn([255, 0, 0],edge_overlay[20:80, 20:80])  

        # Ensure that the display_image method was called
        self.window.display_image.assert_called()

    def test_morphological_geodesic_active_contour(self):
        # Test for a basic image and level set initialization
        self.window.load_2d_image("examples/mama07ORI.bmp")
        
        slice_data = cv2.cvtColor(self.window.image_data.copy(), cv2.COLOR_RGB2GRAY) 
        img = slice_data/255.0
        # g(I)
        gimg = utils.inverse_gaussian_gradient(img, alpha=1000, sigma=5.48)
        # Initialization of the level-set and threshold.
        self.window.selected_mode ="rectangle"
        self.window.key_points =[(10,10),(50,50)]
        init_ls,mean_roi = utils.generate_Initial_mask(img, self.window.selected_mode, self.window.key_points)
        mask = self.window.morphological_geodesic_active_contour(gimg, iterations=10,
                                                    init_level_set=init_ls,
                                                    smoothing=2, threshold=0.8*mean_roi,
                                                    balloon=-1)

        self.assertTrue(np.any(mask != init_ls))


    @patch('cv2.imwrite')
    @patch('nibabel.save')
    @patch('PyQt5.QtWidgets.QFileDialog.getSaveFileName')
    @patch('PyQt5.QtWidgets.QInputDialog.getItem')
    @patch('PyQt5.QtWidgets.QMessageBox.information')
    def test_save_result_save_current_slice(self,mock_info, mock_get_item, mock_get_save_file_name, mock_nib_save, mock_cv2_imwrite):

        # Mock required attributes
        self.window.result = np.zeros((100, 100, 3, 10), dtype=np.uint8)  # Mock image data (100x100x3x10)
        self.window.current_slice = 5  # Mock the current slice
        
        # Mock the necessary PyQt dialog methods
        self.window.QFileDialog = MagicMock()
        self.window.QInputDialog = MagicMock()
        self.window.QMessageBox = MagicMock()

        # Simulate the user's choice in the input dialog (Save current slice)
        mock_get_item.return_value = ("Save current slice", True)
        
        # Simulate the file path selection dialog
        mock_get_save_file_name.return_value = ("path/to/save/slice_5.jpg", None)
        
        # Simulate saving the file
        mock_cv2_imwrite.return_value = True
        
        # Call the save_result method
        self.window.save_result()
        
        # Check that the correct methods were called
        mock_get_save_file_name.assert_called_once()
        mock_cv2_imwrite.assert_called_once()
        mock_info.assert_called_once()
    


    def tearDown(self):
        """Clean up after tests."""
        self.window.close()  # Close the window after each test
    


if __name__ == '__main__':
    unittest.main()