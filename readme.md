# ToKEn viSuAl 👁️✨

**Brief Description:**

ToKEn viSuAl is a Python-powered app that analyzes your text with two visual features:
- Adds a splash of color to help you understand it better 🌈.
- It shows a list of the top-k most probable tokens.
It uses OpenAI's powerful language models to figure out how likely each word (or part of a word) is to appear. 

**Features:**

* **Token Probability Visualization:** See which words matter most! Color intensity shows how likely each token is.
* **Most Likely Token Score:** See scores for the top-k most probable tokens.
* **Customizable System Prompt:** Guide the analysis with your own prompts 💡.
* **OpenAI Integration:**  Tap into the power of GPT-3.5-turbo and GPT-4 🚀.
* **Adjustable Parameters:** Tweak  temperature, maximum tokens, and seed for  fine-tuned results.
* **Memory Capability:** Optionally keep the context of your chat history for even deeper analysis 🧠.

**Installation**

1. **Clone the GitHub Repository:**
   ```bash
   git clone https://github.com/<your-username>/token-probs.git
   ```

2. **Install Dependencies:**
   ```bash
   cd token-probs
   pip install -r requirements.txt 
   ```

**Getting Started**

1. **Set Your OpenAI API Key:**
   Choose one of these ways:
    *  **Environment Variable:**
       ```bash
       export OPENAI_API_KEY=sk-....  
       ```
    *  **Directly in the App:**  Enter your API key in the right spot 🔑.

2. **Run the Application:**
   ```bash
   python tokens_prob.py  
   ```
3. **Start chatting in your web browser!** 💬

**How to Use**

1. **Type in your text.** 📝
2. **(Optional) Add a custom system prompt to focus the analysis.** 🤔
3. **Play around with the parameters!**  (temperature, max tokens, seed) 
4. **See your text light up with color-coded tokens!** 🤩
5. **Hover over the colormap for a closer look at probabilities.** 📊

**Project Structure**

* `token-probs/`
    * `tokens_prob.py`: The heart of the application. 
    * `requirements.txt`: All the Python libraries we need. 

**Credits**

This is an adapted version of the viztoken project from HoloViz https://holoviz-dev.github.io/blog-dev/posts/openai_logprobs_colored/! 🙌 

