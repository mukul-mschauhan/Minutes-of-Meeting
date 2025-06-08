# Minutes-of-Meeting
# 📋 AI-Powered Minutes of Meeting (MoM) Generator

![image](https://github.com/user-attachments/assets/fce1722a-d166-4856-8627-9762ad07d762)


Generate structured, professional, and downloadable **Minutes of Meeting (MoM)** from handwritten notes, PDFs, Word Docs, Text files, and Images — all powered by **Google Gemini 1.5 Flash** and **LangChain**.

> ✅ Ideal for Construction, Civil, MEP, Electrical, and Project Management Teams  
> ✅ Converts raw unstructured notes to standardized MoM table  
> ✅ Exports to Word and (optionally) PDF with Summary + To-Do List

---

## 🚀 Features

- 🧠 **Gemini Vision + LangChain** for contextual understanding of notes
- 📝 Accepts multiple input types: JPG, PNG, PDF, DOCX, TXT
- 🏗️ Structured output with:
  - Work Area
  - Sub-Activity / Component
  - Floor / Section
  - Description
  - Assigned To
  - Deadline
  - Status / Completion %
- 📤 **Download as .docx** with Summary and To-Dos
- 🧼 Clean Streamlit interface with user instructions

---

## 🖼️ Sample Output
| Work Area | Sub-Activity      | Floor     | Remarks                | Assigned To   | Deadline   | Status    |
| --------- | ----------------- | --------- | ---------------------- | ------------- | ---------- | --------- |
| Fire      | Dismantling Shaft | 6th Floor | Remove shaft partition | Not Mentioned | 22/05/2025 | Completed |
| Plumbing  | Handover          | 6th Floor | Handover done          | Vendor A      | 21/05/2025 | Completed |


✔️ Summary  
✔️ Key Action Items  
✔️ Auto-generated To-Do List

---

## 🛠️ Tech Stack

- `Streamlit` – UI
- `LangChain` – Prompt orchestration
- `Google Generative AI` – Text & Vision model (`gemini-1.5-flash`)
- `python-docx` – Word file generation
- `dotenv` – Secure API key management

---

## 📂 File Structure
├── app2.py # Streamlit App

├── generate_mom.py # LangChain + Gemini Logic

├── formatting.py # Word export logic

├── .env # Stores your Gemini API Key

├── requirements.txt # Python dependencies

├── README.md # Project documentation


---

## 🔧 Installation & Setup

1. **Clone this repo**  
   ```bash
   git clone https://github.com/yourusername/ai-mom-generator.git
   cd ai-mom-generator

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

3. **Create ``.env`` file** and add your Gemini API key:
   ```bash
   gemini_api_key=your_google_api_key_here

4. **Run the Streamlit App**:
   ```bash
   streamlit run app2.py

📌 Example Use Case
🛠️ A construction project team conducts an on-site review. They jot down handwritten notes on tasks like plumbing, shaft wall removal, and electrical ducting.
📸 They upload a photo of the notes.
🧠 The app reads it via Gemini + LangChain and generates a clean, downloadable Word document with tasks, status, and deadlines.

📃 License
This project is open-source under the MIT License.

🙌 Credits
Built by Mukul Chauhan, AI Strategist & Project Consultant.

💡 Future Enhancements

✅ Upload multiple files together (multi-modal ingestion)
✅ Multi-language support for Hindi / regional scripts
✅ Dashboard with filters by Work Area, Assigned To
✅ PDF + Word export in 1 click


---
Let me know if you want this `README.md` as a downloadable file or auto-uploaded to your GitHub.
