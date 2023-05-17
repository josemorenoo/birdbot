# BirdBot - Crypto Projects Activity Twitter Bot

#### note: this README was auto-generated using ChatGPT, use at your own peril


BirdBot is a Twitter bot that posts daily summaries of developer activities in various cryptocurrency projects. The bot generates and shares bar graphs displaying metrics such as the number of commits, lines of code added, and unique authors contributing to project repositories.

## Features
- Posts daily summaries of developer activities in cryptocurrency projects
- Generates and shares bar graphs displaying metrics like commits, lines of code, and unique authors
- Automatically fetches reports and relevant assets for visualizations
- Supports price delta information along with the activity data
- Configurable content and posting frequency

## Installation & Setup

### Prerequisites
- Python 3.6 or later
- [Tweepy](http://www.tweepy.org/) library
- Twitter Developer Account and API keys

### Installation
1. Clone the repository:
```
git clone https://github.com/yourusername/BirdBot.git
```

2. Change the current working directory to the project directory:
```
cd BirdBot
```

3. Create a virtual environment:
```
python3 -m venv env
```

4. Activate the virtual environment
- Linux or macOS:
```
source env/bin/activate
```

- Windows:
```
env\Scripts\activate
```

5. Install the required dependencies:
```
pip install -r requirements.txt
```

6. Create a file named `local_bird_config.json` in the `config` directory with the following content:
```json
{
  "CONSUMER_KEY": "<YOUR_CONSUMER_KEY>",
  "CONSUMER_SECRET": "<YOUR_CONSUMER_SECRET>",
  "ACCESS_KEY": "<YOUR_ACCESS_KEY>",
  "ACCESS_SECRET": "<YOUR_ACCESS_SECRET>",
  "CMC_KEY": "<YOUR_CMC_KEY>"
}
```
Replace the placeholders with your Twitter API keys.

7. Run the BirdBot:
```
python birdbot.py
```

## Usage

You can configure the content and posting frequency of the BirdBot by modifying the `birdbot.py` file. The bot can generate and post a variety of charts, such as commits and lines of code by location, commits by unique authors, and more, on a daily, weekly, or monthly basis.

## Contributing

Contributions are always welcome! If you have an idea for a new feature, enhancement, or bug fix, please feel free to create an issue or submit a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.
