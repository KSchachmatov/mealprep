<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

<img src="readmeai/assets/logos/purple.svg" width="30%" style="position: relative; top: 0; right: 0;" alt="Project Logo"/>

# MEALPREP

<em>Empowering your culinary journey with AI precision.</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/license/KSchachmatov/mealprep?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
<img src="https://img.shields.io/github/last-commit/KSchachmatov/mealprep?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/KSchachmatov/mealprep?style=default&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/KSchachmatov/mealprep?style=default&color=0080ff" alt="repo-language-count">

<!-- default option, no dependency badges. -->


<!-- default option, no dependency badges. -->

</div>
<br>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
    - [Project Index](#project-index)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

mealprep is a comprehensive developer tool that combines Docker, AI, and database management to revolutionize meal planning.

**Why mealprep?**

This project streamlines meal preparation with its core features:

- **🐳 Dockerized Environment:** Easily set up and deploy the application.
- **🚀 AI-Powered Meal Planning:** Efficiently plan meals based on dietary preferences and ingredients.
- **💡 Streamlit Interface:** User-friendly interface for interactive meal planning.
- **🔧 Flexible Configuration:** Customize settings for tailored meal management.

---

## Features

|      | Component       | Details                              |
| :--- | :-------------- | :----------------------------------- |
| ⚙️  | **Architecture**  | <ul><li>Follows a modular architecture with clear separation of concerns.</li><li>Utilizes Python for backend logic and Streamlit for frontend presentation.</li></ul> |
| 🔩 | **Code Quality**  | <ul><li>Consistent code style following PEP 8 guidelines.</li><li>Includes unit tests for critical functionalities.</li></ul> |
| 📄 | **Documentation** | <ul><li>Comprehensive documentation available in the form of README, inline comments, and Docker setup instructions.</li></ul> |
| 🔌 | **Integrations**  | <ul><li>Integrates with TimescaleDB for efficient time-series data storage.</li><li>Uses Pandas for data manipulation and Pydantic for data validation.</li></ul> |
| 🧩 | **Modularity**    | <ul><li>Codebase is organized into reusable modules for easy maintenance and extensibility.</li><li>Separate modules for database interactions, data processing, and UI components.</li></ul> |
| 🧪 | **Testing**       | <ul><li>Includes unit tests using pytest to ensure code reliability and functionality.</li><li>Mocking used for external dependencies to isolate testing.</li></ul> |
| ⚡️  | **Performance**   | <ul><li>Optimized queries for TimescaleDB to handle large datasets efficiently.</li><li>Utilizes asynchronous programming for improved responsiveness.</li></ul> |
| 🛡️ | **Security**      | <ul><li>Follows best practices for handling sensitive data.</li><li>Uses Python-dotenv for managing environment variables securely.</li></ul> |
| 📦 | **Dependencies**  | <ul><li>Dependencies managed using uv and listed in pyproject.toml.</li><li>Includes clear dependency versions to ensure compatibility.</li></ul> |

---

## Project Structure

```sh
└── mealprep/
    ├── Dockerfile
    ├── README.md
    ├── docker-compose.yml
    ├── example.env
    ├── init.sql
    ├── main.py
    ├── pyproject.toml
    ├── src
    │   ├── main.py
    │   ├── mealprep/
	│	│	├── config/
	│	│	│	├── settings.py
	│	│	├── db/
	│	│	│	├── database.py
	│	│	│	├── models.py
	│	│	│	└── vector_store.py
	│	│	├── helpers/
	│	│	│	└── utils.py
	│	│	├── llm/
	│	│	│	├── claude_client.py
	│	│	│	└── openai_client.py
	│	│	├── services/
	│	│	│	├── meal_services.py
	│	│	│	└── shopping_service.py
    │   └── mealprep.egg-info/
    ├── tests
    │   ├── __init__.py
    │   └── test_meal_service.py
    └── uv.lock
```

### Project Index

<details open>
	<summary><b><code>MEALPREP/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/Dockerfile'>Dockerfile</a></b></td>
					<td style='padding: 8px;'>- Define the Docker environment for a Streamlit app<br>- Set up dependencies, copy code, and expose the app on port 8501<br>- Implement a health check and run Streamlit to serve the application.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/pyproject.toml'>pyproject.toml</a></b></td>
					<td style='padding: 8px;'>- Define the project structure and dependencies for the AI-powered meal planning assistant<br>- The code file in pyproject.toml specifies build requirements, project details, and necessary dependencies<br>- It sets up the build system using setuptools and defines project metadata such as name, version, and description<br>- This file ensures smooth project setup and management.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/init.sql'>init.sql</a></b></td>
					<td style='padding: 8px;'>- Initialize database schema with tables for meals, recipes, and meal plans, including necessary extensions and indexes<br>- Define relationships between meals and meal plans<br>- Optimize for vector similarity search in recipes<br>- Use JSONB for metadata storage<br>- Ensure data integrity and efficient querying for meal planning and recipe management.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/docker-compose.yml'>docker-compose.yml</a></b></td>
					<td style='padding: 8px;'>- Define a Docker Compose configuration for a meal prep project<br>- Set up a TimescaleDB service for data storage and a Streamlit service for app functionality<br>- Ensure proper communication between services and define necessary environment variables<br>- Use volumes for data persistence and specify health checks for reliability.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/main.py'>main.py</a></b></td>
					<td style='padding: 8px;'>Prints a greeting message from mealprep when executed.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- src Submodule -->
	<details>
		<summary><b>src</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ src</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/main.py'>main.py</a></b></td>
					<td style='padding: 8px;'>- Generate a user-friendly AI Meal Planner interface using Streamlit<br>- The code in <code>main.py</code> allows users to suggest single meals based on ingredients, dietary preferences, and number of people<br>- It also supports generating multi-day meal plans with shopping lists, meal acceptance/rejection, and plan saving/loading functionalities<br>- The interface simplifies meal planning and enhances user experience.</td>
				</tr>
			</table>
			<!-- mealprep.egg-info Submodule -->
			<details>
				<summary><b>mealprep.egg-info</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.mealprep.egg-info</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep.egg-info/PKG-INFO'>PKG-INFO</a></b></td>
							<td style='padding: 8px;'>- Provide a high-level overview of the AI-powered meal planning assistant, detailing its dependencies and version requirements<br>- This metadata file, located in the projects egg-info directory, outlines essential information such as project name, version, and required Python packages<br>- It serves as a crucial reference point for understanding the projects dependencies and compatibility.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep.egg-info/SOURCES.txt'>SOURCES.txt</a></b></td>
							<td style='padding: 8px;'>Describe the purpose and use of the README.md file in the project structure.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep.egg-info/requires.txt'>requires.txt</a></b></td>
							<td style='padding: 8px;'>- Ensure seamless integration of essential dependencies for the project by specifying required packages in the requires.txt file<br>- This file lists crucial libraries like Streamlit, Pandas, and psycopg2-binary, enabling smooth functionality across the codebase architecture.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep.egg-info/top_level.txt'>top_level.txt</a></b></td>
							<td style='padding: 8px;'>Enable meal preparation planning and organization within the project architecture.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep.egg-info/dependency_links.txt'>dependency_links.txt</a></b></td>
							<td style='padding: 8px;'>Generate a summary that highlights the main purpose and use of the code file provided in the entire codebase architecture.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- mealprep Submodule -->
			<details>
				<summary><b>mealprep</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.mealprep</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep/insert_vectors.py'>insert_vectors.py</a></b></td>
							<td style='padding: 8px;'>- Generate and insert pescetarian recipe data into the VectorStore for meal preparation, filtering out meat-based recipes<br>- Prepare records for insertion by extracting content and embeddings, then create tables and insert data for efficient storage and retrieval.</td>
						</tr>
					</table>
					<!-- llm Submodule -->
					<details>
						<summary><b>llm</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.mealprep.llm</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep/llm/openai_client.py'>openai_client.py</a></b></td>
									<td style='padding: 8px;'>- Implement a client to interact with the OpenAI API, providing structured meal suggestions<br>- The client utilizes a given prompt, along with optional similar recipes, to generate meal recommendations<br>- It handles API communication, error handling, and structured output parsing to deliver validated meal suggestions.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- config Submodule -->
					<details>
						<summary><b>config</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.mealprep.config</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep/config/settings.py'>settings.py</a></b></td>
									<td style='padding: 8px;'>- Define and configure application settings for logging, language models, databases, and vector stores<br>- Includes OpenAI-specific settings and database connection details<br>- Provides a method to retrieve cached settings and functions to fetch API keys and database URLs<br>- Centralizes and manages various configuration options for the project.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- db Submodule -->
					<details>
						<summary><b>db</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.mealprep.db</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep/db/models.py'>models.py</a></b></td>
									<td style='padding: 8px;'>- Define a Pydantic model for meal suggestions with fields for meal name, ingredients, and recipe steps<br>- This model serves as a structured representation of meal data within the database models, facilitating easy access and manipulation of meal information.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep/db/vector_store.py'>vector_store.py</a></b></td>
									<td style='padding: 8px;'>- Manage vector operations and database interactions<br>- Generate embeddings, create tables, indexes, upsert data, search for similar embeddings, and delete records<br>- Utilizes OpenAI and Timescale Vector clients for efficient data handling<br>- Offers flexibility in querying with metadata filters and predicates<br>- Provides detailed search functionality with time-based filtering options.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep/db/database.py'>database.py</a></b></td>
									<td style='padding: 8px;'>- Describe the purpose and use of the <code>database.py</code> file in the projects architecture<br>- The file provides a robust interface for interacting with a PostgreSQL database to manage meal-related data, including adding meals, updating feedback, retrieving meal records, and saving meal plans<br>- It encapsulates database operations for meals, ingredients, and user feedback, facilitating seamless data management within the meal preparation application.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep/db/database_sqlite.py'>database_sqlite.py</a></b></td>
									<td style='padding: 8px;'>- Manage meal data in a SQLite database, including adding, updating, and retrieving meals<br>- Ensure the existence of a meals table and connect to the database<br>- Retrieve meal names from the past N days and fetch meal records by name<br>- Close the database connection when done.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- helpers Submodule -->
					<details>
						<summary><b>helpers</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.mealprep.helpers</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep/helpers/utils.py'>utils.py</a></b></td>
									<td style='padding: 8px;'>- Enhances DataFrame with dietary preferences based on ingredients, categorizing meals as with_meat, pescetarian, vegetarian, vegan, or omnivore<br>- Identifies ingredients like meat, fish, shellfish, dairy, eggs, and honey, excluding desserts with fish or meat<br>- The function enriches data for dietary analysis and meal planning within the project's architecture.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- services Submodule -->
					<details>
						<summary><b>services</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.mealprep.services</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep/services/shopping_service.py'>shopping_service.py</a></b></td>
									<td style='padding: 8px;'>- Implement a service that handles shopping-related functionalities for the meal prep application<br>- This code file plays a crucial role in managing shopping tasks within the projects architecture.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/KSchachmatov/mealprep/blob/master/src/mealprep/services/meal_service.py'>meal_service.py</a></b></td>
									<td style='padding: 8px;'>- The <code>MealService</code> class in <code>meal_service.py</code> facilitates meal planning by suggesting recipes based on available ingredients, dietary preferences, and past meals<br>- It also allows for adding new meals to the database, retrieving recent meals, providing feedback, and generating meal plans with shopping lists<br>- This service streamlines the meal planning process for users, enhancing their culinary experience.</td>
								</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Uv
- **Container Runtime:** Docker

### Installation

Build mealprep from the source and intsall dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/KSchachmatov/mealprep
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd mealprep
    ```

3. **Install the dependencies:**

<!-- SHIELDS BADGE CURRENTLY DISABLED -->
	<!-- [![docker][docker-shield]][docker-link] -->
	<!-- REFERENCE LINKS -->
	<!-- [docker-shield]: https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white -->
	<!-- [docker-link]: https://www.docker.com/ -->

	**Using [docker](https://www.docker.com/):**

	```sh
	❯ docker build -t KSchachmatov/mealprep .
	```
<!-- SHIELDS BADGE CURRENTLY DISABLED -->
	<!-- [![uv][uv-shield]][uv-link] -->
	<!-- REFERENCE LINKS -->
	<!-- [uv-shield]: https://img.shields.io/badge/uv-DE5FE9.svg?style=for-the-badge&logo=uv&logoColor=white -->
	<!-- [uv-link]: https://docs.astral.sh/uv/ -->

	**Using [uv](https://docs.astral.sh/uv/):**

	```sh
	❯ uv sync --all-extras --dev
	```

### Usage

Run the project with:

**Using [docker](https://www.docker.com/):**
```sh
docker run -it {image_name}
```
**Using [uv](https://docs.astral.sh/uv/):**
```sh
uv run python {entrypoint}
```

### Testing

Mealprep uses the {__test_framework__} test framework. Run the test suite with:

**Using [uv](https://docs.astral.sh/uv/):**
```sh
uv run pytest tests/
```

---

## Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

## Contributing

- **💬 [Join the Discussions](https://github.com/KSchachmatov/mealprep/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/KSchachmatov/mealprep/issues)**: Submit bugs found or log feature requests for the `mealprep` project.
- **💡 [Submit Pull Requests](https://github.com/KSchachmatov/mealprep/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/KSchachmatov/mealprep
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/KSchachmatov/mealprep/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=KSchachmatov/mealprep">
   </a>
</p>
</details>

---

## License

Mealprep is protected under the [LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## Acknowledgments

- Credit `contributors`, `inspiration`, `references`, etc.

<div align="right">

[![][back-to-top]](#top)

</div>


[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square


---
