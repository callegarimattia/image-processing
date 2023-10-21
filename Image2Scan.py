import argparse
import cv2
import numpy as np
import imutils


class Image2Scan:
    def main():
        parser = argparse.ArgumentParser(
            prog="image2scan", description="Convert image to scan"
        )
        parser.add_argument(
            "--i",
            "--image",
            type=str,
            help="Path to image",
            dest="image",
            default="defaultImage.jpg",
        )
        args = parser.parse_args()
        scan = Image2Scan().scan(args.image)
        cv2.imwrite("scan.jpg", scan)

    def scan(self, image):
        print("Converting image to scan...")
        image = cv2.imread(image)
        original = image.copy()
        cv2.imshow("Original", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        preprocessed = self.preprocessing(image)
        edged = self.find_edges(preprocessed)
        outline = self.find_outline(edged, original)
        warped = self.four_point_transform(image, outline.reshape(4, 2))
        scan = self.postprocessing(warped)
        return scan

    def preprocessing(self, image):
        print("Preprocessing image...")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        morphed = cv2.morphologyEx(
            blurred, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=10
        )
        cv2.imshow("Preprocessed", morphed)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return morphed

    def find_edges(self, image, sigma=0.33):
        print("Finding edges...")
        v = np.median(image)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
        cv2.imshow("Edged", edged)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return edged

    def find_outline(self, image, original):
        print("Finding outline...")
        cnts = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # if our approximated contour has four points, then we
            # can assume that we have found our document
            if len(approx) == 4:
                screenCnt = approx
                cv2.drawContours(original, [screenCnt], -1, (0, 255, 0), 10)
                cv2.imshow("Outline", original)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                return screenCnt
        return None

    def four_point_transform(self, image, pts):
        def order_points(pts):
            rect = np.zeros((4, 2), dtype="float32")
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]
            return rect

        print("Four point transform...")
        rect = order_points(pts)
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array(
            [
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1],
            ],
            dtype="float32",
        )

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        cv2.imshow("Warped", warped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return warped

    def postprocessing(self, image):
        print("Postprocessing image...")
        scan = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Scanned", imutils.resize(scan, height=650))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return scan


if __name__ == "__main__":
    Image2Scan.main()
