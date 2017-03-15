from periphery import I2C
import time
import array
import math

# Open i2c-0 controller
i2c = I2C("/dev/i2c-2")

# open inut file and read bytes
with open("celeste.png", "rb") as f:
  filebytes = f.read()

# display filesize
print(str(len(filebytes))+" bytes")

# number of 32-byte pages
pages = math.floor(len(filebytes)/32)
# bytes left over
over = len(filebytes)%32

# write each 32-byte page
for i in range(0, 32):
  fileoffset = i*32
  highbyte = fileoffset >> 8 & 0xff
  lowbyte = fileoffset & 0xff
  print(str(highbyte) + " " + str(lowbyte))
  #print(filebytes[fileoffset:fileoffset+32])
  write = bytes([highbyte, lowbyte])+filebytes[fileoffset:fileoffset+32]
  print(write)
  msg = [I2C.Message(write)]
  #print(msgs)
  #time.sleep(0.01)
  i2c.transfer(0x50, msg)
  time.sleep(0.004)

data = bytearray()
for i in range(0, math.floor(65536/8192)):
  msgs = [I2C.Message([0x00, 0x00]), I2C.Message(bytes(b'\x00' * 8192), read=True)]
  i2c.transfer(0x50, msgs)
  data += msgs[1].data

with open("out.png", "wb") as f:
  f.write(data)

i2c.close()
