# Discord Data Package Utils

The `discord_data_package_utils` project is designed to process and analyze data exported from Discord. It provides utilities for handling message data, account information, and analytics. The project is modular, with scripts organized into directories based on their functionality.

To start, open the package repository using `cd package`. Then, clone the utils repository using `git clone https://github.com/notafrogo/discord_data_package_utils.git`.

## Directories Overview

### `discord_data_package_utils/messages/`
This directory contains scripts for processing message data. The scripts must be executed in the following order:

1. **`aggregate_messages.py`**: Aggregates messages from multiple folders into a single CSV file.
2. **`sort_messages.py`**: Sorts the aggregated messages by timestamp.
3. **`search_links.py`**: Searches for links in the message contents and generates a file with the extracted links.
4. **`save_images.py`**: Downloads images from the extracted links file.

#### Rules for the `messages` Folder
The `messages` folder is the root directory containing raw message data. It must follow these rules:
- Each subfolder represents a channel and must include:
  - `channel.json`: Metadata about the channel (e.g., `id`, `type`).
  - `messages.json`: A list of messages with fields like `ID`, `Timestamp`, `Contents`, and `Attachments`.
- Ensure all files are valid JSON and properly formatted.

### `discord_data_package_utils/account/`
This directory contains scripts for handling account-related data. These scripts process information about the Discord account owner.

- **`account_details.py`**: Extracts and organizes account details such as username, email, and phone number from the exported data.
- **`activity_log.py`**: Processes the account's activity log, summarizing actions like logins, password changes, and other account events.

### `discord_data_package_utils/analytics/`
This directory contains scripts for analyzing Discord data to generate insights.

- **`message_statistics.py`**: Analyzes message data to compute statistics such as the number of messages sent per channel, most active times, and word frequency.
- **`channel_activity.py`**: Generates reports on channel activity, including participation trends and user contributions.

## Usage Instructions

### Step 1: Process Messages
Follow the steps outlined in the `discord_data_package_utils/messages/` section:
1. Run `aggregate_messages.py` to create `messages.csv`.
2. Run `sort_messages.py` to sort the messages.
3. Run `search_links.py` to extract links.
4. Run `save_images.py` to download images.

### Step 2: Process Account Data
Run the scripts in the `discord_data_package_utils/account/` directory to extract and analyze account-related information.

```bash
python account_details.py
python activity_log.py
```

### Step 3: Analyze Data
Run the scripts in the `discord_data_package_utils/analytics/` directory to generate insights from the processed data.

```bash
python message_statistics.py
python channel_activity.py
```

## Notes
- Ensure all required input files are in the correct format and location before running each script.
- The scripts are designed to work sequentially where applicable. Running them out of order may result in errors or incomplete processing.
- Customize file paths and directory names in the scripts if your project structure differs from the default.