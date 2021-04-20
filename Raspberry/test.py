class test:

    calibration_data = {  #default values
    "-vertical" : 20,
    "+vertical" : -4,
    "-horizontal" : -20,
    "+horizontal" : 20,
    "vertical_res" : 1080,
    "horizontal_res" : 1920
    }

    def remap(self,x, oMin, oMax, nMin, nMax ):
        ## 0.00000762551 avg time
        # add out off range option here or somewhere
        #
        #check reversed input range
        reverseInput = False
        oldMin = min( oMin, oMax )
        oldMax = max( oMin, oMax )
        if not oldMin == oMin:
            reverseInput = True

        #check reversed output range
        reverseOutput = False   
        newMin = min( nMin, nMax )
        newMax = max( nMin, nMax )
        if not newMin == nMin :
            reverseOutput = True

        portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
        if reverseInput:
            portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

        result = portion + newMin
        if reverseOutput:
            result = newMax - portion

        return result
    def convertToPix(self,horizontal,vertical):
        horizontal = self.remap(horizontal,self.calibration_data["-horizontal"],self.calibration_data["+horizontal"],0,self.calibration_data["horizontal_res"])
        vertical = self.remap(vertical,self.calibration_data["+vertical"],self.calibration_data["-vertical"],0,self.calibration_data["vertical_res"])
        return horizontal, vertical    

test = test()


for x in range(-35, 56, 1):
    print (x)
    print(test.convertToPix(x,x))

