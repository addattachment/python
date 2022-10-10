
if __name__ == '__main__':
    # first we need to enter the device's IP in the config file
    # then we open the Emotibit Oscilloscope to see if data is flowing correctly
        #   if LSL is connected
    print("Is the LSL stream connected in Emotibit Oscilloscope?")

    # we establish communication to the emotibit: [CMD: HE]
    # then: we send the command to start record (to SD): [CMD: RB]

    # finally: stop command [CMD: RE]

    #todo: necessary to write custom software?? No, if we use the LSL marker stream!