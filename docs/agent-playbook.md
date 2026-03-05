# Agent Playbook

Task routing matrix for reliable execution.

## 1) Cloud Video + BGM Draft

- Read: `rules/setup.md`, `rules/media.md`, `rules/audio-voice.md`
- Reference: `examples/cloud_video_music_tts_demo.py`
- Required checks:
  - BGM goes to audio track.
  - project saved successfully.

## 2) Narration + Subtitle Alignment

- Read: `rules/text.md`, `rules/audio-voice.md`
- APIs: `add_tts_intelligent`, `add_narrated_subtitles`
- Required checks:
  - subtitle timing aligns with narration.
  - subtitle track exists.

## 3) Recording + Smart Zoom

- Read: `rules/recording.md`
- Execute: `tools/recording/recorder.py`
- Required checks:
  - recording output exists.
  - generated draft can be opened.

## 4) Effects / Transitions

- Read: `rules/effects.md`, `rules/keyframes.md`
- Tools: `scripts/asset_search.py`
- Required checks:
  - selected IDs resolved.
  - no None returns from effect/transition methods.

## 5) Commentary from Long Video

- Read: `rules/generative.md`
- Prompt: `prompts/movie_commentary.md`
- Execute: `scripts/movie_commentary_builder.py`
- Required checks:
  - input media pre-optimized (<=30 min, 360p preferred).
  - storyboard JSON parsed and applied.

## 6) Export and CI-facing Validation

- Read: `rules/core.md`, `rules/cli.md`
- Execute:
  - `scripts/auto_exporter.py`
  - `scripts/api_validator.py --json`
- Required checks:
  - output file exists.
  - CLI return code and JSON contract are valid.
