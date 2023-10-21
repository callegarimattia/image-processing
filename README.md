# OpenCV Document Scanner

The OpenCV Document Scanner is a Python utility that enables you to convert photos of documents into high-quality scans. This tool leverages the OpenCV library, a powerful computer vision library, to process and enhance your images, making them look like professionally scanned documents. Whether you're digitizing important paperwork, receipts, or handwritten notes, this utility can help you achieve clear and crisp results.

## Features

- Automatic edge detection and cropping to isolate the document from the background.
- Perspective correction to rectify tilted or skewed documents.
- Enhances image quality through adaptive thresholding and contrast adjustments.
- Supports various image formats, including JPEG, PNG, and more. (IN PROGRESS)
- Easy-to-use Python script for quick conversion of photos into scans.

## Requirements

Before using this utility, ensure you have the following prerequisites:

- Python 3.11
- OpenCV library (cv2)
- NumPy
- argparse
- imutils

You can install the required Python packages using pipenv inside the root of the repository:

```bash
pipenv install
```

## Usage

1. Clone this repository

2. Place the photos of your documents in a folder or directory.

3. Open a terminal and navigate to the folder containing `Image2Scan.py`.

4. Run the script using the following command, providing the path to your input images:

```bash
python Image2Scan.py --input input_folder 
```

Replace `input_folder` with the path to your folder containing the photos of documents.

The script will process each image, apply document detection and correction, and save the resulting scans in the same folder.

## Example

```bash
python Image2Scan.py --input my_photos 
```

This will process all images in the `my_photos` folder and save the scanned documents in the same folder.

## Contributing

If you have suggestions for improvements or find any issues, please open an issue or submit a pull request on the [GitHub repository](https://github.com/your-username/opencv-document-scanner). Your contributions are highly appreciated!

## Acknowledgments

- This utility is inspired by various open-source document scanning projects and the power of the OpenCV library.

Enjoy converting your photos into high-quality scans with the OpenCV Document Scanner!
