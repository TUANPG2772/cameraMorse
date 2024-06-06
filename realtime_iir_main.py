import multiprocessing
import time
import realtime_plot_window
import webcam2rgb

def main():
    # Initialize Realtime window containing graph, filter, and decoder
    realTimeWindow = realtime_plot_window.RealtimeWindow("Morse Decoder")
        
    # Create callback method reading camera and plotting in windows
    def hasData(retval, data, frame):
        # Calculate brightness b = data[0],  g = data[1], r = data[2]
        luminance = (0.2126 * data[2]) + (0.7152 * data[1]) + (0.0722 * data[0])
        # Pass signal and frame to realtime window
        realTimeWindow.addData(luminance, frame)

    # Create instances of camera
    camera = webcam2rgb.Webcam2rgb()
    # Start the thread and stop it when we close the plot windows
    realTimeWindow.decoder.timerStart = time.time()
    camera.start(callback=hasData)
    print("Camera Sample Rate: ", camera.cameraFs(), "Hz")
    
    # Keep the main process running while the plot window is displayed
    while True:
        time.sleep(1)

if __name__ == "__main__":
    # Start the main process in a separate process
    main_process = multiprocessing.Process(target=main)
    main_process.start()
    
    # Display the plot window
    realtime_plot_window.plt.show()
    
    # Wait for the main process to finish
    main_process.join()
