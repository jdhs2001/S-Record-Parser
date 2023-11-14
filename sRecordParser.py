# Main (highest level) function
def parseFile():
    for line in lines:
        # The record type is always the first two bytes
        recordType = line[0]+line[1]
        # And the byte count is always the second two bytes
        byteCount = line[2]+line[3]
        # Cast the byte count as a base 16 int (which is hexadecimal) 
        byteCount = int(byteCount, 16)
        # Determine the address depending on the record type as well as the bytes of data
        address, bytesOfData, dataStart = getAddrAndData(recordType, byteCount, line)
        # Cast the startAddress and end address as a hex value as well so we can calculate range 
        startAddress = hex(int(address, 16))
        endAddress = hex(int(address, 16) + bytesOfData)        

        print('Record Type:', recordType, '\nByte Count:', byteCount,'\nBytes of Data', 
              bytesOfData,'\nAddress Range:',startAddress,'-',endAddress,'\nData:')
        
        # I am aware that this is very hard to read, but it simply takes the pairs of bytes 
        # that would be contained in each memory space and prints them out
        for a,b in zip(line[dataStart:(len(line)-4):2], line[dataStart+1:(len(line)-3):2]):
            print(a + b,' ', end='')
        print('\n')
        # calculate the checksum and assign the returned values
        checkSum, expCheckSum = calcCheckSum(line)
        # Check to see that they are equal
        if (checkSum == expCheckSum):
            print('Calculated checksum:', checkSum,'| Expected checksum:', expCheckSum, '--Checksum is valid--')
        else:
            print('Calculated checksum:', checkSum,'| Expected checksum:', expCheckSum,'--Checksum failed--')
        print()

# Get the address, where the data starts, and the number of bytes in the line
def getAddrAndData(type, bC, line):

    if(type == 'S1' or type == 'S9'):
        addr = line[4:8]
        bytesOfdata = bC - 3
        start = 8

    elif(type == 'S2' or type == 'S8'):
        addr = line[4:10]
        bytesOfdata = bC - 4
        start = 10

    elif(type == 'S3' or type == 'S7'):
        addr = line[4:12]
        bytesOfdata = bC - 5
        start = 12

    else:
        addr = line[4:8]
        bytesOfdata = 0
        start = len(line)

    return (addr, bytesOfdata, start)

# Calculate the Checksum and return True or False
def calcCheckSum(line):
    # Create a list for the bytes of data so I can use the sum function
    dataByteList = []
    # Get the necessary bytes for the dataByteList and convert them to an integer(base 16), then append byte
    for a,b in zip(line[2:(len(line)-4):2], line[3:(len(line)-3):2]):
            dataByte = a + b
            dataByte = int(dataByte, 16)
            dataByteList.append(dataByte)
    # Add up the list to get the checksum and Take the ones complement of the checksum
    checkSum = sum(dataByteList)
    checkSum = 65535 - (checkSum & 65535)
    checkSum = (hex(checkSum))
    # Check if the calculated chacksum == the expected checksum 
    finalCheckSum = (checkSum[len(checkSum)-2:len(checkSum)]).upper().strip()
    expCheckSum = (line[len(line)-3:len(line)]).upper().strip()
    return finalCheckSum, expCheckSum

# Open the file and read the lines
try:
    file = open("Lab10.s19","r")
    lines = file.readlines()
    file.close
except OSError:
    print('Unable to open file, please try again')
else: 
    parseFile()

