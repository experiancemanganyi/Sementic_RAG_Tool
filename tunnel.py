from pyngrok import ngrok
import subprocess
import time

NGROK_TOKEN = "33hZPCWsAEYC7imoSIwGqaGfc1d_871aFoJ9JZ1Tt5zWGGReZ"

subprocess.Popen(['uvicorn', 'api:app', '--host', '0.0.0.0', '--port', '8080'])

time.sleep(5)

ngrok.set_auth_token(NGROK_TOKEN)
ngrok.kill()

public_url = ngrok.connect(8080)
print(f"\n{public_url}/my_rag")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down...")
    ngrok.kill()