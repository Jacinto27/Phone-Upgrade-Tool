# Phone Upgrade Tool

## Introduction
I needed to update my phone. The first issue that I ran into was the limited flexibility that many phone comparison
tools offer online. The second issue that I ran into was the lackluster ability that current public AI tools have for 
these sort of things, so I made a quick solution in python for that.

## Features
<!-- List of features -->
It takes a phone and outputs a list of phones that are better than it ranked by price in US Dollars.


It compares: battery, ram memory , storage space, video quality, and screen resolution. Additionally, it has the option 
to compare OS versions and can even limit  results for the same original phone's OS.

### Prerequisites
<!-- List of prerequisites and how to install them -->
pandas~=2.0.3 \
Levenshtein~=0.23.0

### Usage
Run phonecomparisor.py. 

## Deployment
<!-- Additional notes about how to deploy this on a live system -->
Currently working on a portable release version. 
## Built With
I used this Kaggle dataset: https://www.kaggle.com/datasets/berkayeserr/phone-prices

Thank you :- [@berkay-eser] https://github.com/berkay-eser  :)

## Versioning
0.9: Core functionalities finished.

## License
This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives (CC BY-NC-ND)- see the [LICENSE.md](LICENSE.md) file for details.

## Notes
Here are some things I won't be fixing:

-The price information on the dataset is iffy, the only other reliable way to get phone prices is through 
scrapping seller or re-seller sites, which I won't do.

-Some information on the dataset is not accurate in terms of memory or performance for some phone models
, besides the nuances there is  comparing any two things, some comparisons just aren't that reliable.

-Basically, the biggest improvement is improving the data, if you have better data the tool will provide better results
without needing to modify it (obviously, accommodate the new data accordingly.)