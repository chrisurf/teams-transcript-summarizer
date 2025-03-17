#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Teams Meeting Transcript Summarizer

This script uses the sumy library to generate concise summaries of Microsoft Teams
meeting transcripts, following a structured format with overview, key points, and action items.
"""

import argparse
import re
from typing import List, Dict, Any, Tuple

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


class TeamsMeetingSummarizer:
    """Class for summarizing Microsoft Teams meeting transcripts."""

    def __init__(self, language: str = "english"):
        """
        Initialize the summarizer with the specified language.
        
        Args:
            language: Language of the meeting transcript (default: english)
        """
        self.language = language
        self.stemmer = Stemmer(language)
        self.tokenizer = Tokenizer(language)
        self.stop_words = get_stop_words(language)
        
        # Initialize different summarizers
        self.lsa_summarizer = LsaSummarizer(self.stemmer)
        self.lsa_summarizer.stop_words = self.stop_words
        
        self.lex_rank_summarizer = LexRankSummarizer(self.stemmer)
        self.lex_rank_summarizer.stop_words = self.stop_words
        
        self.luhn_summarizer = LuhnSummarizer(self.stemmer)
        self.luhn_summarizer.stop_words = self.stop_words

    def _extract_metadata(self, transcript: str) -> Dict[str, Any]:
        """
        Extract meeting metadata from the transcript.
        
        Args:
            transcript: The meeting transcript text
            
        Returns:
            Dictionary containing meeting metadata
        """
        metadata = {}
        
        # Try to extract meeting title
        title_match = re.search(r"Meeting\s+Title:?\s*(.*?)(?:\n|$)", transcript, re.IGNORECASE)
        if title_match:
            metadata["title"] = title_match.group(1).strip()
        else:
            metadata["title"] = "Meeting Summary"
        
        # Try to extract date
        date_match = re.search(r"Date:?\s*(.*?)(?:\n|$)", transcript, re.IGNORECASE)
        if date_match:
            metadata["date"] = date_match.group(1).strip()
            
        # Try to extract participants
        participants = []
        participant_matches = re.findall(r"(?:Attendees|Participants):?\s*(.*?)(?:\n\n|\n[A-Z]|$)", 
                                         transcript, re.IGNORECASE | re.DOTALL)
        if participant_matches:
            participants_text = participant_matches[0]
            participants = [p.strip() for p in re.split(r"[,;]|\n", participants_text) if p.strip()]
            
        metadata["participants"] = participants
        
        return metadata

    def _identify_action_items(self, sentences: List[str]) -> List[str]:
        """
        Identify potential action items from the summarized sentences.
        
        Args:
            sentences: List of sentences to analyze
            
        Returns:
            List of identified action items
        """
        action_items = []
        action_keywords = ["will", "should", "need to", "needs to", "going to", 
                          "have to", "must", "assigned", "task", "action", "follow up",
                          "follow-up", "todo", "to-do", "deadline"]
        
        for sentence in sentences:
            sentence_lower = str(sentence).lower()
            if any(keyword in sentence_lower for keyword in action_keywords):
                # Extract who is responsible if possible
                responsible_match = re.search(r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?) (?:will|should|needs to|is going to)", 
                                             str(sentence))
                if responsible_match:
                    person = responsible_match.group(1)
                    action = str(sentence).replace(person, f"**{person}**", 1)
                    action_items.append(action)
                else:
                    action_items.append(str(sentence))
                    
        return action_items

    def _identify_topics(self, transcript: str) -> List[str]:
        """
        Identify the main topics discussed in the meeting.
        
        Args:
            transcript: The meeting transcript text
            
        Returns:
            List of identified topics
        """
        # Look for agenda items or section headings
        topic_matches = re.findall(r"(?:Agenda Item|Topic|Section)[\s\d]*:?\s*(.*?)(?:\n|$)", 
                                  transcript, re.IGNORECASE)
        
        # If no explicit topics found, use summarization to extract topics
        if not topic_matches:
            parser = PlaintextParser.from_string(transcript, self.tokenizer)
            summary_sentences = list(self.lsa_summarizer(parser.document, 5))
            
            topics = []
            for sentence in summary_sentences:
                # Extract noun phrases as potential topics
                sentence_str = str(sentence)
                words = sentence_str.split()
                if len(words) > 3:
                    topic = " ".join(words[:3]) + "..."
                    topics.append(topic)
            
            return topics[:3]  # Limit to top 3 topics
        
        return topic_matches

    def summarize(self, transcript: str, summary_ratio: float = 0.2) -> str:
        """
        Generate a structured summary of the Teams meeting transcript.
        
        Args:
            transcript: The meeting transcript text
            summary_ratio: Ratio of original content to include in summary
            
        Returns:
            Formatted summary with overview, key points, and action items
        """
        # Extract metadata
        metadata = self._extract_metadata(transcript)
        
        # Prepare text for summarization
        cleaned_transcript = self._preprocess_transcript(transcript)
        
        # Generate summary using sumy
        parser = PlaintextParser.from_string(cleaned_transcript, self.tokenizer)
        
        # Calculate sentences to extract based on ratio
        total_sentences = len(parser.document.sentences)
        sentences_count = max(5, int(total_sentences * summary_ratio))
        
        # Get summary sentences using LexRank (often works well for meetings)
        summary_sentences = list(self.lex_rank_summarizer(parser.document, sentences_count))
        
        # Identify topics and action items
        topics = self._identify_topics(transcript)
        action_items = self._identify_action_items(summary_sentences)
        
        # Compile the structured summary
        summary = self._format_summary(metadata, summary_sentences, topics, action_items)
        
        return summary

    def _preprocess_transcript(self, transcript: str) -> str:
        """
        Preprocess the transcript for better summarization.
        
        Args:
            transcript: The original transcript text
            
        Returns:
            Preprocessed transcript
        """
        # Remove timestamps and speaker identifiers like [10:15 AM] John Doe:
        cleaned = re.sub(r'\[\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?\]\s*[^:]+:', '', transcript)
        
        # Remove URLs
        cleaned = re.sub(r'https?://\S+', '', cleaned)
        
        # Remove common Teams meeting artifacts
        cleaned = re.sub(r'(?:Meeting started|Meeting ended|Recording started|Recording stopped).*', '', cleaned)
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned

    def _format_summary(self, metadata: Dict[str, Any], 
                       summary_sentences: List[str],
                       topics: List[str],
                       action_items: List[str]) -> str:
        """
        Format the summary according to the structured template.
        
        Args:
            metadata: Meeting metadata
            summary_sentences: Summarized sentences
            topics: Identified topics
            action_items: Identified action items
            
        Returns:
            Formatted summary text
        """
        # Build the summary
        summary_parts = [f"# {metadata['title']}"]
        
        if 'date' in metadata:
            summary_parts.append(f"Date: {metadata['date']}")
        
        if metadata['participants']:
            participants_str = ", ".join(metadata['participants'][:5])
            if len(metadata['participants']) > 5:
                participants_str += f" and {len(metadata['participants']) - 5} others"
            summary_parts.append(f"Participants: {participants_str}")
        
        # 1. Overview section
        summary_parts.append("\n## 1. Overview")
        
        # Extract 2-3 most important sentences for overview
        overview_sentences = [str(s) for s in summary_sentences[:min(3, len(summary_sentences))]]
        summary_parts.append(" ".join(overview_sentences))
        
        # 2. Key Discussion Points
        summary_parts.append("\n## 2. Key Discussion Points")
        
        # Create topic summaries
        for i, topic in enumerate(topics[:5]):  # Limit to 5 topics max
            # Find sentences that might relate to this topic
            topic_lower = topic.lower()
            related_sentences = []
            
            for sentence in summary_sentences:
                sentence_str = str(sentence).lower()
                # Simple relevance check - could be improved with NLP techniques
                if any(word in sentence_str for word in topic_lower.split() if len(word) > 3):
                    related_sentences.append(str(sentence))
            
            # If no directly related sentences found, use the next unused summary sentence
            if not related_sentences and i < len(summary_sentences):
                related_sentences = [str(summary_sentences[i])]
            
            if related_sentences:
                summary_parts.append(f"- **{topic}**: {' '.join(related_sentences[:2])}")
        
        # 3. Action Items
        if action_items:
            summary_parts.append("\n## 3. Action Items")
            for item in action_items:
                summary_parts.append(f"- {item}")
        else:
            summary_parts.append("\n## 3. Action Items")
            summary_parts.append("No specific action items identified.")
        
        return "\n\n".join(summary_parts)


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
