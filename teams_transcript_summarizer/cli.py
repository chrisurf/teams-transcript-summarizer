#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Command-line interface for the Teams Meeting Transcript Summarizer.
"""

import argparse
from .summarizer import TeamsMeetingSummarizer

def main():
    """Command line interface for the Teams meeting summarizer."""
    parser = argparse.ArgumentParser(description='Summarize Microsoft Teams meeting transcripts.')
    parser.add_argument('input_file', help='Path to the transcript file')
    parser.add_argument('--output', '-o', help='Output file path (optional)')
    parser.add_argument('--language', '-l', default='english', 
                        help='Language of the transcript (default: english)')
    parser.add_argument('--ratio', '-r', type=float, default=0.2,
                        help='Summary ratio (0.0-1.0, default: 0.2)')
    
    args = parser.parse_args()
    
    # Read the transcript
    try:
        with open(args.input_file, 'r', encoding='utf-8') as file:
            transcript = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Create summarizer and generate summary
    summarizer = TeamsMeetingSummarizer(language=args.language)
    summary = summarizer.summarize(transcript, summary_ratio=args.ratio)
    
    # Output summary
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(summary)
            print(f"Summary written to {args.output}")
        except Exception as e:
            print(f"Error writing to output file: {e}")
            print(summary)
    else:
        print(summary)


if __name__ == "__main__":
    main()
