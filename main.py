from utils import *
from main_server import Server



if __name__ == '__main__':
    try:
        port = prompt_port()
        socket_port = socket_port_prompt()
        server2 = Server(("0.0.0.0", port), socket_port)
        # app.run(host='0.0.0.0', port=3000)

        server2.start()
    except KeyboardInterrupt:
        print("Shutting down server")
        try:
            server2.exit_flag = True
            server2.shutdown()
            time.sleep(2)
        except:
            pass
        quit()