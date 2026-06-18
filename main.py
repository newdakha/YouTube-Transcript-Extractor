#!/usr/bin/env python3
"""
YouTube Video → Text
Использование:
    python yt_transcribe.py <URL или video_id>

Установка зависимости:
    pip install youtube-transcript-api
"""

import sys
import re

def extract_video_id(url_or_id: str) -> str:
    """Извлекает video_id из ссылки или возвращает как есть."""
    patterns = [
        r"(?:v=|youtu\.be/|embed/|shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    # Если передан голый ID
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id
    raise ValueError(f"Не удалось извлечь video_id из: {url_or_id}")


def get_transcript(video_id: str, lang: str = None) -> str:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
    except ImportError:
        print("Установи библиотеку:\n  pip install youtube-transcript-api")
        sys.exit(1)

    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)

        # Пробуем нужный язык → авто-сгенерированный → любой доступный
        transcript = None
        if lang:
            try:
                transcript = transcript_list.find_transcript([lang])
            except Exception:
                pass

        if transcript is None:
            try:
                transcript = transcript_list.find_generated_transcript(
                    [lang] if lang else ["ru", "en", "uk", "kk"]
                )
            except Exception:
                pass

        if transcript is None:
            transcript = next(iter(transcript_list))

        print(f"Язык субтитров: {transcript.language} ({transcript.language_code})\n")
        data = transcript.fetch()

        lines = []
        for entry in data:
            # новая версия возвращает объекты, старая — словари
            text = (entry.text if hasattr(entry, "text") else entry.get("text", "")).strip()
            if text:
                lines.append(text)

        return " ".join(lines)

    except TranscriptsDisabled:
        print("Субтитры отключены для этого видео.")
        sys.exit(1)
    except NoTranscriptFound:
        print("Субтитры не найдены. Попробуй указать язык вручную: python yt_transcribe.py <url> en")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Использование: python yt_transcribe.py <YouTube URL или video_id> [язык, напр. ru или en]")
        sys.exit(1)

    url_or_id = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        video_id = extract_video_id(url_or_id)
    except ValueError as e:
        print(e)
        sys.exit(1)

    print(f"Video ID: {video_id}")
    print("Получаю субтитры...\n")

    text = get_transcript(video_id, lang)

    print("=" * 60)
    print(text)
    print("=" * 60)

    # Сохраняем в файл
    output_file = f"{video_id}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\nСохранено в: {output_file}")


if __name__ == "__main__":
    main()
