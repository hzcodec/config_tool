import base64

string = '2017-05-31'
data = base64.b64encode(string.encode())
print(data)

data2 = base64.b64decode(data.decode())
print(data2)
