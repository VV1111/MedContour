
# medical contour extraction Package

This package provides a user-friendly graphical user interface (GUI) for automatic contour annotation on medical images. Users can mark key points on the image by clicking, and the software will automatically generate and display the contour based on these key points.

## Features

- **Main Application**: The core functionality of the package provides an interface for automatic contour annotation on medical images.
- **GUI Application**: A PyQt5-based GUI to visualize and interact with contour extraction results.
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
├──  **`medicalcontour/`**: This is the main directory containing the Python modules that implement the core functionality of the medical contour extraction package.

│ ├── **`__init__.py`**: Makes `medicalcontour` a Python package.

│ ├── **`main.py`**: Contains the main logic for running the  medical contour extraction tasks.

│ ├── **`utils.py`**: Contains utility functions to handle image processing and other helper methods.

│ ├── **`Testcomponent.py`**: Contains the PyQt5 code for the graphical user interface (GUI) for testing image  medical contour extraction.

├──  **`example/`**: This folder contains example files used for testing or demonstrating the s medical contour extraction package. For example, it includes sample medical images.

├──  **`docs/`**:

│ ├── **`Component Specification.md`**:

│ ├── **`Functional Specification.md`**:

│ ├── **`present.pdf`**:

├── **`requirements.txt`**: This file lists the Python libraries and their versions required to run the project.

├── **`setup.py`**: This is the setup script to install the package.

├── **`demo.mov`**: To see the capabilities of the medical contour extraction tool in action, you can check out the demo below. The demo demonstrates the core functionality of the medical contour extraction and its graphical user interface:

├── **`README.md`**: Project description and documentation.

<!-- medicalcontour/ 
├── medicalcontour/ # Main package folder 
│ ├── init.py # Package initialization file 

│ ├── main.py # Main application file 

│ ├── utils.py # Utility functions 

│ └── TestImageSegmentationApp.py # GUI application code

├── example/ # Example images or data 
│ ├──slice.png
│ ├── volume-2.nii.gz # Example medical image 
├── requirements.txt # Project dependencies 
├── setup.py # Installation script 
├── README.md # Project description and documentation  -->



## Installation

### Prerequisites

To use this package, you need to have Python 3.6 or higher installed. The package also requires several Python libraries that are listed in the `requirements.txt` file.

### Steps

1. Clone this repository or download the package.
2. Navigate to the package directory where `setup.py` is located.
3. Install the package and dependencies using pip:

   ```bash
   pip install medicalcontour


Alternatively, you can install the dependencies directly using:
    
    pip install -r requirements.txt

Usage
Running the Main Application
To run the main application (which is likely a command-line interface or core functionality of the package), use the following command:

    
    from medicalcontour.main import main

    main()

    # or
    python -m medicalcontour.main 

This will execute the main() function in the main.py file, starting the primary functionality of the medical contour extraction application.

Running the GUI Application
If you would like to test the  medical contour extraction with a graphical user interface, run the GUI application using:
    python -m medicalcontour.Testcomponent
This will open the GUI window where you can interact with the  medical contour extraction process.

Utility Functions
To use utility functions from utils.py, simply import them into your script:

    import medicalcontour.utils as utils


