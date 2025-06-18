<br />
<div align="center">
  <h3 align="center">Trivial Rescue IA</h3>

  <p align="center">
    Search algorithms for optimizing disaster relief food distribution routes.
    <br />
    <br />
    <a href="#-demo">View Demo</a>
    &middot;
    <a href="#-getting-started-with-development">Start Developing</a>
  </p>

<h4 align="center">
⭐ Don't forget to Starring ⭐
</h4>

  <div align="center">

[![Python][Python-badge]][Python-url]

  </div>

  <div align="center">

![University][university-badge]
![Subject][subject-badge]
![Grade][grade-badge]

  </div>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>📋 Table of Contents</summary>

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [Getting Started with Development](#-getting-started-with-development)
- [Contributing](#-contributing)
- [Developed by](#-developed-by)
</details>



## 🔍 About The Project

### 🎯 The goal

The goal of the project was to develop search algorithms that optimize food distribution during natural disasters. The system efficiently allocates limited resources to affected areas while considering vehicle constraints, fuel limitations, and changing weather conditions. It prioritizes critical zones based on population density and severity, managing different vehicle types (drones, helicopters, trucks, boats) with varying capabilities to maximize coverage of disaster-affected areas within tight time windows using both informed and uninformed search strategies.

### ⚙️ How it works?

Our solution consists of two main components: a map generation script that creates realistic disaster scenarios with terrestrial, aerial, and maritime routes, and a route optimization script that visualizes the map and implements various search algorithms. Given the tonnage of supplies to distribute, the system automatically finds the optimal delivery routes by analyzing different pathways and vehicle capabilities to ensure efficient resource allocation across affected areas.

### 🎬 Demo

https://github.com/user-attachments/assets/4f26a1e6-976d-4d5f-ab63-4f46d37c6538

### 🧩 Features

The algorithms implemented in this project are:

- Depth First Search
- Breadth First Search
- A*
- Greedy (without multiple capitals)
- IDDFS
- Dijkstra (without multiple capitals)
- Bidirectional DFS
- Bidirectional BFS
- Depth Limited Search (with multiple capitals)



## 🚀 Getting Started with Development

To get a local copy up and running follow these simple example steps.

### 1. Prerequisites

Start by installing the following tools:

- [Git](https://git-scm.com/downloads) - Version Control System
- [Python](https://www.python.org/downloads/) - Programming Language

### 2. Cloning

Now clone the repository to your local machine. You can do this using Git:

```bash
$ git clone git@github.com:darguima/Trivial-Rescue-IA.git
# or
$ git clone https://github.com/darguima/Trivial-Rescue-IA.git
```

### 3. Creating a Virtual Environment

It's a good practice to create a virtual environment for your project to manage dependencies. You can do this with the following commands:

```bash
$ python3 -m venv .venv
```

Each time you open a new terminal, you need to activate the virtual environment. You can do this with the following command:

```bash
$ source .venv/bin/activate
```

### 4. Install Dependencies

Install the required dependencies for the project. This is typically done using a package manager like `pip`. Run the following command:

```bash
$ pip install -r requirements.txt
```

### 5. Generating a Random Map

Then generate a random map with the following command:

```bash
# Feel free to change the settings of the generator on the firsts lines of the script
$ python src/generate_matrix_map.py
```

This will create `random_cities.json` and `random_cities_routes.json` to be used in the project.


### 6. Running the Project

Finally, you can run the project with the following command:

```bash
$ python src/main.py
```


## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## 👨‍💻 Developed by

- [Afonso Pedreira](https://github.com/afooonso)
- [Afonso Dionísio Santos](https://github.com/Afonso-santos)
- [Dário Guimarães](https://github.com/darguima)
- [Hugo Rauber](https://github.com/HugoLRauber)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[university-badge]: https://img.shields.io/badge/University-Universidade%20do%20Minho-red?style=for-the-badge
[subject-badge]: https://img.shields.io/badge/Subject-IA-blue?style=for-the-badge
[grade-badge]: https://img.shields.io/badge/Grade-18%2F20-brightgreen?style=for-the-badge

[Python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white  
[Python-url]: https://www.python.org/
