def Generate_chest(pos, item_id, count, custom_data):
    x, y, z = pos
    chest = {
    "x": x,
    "y": y,
    "z": z,
    "items": [
        {
            "slot": i,
            "id": item_id,
            "count": count,
            "custom_data": d
        } for i, d in enumerate(custom_data)
    ]
}
    return chest
def Serialize_ChestCommand(chest):
    items = chest['items']
    items_command = ''
    for item in items:

        command =  (
            "{"
            f"Slot:{item['slot']}b,"
            f'id:"{item["id"]}",'
            f"count:{item['count']},"
            'components:{'
            '"minecraft:custom_data":'
            f"{item['custom_data']}"
            "}"
            "}"
        )
        items_command += command + ','
    command = f"setblock {chest['x']} {chest['y']} {chest['z']} " 
    command += 'chest{'
    command += 'Items' + '[' + items_command[:-1] + ']}'
    print(command)
def main():
    pos = (0, 63, 0)
    item_id = 'minecraft:potato'
    slot = 0
    count = 1
    custom_data = [{f"key{i}": f"content{i}"} for i in range(27)]
    chest = Generate_chest(pos, item_id, count, custom_data)
    Serialize_ChestCommand(chest)

if __name__ == '__main__':
    main()