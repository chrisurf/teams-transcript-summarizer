#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teams Meeting Transcript Summarizer

This script uses a local LM Studio REST API to generate concise summaries of Microsoft Teams
meeting transcripts, following a structured format with overview, key points, and action items.
"""

import argparse
import json
import sys
import requests
from pathlib import Path
from datetime import datetime

# Update the import logic for meeting_summary_prompts
script_dir = Path(__file__).resolve().parent
prompts_path = script_dir / "prompts"
sys.path.insert(0, str(prompts_path))

try:
    from meeting_summary_prompts import system_prompt, create_user_prompt
except ImportError:
    print("Error: Could not import meeting_summary_prompts.py")
    print("Make sure the prompts directory exists and contains meeting_summary_prompts.py.")
    sys.exit(1)

def summarize_transcript(transcript, language="english", ratio=0.2, api_url="http://localhost:1234/api/v0/chat/completions"):
    """
    Generate a summary of the meeting transcript using the LM Studio API.
    
    Args:
        transcript: The meeting transcript text
        language: Language for the summary instructions
        ratio: The summary ratio (how detailed the summary should be)
        api_url: The API URL for the LM Studio server
        
    Returns:
        The generated summary text
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    # Create the user prompt with the transcript and language
    user_content = create_user_prompt(transcript, language, ratio)
    
    # Prepare the API request data
    data = {
        "model": "localhost",  # Using local model, adjust if needed
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.3,
        "max_tokens": -1,
        "stream": False
    }
    
    try:
        # Send the request to the API
        response = requests.post(api_url, headers=headers, data=json.dumps(data), timeout=300)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response JSON
        response_data = response.json()
        
        # Extract the summary from the response
        if "choices" in response_data and len(response_data["choices"]) > 0:
            summary = response_data["choices"][0]["message"]["content"]
            return summary
        else:
            raise ValueError("Invalid response format from API")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the LM Studio API at", api_url)
        print("Make sure LM Studio is running and the API is available.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: Request to the LM Studio API timed out.")
        print("The transcript might be too long or the model is taking too long to respond.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Could not parse the API response as JSON.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    """Command line interface for the Teams meeting summarizer."""
    parser = argparse.ArgumentParser(
        description='Summarize Microsoft Teams meeting transcripts using LM Studio API.'
    )
    parser.add_argument(
        'input_file', 
        help='Path to the transcript file'
    )
    parser.add_argument(
        '--output', '-o', 
        help='Output file path (optional)'
    )
    parser.add_argument(
        '--language', '-l', 
        default='english',
        choices=['english', 'french', 'german', 'spanish', 'portuguese', 'italian'],
        help='Language of the instructions (default: english)'
    )
    parser.add_argument(
        '--ratio', '-r', 
        type=float, 
        default=0.2,
        help='Summary ratio (0.0-1.0, default: 0.2)'
    )
    parser.add_argument(
        '--api-url', '-u',
        default='http://localhost:1234/api/v0/chat/completions',
        help='URL for the LM Studio API (default: http://localhost:1234/api/v0/chat/completions)'
    )
    parser.add_argument(
        '--destination', '-d',
        help='Destination directory to store the output as a .md file (optional)'
    )
    
    args = parser.parse_args()
    
    # Check if the ratio is valid
    if args.ratio < 0.0 or args.ratio > 1.0:
        print("Error: Summary ratio must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Read the transcript
    try:
        input_path = Path(args.input_file)
        if not input_path.exists():
            print(f"Error: Input file '{args.input_file}' does not exist.")
            sys.exit(1)
            
        with open(input_path, 'r', encoding='utf-8') as file:
            transcript = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Generate the summary
    summary = summarize_transcript(transcript, args.language, args.ratio, args.api_url)
    
    # Output the summary
    if args.destination:
        try:
            # Ensure the destination directory exists
            destination_path = Path(args.destination)
            destination_path.mkdir(parents=True, exist_ok=True)
            
            # Generate the filename with timestamp
            timestamp = datetime.now().strftime("%Y_%m_%d")
            input_filename = input_path.stem.replace(" ", "_")
            output_filename = f"{timestamp}_{input_filename}.md"
            output_file = destination_path / output_filename
            
            # Write the summary to the .md file
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(summary)
            print(f"Summary written to {output_file}")
        except Exception as e:
            print(f"Error writing to destination directory: {e}")
            print("\nSummary:")
            print(summary)
    elif args.output:
        try:
            output_path = Path(args.output)
            
            # Create the directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(summary)
            print(f"Summary written to {args.output}")
        except Exception as e:
            print(f"Error writing to output file: {e}")
            print("\nSummary:")
            print(summary)
    else:
        print(summary)

if __name__ == "__main__":
    main()