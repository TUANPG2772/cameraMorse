import realtime_plot_window
import webcam2rgb
import time

if __name__ == "__main__":
    # Initialize Realtime window containing graph, filter and decoder
    realTimeWindow = realtime_plot_window.RealtimeWindow("Morse Decoder")
        
    # Create callback method reading camera and plotting in windows
    def hasData(retval, frame):
        if retval:
            # Calculate brightness b = frame[0], g = frame[1], r = frame[2]
            luminance = (0.2126 * frame[:,:,2]) + (0.7152 * frame[:,:,1]) + (0.0722 * frame[:,:,0])
            # Pass signal to realtime window
            realTimeWindow.addData(luminance.mean())
        
    # Create instances of camera
    camera = webcam2rgb.Webcam2rgb()
    # Start the thread and stop it when we close the plot windows
    realTimeWindow.decoder.timerStart = time.time()
    camera.start(callback=hasData, cameraNumber=0)
    print("Camera Sample Rate: ", camera.cap.get(cv2.CAP_PROP_FPS), "Hz")
    realtime_plot_window.plt.show()
    camera.stop()

    # Debug
    timeElapsed = time.time() - realTimeWindow.decoder.timerStart
    print('\nMeasured Sampling Rate: ' + str(realTimeWindow.decoder.totalSampleCount / timeElapsed))
    
    # Print Sequences
    print('\nSequence Detected:')  
    print(realTimeWindow.decoder.morseSequence)
    print('\nDecoded Morse Code Sequence: ' + realTimeWindow.decoder.decodedLetters)
