import base64

endDate = '2017-05-31'
data = base64.b64encode(endDate.encode())
print(data)

data2 = base64.b64decode(data.decode())
print(data2)