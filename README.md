# YouTube Video Summarizer with Gemini API

A Python tool that uses Google's Gemini API to automatically summarize YouTube videos.

## Features

- 🎥 Summarize any YouTube video using AI
- 🌐 Multi-language support (Chinese, Spanish, French, etc.)
- 🚀 Support for multiple Gemini models
- 🎨 Beautiful CLI output with progress indicators
- 💾 Save summaries to file
- 🔧 Custom prompt support
- 🔐 Environment variable support for API keys

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Gemini API key:
   - Copy `.env.example` to `.env`
   - Add your Gemini API key to the `.env` file
   - Or set it as an environment variable: `export GEMINI_API_KEY=your_key_here`

## Usage

### Basic usage:
```bash
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### With custom prompt:
```bash
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID" --prompt "Summarize this video in 3 bullet points"
```

### Save to file:
```bash
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID" -o summary.txt
```

### Use different model:
```bash
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID" --model gemini-2.5-flash
```

### Summarize in different languages:
```bash
# Chinese
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID" --lang zh
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID" --lang chinese

# Spanish
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID" --lang spanish

# French
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID" -l fr
```

### With API key flag:
```bash
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID" --api-key YOUR_API_KEY
```

## Examples

1. **Summarize a tech tutorial:**
```bash
python youtube_summarizer.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --prompt "Extract the main steps and technical concepts from this tutorial"
```

2. **Get key takeaways from a lecture:**
```bash
python youtube_summarizer.py "https://youtu.be/VIDEO_ID" \
  --prompt "List the main concepts discussed and any important definitions"
```

3. **Create study notes:**
```bash
python youtube_summarizer.py "https://youtube.com/watch?v=VIDEO_ID" \
  --prompt "Create detailed study notes with headings and bullet points" \
  -o lecture_notes.txt
```

4. **Get summary in Chinese:**
```bash
python youtube_summarizer.py "https://youtube.com/watch?v=VIDEO_ID" \
  --lang zh \
  -o chinese_summary.txt
```

5. **Combine custom prompt with language:**
```bash
python youtube_summarizer.py "https://youtube.com/watch?v=VIDEO_ID" \
  --lang chinese \
  --prompt "用三个要点总结这个视频的核心内容"
```

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID&t=123s`
- `https://www.youtube.com/embed/VIDEO_ID`

## Supported Languages

The tool supports multiple output languages. Use the `--lang` or `-l` flag:

- **Chinese**: `zh`, `cn`, `chinese`
- **English**: `en`, `english` (default)
- **Spanish**: `es`, `spanish`
- **French**: `fr`, `french`
- **German**: `de`, `german`
- **Japanese**: `ja`, `japanese`
- **Korean**: `ko`, `korean`
- Or specify any other language by name

## Requirements

- Python 3.8+
- Valid Gemini API key
- Internet connection

## Notes

- The tool uses `gemini-2.5-flash` model by default (fast and efficient)
- For more detailed summaries, you can specify different models with `--model` flag
- API usage is subject to Google's rate limits and pricing