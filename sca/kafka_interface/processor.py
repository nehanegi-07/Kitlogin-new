"""
Created on May 14th 2022

__author__ = "Mani Malarvannan"
__copyright__ ="Copyright 2022 AnalyticKit Inc"
"""
from confluent_kafka import Consumer, KafkaException, KafkaError, Producer
from common.config import ConfigHolder
import logging
import traceback


class KafkaProcessor:
    ch = None

    def __init__(self, file_name=None, config=None):
        '''
        Create KafkaProducer with file_names

        Parameters
        ----------
        file_name : TYPE
            Configuration file names

        Returns
        -------
        None.

        '''
        if file_name is None and config is None:
            raise ValueError("Both file_names and config are None")

        if file_name is not None and config is not None:
            raise ValueError("Both file_names and config are not None")

        if config is None:
            KafkaProcessor.ch = ConfigHolder(file_name)
        else:
            KafkaProcessor.ch = config

        self.logger = logging.getLogger(__name__)
        self.log_level = KafkaProcessor.ch.get_value("log_level")

        if self.log_level == "info":
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.DEBUG)

    def get_kafka_config(self):
        '''
        Get all the config parameters required to create Confluent
        Kafka Consumer/Producer Use the AWS Secret Manager to get user/pass
        for SASL authentication

        Returns
        -------
        config : dict
            Configuration parameters used to connect to Kafka Topic

        '''
        secret = self.get_secret()
        sasl_username = secret["username"]
        sasl_password = secret["password"]

        config = {
            'bootstrap.servers': self.get_config_value("bootstrap_servers"),
            'group.id': self.get_config_value("group_id"),
            'session.timeout.ms': self.get_config_value("session_timeout"),
            'default.topic.config': {'auto.offset.reset':
                                         self.get_config_value("auto_offset_reset")},
            'security.protocol': self.get_config_value("security_protocol"),
            'sasl.mechanisms': self.get_config_value("sasl_mechanism"),
            'sasl.username': sasl_username,
            'sasl.password': sasl_password
        }
        return config

    def receive_last_message(self, topic_name):
        '''
        Get the last message from the give topic

        Parameters
        ----------
        topic_name : str
            Name of the topic

        Returns
        -------
        message : str
            last message from Kafka topic

        '''

        try:
            conf = self.get_kafka_config()
            consumer_poll_timeout = KafkaProcessor.ch.get_value(
                "consumer_poll_timeout")
            c = Consumer(**conf)
            topics = [topic_name]
            c.subscribe(topics)
            messages = None
            # dummy poll
            c.poll()
            # go to end of the stream
            c.seek_to_end()
            # start iterate
            for message in c:
                return message

        finally:
            if c is not None:
                c.close()

    def receive_messages(self, topic_name):
        '''
        For the ui_change_event from the mobile app, identifies the
        XML file, retrieves it and sends the lxml root object.

        Parameters
        ----------
        topic_name : str
            Name of the topic to connect to receive the message.

        Raises
        ------
        KafkaException
            Wraps confluent_kafka.KafkaError.

        Returns
        -------
        messages : TYPE
            DESCRIPTION.

        '''
        try:
            conf = self.get_kafka_config()
            consumer_poll_timeout = KafkaProcessor.ch.get_value(
                "consumer_poll_timeout")
            c = Consumer(**conf)
            topics = [topic_name]
            c.subscribe(topics)
            messages = []
            while True:
                msg = c.poll(timeout=float(consumer_poll_timeout))
                self.logger.info("msg=%s" % msg)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        self.logger.error('%s [%d] reached end at \
                                          offset %d\n' %
                                          (msg.topic(), msg.partition(),
                                           msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    self.logger.debug('%s [%d] at offset %d with key %s:\n' %
                                      (msg.topic(), msg.partition(),
                                       msg.offset(),
                                       str(msg.key())))
                    messages.append(msg.value())
                    break
        except Exception as exp:
            self.logger.error("Couldn't initialize kafka consumer for \
                              topic" + str(exp),
                              {'exp': traceback.format_exc()})
            raise
        finally:
            if c is not None:
                c.close()

        return messages

    def send_messages(self, topic_name, xml_list):
        '''
            This function sends list of messages to Kafka topic
            specified in the topic_name. It sends all the messages and
            finally calls the flush, if not each message will be sent one
            after the other which reduces the performance If for any
            reason, the buffer is full, it waits and tries
            to resend the message

    For now the poll parameter is hard-coded

        Parameters
        ----------
        topic_name : str
            Name of the topic to send the message.
        xml_list : List
            List of XML messages to send to the specified topic.

        Returns
        -------
        None.

        '''
        try:
            conf = self.get_kafka_config()
            del conf["session.timeout.ms"]
            del conf["default.topic.config"]
            p = Producer(**conf)

            for xml in xml_list:
                p.produce(topic_name, xml,
                          callback=self.delivery_callback)
                p.poll(0)
        except BufferError as e:
            self.logger.error("Buffer full, waiting for \
                              free space on the queue" + str(e))
            p.poll(60)
            p.produce(topic_name, xml, callback=self.delivery_callback)

        except:
            self.logger.error("Couldn't create Kafka Producer" + str(" "),
                              {'exp': traceback.format_exc()})
            raise
        finally:
            if p is not None:
                p.flush()

    def send_messages_with_key(self, topic_name, xml_list):
        '''
            This function sends list of messages to Kafka topic
            specified in the topic_name. It sends all the messages and
            finally calls the flush, if not each message will be sent one
            after the other which reduces the performance If for any
            reason, the buffer is full, it waits and tries
            to resend the message. This function is used only to send to
            SAP-PI. For ESB key is not required.

    For now the poll parameter is hard-coded

        Parameters
        ----------
        topic_name : str
            Name of the topic to send the message.
        xml_list : List
            List of XML messages to send to the specified topic.
        key : str
            key used by SAP Advantaco

        Returns
        -------
        None.

        '''
        try:
            conf = self.get_kafka_config()
            del conf["session.timeout.ms"]
            del conf["default.topic.config"]
            p = Producer(**conf)
            key = KafkaProcessor.ch.get_value("kafka_key")

            for xml in xml_list:
                p.produce(topic_name, xml, key=key,
                          callback=self.delivery_callback)
                p.poll(0)
        except BufferError as e:
            self.logger.error("Buffer full, waiting for \
                              free space on the queue" + str(e))
            p.poll(60)
            p.produce(topic_name, xml, callback=self.delivery_callback)

        except:
            self.logger.error("Couldn't create Kafka Producer" + str(" "),
                              {'exp': traceback.format_exc()})
            raise
        finally:
            if p is not None:
                p.flush()

