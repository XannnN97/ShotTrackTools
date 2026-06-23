#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Remove .png suffix from Clip Name for all clips in the current Media Pool folder.
Place in Workspace > Scripts menu for quick access.
"""

# When running inside Resolve (menu or console), 'resolve' is pre-defined.
# If not defined, try to import for external execution.
if 'resolve' not in globals():
    import DaVinciResolveScript as dvr
    resolve = dvr.scriptapp("Resolve")

def main():
    project = resolve.GetProjectManager().GetCurrentProject()
    if not project:
        print("Error: No project is currently open.")
        return

    mediaPool = project.GetMediaPool()
    folder = mediaPool.GetCurrentFolder()
    if not folder:
        print("Error: Could not get current media pool folder.")
        return

    clips = folder.GetClipList()
    if not clips:
        print("No clips found in current folder.")
        return

    renamed_count = 0
    for clip in clips:
        name = clip.GetClipProperty("Clip Name")
        if name and name.endswith(".png"):
            new_name = name[:-4]
            clip.SetClipProperty("Clip Name", new_name)
            renamed_count += 1
            print(f"Renamed: {name} -> {new_name}")

    print(f"Done! {renamed_count} clip(s) renamed in '{folder.GetName()}'.")

if __name__ == "__main__":
    main()