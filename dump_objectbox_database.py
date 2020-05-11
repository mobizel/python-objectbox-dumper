import json

import objectbox
from objectbox.model import *

object_box = json.load(open('default.json', 'r'))
entities = object_box['entities']


def get_id_uid(object_box_id):
    box_id, box_uid = [int(i) for i in object_box_id.split(':')]
    print('Parsed id={}, uid={}'.format(box_id, box_uid))
    return box_id, box_uid


def get_property(table, name, box_type=None):
    for prop in table['properties']:
        if prop['name'] == name:
            box_id, uid = get_id_uid(prop['id'])
            print('Creating {} property id={} uid={}'.format(name, box_id, uid))
            return Property(box_type, id=box_id, uid=uid) if name != 'id' else Id(id=box_id, uid=uid)


def find_table(name):
    for entity in entities:
        if entity['name'] == name:
            return entity


json_campaign = find_table('CampaignDB')
campaign_id, campaign_uid = get_id_uid(json_campaign['id'])


@Entity(id=campaign_id, uid=campaign_uid)
class CampaignDB:
    id = get_property(json_campaign, 'id')
    city = get_property(json_campaign, 'city', str)
    name = get_property(json_campaign, 'name', str)
    isCoworker = get_property(json_campaign, 'isCoworker', bool)
    startAt = get_property(json_campaign, 'startAt', str)
    endAt = get_property(json_campaign, 'endAt', str)


campaign_last_prop_id, campaign_last_prop_uid = get_id_uid(json_campaign['lastPropertyId'])
last_entity_id, last_entity_uid = get_id_uid(object_box['lastEntityId'])
last_index_id, last_index_uid = get_id_uid(object_box['lastIndexId'])
last_relation_id, last_relation_uid = get_id_uid(object_box['lastRelationId'])

model = objectbox.Model()
model.entity(CampaignDB, last_property_id=IdUid(campaign_last_prop_id, campaign_last_prop_uid))
model.last_entity_id = IdUid(last_entity_id, last_entity_uid)
model.last_index_id = IdUid(last_index_id, last_index_uid)
model.last_relation_id = IdUid(last_relation_id, last_relation_uid)

print('Model={}'.format(model.last_entity_id))

print('Opening database...')
ob = objectbox.Builder().model(model).directory("ouest").build()
print('Build done')

print('Opening table...')
box = objectbox.Box(ob, CampaignDB)

print('Dumping data')
# id = box.put(person)
for person in box.get_all():
    print(person.first_name)
