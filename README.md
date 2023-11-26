# README

## TL;DR

A toy spider using Selenium and XPath to collect info.

## Table of Contents

- [Usage](#Usage)
- [References](#References)
- [Maintainers](#Maintainers)
- [License](#License)

## Usage

Use python venv:

```bash
python3 -m venv venv
source venv/bin/activate
```

Or using anaconda:

```bash
conda create -n <venv_name>
conda activate <venv_name>
```

Run the following command.

```bash
pip3 -r requirements.txt

python3 main.py --url https://www.baidu.com \
                --enable-proxy \
                --skip-cloudflare-waf \
                --set-driver-path resources/chromedriver
```

## References

- [Selenium-python](https://selenium-python.readthedocs.io/installation.html)
- [Chrome Driver - WebDriver from Chrome](https://sites.google.com/chromium.org/driver/downloads?authuser=0)
- [Chrome for Testing availability](https://googlechromelabs.github.io/chrome-for-testing/)
- [stealth.min.js](https://cdn.jsdelivr.net/gh/requireCool/stealth.min.js/stealth.min.js)

## Maintainers

[@Leryn](https://github.com/leryn1122).

## License

[MIT](LICENSE-MIT) or [Apache-2.0](LICENSE-Apache-2.0) © Leryn
