from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="teams-summarize",
    version="0.1.0",
    author="chrisurf",
    author_email="me@chrisurf.com",
    description="A tool to generate concise summaries of Microsoft Teams meeting transcripts using LM Studio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisurf/teams-transcript-summarizer",
    py_modules=["teams_summarize", "prompts.meeting_summary_prompts"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "teams-summarize=teams_summarize:main",
        ],
    },
)