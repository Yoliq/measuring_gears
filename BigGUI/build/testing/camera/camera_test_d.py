import cv2
import datetime

def generate_filename(extension: str='txt') -> str:
    """
    Generates a filename based on the current date and time in the format 'YYYY_MM_DD_HHMMSS.csv'.
    
    Returns:
    str: The generated filename.
    """
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date and time as 'YYYY_MM_DD_HHMMSS'
    filename = now.strftime("%Y_%m_%d_%H%M%S") + "." + extension

    return filename

def capture_and_save_image(save_path, scale_factor=1):
    # Open the default camera (usually the first connected USB camera)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    # Read one frame (the image)
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read from camera.")
        cap.release()
        return
    
    # Release the camera
    cap.release()
    
    # Scale the image
    if scale_factor != 1:
        width = int(frame.shape[1] * scale_factor)
        height = int(frame.shape[0] * scale_factor)
        resized_frame = cv2.resize(frame, (width, height))
    else:
        resized_frame = frame
    
    # Save the image to the provided path
    cv2.imwrite(save_path, resized_frame)
    print(f"Image saved to {save_path}")

# Example usage
# capture_and_save_image(0.5, "output_image.jpg")

if __name__ == '__main__':
    pic_name = generate_filename('jpg')
    capture_and_save_image(f'C:\\Users\\danie\\Documents\\Python\\camera_pj\\data\\{pic_name}')
    print('OK')