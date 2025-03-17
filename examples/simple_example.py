#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple example demonstrating how to use the Teams Meeting Transcript Summarizer.
"""

import os
import sys

# Import from the package
from teams_transcript_summarizer import TeamsMeetingSummarizer

def main():
    """Run a simple demonstration of the Teams Meeting Transcript Summarizer."""
    
    # Path to the sample transcript
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'samples', 'sample_transcript.txt')
    
    # Initialize the summarizer
    summarizer = TeamsMeetingSummarizer(language="english")
    
    print("Reading sample transcript from:", sample_path)
    
    # Read the sample transcript
    try:
        with open(sample_path, 'r', encoding='utf-8') as file:
            transcript = file.read()
    except Exception as e:
        print(f"Error reading sample file: {e}")
        return
    
    print("\nGenerating summary...\n")
    
    # Generate the summary
    summary = summarizer.summarize(transcript)
    
    # Print the summary
    print("=" * 80)
    print(summary)
    print("=" * 80)
    
    # Save the summary to a file
    output_path = os.path.join(os.path.dirname(__file__), 'summary_output.md')
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(summary)
        print(f"\nSummary saved to: {output_path}")
    except Exception as e:
        print(f"Error saving summary to file: {e}")

if __name__ == "__main__":
    main()
