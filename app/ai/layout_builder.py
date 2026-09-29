def build_comic_layout(story_panels: list, image_paths: list) -> list:
    layout = []
    for idx, panel in enumerate(story_panels):
        layout.append({
            "panel": panel.get("panel", idx + 1),
            "title": panel.get("title", f"Panel {idx + 1}"),
            "description": panel.get("description", ""),
            "caption": panel.get("caption", ""),
            "dialogue": panel.get("dialogue", ""),
            "image_prompt": panel.get("image_prompt", ""),
            "image_path": image_paths[idx]
        })
    return layout