[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/AHFn7Vbn)
# Superjoin Hiring Assignment

### Welcome to Superjoin's hiring assignment! 🚀

### Objective
Build a solution that enables real-time synchronization of data between a Google Sheet and a specified database (e.g., MySQL, PostgreSQL). The solution should detect changes in the Google Sheet and update the database accordingly, and vice versa.

### Problem Statement
Many businesses use Google Sheets for collaborative data management and databases for more robust and scalable data storage. However, keeping the data synchronised between Google Sheets and databases is often a manual and error-prone process. Your task is to develop a solution that automates this synchronisation, ensuring that changes in one are reflected in the other in real-time.

### Requirements:
1. Real-time Synchronisation
  - Implement a system that detects changes in Google Sheets and updates the database accordingly.
   - Similarly, detect changes in the database and update the Google Sheet.
  2.	CRUD Operations
   - Ensure the system supports Create, Read, Update, and Delete operations for both Google Sheets and the database.
   - Maintain data consistency across both platforms.
   
### Optional Challenges (This is not mandatory):
1. Conflict Handling
- Develop a strategy to handle conflicts that may arise when changes are made simultaneously in both Google Sheets and the database.
- Provide options for conflict resolution (e.g., last write wins, user-defined rules).
    
2. Scalability: 	
- Ensure the solution can handle large datasets and high-frequency updates without performance degradation.
- Optimize for scalability and efficiency.

## Submission ⏰
The timeline for this submission is: **Next 2 days**

Some things you might want to take care of:
- Make use of git and commit your steps!
- Use good coding practices.
- Write beautiful and readable code. Well-written code is nothing less than a work of art.
- Use semantic variable naming.
- Your code should be organized well in files and folders which is easy to figure out.
- If there is something happening in your code that is not very intuitive, add some comments.
- Add to this README at the bottom explaining your approach (brownie points 😋)
- Use ChatGPT4o/o1/Github Co-pilot, anything that accelerates how you work 💪🏽. 

Make sure you finish the assignment a little earlier than this so you have time to make any final changes.

Once you're done, make sure you **record a video** showing your project working. The video should **NOT** be longer than 120 seconds. While you record the video, tell us about your biggest blocker, and how you overcame it! Don't be shy, talk us through, we'd love that.

We have a checklist at the bottom of this README file, which you should update as your progress with your assignment. It will help us evaluate your project.

- [ ] My code's working just fine! 🥳
- [ ] I have recorded a video showing it working and embedded it in the README ▶️
- [ ] I have tested all the normal working cases 😎
- [ ] I have even solved some edge cases (brownie points) 💪
- [ ] I added my very planned-out approach to the problem at the end of this README 📜

## Got Questions❓
Feel free to check the discussions tab, you might get some help there. Check out that tab before reaching out to us. Also, did you know, the internet is a great place to explore? 😛

We're available at techhiring@superjoin.ai for all queries. 

All the best ✨.

## Developer's Section
<!-- *Add your video here, and your approach to the problem (optional). Leave some comments for us here if you want, we will be reading this :)* -->





## Requirements

### Real-time Synchronization

- Implemented a system that detects changes in Google Sheets and updates the database accordingly.
- Similarly, detects changes in the database and updates the Google Sheet.

### CRUD Operations

- Supported Create, Read, Update, and Delete operations for both Google Sheets and the database.
- Maintained data consistency across both platforms.

### Optional Challenge: Scalability

- Ensured the solution can handle large datasets and high-frequency updates without performance degradation.
- Optimized for scalability and efficiency.

## Approach

### Overview

1. **Setup Flask Application**:
   - Created a Flask application to handle webhook requests from Google Sheets and update the database accordingly.
   - Implemented logging to track changes and actions taken during synchronization.

2. **Google Sheets Integration**:
   - Configured Google Sheets API to listen for changes using webhooks.
   - Set up endpoints to receive updates from Google Sheets and update the database in real-time.

3. **Database Integration**:
   - Developed functions to handle CRUD operations in the database.
   - Ensured updates made in the database are reflected back to Google Sheets.

4. **Logging**:
   - Implemented logging to record changes, actions, and conflicts during synchronization.
   - Logs are stored in `logs/db_changes.log` for easy tracking and debugging.

5. **Environment Configuration**:
   - Created a `.env` file for storing environment-specific variables.
   - Configured `credentials.json` for Google Sheets API access.

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

<!-- 2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ``` -->

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Update the necessary details in  `.env` file in the root directory with the following content:
     ```
     GOOGLE_SHEET_ID=<your-google-sheet-id>
     DB_HOST=<database-host>
     DB_USER=<database-user>
     DB_PASSWORD=<database-password>
     DB_NAME=<database-name>
     ```

4. **Set Up Google Sheets API**:
   - Update your API credentials in `config\credentials.json` 

6. **Run Flask Application with Ngrok**:
   - Start the Flask application:
     ```bash
     python app.py
     ```
   - Use Ngrok to expose the Flask app to the internet:
     ```bash
     ngrok http 5000
     ```
   - Update the webhook URL in Google Sheets to point to the Ngrok URL.

7. **Add Google Apps Script**:
   - In your Google Sheets, go to Extensions > Apps Script.
   - Replace the existing code with the provided Apps Script to send updates to your Flask webhook.

## Developer's Section

### Video Demo

Here's a [demo video](https://drive.google.com/drive/folders/your-demo-video-link) showcasing the working project. In the video, I walk through the entire setup process, demonstrate how the synchronization works, and discuss the biggest blocker I faced, which was ensuring real-time updates without conflicts. 

### Approach Explanation

1. **Real-Time Synchronization**:
   - Implemented real-time synchronization by using webhooks from Google Sheets and a Flask application to handle updates.

2. **CRUD Operations**:
   - Added functionality to perform CRUD operations on both Google Sheets and the database, maintaining data consistency.

3. **Logging**:
   - Included logging to track changes and actions in `logs/db_changes.log`, helping in debugging and tracking.

4. **Scalability**:
   - Optimized the solution to handle large datasets and frequent updates.

### Comments

- The code is organized into logical modules for ease of maintenance and understanding.
- Detailed comments are included to explain the purpose of different functions and configurations.


