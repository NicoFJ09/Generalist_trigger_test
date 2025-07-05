# AI Email Assistant

An intelligent system for automatically responding to emails using AI, memory, and human supervision.

## Environment Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env.local` file in the root of the project:

```env
OPENAI_API_KEY=your_openai_key
COMPOSIO_API_KEY=your_composio_key
GMAIL_INTEGRATION_ID=your_gmail_id
```

## Running the Program

### Start the System

```bash
python src/main.py
```

## Authentication Procedure

1. **OAuth Connection**: The system will automatically start the authentication process.
2. **Browser Authorization**: A browser window will open to authorize Gmail access.
3. **Complete OAuth**: Follow the instructions in the browser to authorize the application.
4. **Confirmation**: The system will confirm when the connection is active.
5. **Active Listener**: The program will begin listening for new emails automatically.

## Available Features

### Automatic Email Processing

* **Detection**: Automatically detects new incoming emails.
* **AI Extraction**: Extracts sender information using artificial intelligence.
* **Response Generation**: Creates personalized replies based on your profile.
* **Approval**: Displays the original email and the proposed reply for your review.
* **Sending**: Sends the reply only after your confirmation.

### Interactive Commands

**`help`**

* Show help with all available commands.
* Full list of features and examples.

**`prompt <text>`**

* Ask the AI direct questions.
* Example: `prompt What is the status of my system?`

**`memory`**

* View statistics of processed emails.
* Display learned information about senders.
* Review conversation history.

**`profile`**

* Show information about your Gmail profile.
* View connected account details.

**`quit`**

* Safely exit the program.

## Custom Configuration

Edit `src/config/agent_config.py` to customize:

* **AI Model**: Change the OpenAI model used.
* **Temperature**: Adjust the creativity of generated responses.
* **Tone**: Modify the tone of the replies (professional, casual, etc.).
* **Personal Information**: Update your name, role, and user details.
* **Extraction Categories**: Define what information to extract from emails.
* **Memory**: Configure how many emails to remember per sender.

## Demo Video

🎬 [Watch the demonstration on YouTube](https://youtu.be/oZtXOOnoNbQ)
