from __future__ import annotations

import json
from pathlib import Path

import cadquery as cq


def build_part(cfg: dict) -> cq.Workplane:
    length = float(cfg["length"])
    width = float(cfg["width"])
    height = float(cfg["height"])
    hole_diameter = float(cfg["hole_diameter"])
    fillet_radius = float(cfg["fillet_radius"])
    edge_margin = float(cfg["edge_margin"])

    if min(length, width, height, hole_diameter) <= 0:
        raise ValueError("all dimensions must be positive")
    if edge_margin <= hole_diameter:
        raise ValueError("edge_margin must be greater than hole_diameter")

    part = (
        cq.Workplane("XY")
        .box(length, width, height)
        .edges("|Z")
        .fillet(fillet_radius)
    )

    hole_points = [
        (length / 2 - edge_margin, width / 2 - edge_margin),
        (-length / 2 + edge_margin, width / 2 - edge_margin),
        (length / 2 - edge_margin, -width / 2 + edge_margin),
        (-length / 2 + edge_margin, -width / 2 + edge_margin),
    ]

    return part.faces(">Z").workplane().pushPoints(hole_points).hole(hole_diameter)


def validate(part: cq.Workplane) -> None:
    solid = part.val()
    bbox = solid.BoundingBox()
    if bbox.xlen < 20 or bbox.ylen < 20 or bbox.zlen < 5:
        raise ValueError("bounding box too small, check parameters")


def main() -> None:
    config_path = Path("params.json")
    output_dir = Path("generated")
    output_dir.mkdir(parents=True, exist_ok=True)

    config = json.loads(config_path.read_text(encoding="utf-8"))
    part = build_part(config)
    validate(part)

    output_step = output_dir / f"{config['part_no']}_{config['revision']}.step"
    cq.exporters.export(part, str(output_step))

    report = {
        "part_no": config["part_no"],
        "revision": config["revision"],
        "output": str(output_step),
        "status": "ok",
    }
    (output_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Export success: {output_step}")


if __name__ == "__main__":
    main()
