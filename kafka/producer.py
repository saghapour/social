import logging
from typing import Any

from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.serialization import StringSerializer

from utils.config_reader import Config


class ProtoProducer:
    def __init__(self, topic: str, msg_type: Any):
        config = Config.read_conf('defaults')
        schema_registry = SchemaRegistryClient({'url': config.kafka.schema_registry})
        protobuf_serializer = ProtobufSerializer(msg_type, schema_registry)
        producer_config = {
            'bootstrap.servers': config.kafka.bootstrap_servers,
            'key.serializer': StringSerializer(),
            'value.serializer': protobuf_serializer
        }
        self.__msg_type = msg_type
        self._topic = topic
        self.__producer = SerializingProducer(producer_config)
        self.__logger = logging.Logger(__name__)

    def produce(self, key, msg):
        if type(msg) != self.__msg_type:
            raise TypeError(f"Expected {self.__msg_type} but received {type(msg)}")

        self.__producer.poll(0.0)
        self.__producer.produce(self._topic, key, msg, on_delivery=self.__on_delivery)
        self.__producer.flush()

    def __on_delivery(self, err, msg):
        if err is not None:
            self.__logger.error(f"Error occurred for key {msg.key()}: {err}")
