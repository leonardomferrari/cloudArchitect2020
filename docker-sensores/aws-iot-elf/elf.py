#!/usr/bin/env python


# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License is
# located at
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import os
import json
import time
import uuid
import logging
import argparse
import datetime
import threading
from boto3.session import Session
from botocore.exceptions import ClientError
from random import choice
from string import lowercase

# from AWS IoT SDK @ https://github.com/aws/aws-iot-device-sdk-python
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient, DROP_OLDEST


log = logging.getLogger('iot-elf')
# log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
# ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s:%(name)s:%(levelname)s - %(message)s')
formatter.converter = time.gmtime  # switch to a UTC converter for the format
ch.setFormatter(formatter)
log.addHandler(ch)

AWS_IOT_MQTT_PORT = 8883
DEFAULT_TOPIC = "elf"
elf_cfg_dir = "misc"
full_certs = "things.json"
cfg_dir = os.getcwd() + '/' + elf_cfg_dir + '/'
elf_file_dir = "misc"
elf_file = "elf.json"
elf_id_key = "elf_id"
elf_id = None
policy_name_key = "elf_policy"
policy_arn_key = "elf_policy_arn"
thing_name_template = "thing_{0}"


make_string = lambda x: "".join(choice(lowercase) for i in range(x))


def certs_exist():
    path = os.getcwd() + '/' + elf_cfg_dir
    files = os.listdir(path)
    if thing_name_template.format(0) + ".pem" in files:
        # if certs created previously there will always be a zero'th pem file
        log.info("Previously created certs exist. Please 'clean' before creating.")
        return True

    return False


def _update_things_config(things):
    things_file = cfg_dir + full_certs
    with open(things_file, "w") as fc_file:
        json.dump(things, fc_file, indent=2,
                  separators=(',', ': '), sort_keys=True)
        log.info("Wrote {0} things to config file: {1}".format(
            len(things), things_file))


def _get_things_config():
    things = None
    things_file = cfg_dir + full_certs
    if os.path.exists(things_file) and os.path.isfile(things_file):
        try:
            with open(things_file, "r") as in_file:
                things = json.load(in_file)
        except OSError as ose:
            log.error('OSError while reading ELF thing config file. {0}'.format(
                ose))
    return things


def _update_elf_config(cfg):
    dirname = os.getcwd() + '/' + elf_file_dir
    log.debug(
        '[_update_elf_config] checking for directory:{0}'.format(dirname))
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except OSError as ose:
            log.error("Error creating directory:{0} {1}".format(dirname, ose))
            log.error("Tring to create directory: {0} again".format(dirname))
            os.makedirs(dirname)

    filename = os.getcwd() + '/' + elf_file_dir + '/' + elf_file
    try:
        with open(filename, "w") as out_file:
            json.dump(cfg, out_file)
            log.debug("Wrote ELF config to file: {0}".format(cfg))
    except OSError as ose:
        log.error('OSError while writing ELF config file. {0}'.format(ose))


def _get_elf_config():
    elf = None
    filename = os.getcwd() + '/' + elf_file_dir + '/' + elf_file
    if os.path.exists(filename) and os.path.isfile(filename):
        try:
            with open(filename, "r") as in_file:
                elf = json.load(in_file)
        except OSError as ose:
            log.error('OSError while reading ELF config file. {0}'.format(ose))
    return elf


def _get_iot_session(region, profile_name):
    if profile_name is None:
        log.debug("ELF loading AWS IoT client using 'default' AWS CLI profile")
        return Session(region_name=region).client('iot')

    log.debug("ELF loading AWS IoT client using '{0}' AWS CLI profile".format(
        profile_name))
    return Session(
        region_name=region,
        profile_name=profile_name).client('iot')


#def _get_json_message(json_message):
#   msg = {}
#   if json_message is None:
#        return msg
#
#    if os.path.exists(json_message) and os.path.isfile(json_message):
#        try:
#            with open(json_message, "r") as in_file:
#                msg = json.load(in_file)
#        except OSError as ose:
#            log.error('OSError while reading JSON Message file. {0}'.format(
#                ose))
#    return msg

# replaces _get_json_message()
def _get_json_messages_simulated(json_message):
    msg = {}
    if json_message is None:
        return msg

    if os.path.exists(json_message) and os.path.isfile(json_message):
        try:
            list_of_events = []
            with open(json_message, 'r') as f:
                for line in f:
                    # Using yaml package instead of json due to unicode issues
                    # in Python 2
                    list_of_events.append(yaml.safe_load(line))
                    msg = list_of_events
        except OSError as ose:
            log.error("OSError while reading JSON Message file. {0}".format(
                ose))
    return msg

def _create_and_attach_policy(region, topic, thing_name, thing_cert_arn, cli):
    # Create and attach to the principal/certificate the minimal action
    # privileges Thing policy that allows publish and subscribe
    tp = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                # "iot:*"
                "iot:Connect",
                "iot:Publish",
                "iot:Receive",
                "iot:Subscribe"
            ],
            "Resource": [
                "arn:aws:iot:{0}:*:*".format(region)
            ]
        }]
    }

    iot = _get_iot_session(region, cli.profile_name)
    policy_name = 'policy-{0}'.format(thing_name)
    policy = json.dumps(tp)
    log.debug('[_create_and_attach_policy] policy:{0}'.format(policy))
    p = iot.create_policy(
        policyName=policy_name,
        policyDocument=policy
    )
    log.debug("[_create_and_attach_policy] Created Policy: {0}".format(
        p['policyName']))

    iot.attach_principal_policy(
        policyName=policy_name, principal=thing_cert_arn)
    log.debug("[_create_and_attach_policy] Attached {0} to {1}".format(
        policy_name, thing_cert_arn))

    return p['policyName'], p['policyArn']


class ElfThread(threading.Thread):
    """
    The abstract thread that sets up interaction with AWS IoT Things
    """

    def __init__(self, thing_name, cli, thing, cfg, args=(), kwargs={}):
        super(ElfThread, self).__init__(
            name=thing_name, args=args, kwargs=kwargs
        )
        self.thing_name = thing_name
        self.thing = thing
        self.root_cert = cli.root_cert
        if cli.append_thing_name:
            self.topic = '{0}/{1}'.format(cli.topic, self.thing_name)
        else:
            self.topic = cli.topic

        self.region = cli.region
        self.cfg = cfg
        self.duration = cli.duration
        self.aws_iot = _get_iot_session(self.region, cli.profile_name)
        self.message_qos = cli.qos

        if policy_name_key not in thing.keys():
            policy_name, policy_arn = _create_and_attach_policy(
                self.region, self.topic,
                self.thing_name, self.thing['certificateArn'],
                cli
            )
            self.policy_name = policy_name
            self.policy_arn = policy_arn
            log.debug("[elf_thread] attached policy on cert:{0}".format(
                thing['certificateArn']))
        else:
            log.debug("[elf_thread] policy_name:{0} exists.".format(
                policy_name_key))
            self.policy_name = thing[policy_name_key]
            self.policy_arn = thing[policy_arn_key]

        # setup MQTT client
        eid = uuid.UUID(cfg[elf_id_key])

        # use ELF ID and a random string since we must use unique Client ID per
        # client.
        cid = eid.urn.split(":")[2] + "_" + make_string(3)

        self.mqttc = AWSIoTMQTTClient(clientID=cid)

        t_name = cfg_dir + thing_name_template.format(0)
        endpoint = self.aws_iot.describe_endpoint()
        log.info("ELF connecting asynchronously to IoT endpoint:'{0}'".format(
            endpoint['endpointAddress']))
        self.mqttc.configureEndpoint(
            hostName=endpoint['endpointAddress'], portNumber=AWS_IOT_MQTT_PORT
        )
        self.mqttc.configureCredentials(
            CAFilePath=self.root_cert,
            KeyPath=t_name + ".prv",
            CertificatePath=t_name + ".pem"
        )
        self.mqttc.configureAutoReconnectBackoffTime(1, 128, 20)
        self.mqttc.configureOfflinePublishQueueing(90, DROP_OLDEST)
        self.mqttc.configureDrainingFrequency(3)
        self.mqttc.configureConnectDisconnectTimeout(20)
        self.mqttc.configureMQTTOperationTimeout(5)

        self.mqttc.connect()  # keepalive default at 30 seconds


class ElfPoster(ElfThread):
    """
    The thread that does the actual message sending for the desired duration
    """

    def __init__(self, thing_name, cli, thing, cfg, args=(), kwargs={}):
        super(ElfPoster, self).__init__(
            thing_name=thing_name, cli=cli, thing=thing, cfg=cfg, args=args,
            kwargs=kwargs
        )
        self.message = cli.message
        self.json_message = cli.json_message

#    def run(self):
#        start = datetime.datetime.now()
#        finish = start + datetime.timedelta(seconds=self.duration)
#        while finish > datetime.datetime.now():
#            time.sleep(1)  # wait a second between publishing iterations
#            msg = {
#            }
#            if self.json_message is None:
#                msg['msg'] = "{0}".format(self.message)
#            else:
#                msg.update(_get_json_message(self.json_message))
#
#            # publish a JSON equivalent of this Thing's message with a
#            # timestamp
#            s = json.dumps(msg, separators=(', ', ': '))
#            log.info("ELF {0} posted a {1} bytes message: {2} on topic: {3}".format(
#                self.thing_name, len(s.encode("utf8")), s, self.topic))
#            self.mqttc.publish(self.topic, s, self.message_qos)

# Overrides previous override of the ElfPoster.run()
def run(self):
    msg_list = _get_json_messages_simulated(self.json_message)
    start = datetime.datetime.now()
    finish = start + datetime.timedelta(seconds=self.duration)
    for msg in msg_list:
        s = json.dumps(msg, separators=(', ', ': '))
        # publish a JSON equivalent of this Thing's message with a
        # timestamp
        log.info("ELF {0} posted a {1} bytes message: {2} on topic: {3}".format(
            self.thing_name, len(s.encode("utf8")), s, self.topic))
        self.mqttc.publish(self.topic, s, self.message_qos)
        # Check if the posting should stop
        time.sleep(1)  # wait a second between publishing iterations
        if finish < datetime.datetime.now():
            break

class ElfListener(ElfThread):
    """
    The thread that subscribes to a topic for the desired duration
    """

    def listener_callback(self, client, userdata, message):
        log.info("Received message: {0} from topic: {1}".format(
            message.payload, message.topic))

    def run(self):
        self.mqttc.subscribe(self.topic, 1, self.listener_callback)
        log.info("ELF {0} subscribed on topic: {1}".format(
            self.thing_name, self.topic))

        start = datetime.datetime.now()
        finish = start + datetime.timedelta(seconds=self.duration)
        while finish > datetime.datetime.now():
            time.sleep(1)  # wait a second between iterations


def _init(cli):
    # Initialize local configuration file and ELF's unique ID
    global elf_id
    elf = _get_elf_config()
    if elf:
        elf_id = uuid.UUID(elf[elf_id_key])
        log.info("Read ELF ID from config: {0}".format(elf_id))
    else:  # file does not exist, so create our ELF ID
        elf_id = uuid.uuid4()
        out_item = {elf_id_key: elf_id.urn}
        _update_elf_config(out_item)
        log.info("Wrote ELF ID to config: {0}".format(out_item[elf_id_key]))


def create_things(cli):
    """
    Create and activate a specified number of Things in the AWS IoT Service.
    """
    _init(cli)
    region = cli.region
    iot = _get_iot_session(region, cli.profile_name)
    count = cli.thing_count
    things = list()
    if certs_exist():
        return

    if count == 0 or count > 1:
        log.info("[create_things] ELF creating {0} things".format(count))
    else:
        log.info("[create_things] ELF creating {0} thing".format(count))

    i = 0
    while i < count:
        ###
        # This is portion of the loop is the core of the `create` command
        # generate a numbered thing name
        t_name = thing_name_template.format(i)
        # Create a Key and Certificate in the AWS IoT Service per Thing
        keys_cert = iot.create_keys_and_certificate(setAsActive=True)
        # Create a named Thing in the AWS IoT Service
        iot.create_thing(thingName=t_name)
        # Attach the previously created Certificate to the created Thing
        iot.attach_thing_principal(
            thingName=t_name, principal=keys_cert['certificateArn'])
        # This is the end of the core of the `create` command
        ###

        things.append({t_name: keys_cert})
        cert_arn = things[i][t_name]['certificateArn']
        log.info("Thing:'{0}' associated with cert:'{1}'".format(
            t_name, cert_arn))

        # Save all the Key and Certificate files locally for future cleanup
        # ..could be added to Keyring later (https://github.com/jaraco/keyring)
        try:
            certname = cfg_dir + t_name + ".pem"
            public_key_file = cfg_dir + t_name + ".pub"
            private_key_file = cfg_dir + t_name + ".prv"
            with open(certname, "w") as pem_file:
                # out_file.write(things[i][thing_name])
                pem = things[i][t_name]['certificatePem']
                pem_file.write(pem)
                log.info("Thing Name: {0} and PEM file: {1}".format(
                    t_name, certname))

            with open(public_key_file, "w") as pub_file:
                pub = things[i][t_name]['keyPair']['PublicKey']
                pub_file.write(pub)
                log.info("Thing Name: {0} Public Key File: {1}".format(
                    t_name, public_key_file))

            with open(private_key_file, "w") as prv_file:
                prv = things[i][t_name]['keyPair']['PrivateKey']
                prv_file.write(prv)
                log.info("Thing Name: {0} Private Key File: {1}".format(
                    t_name, private_key_file))

            _update_things_config(things)
        except OSError as ose:
            log.error('OSError while writing an ELF file. {0}'.format(ose))
        i += 1
        # end 'while' - if there's more, do it all again

    log.info(
        "[create_things] ELF created {0} things in region:'{1}'.".format(
            i, region))


def send_messages(cli):
    """
    Send messages through the AWS IoT service from the previously created
    number of Things.
    """
    _init(cli)
    iot = _get_iot_session(cli.region, cli.profile_name)

    message = cli.message
    # root_cert = args.root_cert
    topic = cli.topic
    duration = cli.duration
    # region = args.region
    log.info(
        "[send_messages] ELF sending:'{0}' on topic root:'{1}' for:{2} secs".format(
            message, topic, duration))

    cfg = _get_elf_config()
    things = _get_things_config()
    if not things:
        log.info("[send_messages] ELF couldn't find previously created things.")
        return

    # setup Things and ElfPoster threads
    i = 0
    ep_list = list()
    for t in things:
        thing_name = thing_name_template.format(i)
        thing = t[thing_name]
        ep = ElfPoster(thing_name, cli, thing, cfg)

        things[i][thing_name][policy_name_key] = ep.policy_name
        things[i][thing_name][policy_arn_key] = ep.policy_arn

        ep_list.append(ep)
        ep.start()
        i += 1

    _update_things_config(things)

    # wait for all the ElfPoster threads to finish their post_duration
    for ep in ep_list:
        ep.join()

    # Now disconnect the MQTT Client
    for ep in ep_list:
        ep.mqttc.disconnect()


def subscribe(cli):
    """
    Subscribe and output messages from messaging topics for all previously
    created Things
    """
    _init(cli)
    iot = _get_iot_session(cli.region, cli.profile_name)

    topic = cli.topic
    duration = cli.duration
    log.info(
        "ELF subscribing on topic root:'{0}' for:{1} secs".format(
            topic, duration))

    cfg = _get_elf_config()
    things = _get_things_config()
    if not things:
        log.info("[subscribe] ELF couldn't find previously created things.")
        return

    # setup Things and ElfListener threads
    i = 0
    el_list = list()
    for t in things:
        thing_name = thing_name_template.format(i)
        thing = t[thing_name]
        el = ElfListener(thing_name, cli, thing, cfg)

        things[i][thing_name][policy_name_key] = el.policy_name
        things[i][thing_name][policy_arn_key] = el.policy_arn

        el_list.append(el)
        el.start()
        i += 1

    _update_things_config(things)

    # wait for all the ElfListener threads to finish their duration
    for el in el_list:
        el.join()

    # Now disconnect the MQTT Client
    for el in el_list:
        el.mqttc.disconnect()


def clean_up(cli):
    """
    Clean up all Things previously created in the AWS IoT Service and files
    stored locally.
    """
    _init(cli)
    log.info("[clean_up] ELF is cleaning up...")
    iot = _get_iot_session(cli.region, cli.profile_name)
    only_local = cli.only_local

    if not only_local:
        elf = _get_elf_config()
        things = _get_things_config()
        if things is None:
            log.info('[clean_up] There is nothing to clean up.')
            return

        i = 0
        for t in things:
            # for each Thing in the configuration file
            thing_name = thing_name_template.format(i)
            thing = t[thing_name]
            # First use the DetachPrincipalPolicy API to detach all policies.
            if policy_name_key in thing:
                try:
                    log.debug('[clean_up] detaching principal policy:{0}'.format(
                        thing[policy_name_key]))
                    iot.detach_principal_policy(
                        policyName=thing[policy_name_key],
                        principal=thing['certificateArn']
                    )
                    # Next, use the DeletePolicy API to delete the policy from
                    # the service
                    log.debug('[clean_up] deleting policy:{0}'.format(
                        thing[policy_name_key]))
                    iot.delete_policy(
                        policyName=thing[policy_name_key]
                    )
                except ClientError as ce:
                    log.info(
                        '[clean_up] could not detach, or delete policy:{0} from cert:{1}'.format(
                            thing[policy_name_key], thing['certificateArn']))
                    log.debug('[clean_up] {0}'.format(ce))

            else:
                log.info('[clean_up] could not find policy to clean')

            # Next, use the UpdateCertificate API to set the certificate to the
            # INACTIVE status.
            try:
                log.debug('[clean_up] deactivating certificate:{0}'.format(
                    thing['certificateId']))
                iot.update_certificate(
                    certificateId=thing['certificateId'],
                    newStatus='INACTIVE'
                )

                # Next, use the DetachThingPrincipal API to detach the
                # Certificate from the Thing.
                log.debug('[clean_up] detaching certificate:{0} from thing:{1}'.format(
                    thing['certificateArn'], thing_name))
                iot.detach_thing_principal(
                    thingName=thing_name,
                    principal=thing['certificateArn']
                )
                time.sleep(1)

                # Last, use the DeleteCertificate API to delete each created
                # Certificate.
                log.debug('[clean_up] deleting certificate:{0}'.format(
                    thing['certificateId']))
                iot.delete_certificate(certificateId=thing['certificateId'])

            except ClientError as ce:
                log.info('[clean_up] could not find, detach, or delete certificate:{0}'.format(
                    thing['certificateId']))
                log.debug('[clean_up] {0}'.format(ce))

            # Then, use the DeleteThing API to delete each created Thing
            log.debug('[clean_up] deleting thing:{0}'.format(thing_name))
            iot.delete_thing(thingName=thing_name)
            log.info(
                '[clean_up] Cleaned things, policies, & certs for:{0}'.format(
                    thing_name))
            i += 1

        log.info(
            '[clean_up] Cleaned {0} things, policies, & certs.. cleaning locally.'.format(i))
        # end of IF

    # Finally, delete the locally created files
    log.debug('[clean_up] local files')
    path = os.getcwd() + '/' + elf_cfg_dir
    files = os.listdir(path)
    for f in files:
        if not f == elf_file:
            log.debug("[clean_up] File found: {0}".format(f))
            os.remove(path + '/' + f)

    log.info("[clean_up] ELF has completed cleaning up in region:{0}".format(
        cli.region))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Simple way to generate IoT messages for multiple Things.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--region', dest='region', help='The AWS region to use.',
                        default='us-west-2')
    parser.add_argument('--profile', dest='profile_name',
                        help='The AWS CLI profile to use.')
    subparsers = parser.add_subparsers()

    create = subparsers.add_parser(
        'create',
        description='Create a number of Things that will interact with AWS IoT')
    create.add_argument('thing_count', nargs='?', default=1, type=int,
                        help="How many 'Things' to create.")
    create.set_defaults(func=create_things)

    send = subparsers.add_parser(
        'send',
        description='Send the given message from each created Thing to the topic.')
    send.add_argument('message', nargs='?', default="IoT ELF Hello",
                      help="The message each Thing will send.")
    send.add_argument('--json-message', dest='json_message',
                      help="The JSON content to be included in an ELF message.")
    send.add_argument('--root-cert', dest='root_cert',
                      default="aws-iot-rootCA.crt",
                      help="The root certificate for the credentials")
    send.add_argument('--topic', dest='topic', default=DEFAULT_TOPIC,
                      help='The topic to which the message will be sent.')
    send.add_argument('--append-thing-name', dest='append_thing_name',
                      default=False, action='store_true',
                      help='Include the thing name in the topic.')
    send.add_argument(
        '--duration', dest='duration', type=int, default=10,
        help='The messages will be sent once a second for <duration> seconds.')
    send.add_argument(
        '--qos', dest="qos", type=int, default=0,
        help='The Quality of Service (QoS) to use when sending messages')
    send.set_defaults(func=send_messages)

    subs = subparsers.add_parser(
        'subscribe',
        description='Subscribe each created Thing to the topic.')
    subs.add_argument(
        '--root-cert', dest='root_cert',
        default="aws-iot-rootCA.crt",
        help="The root certificate for the credentials")
    subs.add_argument('--topic', dest='topic', default=DEFAULT_TOPIC,
                      help='The topic on which to subscribe.')
    subs.add_argument('--append-thing-name', dest='append_thing_name',
                      default=False, action='store_true',
                      help='Include the thing name in the topic.')
    subs.add_argument(
        '--duration', dest='duration', type=int, default=10,
        help='The subscription will listen on the topic for <duration> seconds.')
    subs.add_argument(
        '--qos', dest="qos", type=int, default=0,
        help='The Quality of Service (QoS) to use when subscribed to the topic')
    subs.set_defaults(func=subscribe)

    clean = subparsers.add_parser(
        'clean',
        description='Clean up artifacts used to communicate with AWS IoT')
    clean.set_defaults(func=clean_up)
    clean.add_argument(
        '--force', '--only-local', dest='only_local',
        action='store_true',
        help='WARNING - Force clean only the locally stored ELF files. ELF will NOT clean up the resources created in the AWS IoT service.')

    args = parser.parse_args()
    args.func(args)
