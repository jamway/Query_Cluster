FROM ubuntu:18.04
LABEL author = "Chan, Wei-chuang <weichuangchan@gmail.com>"

# Install Ubuntu Packages
RUN apt-get autoremove && apt-get clean && apt-get update && apt-get install -y \
python3.6 \
python3-pip \
nano \
vim

# Install Python Packages
RUN pip3 install \
numpy \
scipy \
matplotlib \
ipython \
scikit-learn \
jupyter \
google \
google-cloud \
google-cloud-monitoring \
google-cloud-storage \
google-cloud-pubsub \
google-cloud-bigquery \
google-cloud-logging \
pandas \
sympy \
nose \
gensim==3.4

RUN export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update -y && apt-get install google-cloud-sdk -y
# Set Environment Variables
ENV PROJECT_ID project_Id
ENV JOB_ID deployment_id
ENV EMAIL email
ENV QUERY query
# Copy all files
COPY credentials.json /opt/main/credentials.json
COPY script.py ./
COPY run.sh ./

# Make required directories
RUN mkdir ./data && chmod 777 ./data
RUN mkdir ./model && chmod 777 ./model

RUN chmod 777 ./script.py

# Credentials Set Up
RUN gcloud auth activate-service-account --key-file=/opt/main/credentials.json

ENTRYPOINT ./script.py





