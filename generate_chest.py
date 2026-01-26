import argparse

def generate_command(pos, item_id, component):
    chest = Chest()
    command = ''
    space = ' '
    command += "setblock" + space
    command += pos + space
    print(command)
    item = Item(item_id, 1, component)
    chest.add_item(item)
    print(len(chest.items))


class Chest:
    def __init__(self):
        self.items = []
        self.slot = [f"{i}b" for i in range(27)]
    def add_item(self, item):
        if len(self.items) < len(self.slot):
            self.items.append(item)

class Item:
    def __init__(self, id, count, component):
        self.id = id
        self.count = count
        self.component = component

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="potato_chest.mcfunction", help="Output .mcfunction path")
    ap.add_argument("--pos", default="0 63 0", help='Position, e.g. "~ ~ ~" or "0 64 0"')
    ap.add_argument("--facing", default="north", choices=["north", "south", "east", "west"])
    ap.add_argument("--type", default="single", choices=["single", "left", "right"],
                    help='Chest half type (single for normal chest; left/right for double chest halves)')
    ap.add_argument("--item", default="minecraft:potato", help='Item id, e.g. "minecraft:potato"')
    ap.add_argument("--count", type=int, default=64, help="Stack count (1..64)")
    ap.add_argument(
        "--item_nbt",
        default="\"key\":\"content\"",
       
    )
    args = ap.parse_args()
    generate_command(args.pos, args.item, args.item_nbt)

if __name__ == '__main__':
    main()