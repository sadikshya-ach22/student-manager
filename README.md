# Memex

A full-stack, reactive personal knowledge base and resource management dashboard designed to organize educational links, notes, and study materials. 

## Overview
Memex provides a dynamic user interface for categorizing and storing nested web resources. It leverages a modern Python web framework to handle reactive state management and implements a custom local data persistence layer, ensuring that all categories and resources are saved seamlessly across user sessions.

## Key Features
* **State-Driven UI:** Built entirely in Python using reactive state variables to dynamically render the dashboard.
* **Full CRUD Operations:** Users can Create, Read, Update, and Delete custom folders and nested resource links.
* **Local Data Persistence:** Engineered a custom JSON serialization engine to automatically save and load user state, preventing data loss upon browser refresh.
* **Responsive Design:** Clean, grid-based UI that adapts to user inputs instantly.

## Tech Stack
* **Language:** Python 3
* **Framework:** [Reflex](https://reflex.dev/) (Full-stack web framework)
* **Storage:** Native JSON serialization

## Getting Started

To run this application locally on your machine:

### 1. Clone the repository
```bash
git clone [https://github.com/sadikshya-ach22/Memex.git](https://github.com/sadikshya-ach22/Memex.git)
cd Memex
