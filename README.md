# decenter-ai.streamlit.app

# DeCenter AI

Decentralized AI Model Training Infrastructure
Visit: https://decenter-ai.streamlit.app

## Description

DeCenter AI is a PaaS infrastructure that empowers machine learning engineers to train AI models more quickly and
affordably through decentralized parallel training mechanisms.

## Table of Contents

- [decenter-ai.streamlit.app](#decenter-aistreamlitapp)
- [DeCenter AI](#decenter-ai)
- [Description](#description)
- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Overview](#overview)
- [How to use the demo](#how-to-use-the-demo)
- [How to Contribute](#how-to-contribute)
- [License](#license)
- [Contributors](#contributors)
- [Support](#support)
- [Links](#links)

## Prerequisites

To run project, you need to have the following prerequisites:

- Python (version 3.10 or higher) installed on your machine.
- The necessary Python packages and dependencies installed. You can find the required packages in the `requirements.txt`
  file of the project repository.
- Download and extract the sample python code (model training code), Dataset, requirement text and pre-trained model for
  the demo [sample1.zip](https://github.com/DeCenter-AI/decenter-ai.streamlit.app//files/12517829/sample1.zip)

## How to Run with Python3

To run using `Python` and `make`, follow these steps:

```shell
   git clone https://github.com/DeCenter-AI/decenter-ai.streamlit.app decenter.app
   cd decenter.app
   make install
#   create .env file and fill in the environment variables
   make run
```

## How to Run via Docker

To run the project using `Docker`, follow these steps:

```shell
docker build -t decenter.streamlit .
docker run -p 8501:8501 decenter.streamlit
```

> For developers,
> I recommend <br>
> ```docker run -it -e "mode=development" -p 8501:8501 decenter``` <br>
> playaround and test your code!


> Please note that you will need to replace `<repository_url>` with the actual URL of this/forked repo

I hope this helps! Raise issues to clarify your doubts and notify bugs.

## Overview

DeCenter AI functions as a PaaS infrastructure, empowering machine learning engineers to expedite and make the training
of AI models more cost-effective through decentralized parallel training methods.

The core objective of DeCenter AI is to democratize and decentralize AI model training. By offering a distributed
training platform, it allows data scientists, machine learning engineers, researchers, and AI specialists to
collaboratively contribute to the training of AI models. Structured around a distributed parallel training mechanism,
DeCenter AI has been designed to facilitate the training of various ML and DL models in a significantly reduced time
frame and cost compared to the current norms.
Our platform incorporates a built-in incentive system, fueled by DCEN Tokens. This system not only rewards contributors
and participants but also encourages them to undertake tasks such as reviewing, testing, and rating AI models.

### Features

- Intuitive AI model deployment UI
- Customizable node configuration
- Private decentralized infrastructure
- Scheduled model training

### Target Customers

- Data scientists
- Machine learning engineers
- AI Engineers
  View
  our [Customer profile](https://www.canva.com/design/DAFri_nB4wo/eI4WrI2aQGyfy6T1bx4ZTQ/view?utm_content=DAFri_nB4wo&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink).

### Benefits

- Rapid iteration
- Cost effective
- Seamless deployment
- Automated resource management


## How to use the demo

1. Visit https://decenter-ai.streamlit.app
2. Enter model name
3. Upload training dataset
4. Select training script
5. Click train
6. Model training commences
7. After training is done , you can download your trained model

## How to Contribute

We welcome contributions from the community! To get started, follow these steps:

1. Fork the repository on GitHub.
2. Clone your fork of the repository to your local machine.
3. Create a new branch for your changes: `git checkout -b <your-username>/your-feature-branch`.
4. Make your changes and commit them to your branch.
5. Push your changes to your fork on GitHub.
6. Open a pull request from your fork's branch to the main repository.

Please make sure to follow the [Code of Conduct](./CODE_OF_CONDUCT.md) when contributing to this project.

## License

DeCenter AI is released under the [MIT License](https://opensource.org/licenses/MIT).

## Contributors

- Victor Kaycee [Email](victorkaycee17@gmail.com).  [Linkedln](https://www.linkedin.com/in/victor-kaycee).
- Hiro Nasfame [Email](laciferin@gmail.com).  [Linkedln](http://linkedin.com/in/laciferin/).
- William Ikeji  [Email](williamikeji@gmail.com).  [Linkedln](https://www.linkedin.com/in/codypharm/).
- Dinesh  [Email](dineshjnld22@gmail.com).  [Linkedln](https://www.linkedin.com/in/-dinesh-7a83b2241).


## Support

For any inquiries or assistance, please contact our support team at admin@decenterai.com or visit
our [website](https://decenterai.com/).

## Links

[Deck](https://bit.ly/decenterai).
