
# Image Segmentation Package

This package provides a user-friendly graphical user interface (GUI) for automatic contour annotation on medical images. Users can mark key points on the image by clicking, and the software will automatically generate and display the contour based on these key points.

## Features

- **Main Application**: The core functionality of the package provides an interface for running image segmentation tasks.
- **GUI Application**: A PyQt5-based GUI to visualize and interact with segmentation results.
- **Utility Functions**: Includes a set of utility functions for image processing, such as handling images and interacting with medical imaging data.

## Components

The package consists of several key components:

1. **Image Input Manager**: Manages loading medical image files, checks file formats, and displays them in the GUI.
2. **Point Annotation Manager**: Allows users to annotate key points on the image by clicking, dragging, or deleting points.
3. **Contour Generation Engine**: Uses the annotated key points to generate a smooth contour on the image.
4. **Contour Update Manager**: Updates the contour when the user modifies the key points.
5. **Contour Save Manager**: Saves the final contour and key point data to a user-specified file format.
6. **User Interface Manager**: Handles the GUI elements, ensuring smooth interactions and updates between the user and the application.

### Interactions Between Components

- **Image Input Manager**: Loads and displays the medical image.
- **Point Annotation Manager**: Records user-clicked key points on the image for contour generation.
- **Contour Generation Engine**: Creates a contour based on the annotated key points.
- **Contour Update Manager**: Allows users to refine contours by adjusting points.
- **Contour Save Manager**: Saves the final contour and key points.


### Structure:
- **`medicalcontour/`**: This is the main directory containing the Python modules that implement the core functionality of the image segmentation package.
  - **`__init__.py`**: Makes `medicalcontour` a Python package.
  - **`main.py`**: Contains the main logic for running the segmentation tasks.
  - **`utils.py`**: Contains utility functions to handle image processing and other helper methods.
  - **`TestImageSegmentationApp.py`**: Contains the PyQt5 code for the graphical user interface (GUI) for testing image segmentation.
- **`example/`**: This folder contains example files used for testing or demonstrating the segmentation package. For example, it may include sample medical images.
- **`requirements.txt`**: This file lists the Python libraries and their versions required to run the project.
- **`setup.py`**: This is the setup script to install the package.
- **`README.md`**: Project description and documentation.

## Installation

### Prerequisites

To use this package, you need to have Python 3.6 or higher installed. The package also requires several Python libraries that are listed in the `requirements.txt` file.

### Steps

1. Clone this repository or download the package.
2. Navigate to the package directory where `setup.py` is located.
3. Install the package and dependencies using pip:

   ```bash
   pip install .


Alternatively, you can install the dependencies directly using:
    
    pip install -r requirements.txt

Usage
Running the Main Application
To run the main application (which is likely a command-line interface or core functionality of the package), use the following command:

    python -m medicalcontour.main

This will execute the main() function in the main.py file, starting the primary functionality of the segmentation application.

Running the GUI Application
If you would like to test the segmentation with a graphical user interface, run the GUI application using:
    python -m medicalcontour.TestImageSegmentationApp
This will open the GUI window where you can interact with the segmentation process.

Utility Functions
To use utility functions from utils.py, simply import them into your script:

    import medicalcontour.utils as utils


