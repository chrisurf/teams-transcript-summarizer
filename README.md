# Teams Transcript Summarizer

A Python tool that generates concise, structured summaries of Microsoft Teams meeting transcripts using the [sumy](https://github.com/miso-belica/sumy) text summarization library.

## Features

- Automatically extracts and formats meeting metadata (title, date, participants)
- Generates concise summaries using state-of-the-art summarization algorithms
- Identifies key discussion topics from the conversation
- Detects action items and who is responsible for them
- Structures output in a clear format with overview, discussion points, and action items
- Supports customizable summary length and multiple languages

## Installation

### Prerequisites

- Python 3.6 or higher

### Install from GitHub

```bash
# Clone the repository
git clone https://github.com/chrisurf/teams-transcript-summarizer.git
cd teams-transcript-summarizer

# Install the package and dependencies
pip install -e .
```

### Install with pip (coming soon)

```bash
pip install teams-transcript-summarizer
```

## Usage

### Command Line Usage

After installation, you can use the tool from the command line:

```bash
# Basic usage
teams-summarize path/to/transcript.txt

# Save output to a file
teams-summarize path/to/transcript.txt --output summary.md

# Specify a different language
teams-summarize path/to/transcript.txt --language french

# Adjust summary ratio (percentage of original content)
teams-summarize path/to/transcript.txt --ratio 0.3
```

### Python API Usage

You can also use the tool programmatically in your Python projects:

```python
from teams_summarizer import TeamsMeetingSummarizer

# Initialize the summarizer
summarizer = TeamsMeetingSummarizer(language="english")

# Read a transcript file
with open("path/to/transcript.txt", "r", encoding="utf-8") as f:
    transcript_text = f.read()

# Generate summary
summary = summarizer.summarize(transcript_text, summary_ratio=0.2)

# Print or save the summary
print(summary)
```

## Example Output

For a sample meeting transcript, the tool will generate output like:

```markdown
# Q1 Product Roadmap Discussion

Date: March 15, 2025
Participants: John Smith, Sarah Johnson, Mike Chen, Emma Williams, David Kim, Lisa Rodriguez

## 1. Overview

The meeting focused on planning the Q1 product roadmap. The team discussed prioritizing mobile optimization, calendar integration, and customizable notifications based on user feedback. The team assigned responsibilities and set deadlines for each feature.

## 2. Key Discussion Points

- **Mobile Performance**: Mobile optimization was identified as a high priority due to a 23% increase in support tickets. Lisa's team will work on this issue with an expected delivery by the end of April.

- **Calendar Integration**: Integration with Google Calendar, Outlook, and Apple Calendar will cover 95% of the user base. This feature will require 6 weeks of development time and is scheduled for May.

- **Customizable Notifications**: The most requested notification options have been compiled by the support team. David's team will implement this feature in parallel with mobile optimization, with completion expected by mid-April.

- **Data Sync Bug**: An intermittent data sync issue affecting 2% of users needs to be fixed. The root cause has been identified as cache management and should take about 1 week to resolve.

## 3. Action Items

- **Fix the data sync bug**: David's team - by end of March
- **Mobile performance optimization**: Lisa's team - by end of April
- **Customizable notifications**: David's team - by mid-April
- **Calendar integration**: Lisa's team - starting May
- **Send detailed roadmap document**: John - by tomorrow
```

## How It Works

The Teams Transcript Summarizer works by:

1. **Preprocessing**: Cleans the transcript by removing timestamps and speaker identifiers
2. **Metadata Extraction**: Identifies meeting title, date, and participants
3. **Summarization**: Applies advanced text summarization algorithms from the sumy library
4. **Topic Identification**: Extracts key topics from the discussion
5. **Action Item Detection**: Identifies sentences that describe tasks or responsibilities 
6. **Structured Formatting**: Organizes the information into a clear, readable format

## Supported Languages

The tool supports multiple languages through the sumy library, including:

- English
- German
- French
- Spanish
- Portuguese
- Italian
- Czech
- Ukrainian
- Russian
- Japanese
- Chinese
- And [many more](https://github.com/miso-belica/sumy#is-my-natural-language-supported)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [sumy](https://github.com/miso-belica/sumy) - The underlying text summarization library
- Microsoft Teams - For the transcript format this tool is designed to process
