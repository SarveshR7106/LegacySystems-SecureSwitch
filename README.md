# Universal Secure Switch for Legacy Systems

## Overview

Many legacy systems such as industrial control systems and metro signaling networks transmit data without encryption, making them vulnerable to interception and cyber-attacks.

This project implements a Universal Secure Switch, which acts as an intermediate layer to transparently secure communication between legacy systems without modifying their hardware or software.

---

## Objectives

* Secure legacy communication without modifying existing systems
* Provide real-time encryption and decryption
* Demonstrate secure versus insecure transmission
* Visualize communication using a monitoring dashboard

---

## Features

### Security

* AES-256-GCM encryption
* ECDH key exchange (dynamic key generation)
* Secure communication tunnel

### Networking

* Socket-based communication
* LAN deployment across multiple machines
* Multi-threaded data handling

### Monitoring Dashboard

* Real-time visualization of:

  * Plaintext before encryption
  * Ciphertext after encryption
  * Decrypted data
* Live log updates
* Data flow representation

---

## System Architecture

Legacy A → Switch A → Encrypted Tunnel → Switch B → Legacy B

* Switch A encrypts outgoing data
* Switch B decrypts incoming data
* Legacy systems operate without modification

---

## Project Structure

PC1 (Sender)

* switchA.py
* legacyA.py

PC2 (Receiver and Dashboard)

* switchB.py
* legacyB.py
* backend/
* frontend/

---

## Technologies Used

* Python

  * Socket programming
  * Threading

* Cryptography

  * AES-256-GCM
  * Elliptic Curve Diffie-Hellman (ECDH)

* Backend

  * Flask

* Frontend

  * HTML, CSS, JavaScript

---

## How to Run

1. Start backend (PC2)
   cd backend
   python server.py

2. Start receiver side (PC2)
   python switchB.py
   python legacyB.py

3. Start sender side (PC1)
   python switchA.py
   python legacyA.py

4. Open dashboard
   Open frontend/index.html in a browser

---

## Demonstration

* Enter a message in Legacy A
* Observe encryption at Switch A
* Data is transmitted in encrypted form
* Decryption occurs at Switch B
* Logs are displayed in real time on the dashboard

---

## Real-World Relevance

This solution demonstrates how modern security mechanisms can be integrated into legacy systems such as industrial control systems, power grids, and transportation networks without requiring costly upgrades.

---

## Key Insight

Security can be added to legacy systems using an intermediate encryption layer, ensuring safe communication without disrupting existing operations.

---

## Future Enhancements

* Attack detection and prevention
* TLS-based secure communication
* Advanced monitoring dashboard with analytics
* Containerized deployment using Docker

---

## Author

Developed as part of a Computer Networks project to demonstrate secure communication for legacy systems.
