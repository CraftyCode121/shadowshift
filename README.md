# ShadowShift ⚡
![ShadowShift Banner](<./Lit your Media(2).png>)

**ShadowShift** is a FastAPI-powered backend for the ShadowShift web platform — an AI-driven service that enhances low-light photos and videos using a custom **ZR-DCE** (Zero-Reference Deep Curve Estimation) model built with TensorFlow's subclassing API.

---

## ✨ Enhancement Preview

![Before vs After](./BEFORE(1).png)

---

## Features

- 🔐 **JWT Authentication** — Secure user registration, login, and token-based access control
- 💳 **Billing System** — Subscription and payment management for tiered access
- 🖼️ **Media Gallery** — Per-user storage and retrieval of uploaded and processed media
- 🤖 **AI Model Serving** — Real-time inference with ZR-DCE to enhance low-light images and videos
- ⚡ **FastAPI** — Async, high-performance REST API with auto-generated docs

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Auth | JWT (OAuth2 Password Flow) |
| AI Model | ZR-DCE — TensorFlow Subclassing API |
| Media | User gallery with upload & retrieval endpoints |
| Billing | Integrated payment/subscription management |

---

## Project Structure

```
shadowshift/
├── app/
│   ├── auth/          # JWT authentication & user management
│   ├── billing/       # Subscription & payment logic
│   ├── media/       # Media upload
│   ├── model/         # ZR-DCE model definition & inference serving
│   └── main.py        # FastAPI app entry point
├── requirements.txt
└── .gitignore
...... other files
```

---

## Getting Started

**1. Clone & install dependencies**

```bash
git clone https://github.com/CraftyCode121/shadowshift.git
cd shadowshift
pip install -r requirements.txt
```
**2. Run the development server**

```bash
uvicorn app.main:app --reload
```

## The Model — ZR-DCE

The enhancement engine is built on **Zero-Reference Deep Curve Estimation (ZR-DCE)**, implemented using TensorFlow's model subclassing API. It enhances low-light images and videos without requiring paired training data, applying learned curve transformations to restore brightness and detail naturally.

---

## License

MIT © [CraftyCode121](https://github.com/CraftyCode121)
