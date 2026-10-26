AI LEARNING ROADMAP GENERATOR
=============================

A Streamlit app that creates a personalized learning roadmap using the Groq API.
The user enters a topic, skill level (Beginner / Intermediate / Advanced), time
available, and optionally uploads a .txt file. The app returns a week-by-week plan.

FILES
-----
app.py            Main Streamlit application
requirements.txt  Python dependencies
README.txt        This file

REQUIREMENTS
------------
- Python 3.9+
- A free Groq API key: https://console.groq.com

RUN LOCALLY
-----------
1. Install dependencies:
      pip install -r requirements.txt

2. Set your API key:
      Windows (PowerShell):  $env:GROQ_API_KEY="your_key_here"
      Mac / Linux:           export GROQ_API_KEY="your_key_here"

3. Start the app:
      streamlit run app.py

4. Open http://localhost:8501 in your browser.

RUN IN GOOGLE COLAB (with Cloudflare public URL)
------------------------------------------------
1. In Colab, click the Secrets (key) icon and add a secret named GROQ_API_KEY.
   Turn on "Notebook access".

2. Upload app.py and requirements.txt to the Colab file panel.

3. Cell 1 - install:
      !pip -q install -r requirements.txt
      !wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
      !chmod +x cloudflared

4. Cell 2 - run app and tunnel:
      import os, re, time, subprocess
      from google.colab import userdata

      os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")

      subprocess.Popen(["streamlit", "run", "app.py",
                        "--server.port", "8501", "--server.headless", "true"])
      time.sleep(5)

      log = open("cf.log", "w")
      subprocess.Popen(["./cloudflared", "tunnel", "--url", "http://localhost:8501"],
                       stderr=log, stdout=log)
      time.sleep(8)

      url = re.search(r"https://[-a-z0-9]+\.trycloudflare\.com", open("cf.log").read())
      print("Your app:", url.group(0) if url else "Not ready, check cf.log")

5. Click the printed trycloudflare.com link.

NOTES
-----
- The Cloudflare URL changes each run and stops when the Colab session ends.
- If you get a model error, Groq may have retired the model. Check current
  models at https://console.groq.com/docs/models and update the model name
  in app.py.
- Never commit or share your API key.
