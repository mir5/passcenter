import asyncio
import websockets
import paramiko

async def ssh_handler(websocket, path):
    ip = websocket.query_params['ip']
    port = int(websocket.query_params.get('port', 22))
    username = 'your_ssh_username'
    password = 'your_ssh_password'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=username, password=password)
    shell = client.invoke_shell()

    async def receive():
        while True:
            message = await websocket.recv()
            shell.send(message)

    async def send():
        while True:
            data = shell.recv(1024)
            if not data:
                break
            await websocket.send(data)

    await asyncio.gather(receive(), send())

start_server = websockets.serve(ssh_handler, "0.0.0.0", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
