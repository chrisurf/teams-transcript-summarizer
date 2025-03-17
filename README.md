# Teams Meeting Summarizer

A Python command-line tool that generates concise, structured summaries of Microsoft Teams meeting transcripts using LM Studio's local API.

## Features

- Automatically generates concise meeting summaries with a clear structure
- Supports multiple languages (English, French, German, Spanish, Portuguese, Italian)
- Customizable summary ratio
- Easy-to-use command-line interface
- Uses local LM Studio API for privacy and flexibility

## Prerequisites

- Python 3.6 or higher
- [LM Studio](https://lmstudio.ai/) installed and running locally
- A compatible language model loaded in LM Studio

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/chrisurf/teams-transcript-summarizer
cd teams-summarize

# Install the package
pip install -e .
```

## Usage

Before using the tool, make sure LM Studio is running with the API server enabled on the default port (1234).

### Basic Usage

```bash
# Basic usage
teams-summarize path/to/transcript.txt

# Save output to a file
teams-summarize path/to/transcript.txt --output summary.md

# Specify a different language
teams-summarize path/to/transcript.txt --language french

# Adjust summary ratio (percentage of original content)
teams-summarize path/to/transcript.txt --ratio 0.3

# Use a different API URL
teams-summarize path/to/transcript.txt --api-url http://localhost:5000/api/v0/chat/completions
```

### Supported Languages

- English (default)
- French
- German
- Spanish
- Portuguese
- Italian

## Output Format

The tool generates summaries in a structured format with three sections:

1. **Overview** - Brief introduction to the meeting purpose, participants, and outcome
2. **Key Discussion Points** - Summary of the main topics discussed
3. **Action Items** - List of tasks assigned during the meeting

## Setting Up LM Studio

1. Download and install [LM Studio](https://lmstudio.ai/)
2. Launch LM Studio
3. Download a model (e.g., Llama 2, Mistral, etc.)
4. Go to the "Local Server" tab
5. Click "Start Server" to begin the API server on http://localhost:1234

## Troubleshooting

- **API Connection Error**: Make sure LM Studio is running and the API server is started.
- **Model Loading Error**: Ensure you have a model loaded in LM Studio before running the summarizer.
- **Long Processing Times**: Large transcripts may take time to process. Consider using a more powerful model or reducing the transcript size.

## License

This project is licensed under the MIT License - see the LICENSE file for details.