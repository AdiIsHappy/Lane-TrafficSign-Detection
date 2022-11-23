# Importing Python libraries
import numpy as np
import cv2
from moviepy.editor import VideoFileClip

def hsl_color_selection(image: np.array) -> np.array:
    # Convert the input image to HSL
    converted_image = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)

    # White color mask
    lower_threshold = np.uint8([0, 200, 0])
    upper_threshold = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(converted_image, lower_threshold, upper_threshold)

    # Yellow color mask
    lower_threshold = np.uint8([10, 0, 100])
    upper_threshold = np.uint8([40, 255, 255])
    yellow_mask = cv2.inRange(converted_image, lower_threshold, upper_threshold)

    # Combine white and yellow masks
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    return masked_image


def region_selection(image):
    mask = np.zeros_like(image)
    # Defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(image.shape) > 2:
        channel_count = image.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # making a rhombus for masking
    rows, cols = image.shape[:2]

    bottom_left = [cols * 0.1, rows * 0.95]
    top_left = [cols * 0.4, rows * 0.6]
    bottom_right = [cols * 0.9, rows * 0.95]
    top_right = [cols * 0.6, rows * 0.6]

    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def draw_lane_lines(image, lines, color=[255, 0, 0], thickness=12):
    
    line_image = np.zeros_like(image)
    if(lines == None): 
        return image
    for line in lines:
        if line is not None:
            cv2.line(line_image, *line, color, thickness)
    return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)


def average_slope_intercept(lines):
    left_lines = []  # (slope, intercept)
    left_weights = []  # (length,)
    right_lines = []  # (slope, intercept)
    right_weights = []  # (length,)
    try:
        if (lines == None):
            return None
    except:
        pass
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2:
                continue
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - (slope * x1)
            length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
            if slope < 0:
                left_lines.append((slope, intercept))
                left_weights.append(length)
            else:
                right_lines.append((slope, intercept))
                right_weights.append(length)
    left_lane = np.dot(left_weights, left_lines) / np.sum(left_weights) if len(left_weights) > 0 else None
    right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None
    return left_lane, right_lane


def pixel_points(y1, y2, line):
    if line is None:
        return None
    slope, intercept = line
    if(slope == 0.0):
        return None
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    y1 = int(y1)
    y2 = int(y2)
    return (x1, y1), (x2, y2)


def lane_lines(image, lines):
    t = average_slope_intercept(lines)
    if(t==None):
        return None
    left_lane, right_lane = t[0], t[1]
    y1 = image.shape[0]
    y2 = y1 * 0.6
    left_line = pixel_points(y1, y2, left_lane)
    right_line = pixel_points(y1, y2, right_lane)
    if ((None == left_line )or (None == right_line)):
        return None
    return left_line, right_line


def detect_lane(image):
    color_select = hsl_color_selection(image)

    gray = cv2.cvtColor(color_select, cv2.COLOR_RGB2GRAY)

    kernel_size = 13
    smooth = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(smooth, low_threshold, high_threshold)

    region = region_selection(edges)

    hough = cv2.HoughLinesP(region, rho=1, theta=np.pi / 180, threshold=20,
                            minLineLength=20, maxLineGap=300)
    
    result = draw_lane_lines(image, lane_lines(image, hough))
    return result


def process_video(test_video, output_video):

    input_video = VideoFileClip(test_video, audio=False)
    processed = input_video.fl_image(detect_lane)
    processed.write_videofile(output_video, audio=False)

def process_webcam():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        updateed_frame = detect_lane(frame)
        cv2.imshow('f', updateed_frame)
        if (cv2.waitKey(1) == ord('q')):
            break
def process_image(test_img, output_img):
    img = cv2.imread(test_img)
    img = detect_lane(img)
    cv2.imwrite(output_img, img)


# if __name__ == '__main__':
#     process_video("D:/ds-project/DS3-TarzonTheWonderCar/Lanedetection/videos/v3.mp4", "vv.mp4")
#     # process_video("D:/ds-project/DS3-TarzonTheWonderCar/test2.mp4", "vv.mp4")