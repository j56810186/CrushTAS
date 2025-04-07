import arrow


FPS = 12
VIDEO_SECONDS = 30
API_CALL_SECONDS = 30


def get_time_from_file_stem(file_stem: str, fps=FPS) -> arrow.Arrow:
    # file stem format: 20250405_223006-0001, date_time-frame (date_time is the start time)
    start_time, frame = file_stem.split('-')
    start_time = arrow.get(start_time, 'YYYYMMDD_HHmmss')
    delta_seconds = int(frame) / fps
    return start_time.shift(seconds=delta_seconds)


def get_frame_stems_in_range(
    key_frame_stem: str,
    fps: int = FPS,
    seconds: int = VIDEO_SECONDS,
) -> list[str]:
    # 解析 key_frame_stem 拿到 frame index
    start_time, frame_str = key_frame_stem.split('-')
    start_time = arrow.get(start_time, 'YYYYMMDD_HHmmss')
    key_frame_index = int(frame_str)

    # 要抓取的 frame 範圍
    total_frames = seconds * fps
    start_index = key_frame_index - seconds // 2 * fps

    # max frame index = 30 seconds per API call * 12 fps = 360 frames
    max_frame_index = 30 * fps
    if start_index < 0:
        start_index = max_frame_index + start_index
        start_time = start_time.shift(seconds=-seconds // 2)

    stems = []
    frame_index = start_index
    for _ in range(total_frames):
        frame_index += 1
        if frame_index > max_frame_index:
            frame_index = frame_index - max_frame_index
            start_time = start_time.shift(seconds=seconds // 2)

        # 取得檔名
        stems.append(f"{start_time.format('YYYYMMDD_HHmmss')}-{frame_index:04d}")
    return stems

