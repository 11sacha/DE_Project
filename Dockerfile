FROM apache/flink:1.17.1-scala_2.12-java11

USER root

# Intall necesary libraries
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --upgrade pip && \
    pip3 install apache-flink pyflink pandas requests


WORKDIR /opt/flink/jobs


COPY process_ads.py .

# Downloads Kafka conector for Flink
RUN curl -fSL -o /opt/flink/lib/flink-connector-kafka-1.17.1.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/1.17.1/flink-connector-kafka-1.17.1.jar && \
    curl -fSL -o /opt/flink/lib/kafka-clients-3.3.1.jar \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.3.1/kafka-clients-3.3.1.jar
