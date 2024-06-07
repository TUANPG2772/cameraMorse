# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 20:19:10 2020

@author: Kamil
"""
import numpy as np
class MorseCodeDecoder():
    
    def __init__(self):
        # Khởi tạo cây nhị phân
        self.tree = MorseCodeBinaryTree()
        
        # Các tham số thời gian
        self.nSamplesDotDuration = 10
        self.nSamplesMinDashDuration = 16
        self.nSamplesMaxDashDuration = 35
        self.nSamplesErrorMargin = 4

        # Chuỗi cho các dãy
        self.sequence = ''
        self.morseSequence = ''
        self.decodedLetters = ''
        
        # Các biến đếm
        self.nSamplesBetweenPosNegPeakList = []
        self.nSamplesBetweenPeaks = 0
        self.nSymbols = 0
        self.nSamplesLow = 0
        self.totalSampleCount = 0

        # Ngưỡng
        self.posAmplitudeThreshold = 10
        self.negAmplitudeThreshold = -10
        self.pulseSettlingSamplecCnt = 5
        
        # Cờ cho bộ nhận đỉnh
        self.posPeakFlag = False
        self.negPeakFlag = False
        self.posPeakFound = False
        
        # Lưu mẫu trước
        self.previousSample = 0

        # Biến đếm thời gian lấy mẫu
        self.timerStart = 0
        self.SamplingTimerCounter = 0
        self.nSamplesLate = 0 

    def Detect(self, sample):
        # Chờ 5 giây để bộ lọc ổn định
        if (self.totalSampleCount >= 150):
            
            # Phát hiện đỉnh dương - đèn bật
            if np.any(sample > self.posAmplitudeThreshold) and not self.posPeakFlag:
                self.posPeakFlag = True
                # Nếu tín hiệu thấp đủ lâu để không phải là khoảng cách giữa các chữ cái
                if( self.nSamplesLow >= 20):
                    if (self.sequence):
                        # Giải mã chữ cái
                        self.decodedLetters += self.tree.DecodeString(self.sequence)
                        if (self.nSamplesLow >= 40):
                            self.decodedLetters += ' '
                        # Cập nhật dãy Morse
                        self.morseSequence += self.sequence + ' '
                        # Đặt lại dãy
                        self.sequence = ''
                    self.nSamplesLow = 0
                    
            # Nếu biên độ vượt ngưỡng và mẫu trước lớn hơn thì đó phải là đỉnh
            if( sample > self.posAmplitudeThreshold and self.previousSample > sample and self.posPeakFlag):
                self.posPeakFound = True
                
            # Phát hiện đỉnh âm - đèn tắt
            if( sample < self.negAmplitudeThreshold and not self.negPeakFlag ):
                self.negPeakFlag = True
     
            # Nếu biên độ nhỏ hơn ngưỡng và mẫu trước nhỏ hơn, đó phải là đỉnh
            if( sample < self.negAmplitudeThreshold and self.previousSample < sample and self.posPeakFlag and self.nSamplesBetweenPeaks >= self.pulseSettlingSamplecCnt):
                # Đặt lại các cờ
                self.posPeakFound = False
                self.posPeakFlag = False
                self.negPeakFlag = False
                self.nSamplesBetwenPosNegPeakList.append(self.nSamplesBetweenPeaks)
                # Tăng biến đếm đỉnh
                self.nSymbols += 1 
                # Kiểm tra nếu đèn bật đủ lâu để là dấu gạch
                if( self.nSamplesBetweenPeaks  >= self.nSamplesMinDashDuration ):
                    self.sequence += '-'
                    
                # Kiểm tra nếu đèn bật đủ lâu để là dấu chấm
                elif( self.nSamplesBetweenPeaks  >= (self.nSamplesDotDuration - self.nSamplesErrorMargin ) and self.nSamplesBetweenPeaks  <= (self.nSamplesDotDuration + self.nSamplesErrorMargin ) ):
                    self.sequence += '.'
                    
                # Đặt lại hẹn giờ
                self.nSamplesBetweenPeaks = 0
        
        # Nếu đèn bật được phát hiện
        if(self.posPeakFound):
            self.nSamplesBetweenPeaks += 1
            self.nSamplesLow = 0
            # Nếu đèn bật bật lâu hơn dấu gạch
            if(self.nSamplesBetweenPeaks > self.nSamplesMaxDashDuration ):
                # Phát hiện sai, đặt lại các cờ & biến
                self.posPeakFound = False
                self.posPeakFlag = False
                self.negPeakFlag = False
                self.nSamplesBetweenPeaks = 0
        # Nếu đèn bật chưa được phát hiện
        else:
            # Im lặng tiếp tục
            self.nSamplesLow += 1
        
        # Lưu mẫu hiện tại để so sánh
        self.previousSample = sample
        self.totalSampleCount += 1


"""
MorseCodeBinary tree object, initializes and populates a binary tree for morse code with methods to decode the whole sequence at once or by symbol.
"""
class MorseCodeBinaryTree(object):

    
    def __init__(self):
        # Định nghĩa nút gốc
        self.rootNode = Node("*")
        self.traverseNode = self.rootNode

        # Tất cả các ký tự trong mã Morse được định nghĩa thuận tiện để điền theo cấp độ của cây nhị phân
        morseDictionary = "ETIANMSURWDKGOHVF*L*PJBXCYZQ**54*3***2**+****16=/*****7***8*90"

        # Nút hiện tại
        currentParentNode = self.rootNode
        # Danh sách nút
        nextNodesPlaceHolder = []

        # Điền cây nhị phân
        # Đối với mỗi ký tự trong chuỗi từ điển
        for character in morseDictionary:
            # Nếu không có đối tượng nút nào sau khi chấm (qua trái)
            if( currentParentNode.dot == None ):
                # Chèn nút với giá trị sẽ tạo ra từ dấu chấm
                 currentParentNode.dot = Node(character)
            # Đã có một đối tượng nút qua trái nên chúng ta sẽ xử lý phía bên phải
            else:
                # Nếu không có đối tượng nút nào sau dấu gạch (qua phải)
                if (currentParentNode.dash == None):
                    # Chèn nút với giá trị sẽ tạo ra từ dấu gạch
                    currentParentNode.dash = Node(character)
                # Đã gán cả hai nút con
                else:
                    # Thêm các nút vào danh sách
                    nextNodesPlaceHolder.append(currentParentNode.dot)
                    nextNodesPlaceHolder.append(currentParentNode.dash)
                    # Loại bỏ nút đầu tiên từ người giữ chỗ để xử lý tiếp theo
                    # tức là di chuyển qua cây
                    currentParentNode = nextNodesPlaceHolder.pop(0)
                    # Tạo nút mới dựa trên dấu chấm
                    currentParentNode.dot = Node(character)


    """
    Phương thức đi qua cây nhị phân mã Morse để giải mã toàn bộ chuỗi đầu vào
    và trả về ký tự tương ứng.
    """
    def DecodeString(self, morseCodeSequence):

        # Bắt đầu từ nút gốc
        currentNode = self.rootNode
        
        # Đối với mỗi ký tự trong chuỗi đầu vào
        for character in morseCodeSequence:
            # Nếu là dấu chấm đi qua bên trái
            if character == ".":
                currentNode = currentNode.dot
            # Ngược lại phải là dấu gạch, đi sang phải
            else:
                currentNode = currentNode.dash

        return currentNode.value


    """
    Phương thức đi qua cây nhị phân mã Morse dựa trên đầu vào và trả về ký tự cho chuỗi nếu cờ được cung cấp.
    """
    def ProcessNode(self, inputChar, endFlag):

        # Nếu là dấu chấm, đi sang trái
        if inputChar == ".":
            if not self.traverseNode.left:
                return '#'
            else:
                self.traverseNode = self.traverseNode.left
        # Nếu là dấu gạch, đi sang phải
        elif inputChar == "-":
            if not self.traverseNode.right:
                return '#'
            else:
                self.traverseNode = self.traverseNode.right
        
        # Nếu chuỗi dấu chấm và dấu gạch đã kết thúc, trả về ký tự
        if endFlag:
            self.traverseNode = self.rootNode
            return self.traverseNode.value
            
        
"""
Đối tượng nút nhị phân
"""
class Node(object):
    # Constructor
    def __init__(self, char):
        # Ký tự tương ứng với chuỗi
        self.value = char
        # Đối tượng nút con
        self.dot = None
        self.dash = None
        
       
def unitTest():
    
    morseDecoder = MorseCodeDecoder()
    
    # Kiểm tra chuỗi toàn bộ cho bảng chữ cái
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+=/"
    alphabetInMorse = [  ".-" , "-..." , "-.-." , "-.." , "." , "..-." , "--." , "...." , ".." , ".---" , "-.-" , ".-.." , "--" , "-." , "---" , ".--." , "--.-" , ".-." , "..." , "-" , "..-" , "...-" , ".--" , "-..-" , "-.--" , "--.." , "-----" , ".----" , "..---" , "...--" , "....-" , "....." , "-...." , "--..." , "---.." , "----." , ".-.-." , "-...-" , "-..-."]
    nCharacterInAlphabet = 39
    
    print("TESTING DECODER! - WHOLE SEQUENCE FOR CHARACTER")
    print("INPUT VALUES: " + alphabet )
    for x in range(nCharacterInAlphabet):
        decodedCharacter = morseDecoder.tree.DecodeString(alphabetInMorse[x])
        if alphabet[x] == decodedCharacter:
            print(decodedCharacter)
        else:
            print("MORSE DECODER IS NOT OPERATING CORRECTLY!")
            print("EXPECTED CHARACTER:" + str(alphabet[x]) + " DECODED: " + str(decodedCharacter))
            return -1

        
    print("DECODER OPERATES CORRECTLY!")   
    return 0
        
if __name__ == "__main__":
    
    unitTest()
               
