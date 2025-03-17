from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="teams-transcript-summarizer",
    version="0.1.0",
    author="Community Contributor",
    author_email="example@example.com",
    description="A tool to generate concise summaries of Microsoft Teams meeting transcripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisurf/teams-transcript-summarizer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "teams-summarize=teams_transcript_summarizer.cli:main",
        ],
    },
)
