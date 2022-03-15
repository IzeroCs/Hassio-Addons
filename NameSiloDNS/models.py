class DomainInfo:
    def __init__(self, data):
        self.auto_renew = data['namesilo']['reply']['auto_renew']
        self.created = data['namesilo']['reply']['created']
        self.expires = data['namesilo']['reply']['expires']
        self.locked = data['namesilo']['reply']['locked']
        self.private = data['namesilo']['reply']['private']
        self.status = data['namesilo']['reply']['status']
        self.traffic_type = data['namesilo']['reply']['traffic_type']
        self.name_servers = NameServers.process(
            data['namesilo']['reply']['nameservers'])
        self.contacts = Contact(data['namesilo']['reply']['contact_ids'])


class DnsRecords:
    def __init__(self, data):
        self.code = data['namesilo']['reply']['code']
        self.detail = data['namesilo']['reply']['detail']
        self.resource_record = self._process_resource_record(
            data['namesilo']['reply'])

    @staticmethod
    def _process_resource_record(reply):
        rs_list = []
        if "resource_record" in reply:
            if isinstance(reply['resource_record'], list):
                for resource_record in reply['resource_record']:
                    rs_list.append(ResourceRecord(resource_record))
            else:
                rs_list.append(ResourceRecord(reply['resource_record']))
        return rs_list


class ResourceRecord:
    def __init__(self, data):
        self.record_id = data['record_id']
        self.type = data['type']
        self.host = data['host']
        self.value = data['value']
        self.ttl = data['ttl']
        self.distance = data['distance']


class NameServers:
    @staticmethod
    def process(data):
        ns_list = []
        for name_server in data['nameserver']:
            ns_list.append(name_server['#text'])
        return ns_list


class Contact:
    def __init__(self, data):
        self.administrative = data['administrative']
        self.billing = data['billing']
        self.registrant = data['registrant']
        self.technical = data['technical']


class ContactModel:
    def __init__(self, **kwargs):
        self.contact_id = self._correct_formating(kwargs.get('contact_id'))
        self.first_name = self._correct_formating(kwargs.get('first_name'))
        self.last_name = self._correct_formating(kwargs.get('last_name'))
        self.address = self._correct_formating(kwargs.get('address'))
        self.city = self._correct_formating(kwargs.get('city'))
        self.state = self._correct_formating(kwargs.get('state'))
        self.country = self._correct_formating(kwargs.get('country'))
        self.email = self._correct_formating(kwargs.get('email'))
        self.phone = self._correct_formating(kwargs.get('phone'))
        self.zip = self._correct_formating(kwargs.get('zip'))

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.contact_id}"

    @staticmethod
    def convert_contact_model(reply):
        return ContactModel(
            contact_id=reply['contact_id'],
            first_name=reply['first_name'],
            last_name=reply['last_name'],
            address=reply['address'],
            city=reply['city'],
            state=reply['state'],
            country=reply['country'],
            zip=reply['zip'],
            email=reply['email'],
            phone=reply['phone']
        )

    @staticmethod
    def _correct_formating(data: str):
        return data.replace(" ", "%20")
