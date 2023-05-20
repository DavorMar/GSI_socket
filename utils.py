import re

def prompt_port():
    port = scan_port()
    if port == 12345678:
        print("couldnt scan port in GSI cfg file.")
    else:
        while True:
            answer = input(f"Do you want to use scanned port {port} for your GSI file? y/n ")
            if answer.lower() == "y":
                return port
            elif answer.lower() == "n":
                break
            else:
                print("Please write a y/n answer")
                continue
    while True:
        port = input("Please input the port your GSI config file is set to or your desired port: ")
        try:
            port = int(port)
        except ValueError:
            print("Input a correct port number between 80 and 99999")
            continue
        if port < 80 or port > 99999:
            print("Input a correct port number between 80 and 99999")
        else:
            print(f"Server is starting on port {port}")
            return port
def socket_port_prompt():
    while True:
        socket_port = input("please input port for your clients to connect to:")
        try:
            socket_port = int(socket_port)
        except ValueError:
            print("Input a correct port number between 80 and 99999")
            continue
        if socket_port < 80 or socket_port > 99999:
            print("Input a correct port number between 80 and 99999")
        else:
            print(f"Server is starting on port {socket_port}")
            return socket_port
def scan_port():
    path = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\cfg\gamestate_integration\gamestate_integration_dota2-gsi.cfg"
    with open(path, "r") as fp:
        read_string = fp.read()

    pattern = r':\d{4,6}'

    try:
        port = int(re.search(pattern, read_string).group()[1:])
        return port
    except AttributeError:
        return 12345678


