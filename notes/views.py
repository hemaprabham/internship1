import cv2
import numpy as np
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status



class UrineStripColorAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        # Ensure that the 'image' key is present in the request data
        if 'image' not in request.data:
            return Response({'error': 'Image not found in request.'}, status=status.HTTP_400_BAD_REQUEST)

        # Load the uploaded image using OpenCV
        image_file = request.data['image']
        image_np = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)

        # Define the lower and upper boundaries of the colors in HSV format
        # You can adjust these boundaries based on the specific colors of the urine strip
        color_boundaries = [
            ([0, 100, 100], [10, 255, 255]),  # Red
            ([25, 100, 100], [35, 255, 255]),  # Orange
            ([35, 100, 100], [85, 255, 255]),  # Yellow
            ([90, 100, 100], [130, 255, 255]),  # Green
            ([130, 100, 100], [170, 255, 255]),  # Blue
            ([170, 100, 100], [190, 255, 255]),  # Indigo
            ([190, 100, 100], [270, 255, 255]),  # Purple
            ([0, 0, 0], [180, 100, 100]),  # Black
            ([0, 0, 100], [180, 100, 255]),  # White
            ([0, 0, 0], [0, 0, 100])  # Void (Assuming black strip for void)
        ]

        colors = []
        for (lower, upper) in color_boundaries:
            # Create a mask for the current color range
            mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))

            # Calculate the average color within the mask region
            masked_image = cv2.bitwise_and(image_np, image_np, mask=mask)
            average_color = np.mean(masked_image, axis=(0, 1))
            average_color = average_color.astype(int)

            # Append the average color to the list of colors
            colors.append(average_color.tolist())

        # Prepare the response in JSON format
        response_data = {'colors': colors}

        return Response(response_data, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        # Add a simple response for handling GET requests to the root URL
        return Response({'message': 'Welcome to the Urine Strip Color Analyzer!'}, status=status.HTTP_200_OK)