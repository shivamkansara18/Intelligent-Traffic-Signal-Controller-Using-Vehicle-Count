🚦 Intelligent Traffic Signal Controller Using Vehicle Density (Web Portal)

An AI-powered web-based traffic signal control system that dynamically calculates green signal time for all four lanes of an intersection based on traffic density from an uploaded image.

The system analyzes a single image containing all four lanes, detects vehicles in each lane using YOLO + OpenCV, and assigns priority-based signal timing to optimize traffic flow under Indian traffic conditions.

📌 Project Overview

Traffic congestion is a major problem in urban areas, especially in India, where traffic consists of mixed vehicle types such as cars, bikes, auto-rickshaws, buses, and trucks. Traditional traffic signal systems operate on fixed timers, leading to inefficiencies and long waiting times.

This project introduces an Intelligent Traffic Signal Controller Web Portal that:

Accepts an image of a four-lane intersection

Detects and counts vehicles in each lane

Calculates optimal green signal duration for each lane

Assigns priority to lanes with higher traffic density

🌐 Web Portal Workflow

User uploads an image containing all four lanes

Image is processed using YOLO-based vehicle detection

Vehicles are counted lane-wise

Traffic density is calculated per lane

Green signal time is assigned dynamically

Output displays:

Vehicle count per lane

Green signal time for each lane

Priority order of lanes

🔍 Key Features

🚗 Real-time vehicle detection from images

🛵 Supports Indian mixed traffic

📊 Lane-wise vehicle counting

⏱️ Dynamic green signal time calculation

🚦 Priority-based traffic control

🌐 User-friendly web interface

🧠 Signal Timing Logic (High-Level)

Lanes with higher vehicle density receive longer green time

Minimum and maximum green time limits are enforced

All four lanes are processed simultaneously

Signal priority adapts automatically based on traffic conditions

🧑‍💻 Tech Stack

Programming Language: Python

Computer Vision: OpenCV

Object Detection: YOLO

Web Framework: Flask

Frontend: HTML, CSS

🛠️ Requirements

Python 3.x

OpenCV

YOLO (pre-trained model)

Flask

NumPy

📷 Input & Output
Input

Image containing all four lanes of an intersection

Output

Vehicle count per lane

Green signal time for:

Lane 1

Lane 2

Lane 3

Lane 4

Priority order based on traffic density

📂 Dataset & Model

Due to size limitations, datasets and model weights are not included in this repository.

Dataset: Indian Driving Dataset (IDD)
https://idd.insaan.iiit.ac.in/

YOLO Model Weights:
https://github.com/ultralytics

🚀 Future Enhancements

Live CCTV video integration

Emergency vehicle detection & priority

Pedestrian signal handling

IoT-based traffic light hardware integration

Real-time dashboard for traffic authorities

🎓 Academic Relevance

This project is suitable for:

Minor / Major Project

Smart City Applications

Intelligent Transportation Systems

Computer Vision & AI-based Systems
