# PyWayout
A simple encrypted sock5 proxy server written in python.

## Usage:
You need Python(version 2.7 or 3.5+) installed on both remote proxy server and your local PC.

### Step 1. Generate secret.key file:
On local PC:  
(Python2) Run: python secret.py [key_length]  
(Python3) Run: python secret3.py [key_length]  

key_length is an optional argument to set generated secret.key file size. The default value 4096 is usually ok.

If a secret.key file already exists, it will ask if you want to overwrite. If you choose 'N' then the old secret.key will be preserved.

### Step 2. Modify config.json file:
* server_host: Host name or IP of your remote server.
* server_port: Port bind on remote server, which the client program connects to.
* client_port: Port bind on local PC, which the browser connects to.

### Step 3. Copy all files to remote server:
Now copy all files to remote server, including the generated secret.key file.

### Step 4. Start remote service:
On remote server:  
(Python2) Run: python server.py  
(Python3) Run: python server3.py  

### Step 5. Start client service:
On local PC:  
(Python2) Run: python client.py  
(Python3) Run: python client3.py  

### Step 6. Configure your browser:
Config your browser proxy options to use sock5 proxy on 127.0.0.1:&lt;client_port&gt;.

### Note:
This is just a simple testing program, the encryption is very basic byte shift operation.  
It may be used to by pass some firewall filter rules but should not be considered very secure.  
