FROM continuumio/anaconda3
RUN apt update && apt --fix-missing --yes dist-upgrade 
RUN adduser conda --system
RUN apt install -y npm
RUN /opt/conda/bin/conda upgrade --yes conda 
RUN /opt/conda/bin/conda upgrade --yes anaconda 
