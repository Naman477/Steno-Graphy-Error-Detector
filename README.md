# Stenography Error Detector

This Spring Boot web application provides a REST API to detect stenography errors by comparing two uploaded text files.

## Project Structure

The project is built with Maven and follows a standard Spring Boot application structure:

```
.
├── src
│   ├── main
│   │   ├── java
│   │   │   └── com
│   │   │       └── stenography
│   │   │           └── errordetector
│   │   │               ├── controller
│   │   │               │   └── AccuracyController.java
│   │   │               ├── dto
│   │   │               │   └── AccuracyReport.java
│   │   │               ├── service
│   │   │               │   └── AccuracyService.java
│   │   │               └── StenographyErrorDetectorApplication.java
│   │   └── resources
│   │       └── application.properties
│   └── test
│       └── java
│           └── com
│               └── example
│                   └── accuracy
│                       └── service
│                           └── AccuracyServiceTest.java (Optional: for unit tests)
├── pom.xml
└── README.md
```

## API Endpoint

The application exposes a single REST endpoint:

**POST /api/v1/accuracy**

This endpoint accepts `multipart/form-data` with two files:
- `sourceFile`: The file containing the original, correct text.
- `targetFile`: The file containing the text as typed by a user.

### Request Example (using curl)

```bash
curl -X POST \
  http://localhost:8080/api/v1/accuracy \
  -H 'Content-Type: multipart/form-data' \
  -F 'sourceFile=@/path/to/your/source.txt' \
  -F 'targetFile=@/path/to/your/target.txt'
```

Replace `/path/to/your/source.txt` and `/path/to/your/target.txt` with the actual paths to your files.

### Response Example (JSON)

```json
{
  "sourceTotalChars": 520,
  "errorsFound": 15,
  "accuracy": "97.12%",
  "differences": [
    "Mismatch found in Line 10: Source: \"original line\" | Target: \"typed line\"",
    "Target file is missing Line 25: \"missing line content\"",
    "Source file has extra content on Line 5: \"extra line content\""
  ]
}
```

## Core Functionality

- **File Reading:** Reads content from uploaded files, normalizing line endings (`\r\n` and `\r` are converted to `\n`).
- **Levenshtein Distance:** Calculates the minimum number of single-character edits (insertions, deletions, or substitutions) required to transform the `targetText` into the `sourceText`. This serves as the `errorsFound` count.
- **Accuracy Calculation:** Uses the formula: `Accuracy = ((Total Characters in Source - Errors) / Total Characters in Source) * 100`.
- **Line-by-Line Differences:** Generates a list of human-readable strings detailing discrepancies between the source and target files on a line-by-line basis.

## How to Build and Run

### Prerequisites

- Java Development Kit (JDK) 8 or higher
- Maven

### Steps

1.  **Clone the repository** (or create the files manually as described above).
2.  **Navigate to the project root directory** (where `pom.xml` is located) in your terminal.
3.  **Build the project using Maven:**
    ```bash
    mvn clean install
    ```
    This command compiles the code, runs tests, and packages the application into a JAR file.

4.  **Run the application:**
    ```bash
    java -jar target/stenography-error-detector-0.0.1-SNAPSHOT.jar
    ```
    The application will start on `http://localhost:8080`.

## Error Handling

-   **Missing/Empty Files:** Returns `400 Bad Request`.
-   **Internal Server Errors:** Returns `500 Internal Server Error` for unexpected issues during file processing.

---
