# Health Platform

This project is a simple health platform that allows for patient registration, statistics calculation, patient search, and a queue system for patient attendance. 

## Features

- **Patient Registration**: Register new patients with their details.
- **Statistics Calculation**: Calculate statistics such as total patients, average age, youngest and oldest patients.
- **Patient Search**: Search for registered patients by name.
- **Queue Management**: Manage a queue for patient attendance.

## Project Structure

```
health-platform
├── src
│   ├── main.py
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── patient_controller.py
│   │   └── queue_controller.py
│   ├── models
│   │   ├── __init__.py
│   │   └── patient.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── registration.py
│   │   ├── statistics.py
│   │   └── search.py
│   └── utils.py
├── tests
│   ├── test_registration.py
│   ├── test_statistics.py
│   └── test_search.py
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd health-platform
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

Follow the on-screen instructions to navigate through the menu and use the functionalities of the health platform.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you'd like to add.

## License

This project is licensed under the MIT License. See the LICENSE file for details.