import requests
r=requests.get('https://localhost:5000/login',verify='root.pem',cert=('cli.crt','cli.key'))
print (r.status_code)
print (r.content.decode())
print (r.headers)
print ('***')
