import requests
import csv

def get_type_relation(id):
    url = f'https://pokeapi.co/api/v2/type/{id}'
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        type_name = result['name']
        damage_relation = result['damage_relations']
        return type_name, damage_relation
    else:
        print("None")
        return None

def save_to_csv(type_name, damage_relations):
    with open('type_relations.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Type', 'Double Damage From', 'Half Damage From', 'Double Damage To', 'Half Damage To', 'No Damage From', 'No Damage To'])
        writer.writerow({'Type': type_name,
                         'Double Damage From': [weakness['name'] for weakness in damage_relations['double_damage_from']],
                         'Half Damage From': [resistance['name'] for resistance in damage_relations['half_damage_from']],
                         'Double Damage To': [strong['name'] for strong in damage_relations['double_damage_to']],
                         'Half Damage To': [weak['name'] for weak in damage_relations['half_damage_to']],
                         'No Damage From': [immune['name'] for immune in damage_relations['no_damage_from']],
                         'No Damage To': [no_damage['name'] for no_damage in damage_relations['no_damage_to']]})

def main():
    with open('type_relations.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Type', 'Double Damage From', 'Half Damage From', 'Double Damage To', 'Half Damage To', 'No Damage From', 'No Damage To'])
        writer.writeheader()
            
    for i in range(1, 19):
        if i == 0:
            continue
        type_name, damage_relations = get_type_relation(i)
        if damage_relations:
            save_to_csv(type_name, damage_relations)

if __name__ == '__main__':
    main()
