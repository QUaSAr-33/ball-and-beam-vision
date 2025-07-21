# Ball and Beam Vision-Based Balancing System

This project implements a **ball and beam system** with:
- ✅ Physical mechanical build (Fusion 360 design included)
- ✅ Vision-based tracking using a standard webcam
- ✅ PID controller running in real-time
- ✅ Servo actuation via Arduino
- ✅ Simscape Multibody simulation & control design

---

## 📂 Repository Structure
- `docs/` – Mathematical derivation, control design, hardware info
- `mechanical/` – CAD files and build images
- `simulink/` – Simscape models and plots
- `arduino/` – Arduino code for servo control
- `python/` – Python script for webcam tracking
- `videos/` – Demo videos of working system

---

## ▶️ Demo
![Demo](videos/demo_short.mp4)

---

## 🔧 Requirements
- Python 3.x with `opencv-python`, `numpy`, `pyserial`
- Arduino (ESP32/Uno) with Servo library
- Webcam
- MATLAB/Simulink R2023b (for models)

---

## 🚀 Quick Start
1. Open `python/vision_tracking.py` and install requirements:
   ```bash
   pip install -r python/requirements.txt
