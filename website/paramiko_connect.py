import paramiko

output_file = "paramiko.log"
def operation(hostname, command):
    
    client = paramiko.SSHClient()
    client.load_host_keys(hostname)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=22, username="appdev", password="JPdesign1!")
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read()
    print("Log Printing:::" + output)

    with open(output_file, "w+") as file:
        file.write(str(output))
    client.close()
    return output_file
    
#96.70.243.179
operation("96.70.243.179", "app")


