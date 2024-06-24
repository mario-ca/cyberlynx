# Usar la imagen oficial de Ubuntu
FROM ubuntu:latest

# Evitar preguntas al instalar paquetes
ARG DEBIAN_FRONTEND=noninteractive

# Actualizar los repositorios e instala rsyslog, nano, iproute2, openssh-server y supervisor
RUN apt-get update && apt-get install -y \
    rsyslog \
    nano \
    iproute2 \
    openssh-server \
    supervisor \
    curl

# Configurar rsyslog para enviar logs a la máquina host y desactivar imklog
RUN sed -i 's/module(load="imklog")/#module(load="imklog")/' /etc/rsyslog.conf && \
    echo '*.* @@172.17.0.1:514' >> /etc/rsyslog.conf

# Configurar SSH para permitir acceso root con contraseña
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    echo 'root:root' | chpasswd

# Configuración de supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Exponer los puertos necesarios para syslog y SSH
EXPOSE 514 22

# Configurar supervisord como el comando principal
CMD ["/usr/bin/supervisord"]
