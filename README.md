# Phone Upgrade Tool
Python Console app that tells you which phone to upgrade to if you give it your current phone model.

For more information visit the [complete documentation](./Docs/overview.md).

<!-- Brief introduction and how to get started -->

## Introduction
I needed to update my phone. The first issue that I ran into was the limited flexibility that many online phone comparison
tools offer. The second issue that I ran into was the lackluster ability that current public AI tools have for 
these sort of things, so I made a quick solution in Python for that.

## Features
<!-- List of features -->
It takes a phone and outputs a list of phones that are better than it ranked by score.
The score takes the difference in quality between the input phone and the result phones and adjusts it for the price difference.

It compares: battery, ram memory , storage space, video quality, and screen resolution. Additionally, it has the option 
to compare OS versions and can even limit results for the same original phone's OS.

It also has a phone data cleaning tool, but this is specifically for the data I used, so it's not expandable or universal.

## Getting Started
Download the repository and run the phonecomparisor.py file, adjust the location of the data if needed. It pulls from the 'Processed' folder in the repository, I call it using the *NOT AT ALL RECOMMENDED* os file location method .dirname, it's not easy to make it run on other PCs so just adjust the location manually by inputting the route to the 'Processed' folder in your compter. 

After thats done, answer the prompts as instructed on the console log, ignore the warnings (I'm working on them) and get an output. 

I tried to turn this into an executable for easier deployment, but I don't want to remove my antivirus for that, I'll create a release version when the project is ironed out.

#Prerequisites
I used Python 3.11
Unsure about library version requirements.

#Usage
This project is for personal and academic use, it is not intended for commercial use. Please consult the LICENSE file for more information.

#Contributing
Feel free to make changes to this tool. Please follow standard git guidelines for feature-branch development through pull requests. Thanks :)

#Authors

Me :) Jacinto27
