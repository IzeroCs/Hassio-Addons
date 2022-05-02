#!/usr/bin/env python3

from array import array
import time
import json
import validators
import os
import re

from whatsmyip.ip import get_ip
from whatsmyip.providers import GoogleDnsProvider
from namesilo import NameSilo

pconfig = "data/options.json"

if os.path.exists(pconfig) == False:
    pconfig = "/" + pconfig

fconfig = open(pconfig)
config = json.load(fconfig)

if config["api"] == "":
    raise Exception("API Token is empty")
elif config["domain"] == "":
    raise Exception("Domain is empty")
elif config["ttl"] < 3600 or config["ttl"] > 2592001:
    raise Exception("TTL less than 2592001, and greater than or equal to 3600")
elif validators.domain(config["domain"]) == False:
    raise Exception("Domain is not validate")
elif isinstance(config["records"], list) == False:
    raise Exception("Records is not list")
elif len(config["records"]) <= 0:
    raise Exception("Records list is empty")
elif config["interval_update"] < 10:
    raise Exception("Interval update greater than or equal to 10")
fconfig.close()

client = NameSilo(token=config["api"], sandbox=False)
domain = config["domain"]
public_ip = "127.0.0.1"
filter_records = config["records"]
log_records = []
ttl_record = config["ttl"]
interval_update = config["interval_update"]

index = 0
log_records = array("i", range(0, len(filter_records)))
for filter in filter_records:
    match = re.search(f"^(.+)\.{domain}$", filter)
    if match != None and len(match.groups()) > 0:
        filter_records[index] = match.groups()[0]
    log_records[index] = False
    index += 1


def debug(str):
    if config["log"]:
        print(str)


domain_info = None
dns_records = None
domain_info_log = False
dns_records_log = False

while True:
    try:
        ip = get_ip(GoogleDnsProvider)

        if ip != public_ip:
            debug(f"Public IP: {ip}")

        public_ip = ip
    except:
        public_ip = None
        debug(f"Public IP: Failed resolve")

    try:
        domain_info = client.get_domain_info(domain)

        if domain_info_log == False:
            debug(f"Domain {domain} exists!")

        domain_info_log = True
    except:
        domain_info = None
        domain_info_log = False
        debug(f"Domain {domain} not exists!")
        time.sleep(5)

    if domain_info:
        try:
            dns_records = client.dns_list_records(domain)

            if dns_records_log == False:
                debug(f"List records: Success")

            dns_records_log = True
        except:
            dns_records_log = False
            debug(f"List record: Failed")

    if public_ip and domain_info and dns_records:
        index = 0
        for filter in filter_records:
            if filter == "@":
                found = False
                for rc in dns_records.resource_record:
                    if rc.type == "A" and rc.host == domain:
                        found = True

                        if log_records[index] == False:
                            log_records[index] = True
                            debug(f"Found record [@]: type={rc.type}, host={rc.host}, "
                                  f"value={rc.value}, ttl={rc.ttl}")

                        if rc.value != public_ip:
                            try:
                                client.dns_update_record(
                                    domain, rc.record_id, "", public_ip, ttl_record)
                                debug(f"Update record [@]: type{rc.type}, host={rc.host}, "
                                      f"value={public_ip}, ttl={ttl_record}")
                                log_records[index] = True
                            except:
                                log_records[index] = False
                                debug(
                                    "Update record [@]: Failed update record")

                if found == False:
                    try:
                        client.dns_add_record(
                            domain, "A", "", public_ip, ttl_record)
                        debug(f"Add record [@]: type=A, host={domain},"
                              f"value={public_ip}, ttl={ttl_record}")
                        log_records[index] = True
                    except:
                        log_records[index] = False
                        debug("Add record [@]: Failed add record")
            elif filter != "@":
                fdomain = filter + "." + domain
                found = False
                for rc in dns_records.resource_record:
                    if rc.type == "A" and rc.host == fdomain:
                        found = True

                        if log_records[index] == False:
                            log_records[index] = True
                            debug(f"Found record [{filter}]: type={rc.type}, host={rc.host}, "
                                  f"value={rc.value}, ttl={rc.ttl}")

                        if rc.value != public_ip:
                            try:
                                client.dns_update_record(
                                    domain, rc.record_id, filter, public_ip, ttl_record)
                                debug(f"Update record [{filter}]: type{rc.type}, host={rc.host}, "
                                      f"value={public_ip}, ttl={ttl_record}")
                                log_records[index] = True
                            except:
                                log_records[index] = False
                                debug(
                                    f"Update record [{filter}]: Failed update record")
                if found == False:
                    try:
                        client.dns_add_record(
                            domain, "A", filter, public_ip, ttl_record)
                        debug(f"Add record [{filter}]: type=A, host={filter}.{domain},"
                              f"value={public_ip}, ttl={ttl_record}")
                        log_records[index] = True
                    except:
                        log_records[index] = False
                        debug(f"Add record [{filter}]: Failed add record")
            index += 1
        time.sleep(interval_update)
    elif public_ip == None:
        time.sleep(5)
    else:
        time.sleep(5)
