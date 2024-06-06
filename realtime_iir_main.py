import realtime_plot_window
import webcam2rgb
import time

if __name__ == "__main__":
    # Initialize Realtime window containing graph, filter, and decoder
    realTimeWindow = realtime_plot_window.RealtimeWindow("Morse Decoder")

    # Create callback method reading camera and plotting in windows
    def hasData(retval, data, frame):
        if retval:
            # Calculate brightness b = data[0],  g = data[1], r = data[2]
            luminance = (0.2126 * data[:, :, 2]) + (0.7152 * data[:, :, 1]) + (0.0722 * data[:, :, 0])
            # Pass signal and frame to realtime window
            realTimeWindow.addData(luminance, frame)
            cv2.imshow("Frame", frame)  # Hiển thị frame qua cv2.imshow
            cv2.waitKey(1)  # Chờ một lát để frame hiển thị
        else:
            print("Error: No data received from camera")

    # Create instances of camera
    camera = webcam2rgb.Webcam2rgb()
    # Start the thread and stop it when we close the plot windows
    realTimeWindow.decoder.timerStart = time.time()
    camera.start(callback=hasData)
    print("Camera Sample Rate: ", camera.cameraFs(), "Hz")
    realTimeWindow.show()  # Hiển thị cửa sổ của RealtimeWindow
    camera.stop()

    # Debug
    timeElapsed = time.time() - realTimeWindow.decoder.timerStart
    print('\n Measured Sampling Rate: ' + str(realTimeWindow.decoder.totalSampleCount / timeElapsed))

    # Print Sequences
    print('\nSequence Detected:')
    print(realTimeWindow.decoder.morseSequence)
    print('\nDecoded Morse Code Sequence: ' + realTimeWindow.decoder.decodedLetters)
