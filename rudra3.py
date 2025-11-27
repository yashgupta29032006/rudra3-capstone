"""
Rudra 3.0 — Multi-Agent Personal Assistant
Author: Yash Gupta

Features:
- Multi-agent architecture (RouterAgent, VisionAgent, AutomationAgent, MemoryAgent, MonitorAgent, IdentityAgent)
- Vision-based UI automation
- Long-running monitoring
- Persisted memory + knowledge storage
- Observability: logs + metrics
- Tool wrappers (screenshot, click, open_app, etc.)
- Gemini-compatible LLM/vision stubs (safe, no API keys inside code)
"""

import os, sys, json, asyncio, time, uuid, subprocess, datetime, traceback
from pathlib import Path
from typing import Dict, Any
import pyautogui
import pyttsx3
from PIL import Image
import sounddevice as sd
import soundfile as sf


BASE_DIR = Path.home() / "Desktop" / "rudra3"
BASE_DIR.mkdir(exist_ok=True)

VOICE_DIR = BASE_DIR / "recordings"
VOICE_DIR.mkdir(exist_ok=True)

LOG_FILE = BASE_DIR / "rudra3.log"
MEMORY_FILE = BASE_DIR / "memory.json"
KNOWLEDGE_FILE = BASE_DIR / "knowledge.json"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", None)
ENABLE_FACE_ID = os.environ.get("ENABLE_FACE_ID", "false").lower() == "true"


class Logger:
    def __init__(self, path):
        self.path = Path(path)
        self.metrics = {"commands_executed": 0, "vision_calls": 0, "errors": 0}

    def _write(self, msg):
        try:
            with open(self.path, "a") as f:
                f.write(msg + "\n")
        except:
            pass

    def trace(self):
        return uuid.uuid4().hex[:8]

    def info(self, msg, t=None):
        t = t or self.trace()
        line = f"{datetime.datetime.utcnow().isoformat()} [INFO] [{t}] {msg}"
        print(line)
        self._write(line)

    def error(self, msg, t=None):
        t = t or self.trace()
        line = f"{datetime.datetime.utcnow().isoformat()} [ERROR] [{t}] {msg}"
        print(line, file=sys.stderr)
        self._write(line)
        self.metrics["errors"] += 1

logger = Logger(LOG_FILE)


class MemoryAgent:
    def __init__(self, file):
        self.file = Path(file)
        self.data = {"chat_history": [], "knowledge": []}
        self._load()

    def _load(self):
        if self.file.exists():
            try:
                self.data = json.loads(self.file.read_text())
            except:
                logger.error("Failed to load memory")

    def save(self):
        try:
            self.file.write_text(json.dumps(self.data, indent=2))
            logger.info("Memory saved")
        except:
            logger.error("Memory save failed")

    def add_chat(self, role, text):
        self.data["chat_history"].append({
            "role": role, "text": text, "time": time.time()
        })
        self.compact()
        self.save()

    def compact(self):
        self.data["chat_history"] = self.data["chat_history"][-50:]

    def add_knowledge(self, query, actions):
        k = self.data["knowledge"]
        if not any(item["query"] == query for item in k):
            k.append({"query": query, "actions": actions})
            self.save()

memory = MemoryAgent(MEMORY_FILE)


async def call_text_model(prompt: str) -> str:
    await asyncio.sleep(0.2)
    return "ANSWER: (Stub LLM Response) " + prompt[:200]


async def call_vision_model(prompt: str, img_bytes: bytes) -> str:
    await asyncio.sleep(0.3)
    return '{"result": null}'


class Tools:
    @staticmethod
    def screenshot(path: Path):
        try:
            subprocess.run(["screencapture", "-x", str(path)], check=True)
            return str(path)
        except Exception as e:
            logger.error(f"screenshot failed: {e}")
            return None

    @staticmethod
    def click(x=None, y=None):
        try:
            if x and y:
                pyautogui.click(x, y)
            else:
                pyautogui.click()
            logger.metrics["commands_executed"] += 1
            return True
        except Exception as e:
            logger.error(f"click failed: {e}")
            return False

    @staticmethod
    def open_app(name):
        try:
            subprocess.run(["open", "-a", name])
            logger.metrics["commands_executed"] += 1
            return True
        except Exception as e:
            logger.error(f"open_app failed: {e}")
            return False

    @staticmethod
    def camera_capture(path: Path):
        try:
            result = subprocess.run(["imagesnap", "-w", "2", str(path)], capture_output=True)
            return str(path) if path.exists() else None
        except:
            return None


class RouterAgent:
    async def route(self, msg: str):
        logger.info("RouterAgent invoked")
        prompt = f"User query: {msg}\nReturn COMMAND:<json> or ANSWER:<text>"
        out = await call_text_model(prompt)

        if isinstance(out, str) and out.upper().startswith("COMMAND:"):
            try:
                json_str = out.split(":", 1)[1].strip()
                plan = json.loads(json_str)
                return {"type": "actions", "actions": plan.get("actions", [])}
            except:
                pass
        return {"type": "answer", "answer": out}

class VisionAgent:
    async def analyze(self, task_text: str):
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        img_path = BASE_DIR / f"vision_{ts}.png"
        Tools.screenshot(img_path)

        with open(img_path, "rb") as f:
            img_bytes = f.read()

        out = await call_vision_model(task_text, img_bytes)
        try:
            return json.loads(out)
        except:
            return {"result": None}

class AutomationAgent:
    async def execute(self, action: Dict[str, Any], cb=None):
        typ = action.get("type")
        val = action.get("value")
        logger.info(f"Automation executing {typ}")

        if typ == "open_app":
            Tools.open_app(val)
            if cb: await cb(f"Opened {val}")

        elif typ == "click":
            if isinstance(val, dict):
                Tools.click(val.get("x"), val.get("y"))
                if cb: await cb(f"Clicked at {val.get('x')},{val.get('y')}")
            else:
                Tools.click()
                if cb: await cb("Clicked current position")

        elif typ == "vision_task":
            vision = VisionAgent()
            res = await vision.analyze(val)
            if cb: await cb(f"Vision result: {res}")

        elif typ == "speak":
            speak_text(str(val))
            if cb: await cb("Spoken.")

        elif typ == "screenshot":
            ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            img_path = BASE_DIR / f"screenshot_{ts}.png"
            Tools.screenshot(img_path)
            if cb: await cb(f"Saved screenshot at {img_path}")

        else:
            if cb: await cb(f"Unknown action: {typ}")

class IdentityAgent:
    async def capture_face(self):
        if not ENABLE_FACE_ID:
            return {"error": "FaceID disabled"}
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        img_path = BASE_DIR / f"face_{ts}.jpg"
        Tools.camera_capture(img_path)
        if img_path.exists():
            return {"face_image": str(img_path)}
        return {"error": "capture_failed"}

class MonitorAgent:
    def __init__(self):
        self.running = False

    async def loop(self):
        logger.info("MonitorAgent started")
        while self.running:
            try:
                app = detect_frontmost_app()
                logger.info(f"Frontmost app: {app}")
            except Exception as e:
                logger.error(f"Monitor error: {e}")
            await asyncio.sleep(15)

    def start(self, loop):
        if not self.running:
            self.running = True
            loop.create_task(self.loop())

    def stop(self):
        self.running = False


def detect_frontmost_app():
    try:
        cmd = 'osascript -e \'tell application "System Events" to get name of first process whose frontmost is true\''
        return subprocess.check_output(cmd, shell=True, universal_newlines=True).strip()
    except:
        return "Unknown"

def speak_text(text):
    try:
        subprocess.Popen(["say", text])
    except:
        engine = pyttsx3.init()
        engine.say(text); engine.runAndWait()



router = RouterAgent()
automation = AutomationAgent()
vision = VisionAgent()
identity = IdentityAgent()
monitor = MonitorAgent()

async def process_message(user_text: str, cb):
    memory.add_chat("user", user_text)

    route = await router.route(user_text)
    if route["type"] == "answer":
        ans = route["answer"]
        memory.add_chat("assistant", ans)
        await cb(ans)
    else:
        actions = route.get("actions", [])
        for action in actions:
            await automation.execute(action, cb)
        memory.add_chat("assistant", json.dumps(actions))

async def cli_loop():
    async def reply_cb(text):
        print(f"[RUDRA] {text}")

    print("Rudra 3.0 CLI (type 'exit' to quit)")
    while True:
        msg = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
        if msg.lower().strip() in ["exit", "quit"]:
            break
        await process_message(msg, reply_cb)

async def main():
    logger.info("Starting Rudra 3.0")
    loop = asyncio.get_running_loop()
    monitor.start(loop)
    await cli_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
