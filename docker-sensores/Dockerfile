# Instala python
FROM python:2.7.11
RUN apt-get update

# Instala el editor
RUN apt-get install -y nano

# Instala el cliente de AWS
RUN pip install awscli

# Consfiguracion de mi usuario de aws para poder conectarme. 
RUN aws configure set aws_access_key_id xxx # provide aws access key id
RUN aws configure set aws_secret_access_key xxxxx # provide aws secret access key
RUN aws configure set default.region us-east-1 # provide aws default region

# Download del repostorio git en un directorio especifico
# RUN git clone https://github.com/awslabs/aws-iot-elf /root/aws-iot-elf

COPY ./aws-iot-elf /root/aws-iot-elf

# Dependecias de Python
RUN pip install -r /root/aws-iot-elf/requirements.txt

RUN curl -o /root/aws-iot-elf/aws-iot-rootCA.crt https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem

# No posciona en este directorio dentro de la maquina.
CMD /bin/bash