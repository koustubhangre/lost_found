# Lost & Found Reports 🧳🔎

A Flask-based web app for **submitting, searching, updating, and deleting** lost and found item reports. Users can log details, upload images, and manage reports securely. Data is stored in **MongoDB** using **MongoEngine**.

---

## ✨ Features

📝 Submit lost or found item reports with details  
(kind, name, description, date, location, contact)

🖼️ Upload an image for each report (optional)

🔍 Search reports by item name and filter by type (lost/found)

🗂️ View the 10 most recent reports on the homepage

✏️ Update or delete your reports

⚡ AJAX-friendly endpoints for smooth experience (can be extended)

🔐 API keys and secrets managed via `.env` and `python-dotenv`

---

## 🔧 Tech Stack

| Layer      | Tool / Framework          |
|------------|----------------------------|
| Frontend   | HTML, CSS, JavaScript      |
| Backend    | Flask                      |
| Database   | MongoDB (via MongoEngine)  |
| Environment| python-dotenv              |
| Utilities  | Werkzeug (secure uploads)  |

---

## 🚀 Getting Started

### 🔨 Setup

Clone the repository:

```bash
git clone <your-repository-url>
cd <your-repository-folder>
Create a virtual environment:

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on macOS/Linux
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file in the root directory:

env
Copy
Edit
SECRET_KEY=your_flask_secret_key
MONGO_URI=mongodb://localhost:27017/lostfound
UPLOAD_FOLDER=static/uploads
Run the app:

bash
Copy
Edit
python app.py
Open your browser and visit: http://localhost:5000

📁 Project Structure
text
Copy
Edit
LostFound/
│
├── app.py                  # Main Flask app
├── config.py               # Config and env loader
├── requirements.txt        # Python dependencies
├── .env                    # Secrets (not pushed)
│
├── models.py               # MongoEngine document model
│
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── submit.html
│   ├── search.html
│   └── update.html
│
├── static/                 # CSS & uploaded images
│   └── uploads/
🛡️ Security Notes
Ensure .env is listed in your .gitignore

Never push secrets or sensitive data to public repositories

💡 Future Enhancements
📧 Email notifications for matched items
🔐 User authentication & login system
🗺️ Timeline or map view for reports
🖼️ Image preview and drag/drop upload

👨‍💻 Author
Your Name
Lost & Found Project
Open for feedback & collaboration on GitHub!
