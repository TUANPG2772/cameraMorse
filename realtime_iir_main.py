import realtime_plot_window
import webcam2rgb
import time

if __name__ == "__main__":

    # Initialize Realtime window containing graph, filter and decoder
    realTimeWindow = realtime_plot_window.RealtimeWindow("Morse Decoder")
        
    # Create callback method reading camera and plotting in windows
    def hasData(retval, data, frame):
        # Calculate brightness b = data[0],  g = data[1], r = data[2]
        luminance = ( (0.2126*data[2]) + (0.7152*data[1]) + (0.0722*data[0]) )
        # Pass signal to realtime window
        realTimeWindow.addData(luminance)
        
    # Create instances of camera
    camera = webcam2rgb.Webcam2rgb()
    # Start the thread and stop it when we close the plot windows
    realTimeWindow.decoder.timerStart = time.time()
    
    # Start camera without cameraNumber argument
    camera.start(callback=hasData)
    print("Camera Sample Rate: ", camera.cameraFs(), "Hz")
    realtime_plot_window.plt.show()
    camera.stop()

    # Debug
    #print('\n Time Pos-to-Neg Peak:')  
    #print(realTimeWindow.decoder.nSamplesBetwenPosNegPeakList)
    timeElapsed = time.time() - realTimeWindow.decoder.timerStart
    print('\n Measured Sampling Rate: ' + str(realTimeWindow.decoder.totalSampleCount / timeElapsed))
    
    # Print Sequences
    print('\nSequence Detected:')  
    print(realTimeWindow.decoder.morseSequence)
    print('\nDecoded Morse Code Sequence: ' + realTimeWindow.decoder.decodedLetters )
