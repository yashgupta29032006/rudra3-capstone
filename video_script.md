# Rudra 3.0 - Capstone Project Video Script  
### Duration: Under 3 minutes  
### Format: Voice-over + screen recordings + simple slide transitions

---

# Scene 1 - Title (0:00–0:06)

**Visual**  
- Black screen fades into title.  
- Text appears:

"Rudra 3.0 - Multi-Agent Personal OS Assistant"  
"AI Agents Intensive Capstone"  
"By Yash Gupta "

**Voice-over:**  
"Hi, I'm Yash Gupta, and this is Rudra 3.0 - a multi-agent personal operating system assistant built for the Kaggle × Google Agents Intensive Capstone."

---

# Scene 2 - The Problem (0:07–0:28)

**Visual**  
- Clips of manual Mac usage: clicking apps, switching windows, checking notifications.  
- Cursor moving manually between tasks.

**Voice-over:**  
"Today, most of us still interact with our computers manually - opening apps, checking notifications, locating buttons, switching screens, and performing repetitive tasks.  
This slows us down, increases cognitive load, and restricts accessibility.  
I wanted to build an agent that can truly see the screen, understand context, automate actions, and act as a personal OS assistant."

---

# Scene 3 - Introducing Rudra 3.0 (0:29–0:44)

**Visual**  
- Rudra 3.0 folder  
- Quick overview of the architecture diagram

**Voice-over:**  
"Rudra 3.0 is a multi-agent macOS assistant that uses vision, memory, tools, and long-running background monitoring to automate the entire computer experience.  
It follows ADK principles with clean separation between agents and tools."

---

# Scene 4 - Architecture Breakdown (0:45–1:20)

**Visual**  
Show a simple diagram with arrows:  
User → RouterAgent → sub-agents → tools → OS  

**Voice-over:**  
"The system is built from five agents:

1. Router Agent – decides whether the query needs an answer or a plan.  
2. Automation Agent – performs clicks, opens apps, takes screenshots, and executes plans.  
3. Vision Agent – captures the screen and returns structured analysis.  
4. Memory Agent – stores chat history and learned behaviors.  
5. Monitor Agent – runs in the background and logs which app is active.

This modular design makes Rudra clean, explainable, and easy to extend."

---

# Scene 5 - Demo: CLI Interaction (1:21–1:45)

**Visual**  
- Recording of your terminal running Rudra 3.0  
- Type commands like:

open chrome

What is on my screen?

vision analyze workspace

take screenshot

**Voice-over:**  
"Here’s a quick demo.  
Rudra supports a CLI interface for deterministic testing.  
When I ask it to open Chrome, it executes the tool.  
When I ask what’s on the screen, it triggers the Vision Agent.  
All responses are structured and logged for observability."

---

# Scene 6 - Demo: Background Monitoring (1:46–2:00)

**Visual**  
- Show log file updating  
- Changing the frontmost app on macOS

**Voice-over:**  
"Rudra continuously runs a monitoring agent that logs which application is active every fifteen seconds.  
This demonstrates long-running operations and system-level awareness."

---

# Scene 7 - Why It’s Valuable (2:01–2:20)

**Visual**  
- Simple icons: automation, accessibility, productivity

**Voice-over:**  
"Rudra reduces repetitive tasks, enhances accessibility, and provides a real OS-level automation layer.  
It bridges natural language, vision, memory, and system tools to create a truly personal computing experience."

---

# Scene 8 - Technology & ADK Alignment (2:21–2:40)

**Visual**  
- List of key concepts with checkmarks  
- Multi-agent  
- Tools  
- Vision  
- Memory  
- Observability  
- Long-running loop  

**Voice-over:**  
"The project demonstrates multi-agent orchestration, tool execution, vision analysis, memory management, observability, and long-running loops - covering well over the required three ADK concepts."

---

# Scene 9 - Closing (2:41–3:00)

**Visual**  
- Rudra logo/name  
- Fade to black

**Voice-over:**  
"This is Rudra 3.0 - a multi-agent, vision-enabled, OS-integrated personal assistant.  
Thank you for watching, and thank you to Kaggle and Google for this opportunity."

---

# End of Script
