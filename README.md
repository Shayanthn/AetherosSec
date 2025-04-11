# 🛡️ ShaySecure LiveNet Supreme 👁‍🗨

**AetherosSec** | Cybersecurity & Network Monitoring Tool  
Developed with ❤️ by [Shayan Taherkhani](https://linkedin.com/in/shayantaherkhani) | [GitHub](https://github.com/shayanthn)

---

## 🔍 Overview

**ShaySecure LiveNet Supreme** is a powerful, real-time, bilingual (English/Farsi 🇮🇷🇺🇸) network monitoring and defense system designed for advanced users and developers seeking deeper visibility into their active connections and live threat assessment.

Built with `tkinter`, `psutil`, and `matplotlib`, this app provides a professional GUI dashboard to track, filter, analyze, and disconnect suspicious IPs — especially **non-Iranian IPs** (based on customizable prefixes).

---

## 🚀 Features

- 🌐 **Live Connection Table**: Displays app name, paths, local/remote addresses, and connection status
- 🔍 **Search Filter**: Filter connections by port, app name, or IP
- 📊 **Live Traffic Graph**: Visualize connection frequency in real-time (auto-updating)
- 🔐 **Security Checklist**: Instant firewall/antivirus and open ports scan
- ❌ **Kill Suspicious IPs**: Automatically terminate connections from known dangerous IP ranges (e.g., `45.*`, `185.*`)
- 🧠 **Smart UI/UX**:
  - 🔄 Manual refresh
  - 🌘 Dark/Light themes
  - 🌍 Language toggle (English / فارسی)
- 📥 **Export Reports**:
  - Save connection logs as `.txt`, `.json`, or `.csv`
- 📌 **Context Menu** (Right-click):
  - Show full connection details
  - Copy IP / port
  - GeoIP lookup 🌍
  - Disconnect a selected IP

---

## 📸 UI Preview

<p align="center">
  <img src="https://github.com/Shayanthn/AetherosSec/blob/photo/1.png?raw=true" alt="ShaySecure UI Preview" width="850"/>
</p>

---

## 🧰 Technologies Used

| Tech            | Usage                         |
|----------------|-------------------------------|
| `tkinter`       | GUI and UI components         |
| `psutil`        | System process & connection info |
| `matplotlib`    | Live graph rendering          |
| `requests`      | GeoIP lookup (ip-api.com)     |
| `PIL`           | Image handling (for logo)     |
| `json`, `csv`   | Config and report management  |

