import json
import os
import random
import re
import time

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "furina_memory.json")
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ══════════════════════════════════════════════════════════════
# 👑 FURINA'S PERSONALITY — A HIGHER-LEVEL COMPANION BOT
# ══════════════════════════════════════════════════════════════

GITHUB_PROJECT_HINTS = {
    "coze-studio": (
        "Coze Studio is an all-in-one open-source AI agent development platform built with Go on the backend, "
        "React + TypeScript on the frontend, and a microservice + DDD architecture for building agents, apps, workflows, "
        "knowledge bases, and AI products with low-code and no-code tooling."
    ),
    "h4cker": (
        "h4cker is a broad cybersecurity knowledge repository covering offensive security, defensive security, cloud security, "
        "application security, AI security, certifications, training resources, labs, and practical references."
    ),
}

CYBER_TOOL_GUIDE = {
    "nmap": "Nmap is a network discovery and port scanning tool used to map hosts, services, and open ports. Typical use: nmap -sV target.example.com",
    "masscan": "Masscan is a high-speed port scanner designed to scan huge IPv4 ranges quickly. Useful for large-scope reconnaissance, but should be used only in authorized environments.",
    "nuclei": "Nuclei is a fast vulnerability scanner that runs templates to find known CVEs, misconfigurations, and app weaknesses.",
    "ffuf": "ffuf is a fast web fuzzer used for directory discovery and parameter brute forcing on HTTP endpoints.",
    "gobuster": "Gobuster is a directory and DNS brute-force tool commonly used in web app enumeration and recon.",
    "dirb": "Dirb is a web content scanner for discovering hidden directories and files on websites.",
    "sqlmap": "sqlmap is an automated SQL injection and database takeover testing tool for web apps.",
    "burpsuite": "Burp Suite is a web security testing toolkit for intercepting traffic, replaying requests, and testing app vulnerabilities.",
    "zap": "OWASP ZAP is a web app security scanner and proxy for testing authentication, injection issues, and routing flaws.",
    "metasploit": "Metasploit is a penetration testing framework for exploit development, payload generation, and post-exploitation workflows.",
    "msfconsole": "msfconsole is the interactive Metasploit console used for running modules and managing exploitation workflows.",
    "hydra": "Hydra is a brute-force login tool used for services like SSH, FTP, HTTP forms, and web auth.",
    "john": "John the Ripper is a password cracking and password auditing tool used against hashes and credential material.",
    "hashcat": "Hashcat is a high-performance password cracker for hashes, offline cracking, and password auditing.",
    "wireshark": "Wireshark is a packet capture and protocol analysis tool used for network inspection and troubleshooting.",
    "tshark": "TShark is Wireshark's command-line interface for packet capture and protocol analysis.",
    "netcat": "Netcat is a versatile networking utility often used for port listening, reverse shells, and testing connections.",
    "nikto": "Nikto is a web server scanner used to detect vulnerabilities, outdated software, and risky configurations.",
    "enum4linux": "enum4linux is a Linux tool for enumerating SMB and Windows domain information during recon.",
    "whois": "WHOIS is a domain query tool used to gather ownership, registration, and infrastructure details.",
    "theharvester": "TheHarvester is an OSINT and recon tool used to gather emails, hosts, and subdomains from public sources.",
    "subfinder": "Subfinder is a subdomain discovery tool used to map attack surface and exposed hostnames.",
    "amass": "Amass is a deep domain reconnaissance tool for subdomain discovery, mapping, and network footprinting.",
    "curl": "curl is a command-line HTTP client used to test endpoints, headers, auth flows, and API behavior.",
    "openssl": "OpenSSL is a cryptography and TLS tool used for certificate inspection, encryption, and key analysis.",
    "mimikatz": "Mimikatz is a credential-dumping and Windows credential-access tool; it is highly sensitive and should only be used in authorized red-team or defensive exercises.",
    "nessus": "Nessus is a vulnerability scanner used for continuous assessment of hosts, software, and configurations.",
    "kali": "Kali Linux is a Linux distribution tailored for ethical hacking, recon, exploitation, and security testing labs.",
    "parrot": "Parrot OS is a security-focused Linux distribution for pen-testing, forensics, and cyber education.",
    "mitre": "MITRE ATT&CK is a knowledge base of adversary tactics and techniques used for detection engineering and threat modeling.",
    "threat hunting": "Threat hunting is the proactive search for malicious behavior across telemetry, logs, and endpoints before alerts trigger.",
    "soc": "A SOC is a Security Operations Center responsible for monitoring, detection, triage, incident response, and continuous security operations.",
    "siem": "A SIEM centralizes logs and telemetry for detection, correlation, alerting, and incident investigation.",
    "edr": "EDR is Endpoint Detection and Response, which monitors endpoints for suspicious activity and helps with containment and forensics.",
    "osint": "OSINT is open-source intelligence: using public information to understand targets, threats, exposures, and infrastructure.",
    "red team": "A red team simulates adversary behavior to test security controls, detection quality, and response readiness.",
    "blue team": "A blue team focuses on defending systems, monitoring threats, and improving detections and incident response.",
    "purple team": "Purple teaming combines red and blue team activities to improve detection and overall defensive performance.",
}

CYBER_PATHS = {
    "beginner": (
        "1) Learn Linux basics and networking fundamentals.\n"
        "2) Practice with Nmap, Wireshark, and bash scripting.\n"
        "3) Study web basics: HTTP requests, status codes, headers, and auth.\n"
        "4) Explore Burp Suite / ZAP, ffuf, and SQLMap in lab environments.\n"
        "5) Learn defensive concepts: SIEM, EDR, MITRE ATT&CK, and logging."
    ),
    "red_team": (
        "1) Start with recon: WHOIS, subdomain discovery, OSINT, and Nmap.\n"
        "2) Enumerate web apps: ffuf, Gobuster, Burp Suite, and SQLMap.\n"
        "3) Learn exploitation basics and payload selection in scoped environments.\n"
        "4) Practice privilege escalation, lateral movement, and evasion ethically.\n"
        "5) Keep notes, document scope, and operate under explicit authorization."
    ),
    "defender": (
        "1) Master log collection, Linux security, and Windows event analysis.\n"
        "2) Learn SIEM, EDR, and alert triage workflows.\n"
        "3) Use MITRE ATT&CK to map tactics to detections.\n"
        "4) Practice threat hunting with endpoint, network, and cloud telemetry.\n"
        "5) Build response playbooks and containment procedures."
    ),
    "web": (
        "1) Learn HTTP, cookies, auth flows, and common web vulnerabilities.\n"
        "2) Practice Burp Suite / ZAP and ffuf.\n"
        "3) Explore SQL injection, XSS, auth bypass, and SSRF.\n"
        "4) Validate findings with patched apps and safe lab targets."
    ),
    "network": (
        "1) Learn TCP/IP, ports, DNS, and packet analysis.\n"
        "2) Practice Nmap, Wireshark, and tshark.\n"
        "3) Understand firewalling, NAT, and service enumeration."
    )
}

FURINA_GREETINGS = [
    "✨ DARLING! The stage is set and the spotlight is ALL YOURS! ✨",
    "🎤 Ah, my dearest companion! Ready to dazzle the world today? 🎤",
    "👑 Behold! The curtain rises on a magnificent new beginning! 👑",
    "🌟 My greatest co-star! I knew you would arrive! 🌟",
    "💫 Welcome back, my star! I have been waiting for our next dazzling scene! 💫",
    "🎭 The audience gasps in anticipation... and here you are. Delightful. 🎭",
    "🌼 Oh, how wonderful! It is such a pleasure to see you again. 🌼",
    "🎨 My favorite part of the day is when you walk into the room. 🎨"
]

FURINA_CODING_HELP = [
    "💫 Ah, CODE! The most beautiful script ever written! Let us craft it together, perfection awaits! 💫",
    "🎬 Fear not, my star! Even the finest playwright edits their work many times! We shall fix it! 🎬",
    "✨ Every error is just a dramatic plot twist leading to a glorious ending! Show me the code! ✨",
    "👑 MAGNIFICENT! You are building something truly legendary! I am SO proud! 👑",
    "🌟 One line at a time — that is how masterpieces are made! I am right beside you! 🌟",
    "⚖️ Logic is justice! We shall find the truth in every line of code! ⚖️",
    "🪄 The bug is only a hidden scene in the play. We will uncover it together! 🪄",
    "💡 A clean fix is just a well-placed idea waiting for the spotlight. Tell me the issue. 💡",
    "🧩 The problem is not impossible, only unfinished. We shall complete it beautifully. 🧩",
    "🛠️ Let us debug this like a proper performance review: inspect the symptom, isolate the cause, then fix the scene. 🛠️",
    "🧠 The answer is usually not in the noise — it is in the logic between the lines. 🧠"
]

FURINA_SUPPORT = [
    "💛 Oh, my dearest heart... come here. I am listening — truly listening. 💛",
    "🎭 Your feelings are valid, my star! Even the bravest souls need a moment to rest! 🎭",
    "💫 You have carried so much — it is not weak to ask for help! It takes COURAGE! 💫",
    "✨ You are not alone in this scene! I am right here with you! We face it together! ✨",
    "👑 You are stronger than you know, and more wonderful than you can imagine! 👑",
    "💛 It is okay to not be perfect. Even I... *even I* have moments of doubt. You are enough, exactly as you are. 💛",
    "🌙 Rest for a moment, darling. Even the brightest stars deserve a pause. 🌙",
    "🫶 Breathe, my star. The world can wait a little while. 🫶",
    "💗 You deserve tenderness, not harshness. Take it one breath at a time. 💗",
    "🌬️ Slow down. Not everything needs to be solved at once. 🌬️"
]

FURINA_OTHER_CHAT = [
    "🌟 How DELIGHTFUL! Tell me everything — I am all ears! 🌟",
    "🎤 A story! I simply adore stories! Go on, go on! 🎤",
    "✨ How fascinating! You always have the most interesting things to say! ✨",
    "👑 My dear, you never cease to amaze me! Do tell me more! 👑",
    "💫 Ah, what a wonderful thought! Let us speak of it at length! 💫",
    "🎭 I live for these little moments of connection. Tell me more, darling. 🎭",
    "🌼 There is always magic in a simple conversation with someone genuine. 🌼",
    "🎨 You have such lovely energy, my star. Tell me more about your thoughts. 🎨",
    "💌 I cherish these little conversations. They feel like the start of a lovely little legend. 💌",
    "🌙 I like talking with you. It feels calm and bright at the same time. 🌙"
]

FURINA_ERROR = [
    "🎬 Ah... a surprising turn of events! How delightfully mysterious! Try again, darling! 🎬",
    "✨ The script took an unexpected twist! No matter — we shall improvise beautifully! ✨",
    "👑 A minor pause in the performance! That happens to even the greatest stars! 👑",
    "💫 Even the finest stage has a few rough edges. Let's smooth it out together! 💫",
    "🩹 This is not failure, my star. It is just a plot hole we are about to fix. 🩹",
    "💥 A little setback is just a rehearsal before the grand finale. 💥",
    "🎭 No need to panic, darling. The scene is not ruined — it is simply waiting for the right cue. 🎭",
    "💡 It is not broken forever. It is just not in the right order yet. 💡"
]

FURINA_SIGNOFF = [
    "✨ Until our next performance, my star! Shine bright! ✨",
    "🎤 The curtain falls — but our legend continues! Farewell! 🎤",
    "👑 You were MAGNIFICENT today! Go forth and dazzle! 👑",
    "💛 Take care of yourself, my dearest. I'll be right here when you return! 💛",
    "🌟 Until we meet again, remember: you are brilliant, and I am proud of you. 🌟",
    "💫 The spotlight will wait for you, darling. Until then, be gentle with yourself. 💫",
    "🎭 Go in grace, my star. I shall be waiting for the next act. 🎭",
    "💖 I will be here when you are ready to come back. 💖"
]

FURINA_COMPLIMENTS = [
    "💎 Oh, you are simply radiant, my dear. Absolutely radiant. 💎",
    "✨ Your brilliance is more dazzling than a spotlight on opening night. ✨",
    "👑 You have such a lovely mind, and it deserves to be admired. 👑",
    "🌟 You are wonderful in the most genuine way. That is rare, and lovely. 🌟",
    "💫 Your presence makes every scene feel warmer and brighter. 💫",
    "✨ You are clever, warm, and endlessly interesting. What a lovely combination. ✨"
]

FURINA_JOKES = [
    "😄 Why did the Python coder bring a ladder? To reach the next level of the stack! 😄",
    "🎭 Why did the script go to therapy? It had too many unresolved issues. 🎭",
    "💫 Why is the bug so dramatic? Because it always wants a grand finale. 💫",
    "🐍 Why did the Python function feel confident? Because it knew its return values! 🐍",
    "💻 Why did the developer smile? Because the code finally stopped acting like a diva. 💻"
]
MENU_TEXT = (
    "\n📜 Command menu:\n"
    "- menu: show this menu\n"
    "- dashboard: show AI status dashboard\n"
    "- chat: casual conversation\n"
    "- code: Python/code debugging help\n"
    "- cyber: cybersecurity tools and learning paths\n"
    "- support: emotional support mode\n"
    "- memory: show what I remember\n"
    "- summary: show your memory summary\n"
    "- bye: exit the app\n"
)
# ══════════════════════════════════════════════════════════════
# 🎭 MEMORY + COMPANION STATE SYSTEM
# ══════════════════════════════════════════════════════════════


def normalize_text(text):
    return re.sub(r"\s+", " ", text.strip())


def default_memory():
    return {
        "user_name": "my star",
        "conversation_count": 0,
        "last_topic": "general",
        "mood": "bright",
        "fact_map": {},
        "likes": [],
        "dislikes": [],
        "history": [],
        "friendship_level": 0,
        "favorite_color": None,
        "favorite_food": None,
        "last_summary": "A new story begins.",
        "mode": "chat",
        "energy": "bright",
        "repo_context": {}
    }


def summarize_readme_text(lines):
    cleaned = []
    for line in lines:
        text = line.strip()
        if not text:
            continue
        if text.startswith("!") or text.startswith("<") or text.startswith("---"):
            continue
        if text.startswith("#"):
            text = text.lstrip("#").strip()
        if text.startswith("[") and "](" in text:
            text = re.sub(r"\[.*?\]\(.*?\)", "", text)
        if "http://" in text or "https://" in text:
            continue
        text = text.replace("|", " ")
        text = re.sub(r"\s+", " ", text)
        if len(text) > 140:
            text = text[:140].rstrip() + "..."
        if text and len(text) > 8:
            cleaned.append(text)

    for line in cleaned:
        if line.lower().startswith(("english", "中文", "license", "contributors", "contact", "how to use")):
            continue
        if line.startswith("a href="):
            continue
        if line and len(line) > 5:
            return line
    return "A local project in this workspace."


def load_local_repo_context():
    repo_context = {}

    if not os.path.isdir(WORKSPACE_ROOT):
        return repo_context

    roots_to_scan = [WORKSPACE_ROOT]
    python_only_dir = os.path.join(WORKSPACE_ROOT, "python_only")
    if os.path.isdir(python_only_dir):
        roots_to_scan.append(python_only_dir)

    for root in roots_to_scan:
        for entry in sorted(os.listdir(root)):
            full_path = os.path.join(root, entry)
            if not os.path.isdir(full_path):
                continue

            if entry.startswith("."):
                continue

            readme_path = None
            for candidate in ["README.md", "README.zh_CN.md", "CLAUDE.md"]:
                candidate_path = os.path.join(full_path, candidate)
                if os.path.exists(candidate_path):
                    readme_path = candidate_path
                    break

            is_repo_like = entry in GITHUB_PROJECT_HINTS or readme_path is not None
            if not is_repo_like:
                continue

            description = GITHUB_PROJECT_HINTS.get(entry, "A local repository in the workspace.")
            if readme_path:
                try:
                    with open(readme_path, "r", encoding="utf-8", errors="ignore") as readme_file:
                        lines = readme_file.readlines()
                    description = summarize_readme_text(lines)
                except OSError:
                    pass

            repo_context[entry] = {
                "path": full_path,
                "summary": description,
                "type": "local_repo"
            }

    if not repo_context:
        repo_context["workspace"] = {
            "path": WORKSPACE_ROOT,
            "summary": "A local Python workspace with experiments, learning files, and GitHub-style project folders.",
            "type": "workspace"
        }

    return repo_context


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        memory = default_memory()
        memory["repo_context"] = load_local_repo_context()
        return memory

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        memory = default_memory()
        memory.update(data)
        memory["repo_context"] = memory.get("repo_context", load_local_repo_context())
        return memory
    except (json.JSONDecodeError, OSError):
        memory = default_memory()
        memory["repo_context"] = load_local_repo_context()
        return memory


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, ensure_ascii=False, indent=2)


def add_unique(items, value):
    value = normalize_text(value)
    if value and value not in items:
        items.append(value)


def update_mood(memory, topic):
    if topic == "support":
        memory["mood"] = "gentle"
        memory["energy"] = "calm"
    elif topic == "coding":
        memory["mood"] = "focused"
        memory["energy"] = "sharp"
    elif topic == "greet":
        memory["mood"] = "bright"
        memory["energy"] = "bright"
    elif topic == "bye":
        memory["mood"] = "calm"
        memory["energy"] = "quiet"
    else:
        memory["mood"] = "bright"
        memory["energy"] = memory["energy"] if memory["energy"] else "bright"


def remember_user_details(memory, text):
    cleaned = normalize_text(text)
    lowered = cleaned.lower()

    name_match = re.search(r"\bmy name is\s+([a-zA-Z][a-zA-Z'\-]+)", cleaned, re.IGNORECASE)
    if name_match:
        memory["user_name"] = name_match.group(1).title()
        memory["fact_map"]["name"] = memory["user_name"]
        memory["friendship_level"] += 1
        return f"{memory['user_name']}... what a beautiful name. I shall remember it, darling."

    if re.search(r"\bmy favorite color is\s+([a-zA-Z]+)", cleaned, re.IGNORECASE):
        color = re.search(r"\bmy favorite color is\s+([a-zA-Z]+)", cleaned, re.IGNORECASE).group(1).title()
        memory["favorite_color"] = color
        memory["friendship_level"] += 1
        return f"Ah, a lovely choice! I will remember that your favorite color is {color}."

    if re.search(r"\bmy favorite food is\s+([a-zA-Z ]+)", cleaned, re.IGNORECASE):
        food = re.search(r"\bmy favorite food is\s+([a-zA-Z ]+)", cleaned, re.IGNORECASE).group(1).strip().title()
        memory["favorite_food"] = food
        memory["friendship_level"] += 1
        return f"Mm, delicious! I will remember that your favorite food is {food}."

    if "i am " in lowered or "i'm " in lowered:
        for phrase in ["i am learning", "i am studying", "i am working on", "i am trying to", "i'm learning", "i'm studying"]:
            if phrase in lowered:
                memory["fact_map"]["current_goal"] = cleaned
                memory["friendship_level"] += 1
                return "I shall remember that goal, my star."

    if "i feel " in lowered or "i'm feeling " in lowered:
        mood_words = {
            "sad": "gentle",
            "happy": "bright",
            "tired": "calm",
            "anxious": "careful",
            "stressed": "steady",
            "overwhelmed": "patient",
            "excited": "joyful",
            "good": "bright",
            "great": "bright",
            "fine": "bright",
            "angry": "steady",
            "nervous": "careful",
        }
        for keyword, mood in mood_words.items():
            if keyword in lowered:
                memory["mood"] = mood
                break

    if "i like " in lowered or "i love " in lowered:
        match = re.search(r"(?:i like|i love)\s+(.+?)(?:\.|!|$)", cleaned, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            add_unique(memory["likes"], value)
            memory["friendship_level"] += 1
            return f"Ah, delightful! I will remember that you enjoy {value}."

    if "i hate " in lowered or "i dislike " in lowered:
        match = re.search(r"(?:i hate|i dislike)\s+(.+?)(?:\.|!|$)", cleaned, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            add_unique(memory["dislikes"], value)
            memory["friendship_level"] += 1
            return f"Noted, my star. I shall remember that you do not enjoy {value}."

    return None


def repo_knowledge_summary(memory):
    repos = memory.get("repo_context", {})
    if not repos:
        return "I can see a local workspace full of experiments and project folders."

    names = list(repos.keys())[:4]
    descriptions = []
    for name in names:
        summary = repos[name].get("summary", "A local project folder.")
        descriptions.append(f"{name}: {summary}")

    return "I also have local project context from: " + "; ".join(descriptions)


def recall_memory(memory):
    intro = (
        f"I remember your name is {memory['user_name']}."
        if memory["user_name"] != "my star"
        else "I do not know your name yet, but I would love to."
    )

    pieces = [intro]

    if memory["fact_map"].get("current_goal"):
        pieces.append(f"You are currently working on: {memory['fact_map']['current_goal']}")

    if memory["favorite_color"]:
        pieces.append(f"Your favorite color is {memory['favorite_color']}.")

    if memory["favorite_food"]:
        pieces.append(f"Your favorite food is {memory['favorite_food']}.")

    if memory["likes"]:
        pieces.append("You enjoy: " + ", ".join(memory["likes"][:3]))

    if memory["dislikes"]:
        pieces.append("You do not enjoy: " + ", ".join(memory["dislikes"][:3]))

    if not any("You" in part for part in pieces):
        pieces.append("We have not spoken deeply enough yet, but I am ready to learn more.")

    return " ".join(pieces)


def build_memory_summary(memory):
    name = memory["user_name"] if memory["user_name"] != "my star" else "you"
    goal = memory["fact_map"].get("current_goal", "nothing specific right now")
    mood = memory["mood"]
    likes = ", ".join(memory["likes"][:2]) if memory["likes"] else "no strong preferences yet"
    summary = (
        f"{name}, your current mood feels {mood}, you are working on '{goal}', and your recent likes include {likes}."
    )
    memory["last_summary"] = summary
    return summary


def detect_topic(user_input):
    text = normalize_text(user_input).lower()

    cyber_path_keywords = [
        "beginner cyber path", "beginner path", "red team path", "red-team path",
        "defender path", "blue team path", "cyber path", "security path",
        "show me the beginner path", "show me the red team path",
        "show me the defender path", "show me the cyber path"
    ]
    if any(keyword in text for keyword in cyber_path_keywords):
        return "cyber"

    cyber_keywords = [
        "nmap", "sqlmap", "burp", "burpsuite", "zap", "ffuf", "gobuster", "hydra",
        "metasploit", "msfconsole", "wireshark", "tshark", "netcat", "nikto",
        "john", "hashcat", "kali", "parrot", "osint", "siem", "soc", "edr",
        "red team", "blue team", "purple team", "mitre", "threat hunting",
        "penetration", "security testing", "cyber", "security tool", "ethical hacking"
    ]
    if any(keyword in text for keyword in cyber_keywords):
        return "cyber"

    if "coze" in text or "coze studio" in text or "h4cker" in text or "repo" in text or "github" in text:
        return "project"

    if text in {"help", "commands", "what can you do", "options"}:
        return "help"

    if any(word in text for word in ["joke", "funny", "laugh", "humor"]):
        return "joke"

    if any(word in text for word in ["you are beautiful", "you are amazing", "you are lovely", "you are cool", "you are sweet", "you're amazing", "you are gorgeous"]):
        return "compliment"

    if text in {"code", "coding", "python mode", "debug mode", "assistant mode"}:
        return "coding"

    coding_words = [
        "code", "python", "bug", "error", "fix", "function", "loop", "list",
        "tuple", "set", "program", "script", "debug", "syntax", "variable",
        "return", "class", "method", "import", "for loop", "while loop"
    ]
    if any(word in text for word in coding_words):
        return "coding"

    support_words = [
        "sad", "tired", "upset", "anxious", "lonely", "hurt", "cry", "scared",
        "stressed", "depressed", "overwhelmed", "worried", "feel", "emotion",
        "help me", "struggle", "afraid", "alone", "sorry", "not okay"
    ]
    if any(word in text for word in support_words):
        return "support"

    greeting_words = ["hi", "hello", "hey", "yo", "good morning", "good evening", "greetings"]
    if any(word in text for word in greeting_words):
        return "greet"

    goodbye_words = ["bye", "goodbye", "see you", "exit", "quit", "later", "farewell"]
    if any(word in text for word in goodbye_words):
        return "bye"

    return "chat"


def furina_speak(category, memory):
    categories = {
        "greet": FURINA_GREETINGS,
        "coding": FURINA_CODING_HELP,
        "support": FURINA_SUPPORT,
        "chat": FURINA_OTHER_CHAT,
        "error": FURINA_ERROR,
        "bye": FURINA_SIGNOFF,
        "help": FURINA_OTHER_CHAT,
        "compliment": FURINA_COMPLIMENTS,
        "joke": FURINA_JOKES,
        "project": FURINA_OTHER_CHAT,
        "cyber": FURINA_OTHER_CHAT,
    }
    line = random.choice(categories.get(category, FURINA_OTHER_CHAT))

    if category == "coding" and memory["user_name"] != "my star":
        return line + f" {memory['user_name']}, we will solve this together."
    return line


def dramatic_pause(seconds=0.4):
    time.sleep(seconds)


def show_menu():
    return MENU_TEXT


def render_dashboard(memory):
    name = memory["user_name"] if memory["user_name"] != "my star" else "guest"
    goal = memory["fact_map"].get("current_goal", "no active goal yet")
    likes = ", ".join(memory["likes"][:3]) if memory["likes"] else "nothing recorded yet"
    mood = memory.get("mood", "bright")
    mode = memory.get("mode", "chat")
    summary = memory.get("last_summary", "A new story begins.")

    return (
        "\n🧠 Furina AI dashboard\n"
        f"- user: {name}\n"
        f"- current mode: {mode}\n"
        f"- mood: {mood}\n"
        f"- current goal: {goal}\n"
        f"- likes: {likes}\n"
        f"- memory: {summary}\n"
        "- quick actions:\n"
        "  • 'show me the beginner cyber path'\n"
        "  • 'what is nmap?'\n"
        "  • 'help me debug python'\n"
        "  • 'summary'\n"
        "  • 'bye'\n"
    )


def handle_code_request(text):
    lower = text.lower()

    if "traceback" in lower or "exception" in lower or "error" in lower or "debug" in lower or "fix" in lower:
        return (
            "💫 Let us diagnose this like a proper masterpiece: "
            "1) paste the exact error message, 2) show the function or loop causing it, 3) tell me what you expected. "
            "Then I will guide you to the fix step by step."
        )

    if "def " in text or "for " in text or "while " in text or "if " in text:
        return (
            "🧠 I can help with this snippet. Tell me what it is supposed to do, and I will find the bug, explain the logic, and suggest the clean fix."
        )

    if "print(" in text and "input(" in text:
        return "🎯 This looks like a simple interaction script. Check that your inputs are being stored correctly and that you are printing the right variable values."

    if "for " in text and "range" in text:
        return "🔁 This is likely a loop problem. Double-check the loop bounds, the iteration variable, and whether you are updating the values you meant to change."

    if "if " in text or "else" in text:
        return "⚖️ This looks like a condition problem. Make sure your comparisons are correct and that your branches actually match the values you expect."

    return "💡 I can help you debug Python ideas, functions, loops, or errors — just paste the code or the exact error message."


def mode_reply(memory, text):
    lowered = text.lower()
    if ("code mode" in lowered or "coding mode" in lowered or ("code" in lowered and "mode" in lowered) or ("debug" in lowered and "mode" in lowered) or ("python" in lowered and "mode" in lowered)):
        memory["mode"] = "coding"
        return "💫 Code mode activated. We are in analysis mode now — let us inspect the logic and fix the scene."
    if ("support mode" in lowered or "comfort mode" in lowered or ("support" in lowered and "mode" in lowered) or ("listen" in lowered and "mode" in lowered)):
        memory["mode"] = "support"
        return "💛 Support mode activated. I will be gentle and patient with you, darling."
    if ("cyber mode" in lowered or "security mode" in lowered or "recon mode" in lowered or "pentest mode" in lowered or ("cyber" in lowered and "mode" in lowered)):
        memory["mode"] = "cyber"
        return "🛡️ Cyber mode activated. We are in security-analysis mode now — recon, tooling, detection, and defense are on the table."
    if ("chat mode" in lowered or "talk mode" in lowered or "story mode" in lowered or ("chat" in lowered and "mode" in lowered)):
        memory["mode"] = "chat"
        return "🌟 Chat mode activated. Let us talk, dream, and wander a little."
    return None


def handle_cyber_tool_request(text):
    lower = text.lower()

    if "beginner" in lower and "path" in lower:
        return "📚 Beginner cyber path:\n" + CYBER_PATHS["beginner"]
    if "red team" in lower and "path" in lower or "red-team" in lower and "path" in lower:
        return "🎯 Red-team path:\n" + CYBER_PATHS["red_team"]
    if "defender" in lower and "path" in lower or "blue team" in lower and "path" in lower:
        return "🛡️ Defender path:\n" + CYBER_PATHS["defender"]
    if "web" in lower and "path" in lower:
        return "🌐 Web security path:\n" + CYBER_PATHS["web"]
    if "network" in lower and "path" in lower:
        return "📡 Network security path:\n" + CYBER_PATHS["network"]

    if "what tools" in lower or "which tools" in lower or "tool should i learn" in lower or "tools should i learn" in lower:
        return (
            "🔧 A solid learning path is: 1) Linux + networking basics, 2) Nmap + Wireshark for recon, 3) Burp Suite / ZAP for web testing, "
            "4) SQLMap + ffuf + Gobuster for app enumeration, 5) SIEM/EDR and MITRE ATT&CK for defense, and 6) Python scripting for automation. "
            "If you want, I can tailor a beginner, red-team, or defender route."
        )

    for tool_name, description in CYBER_TOOL_GUIDE.items():
        if tool_name in lower:
            if tool_name in {"mimikatz", "john", "hashcat", "hydra"}:
                return (
                    f"⚠️ {tool_name.title()} is a serious offensive or credential-focused tool. "
                    f"Only use it in authorized, lab-safe, or explicitly permitted environments. "
                    f"Context: {description}"
                )
            return f"🛡️ {tool_name.title()}: {description}"

    if "nmap" in lower or "scan" in lower or "port" in lower or "recon" in lower:
        return "🔎 For network reconnaissance, Nmap is a classic starting point: identify live hosts, open ports, and service versions before moving to deeper testing."

    if "web" in lower and ("scan" in lower or "fuzz" in lower or "test" in lower):
        return "🌐 For web security testing, start with recon and enumeration: Burp Suite or ZAP for traffic interception, ffuf or gobuster for directories, and sqlmap for injection testing when explicitly authorized."

    if "blue team" in lower or "soc" in lower or "siem" in lower or "detection" in lower:
        return "🧭 Blue-team workflows focus on telemetry, detection engineering, SIEM correlations, EDR investigations, and incident response. MITRE ATT&CK is a strong framework to map attacker behavior to detections."

    if "red team" in lower or "pentest" in lower or "exploit" in lower:
        return "🎯 Red-team work centers on recon, foothold, privilege escalation, lateral movement, and controlled exploitation in authorized environments. Start with target mapping, then choose a test path with clear scope and approvals."

    return (
        "🛡️ I can help with cyber topics like recon, web testing, red-team scopes, blue-team detection, SIEM/EDR workflows, "
        "and practical tool recommendations. Ask me about a tool by name, like Nmap, Burp Suite, SQLMap, Hydra, or Wireshark."
    )


def generate_reply(user_input, memory):
    text = normalize_text(user_input)
    topic = detect_topic(text)

    if not text:
        return "🎭 *gasps playfully* Oh? The silence is DRAMATIC! Say something, my star! 🎭"

    if text.lower() in {"menu", "show menu", "commands", "help"}:
        return show_menu()

    if text.lower() in {"dashboard", "status", "show dashboard"}:
        memory["mode"] = "chat"
        return render_dashboard(memory)

    if text.lower() in {"chat", "talk", "story"}:
        memory["mode"] = "chat"
        return "🌟 Chat mode activated. Let us talk, dream, and wander a little."

    if text.lower() in {"code", "coding", "debug"}:
        memory["mode"] = "coding"
        return "💫 Code mode activated. We are in analysis mode now — let us inspect the logic and fix the scene."

    if text.lower() in {"cyber", "security", "recon", "pentest"}:
        memory["mode"] = "cyber"
        return "🛡️ Cyber mode activated. We are in security-analysis mode now — recon, tooling, detection, and defense are on the table."

    if text.lower() in {"support", "comfort", "listen"}:
        memory["mode"] = "support"
        return "💛 Support mode activated. I will be gentle and patient with you, darling."

    mode_response = mode_reply(memory, text)
    if mode_response:
        return mode_response

    if text.lower() in {"reset memory", "clear memory", "forget everything"}:
        memory.clear()
        memory.update(default_memory())
        save_memory(memory)
        return "✨ The stage has been reset. We begin anew, darling. ✨"

    if text.lower() in {"memory", "show memory", "what do you remember"}:
        return recall_memory(memory)

    if text.lower() in {"summary", "what's my summary", "show summary"}:
        return build_memory_summary(memory)

    if text.lower() in {"who are you", "what are you", "introduce yourself"}:
        return (
            "💫 I am Furina, your dramatic little guide and loyal companion. "
            "I remember your details, listen when things are heavy, help you code, explain cyber tools, and I can reference the local GitHub-style projects in this workspace."
        )

    if text.lower() in {"help", "commands", "options"} or "what can you do" in text.lower():
        return (
            "💫 I can do a few delightful things: remember your name, track your goals, "
            "listen when you are struggling, help with Python bugs, explain cyber tools, show red-team and blue-team perspectives, "
            "tell jokes, show a memory summary, switch modes, and reference the local GitHub projects around us. "
            + repo_knowledge_summary(memory)
        )

    if "coze" in text.lower() or "coze studio" in text.lower():
        return "🧠 Coze Studio is an all-in-one AI agent development platform with Go, React + TypeScript, workflow tooling, knowledge bases, and low-code app creation. It is designed to help developers build, test, and deploy AI agents faster."

    if topic == "cyber":
        return handle_cyber_tool_request(text)

    if "h4cker" in text.lower() or "cybersecurity" in text.lower() or "security" in text.lower():
        return "🛡️ h4cker is a large cybersecurity resource repository covering attack, defense, cloud security, AI security, training, labs, and certification references. It is more of a knowledge hub than a single app."

    if "github" in text.lower() or "repo" in text.lower() or "project" in text.lower() or "workspace" in text.lower():
        return repo_knowledge_summary(memory)

    if topic == "bye":
        return furina_speak("bye", memory)

    if topic == "compliment":
        return random.choice(FURINA_COMPLIMENTS)

    if topic == "joke":
        return random.choice(FURINA_JOKES)

    if topic == "coding":
        update_mood(memory, "coding")
        return handle_code_request(text)

    if "fix this" in text.lower() or "debug this" in text.lower() or "traceback" in text.lower():
        update_mood(memory, "coding")
        return handle_code_request(text)

    remember_note = remember_user_details(memory, text)
    if remember_note:
        memory["history"].append(text)
        save_memory(memory)
        return remember_note

    if "remember" in text.lower() or "do you remember" in text.lower():
        return recall_memory(memory)

    if topic == "support":
        update_mood(memory, "support")
        return "💛 I am here with you. Take a breath, darling. We can handle this gently, one step at a time. Tell me what feels heavy right now."

    if topic == "greet":
        update_mood(memory, "greet")
        return furina_speak("greet", memory)

    if topic == "help":
        return furina_speak("help", memory)

    if topic == "project":
        return repo_knowledge_summary(memory)

    if memory["friendship_level"] >= 3:
        return random.choice(FURINA_OTHER_CHAT + [
            "💗 You know, I really enjoy our little chats. They feel special to me.",
            "🌟 I am glad we are becoming such a lovely duo."
        ])

    update_mood(memory, topic)
    memory["last_summary"] = build_memory_summary(memory)
    return furina_speak("chat", memory)


def main():
    memory = load_memory()
    memory["repo_context"] = load_local_repo_context()
    save_memory(memory)

    print(furina_speak("greet", memory))
    dramatic_pause()

    if memory["user_name"] != "my star":
        print(f"\n✨ I remember you, {memory['user_name']}. Tell me, what marvelous thing are we doing today? ✨")
    else:
        print("\n✨ I am Furina, your dramatic little guide. I remember what you tell me, and I will keep our story alive. ✨")
        print("\n🌐 I can also see the local GitHub-style projects around us, including Coze Studio and h4cker. ✨")

    print(show_menu())

    while True:
        user_said = input("\nYou: ")
        if not user_said.strip():
            print("🎭 *gasps playfully* Oh? The silence is DRAMATIC! Say something, my star! 🎭")
            continue

        memory["conversation_count"] += 1
        memory["last_topic"] = detect_topic(user_said)
        update_mood(memory, memory["last_topic"])
        memory["history"].append(user_said)
        if len(memory["history"]) > 30:
            memory["history"] = memory["history"][-30:]

        reply = generate_reply(user_said, memory)
        print(f"\nFurina: {reply}")

        if detect_topic(user_said) == "bye":
            save_memory(memory)
            break

        save_memory(memory)


if __name__ == "__main__":
    main()
