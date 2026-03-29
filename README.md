# 🔏 Cryptrizx-Binance-Bot

<p align="center">
  <img src="https://raw.githubusercontent.com/Kratugautam99/Cryptrizx-Binance-Bot-Project/main/images/icon.png" alt="Cryptrizx Icon" width="300"/>
</p>



**Cryptrizx-Binance-Bot** is a Python-based trading bot for the **Binance Exchange**, offering both **CLI (Command-Line Interface)** and **GUI (Streamlit Web App)** modes. It empowers traders to automate strategies ranging from simple market/limit orders to advanced executions like OCO, Grid, Stop-Limit, and TWAP.

---
🚀 **Docker Container Link:** https://hub.docker.com/r/kratuzen/cryptrizx-binance-bot

---

## 🔗 Quick Links

| Section | Description |
|---------|-------------|
| [🔑 API Credentials](#-api-credentials) | API Key and Secret for Application |
| [⚡ Features](#-features) | Overview of bot capabilities |
| [📦 Installation](#-installation--setup) | Setup and configuration guide |
| [🖥️ CLI Mode](#-cli) | Command-line interface usage |
| [🌐 GUI Mode](#-gui-mode-usage) | Web interface usage |
| [🏗️ Project Structure](#-proj) | Directory organization |
| [🛠️ Tech Stack](#-tech) | Technologies used |
| [🤝 Contributing](#-contributing) | How to contribute |
| [📄 License](#-license) | License information |

---
## 🔑 API Credentials

To connect the bot with **Binance Futures Testnet**, you need to provide your **API Key** and **Secret Key**.

### Where to Get Them
1. Log in to [Binance Futures Testnet](https://testnet.binancefuture.com).
2. Go to the **API Key** tab (below the trading chart).
3. Click **Generate API Key**.
4. Copy both the **API Key** and **Secret Key** (the secret is shown only once).

### How They’re Used
- **API Key** → Identifies your Testnet account.
- **Secret Key** → Signs requests so Binance knows they’re really from you.
- Together, they allow the bot to:
  - Place and cancel orders
  - Check balances and margin
  - Fetch account and position data

### Important Notes
- These keys are **Testnet‑only**. They will not affect your real Binance account or funds.
- Keep them **private** — never commit them to GitHub or share them publicly.
- Store them in a `.env` file or set them as environment variables when running Docker.
- If you suspect your keys are compromised, delete them in the Testnet dashboard and generate new ones.

### Example `.env` File
```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_secret_here
```

---
## ⚡ Features

### 🤖 **Trading Strategies**
- **Market Orders** - Instant execution at current market price
- **Limit Orders** - Set your desired entry/exit prices
- **Grid Orders** - Automated buying low and selling high in ranges
- **OCO Orders** - One-Cancels-Other for risk management
- **Stop-Limit Orders** - Combine stop loss with limit orders
- **TWAP Orders** - Time-Weighted Average Price execution

### 🎯 **Dual Interface**
- **🖥️ CLI Mode** - Fast, scriptable terminal interface
- **🌐 GUI Mode** - User-friendly web dashboard (Streamlit)

### 🔒 **Security & Management**
- Secure API key management via `.env`
- Comprehensive activity logging (`bot.log`)
- Modular and extensible architecture

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Binance account with API keys
- Git installed on your system

### 1. Clone Repository
```bash
git clone https://github.com/Kratugautam99/Cryptrizx-Binance-Bot-Project.git
cd Cryptrizx-Binance-Bot-Project
```

### 2. Environment Setup
**Using Conda:**
```bash
conda env create -f environment.yml   
```

**Using Venv: (Python Version = 3.13.7)**
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies (If Created by Venv)
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Create/update `.env` file in root directory:
```env
BINANCE_API_KEY=your_actual_api_key_here
BINANCE_API_SECRET=your_actual_api_secret_here
```

---
<a id = "-cli"></a>
## 🖥️ CLI Mode Usage

Execute trading strategies directly from terminal:

### Basic Orders
```bash
python CLI_Mode/market_orders.py
python CLI_Mode/limit_orders.py
```

### Advanced Strategies
```bash
python CLI_Mode/advance/grid_orders.py
python CLI_Mode/advance/oco_orders.py
python CLI_Mode/advance/stop_limit_orders.py
python CLI_Mode/advance/twap_orders.py
```

---

## 🌐 GUI Mode Usage

### Local Deployment
```bash
streamlit run GUI_Mode/app.py
```

### Cloud Deployment
Access the docker container:  
👉 [Cryptrizx-Binance-Bot App](https://hub.docker.com/r/kratuzen/cryptrizx-binance-bot)

---
<a id="-proj"></a>
## 🏗️ Project Structure

```
Cryptrizx-Binance-Bot/
│
├── CLI_Mode/                 # Command-line interface
│   ├── client.py            # Binance API client
│   ├── market_orders.py     # Market order execution
│   ├── limit_orders.py      # Limit order execution
│   └── advance/             # Advanced strategies
│       ├── grid_orders.py
│       ├── oco_orders.py
│       ├── stop_limit_orders.py
│       └── twap_orders.py
│
├── GUI_Mode/                # Web interface
│   └── app.py              # Streamlit application
│
├── images/                  # Assets
│   ├── bg.png
│   └── icon.png
│
├── .env                    # Environment variables
├── bot.log                # Activity logs
└── requirements.txt       # Dependencies
```

---

## 📊 Logs & Monitoring

All trading activities are logged for monitoring and debugging:
```bash
tail -f bot.log  # Monitor logs in real-time
```

---
<a id="-tech"></a>
## 🛠️ Tech Stack

- **Python 3.10+** - Core programming language
- **python-binance** - Binance API integration
- **Streamlit** - Web application framework
- **python-dotenv** - Secure configuration management
- **Logging** - Activity tracking and audit trails

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Areas:
- New trading strategies
- UI/UX improvements
- Performance optimizations
- Documentation enhancements
- Bug fixes and testing

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- Use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
- Use commercially and privately

**Attribution is appreciated but not required.**

---

## ⭐ Support

If this project helps you in your trading journey, please consider:

- Giving a **star** ⭐ on [GitHub](https://github.com/Kratugautam99/Cryptrizx-Binance-Bot-Project)
- Sharing with fellow traders
- Reporting issues and suggesting features

---

<div align="center">

**🔥 Happy Trading with Cryptrizx-Binance-Bot! 🔥**

*Automate with confidence, trade with precision, true creation of Kratu Gautam*

</div>
