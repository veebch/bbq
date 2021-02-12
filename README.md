

[![video](https://img.youtube.com/vi/-270Nn1V2hQ/0.jpg)](https://www.youtube.com/watch?v=-270Nn1V2hQ)

# The Daily Basic-Bitch Quote (and Word a Day and Headline and Cartoon) Scraper

This is a script that parses content from [r/quotes](https://reddit.com/r/quotes) and tidies it up a little to make an ever-changing Quote poster, using content from the hive-mind that is the internet. 

The quote is then displayed on the attached [Waveshare 6inch HD ePaper](https://www.waveshare.com/6inch-hd-e-paper-hat.htm).

The reason for using r/quotes rather than a curated database, is that the karma score on reddit is a really good way to ensure quotes that are interesting and topical. 

The quality of the results depends on the adherence to convention in posts to [r/quotes](https://reddit.com/r/quotes) and the quality of the regex in the script. Currently the script is rarely producing garbled quotes, so it's ready for sharing. 

As well as producing quotes, the script occasionally places other content on the epaper - to keep things interesting.

The script randomly chooses from 4 options:

- Quote (from [r/quotes](https://reddit.com/r/quotes))
- Word of the Day (from [wordsmith.org](https://wordsmith.org))
- Headline (From The Guardian)
- Cartoon (From The New Yorker)

# Installation

First, clone this repository using

    git clone https://github.com/llvllch/bbq

then:

    cd bbq
    
Install the required modules using pip:

    python3 -m pip install -r requirements.txt


Run the code using:

    python3 quotey.py
    
To periodically run the script, set it as a [cronjob](https://opensource.com/article/17/11/how-use-cron-linux)

