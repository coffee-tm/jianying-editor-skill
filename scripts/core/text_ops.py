import os
import re
import asyncio
from typing import Union
import pyJianYingDraft as draft
from utils.formatters import safe_tim, tim

class TextOpsMixin:
    """
    JyProject 的文本与字幕 Mixin。
    """
    def add_text_simple(self, text: str, start_time: Union[str, int] = None, duration: Union[str, int] = "3s", 
                        track_name: str = "Subtitles", **kwargs):
        if start_time is None:
            start_time = self.get_track_duration(track_name)
        self._ensure_track(draft.TrackType.text, track_name)
        
        start_us = safe_tim(start_time)
        dur_us = safe_tim(duration)
        
        # NOTE: pyJianYingDraft 的 TextSegment 直接接受 text 字符串
        seg = draft.TextSegment(text, draft.Timerange(start_us, dur_us), **kwargs)
        self.script.add_segment(seg, track_name)
        return seg

    def add_narrated_subtitles(self, text: str, speaker: str = "zh_female_xiaopengyou", 
                              start_time: Union[str, int] = None, track_name: str = "Subtitles"):
        if start_time is None: start_time = self.get_track_duration(track_name)
        curr_us = safe_tim(start_time)
        
        parts = [p for p in re.split(r'([，。！？、\n\r]+)', text) if p.strip()]
        sentences = []
        for i in range(0, len(parts), 2):
            s = parts[i]
            if i + 1 < len(parts): s += parts[i+1]
            sentences.append(s.strip())

        for s in sentences:
            clean_text = s.rstrip('，。！？、\n\r ')
            if not clean_text: continue
            
            audio_seg = self.add_tts_intelligent(clean_text, speaker=speaker, start_time=curr_us)
            if audio_seg:
                actual_dur_us = audio_seg.target_timerange.duration
                self.add_text_simple(clean_text, start_time=curr_us, duration=actual_dur_us, track_name=track_name)
                curr_us += actual_dur_us + 100000 
        return curr_us

    def add_tts_intelligent(self, text: str, speaker: str = "zh_male_huoli", start_time: Union[str, int] = None, track_name: str = "AudioTrack"):
        from universal_tts import generate_voice
        import uuid
        
        if start_time is None:
            start_time = self.get_track_duration(track_name)
            
        temp_dir = os.path.join(self.root, self.name, "temp_assets")
        os.makedirs(temp_dir, exist_ok=True)
        output_file = os.path.join(temp_dir, f"tts_{uuid.uuid4().hex[:8]}.ogg")
        
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                actual_path = asyncio.run(generate_voice(text, output_file, speaker))
            else:
                actual_path = loop.run_until_complete(generate_voice(text, output_file, speaker))
        except Exception:
            actual_path = asyncio.run(generate_voice(text, output_file, speaker))
            
        if not actual_path: return None
        return self.add_media_safe(actual_path, start_time, track_name=track_name)
