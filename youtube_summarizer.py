#!/usr/bin/env python3
"""
YouTube Video Summarizer using Google Gemini API
"""

import os
import sys
import re
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import google.generativeai as genai
from dotenv import load_dotenv
import validators

console = Console()

class YouTubeSummarizer:
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        """Initialize the summarizer with API key and model."""
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats."""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch\?.*&v=([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def validate_url(self, url: str) -> bool:
        """Validate if the URL is a valid YouTube URL."""
        if not validators.url(url):
            return False
        
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com']
        return any(domain in url for domain in youtube_domains)
    
    def summarize_video(self, video_url: str, prompt: Optional[str] = None, language: str = "English") -> str:
        """Summarize a YouTube video using Gemini API."""
        if not self.validate_url(video_url):
            raise ValueError("Invalid YouTube URL provided")
        
        # Map common language codes to full names
        language_map = {
            'zh': 'Chinese',
            'cn': 'Chinese',
            'chinese': 'Chinese',
            'en': 'English',
            'english': 'English',
            'es': 'Spanish',
            'spanish': 'Spanish',
            'fr': 'French',
            'french': 'French',
            'de': 'German',
            'german': 'German',
            'ja': 'Japanese',
            'japanese': 'Japanese',
            'ko': 'Korean',
            'korean': 'Korean'
        }
        
        # Normalize language input
        lang_lower = language.lower()
        output_language = language_map.get(lang_lower, language)
        
        default_prompt = f"""
        Please provide a comprehensive summary of this YouTube video in {output_language} including:
        1. Main topic and key points
        2. Important insights or findings
        3. Any actionable recommendations
        4. A brief conclusion
        
        Format the summary in a clear, structured way.
        Important: Please write the entire summary in {output_language}.
        """
        
        final_prompt = prompt or default_prompt
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Analyzing video...", total=None)
                
                response = self.model.generate_content([
                    video_url,
                    final_prompt
                ])
                
                progress.update(task, completed=True)
            
            return response.text
        
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

@click.command()
@click.argument('video_url')
@click.option('--api-key', envvar='GEMINI_API_KEY', help='Gemini API key (or set GEMINI_API_KEY env var)')
@click.option('--model', default='gemini-2.5-flash', help='Gemini model to use')
@click.option('--prompt', help='Custom prompt for summarization')
@click.option('--output', '-o', help='Save summary to file')
@click.option('--lang', '-l', default='English', help='Output language (e.g., Chinese, zh, Spanish, French)')
def main(video_url: str, api_key: str, model: str, prompt: str, output: str, lang: str):
    """Summarize YouTube videos using Google Gemini API."""
    
    load_dotenv()
    
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            console.print("[red]Error: No API key provided. Set GEMINI_API_KEY environment variable or use --api-key flag[/red]")
            sys.exit(1)
    
    try:
        console.print(Panel.fit(
            f"[bold cyan]YouTube Video Summarizer[/bold cyan]\n"
            f"[dim]Model: {model}[/dim]",
            border_style="cyan"
        ))
        
        summarizer = YouTubeSummarizer(api_key, model)
        
        console.print(f"\n[yellow]Video URL:[/yellow] {video_url}")
        console.print(f"[yellow]Output Language:[/yellow] {lang}")
        
        summary = summarizer.summarize_video(video_url, prompt, lang)
        
        console.print("\n[green]Summary:[/green]\n")
        console.print(Panel(summary, border_style="green", padding=(1, 2)))
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(f"YouTube Video Summary\n")
                f.write(f"URL: {video_url}\n")
                f.write(f"Model: {model}\n")
                f.write(f"Language: {lang}\n")
                f.write(f"\n{'-' * 50}\n\n")
                f.write(summary)
            console.print(f"\n[green]Summary saved to:[/green] {output}")
    
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()