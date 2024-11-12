# Component Specification

# Software Components
## 1.Image Input Manager
This component allows users to select and load medical image files from their device. It checks that the file format is compatible and handles error messages for unsupported or corrupted files.
### a.Purpose: 
Manages loading of medical images into the GUI for display and annotation.
### b.Input: 
Path to a medical image file (e.g., png or jpg format).
### c.Output: 
Display of the loaded image in the GUI.

## 2.Point Annotation Manager
This component processes user interactions on the displayed image, allowing users to click to add key points, drag to adjust point positions, and delete points as needed. The component saves each point’s coordinates for later use by the contour generation engine.
### a.Purpose:
Enables users to mark, adjust, or remove key points on the image to define regions of interest for contour generation.
### b.Input: 
User interactions (mouse clicks, drags) on the image display.
### c.Output: 
Visual markers on the image representing key points, stored for contour generation.

## 3.Contour Generation Engine (main part)
This component processes the coordinates of the marked key points, using interpolation or curve-fitting algorithms (e.g., Live wire, Active Contour Model, or deep learning based models ) to generate a contour that follows the shape indicated by the points. It then renders the contour on the image in real-time.
### a.Purpose: 
Generates a smooth contour based on the user-marked key points.
### b.Input: 
Coordinates of key points provided by the Point Annotation Manager.
### c.Output: 
A contour line displayed on the image that follows the key points.
 
## 4.Contour Update Manager
This component reprocesses the modified key points whenever the user adjusts, adds, or deletes points, dynamically updating the contour. It enables iterative refinement, ensuring the contour accurately reflects user intentions before saving.
### a.Purpose: 
Allows users to adjust key points to refine the contour and then generates an updated contour.
### b.Input: 
Adjusted coordinates from the Point Annotation Manager.
### c.Output: 
A revised contour line displayed on the image.

## 5.Contour Save Manager
This component saves the finalized contour and key point data to a file format specified by the user, such as JSON or CSV, ensuring data can be reused or analyzed further.
### a.Purpose: 
Manages saving of the finalized contour and key points for future use or analysis.
### b.Input: 
Final contour and key points data.
### c.Output: 
Saved data file containing contour and key points.

## 6.User Interface Manager
This component handles the GUI elements, facilitating user interactions such as loading images, marking points, updating contours, and saving results. It provides a cohesive interface, ensuring the annotation workflow is user-friendly.

### a.Purpose: 
Manages all GUI components, including image display, annotation controls, and save/update options.
### b.Input: 
User interactions (e.g., selecting options, clicking buttons).
### c.Output: 
GUI updates and responses, including image display, contour visualization, and feedback/error messages.

# Interactions between components to achieve use cases
The user begins by selecting a medical image file through an interactive file dialog in the User Interface Manager. Once the file is chosen, the Image Input Manager loads it, converting the image into a grayscale matrix of pixel intensity values, which is displayed in the GUI, allowing the user to start marking key points. As the user places key points on the image, the Point Annotation Manager records each point’s coordinates and grayscale values, storing this data to inform the contour generation process. The Contour Generation Engine then uses these key points and the image data to generate a smooth, fitted contour, displayed alongside the original image for easy comparison and refinement. The user has the option to adjust, add, or remove key points, prompting an automatic update of the contour to reflect the changes. Once the user is satisfied with the contour, they can save the final contour and key point data through the Contour Save Manager, storing it in a chosen format for future reference or further analysis.

# Preliminary project plan
## 1.Setup, basic GUI development and image loading（1 week）
### a.Configure the development environment and install required libraries
### b.Develop a basic GUI layout
### c.Implement the Image Input Manager to load and display images

## 2.Key points annotation, saving, and deletion（1 week）
### a.Capture mouse clicks for image-based coordinates
### b.Display and save coordinates with grayscale values
### c.Add and delete key points:

## 3.Contour generation and optimization（1 week）
### a.Research and experiment with suitable contour generation Methods
### b.Perform optimization

## 4.Project optimization and data saving（1 week）