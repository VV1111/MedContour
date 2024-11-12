# Functional Specification

# background
Contour annotation on medical images is essential for clinical and research applications, such as analyzing tissue shapes, tracking structural changes, and aiding in disease diagnosis. However, manual contouring is time-consuming and demands expertise, as it typically involves painstakingly placing and connecting points to outline anatomical structures accurately. This process can be especially challenging in clinical settings, where efficiency and precision are paramount.

This project aims to streamline this task by developing an intuitive graphical user interface (GUI) for automatic contour annotation. By allowing users to mark only a few key points on significant regions, the software will automatically generate and display a complete contour based on these points. This approach is designed to make contouring faster.

# User Profile
The target users are medical researchers and clinicians who need to annotate medical images quickly but may not have extensive programming experience. This software will provide a simplified GUI where users can interact with images through simple clicks without requiring knowledge of image processing algorithms or code. The software is also useful for computational biology students and researchers who need a quick and efficient way to generate image contours.


# Use Cases
## Use case 1:
### a.Select and Display Medical Image
The user selects a medical image, and the software displays it in the GUI, preparing it for annotation.

    User selects the “Load Image” option in the GUI.
    The system prompts the user to choose an image file from their device.
    The selected image loads and displays in the GUI’s main view.
### b.Annotate Key Points on Image
User clicks on several key points on the displayed image to outline the area of interest.
    User clicks on the image.
    Each click adds a point, with visual markers appearing on the image to represent the points.
    users continue to add points as needed to outline the region.

### c.Generate and Display Contour
After marking key points, the system then automatically connects the points to create a smooth contour, which is displayed on the image.

    User clicks “Generate Contour” button from the GUI.
    The system processes the key points, generating a contour that closely fits the marked area.
    The contour is displayed on the image.

### d.Save or Revise Key Points and Generate Updated Contour
The User can either save the current set of key points and generated contour or make adjustments to the key points to refine the contour. After making changes, the system regenerates and displays an updated contour based on the revised points.

    The user reviews the generated contour and decides to either save it or make adjustments.
    To adjust, the user selects and moves, adds, or deletes specific key points on the image.
    After making adjustments, the user clicks “Update Contour” to regenerate the contour based on the revised key points.
    The updated contour is displayed on the image, and the user has the option to save it or continue refining