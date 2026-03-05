import os
import sys


def resolve_wrapper_path() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_root = os.getenv("JY_SKILL_ROOT", "").strip()
    candidates = [
        env_root,
        os.path.join(current_dir, ".agent", "skills", "jianying-editor"),
        os.path.join(current_dir, ".trae", "skills", "jianying-editor"),
        os.path.join(current_dir, ".claude", "skills", "jianying-editor"),
        os.path.join(current_dir, "skills", "jianying-editor"),
        os.path.abspath(".agent/skills/jianying-editor"),
        os.path.abspath(".trae/skills/jianying-editor"),
        os.path.abspath(".claude/skills/jianying-editor"),
        os.path.dirname(current_dir),  # examples/ under skill root
    ]
    for p in candidates:
        if not p:
            continue
        scripts_dir = os.path.join(os.path.abspath(p), "scripts")
        if os.path.exists(os.path.join(scripts_dir, "jy_wrapper.py")):
            return scripts_dir
    raise ImportError("Could not find jianying-editor/scripts/jy_wrapper.py")


WRAPPER_PATH = resolve_wrapper_path()
if WRAPPER_PATH not in sys.path:
    sys.path.insert(0, WRAPPER_PATH)

from jy_wrapper import JyProject


def main() -> None:
    project = JyProject(project_name="Hello_JianYing_V3", overwrite=True)

    skill_root = os.path.dirname(WRAPPER_PATH)
    assets_dir = os.path.join(skill_root, "assets")
    video_path = os.path.join(assets_dir, "video.mp4")
    bgm_path = os.path.join(assets_dir, "audio.mp3")

    if not os.path.exists(video_path) or not os.path.exists(bgm_path):
        print(f"Demo assets not found: {assets_dir}")
        return

    print("Importing video...")
    project.add_media_safe(video_path, start_time="0s", duration="5s", track_name="VideoTrack")

    print("Adding bgm...")
    project.add_media_safe(bgm_path, start_time="0s", duration="5s", track_name="AudioTrack")

    print("Adding text...")
    # Keep text clips non-overlapping on the same text track to avoid SegmentOverlap.
    project.add_text_simple("Hello JianYing API!", start_time="1s", duration="1.6s", anim_in="复古打字机")
    project.add_text_simple("Simple Clip Demo", start_time="2.7s", duration="1.6s", anim_in="向右滑动")

    print("Saving project...")
    project.save()
    print("Done. Open JianYing and find draft: Hello_JianYing_V3")


if __name__ == "__main__":
    main()
