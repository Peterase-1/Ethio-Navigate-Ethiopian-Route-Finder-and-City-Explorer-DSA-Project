# EthioNavigator

**EthioNavigator** is a desktop-based navigation assistant designed to help users explore Ethiopia's cities and heritage sites. It works completely offline and provides smart, shortest-route recommendations between cities. Users can also search cities, sort them by distance, and discover historical heritages.

---

## Objective

The main goal of this project is to build a **simple offline city navigator** that:

- Helps users **find the shortest path** between Ethiopian cities.
- Promotes tourism by listing **heritage sites**.
- Offers both **normal** and **tourist** navigation modes.
- Includes an **admin panel** for editing city connections and tracking visitor data.

---

## Key Features

- **Offline Navigation** using Dijkstra’s algorithm
- **Tourist Mode** to discover heritage sites on the route
- **Search & Sort Cities** based on current location
- **Recently Viewed Cities** stack
- **Admin Panel** for editing cities and connections
- **AI Chat Assistant** for general questions (requires internet)
- **Visitor Counter** for most visited destinations

---

## How to Run

1. Make sure you have Python 3 installed.
2. Install required libraries:
   pip install -r requirements.txt
3. Run the app.py In gui:
   Admin password "admin123"

---

## Libraries Used

- `tkinter` (GUI)
- `Pillow` (image handling)
- `requests` (AI assistant)
- `networkx`, `heapq` (graph and pathfinding)
- `sqlite3` (offline database)

---

## Note

- The AI assistant requires internet to connect to OpenRouter.
- All other features work **completely offline**.
- Genral Folder Sructure
