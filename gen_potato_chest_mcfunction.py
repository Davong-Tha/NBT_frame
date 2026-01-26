#!/usr/bin/env python3
"""
Generate a .mcfunction that places a chest filled with potatoes,
each stack having custom item NBT (SNBT).

Example:
  python gen_potato_chest_mcfunction.py \
    --out potato_chest.mcfunction \
    --pos "~ ~ ~" \
    --item_nbt 'display:{Name:\'{"text":"Spud of Power","italic":false}\'} ,CustomModelData:12345'
"""

from __future__ import annotations
import argparse
from pathlib import Path

CHEST_SLOTS = 27  # single chest

def normalize_item_nbt(s: str) -> str:
    """
    Accept either:
      - empty string -> no extra tag
      - 'display:{...},CustomModelData:1' -> becomes 'tag:{display:{...},CustomModelData:1}'
      - 'tag:{...}' -> kept as-is
    """
    s = (s or "").strip()
    if not s:
        return ""
    if s.startswith("tag:{") and s.endswith("}"):
        return s
    # If user accidentally includes outer braces, strip them
    if s.startswith("{") and s.endswith("}"):
        s = s[1:-1].strip()
    return f"tag:{{{s}}}"

def make_chest_items(item_id: str, count: int, item_nbt: str) -> str:
    # Each entry is like:
    # {Slot:0b,id:"minecraft:potato",Count:64b,tag:{...}}
    nbt_part = f",{item_nbt}" if item_nbt else ""
    items = []
    for slot in range(CHEST_SLOTS):
        items.append(
            f'{{Slot:{slot}b,id:"{item_id}",Count:{count}b{nbt_part}}}'
        )
    return "[" + ",".join(items) + "]"

def make_setblock_command(pos: str, facing: str, chest_type: str, items_snbt: str) -> str:
    # chest_type: "single" (default), "left", "right" (for double-chest halves)
    # facing: "north|south|east|west"
    # We include state properties + block entity NBT with Items
    return (
        f'/setblock {pos} minecraft:chest[facing={facing},type={chest_type}]'
        f'{{Items:{items_snbt}}} replace'
    )

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="potato_chest.mcfunction", help="Output .mcfunction path")
    ap.add_argument("--pos", default="~ ~ ~", help='Position, e.g. "~ ~ ~" or "0 64 0"')
    ap.add_argument("--facing", default="north", choices=["north", "south", "east", "west"])
    ap.add_argument("--type", default="single", choices=["single", "left", "right"],
                    help='Chest half type (single for normal chest; left/right for double chest halves)')
    ap.add_argument("--item", default="minecraft:potato", help='Item id, e.g. "minecraft:potato"')
    ap.add_argument("--count", type=int, default=64, help="Stack count (1..64)")
    ap.add_argument(
        "--item_nbt",
        default="",
        help=("Custom SNBT for the *item tag*. Examples:\n"
              "  display:{Name:'{\"text\":\"Spud\",\"italic\":false}'}\n"
              "  tag:{display:{Lore:['{\"text\":\"hi\"}']},CustomModelData:7}\n")
    )
    args = ap.parse_args()

    if not (1 <= args.count <= 64):
        raise SystemExit("--count must be between 1 and 64")

    item_nbt = normalize_item_nbt(args.item_nbt)
    items = make_chest_items(args.item, args.count, item_nbt)
    cmd = make_setblock_command(args.pos, args.facing, args.type, items)

    out_path = Path(args.out)
    out_path.write_text(cmd + "\n", encoding="utf-8")
    print(f"Wrote {out_path} with 1 command.")

if __name__ == "__main__":
    main()
