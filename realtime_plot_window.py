import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import morse_decoder
import iir_filter
import cv2

class RealtimeWindow:

    def __init__(self, channel: str):
        # Create a plot window for luminance and filtered signal
        self.fig, (self.ax, self.ax1) = plt.subplots(2)
        plt.title(f"Channel: {channel}")
        self.ax.set_title('Luminance')
        self.ax1.set_title('Filtered Signal')
        self.plotbuffer = np.zeros(800)
        self.plotbuffer1 = np.zeros(800)
        # Create empty lines
        line, = self.ax.plot(self.plotbuffer)
        line2, = self.ax1.plot(self.plotbuffer1)
        self.line = [line, line2]
        # Set axis limits
        self.ax.set_ylim(-1, 1)
        self.ax1.set_ylim(-1, 1)
        # Initialize Ringbuffers
        self.ringbuffer = []
        self.ringbuffer1 = []
        # Add any initialization code here (filters etc)
        # Start the animation        
        self.decodedSequence = ''

        # Design High Pass filter
        samplingFrequency = 30
        # Define cut off frequency
        cutOffFrequencyHighPass = 0.1 # Hz
        # Number order that IIR filter array will be equivalent to
        order = 2
        
        # Generate second order sections
        sos = np.array(iir_filter.GenerateHighPassCoeff(cutOffFrequencyHighPass, samplingFrequency, order))

        # Initialize Morse code decoder object
        self.decoder = morse_decoder.MorseCodeDecoder()
    
        # Create IIR Array object
        self.iirFilter = iir_filter.IIRFilter(sos)
    
        # Initialize filter output variable
        self.filterOutput = 0
        # Start the animation    
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=100)

        # Create a figure for the webcam feed
        self.fig2, self.ax2 = plt.subplots()
        self.ax2.set_title('Webcam Feed')
        self.webcam_frame = self.ax2.imshow(np.zeros((480, 640, 3), dtype=np.uint8))

    # Updates the plot
    def update(self, data):
        # Add new data to the buffer
        self.plotbuffer = np.append(self.plotbuffer, self.ringbuffer)
        self.plotbuffer1 = np.append(self.plotbuffer1, self.ringbuffer1)
        # Only keep the 800 newest ones and discard the old ones
        self.plotbuffer = self.plotbuffer[-800:]
        self.plotbuffer1 = self.plotbuffer1[-800:]
        self.ringbuffer = []
        self.ringbuffer1 = []
        # Set the new 800 points of channel 9
        self.line[0].set_ydata(self.plotbuffer)
        self.line[1].set_ydata(self.plotbuffer1)
        self.ax.set_ylim((min(self.plotbuffer) - 1), max(self.plotbuffer) + 1)
        self.ax1.set_ylim((min(self.plotbuffer1) - 1), max(self.plotbuffer1) + 1)
        # Update the decoded sequence
        self.ax.set_title('Luminance - Detected Sequence: ' + self.decoder.morseSequence)
        self.ax1.set_title('Filtered Signal - Decoded Sequence: ' + self.decoder.decodedLetters)

        return self.line

    # Appends data to the ringbuffer
    def addData(self, signal, frame=None):
        self.ringbuffer.append(signal)
        self.filterOutput = self.iirFilter.Filter(signal)
        self.ringbuffer1.append(self.filterOutput)
        self.decoder.Detect(self.filterOutput)
        if frame is not None:
            self.update_webcam_frame(frame)

    # Updates the webcam frame
    def update_webcam_frame(self, frame):
        self.webcam_frame.set_data(frame)
        self.ax2.draw_artist(self.ax2.patch)
        self.ax2.draw_artist(self.webcam_frame)
        self.fig2.canvas.blit(self.ax2.bbox)
