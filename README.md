<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img alt="Carlos Nava. Full-stack and forward deployed engineer in Mexico. I talk to whoever has the problem, then build and run the fix. Open to remote roles and freelance projects." src="assets/header-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://www.carlosnava.dev"><img alt="Website: carlosnava.dev" src="https://img.shields.io/badge/carlosnava.dev-1e50d4?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
  <a href="https://www.linkedin.com/in/carlosnavam"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0a66c2?style=for-the-badge"></a>
  <a href="mailto:hello@carlosnava.dev"><img alt="Email: hello@carlosnava.dev" src="https://img.shields.io/badge/hello@carlosnava.dev-15171c?style=for-the-badge&logo=minutemailer&logoColor=white"></a>
  <a href="https://www.carlosnava.dev/assets/cv/Carlos_Nava_CV.pdf"><img alt="CV in PDF" src="https://img.shields.io/badge/CV-PDF-5b606b?style=for-the-badge&logo=readdotcv&logoColor=white"></a>
  <a href="https://www.carlosnava.dev/es"><img alt="Versión en español" src="https://img.shields.io/badge/🇲🇽_Español-1f7a4d?style=for-the-badge"></a>
</p>

👋 **Senior full-stack engineer** and **forward deployed engineer** in Mexico 🇲🇽 with **6 years** shipping production software in **Python / Django**, **TypeScript / React / Next.js**, **React Native and Swift (iOS)** and **AI agents (Claude API, OpenAI API, MCP)** on **AWS**. I sit with the people who have the problem, then design, build, deploy and run the fix. I've also led a team of five. 🌎 Open to **remote** roles (US · Mexico · LATAM) and freelance projects.

## 🚀 Building now

<table>
<tr>
<td width="33%" valign="top">
<img alt="Telecom operations platform: 96% of SIM activations and recharges succeed" src="assets/telecom-cover.svg" width="100%">

**📡 Telecom ops platform**<br>
<sub>Freelance · client under NDA · 2025 – now</sub>

SIM activations and recharges on AT&T and Movistar, built solo from discovery to production. **96%** success, **~MXN $1M** a month, **60%** less operating time.

`Django` `React` `AWS VPN` `SOAP` `Claude API` `MCP`
</td>
<td width="33%" valign="top">
<a href="https://therelic.app"><img alt="Relic on an iPhone: remember what you read" src="https://www.carlosnava.dev/assets/projects/relic-preview.webp" width="100%"></a>

**📚 [Relic](https://therelic.app)**<br>
<sub>iOS · founder, solo dev · 2025 – now</sub>

Brings back your book highlights every morning. Paying subscribers in 🇺🇸 🇲🇽 🇹🇼. Its MCP server is listed in the Claude and ChatGPT directories. ~15K lines of Swift, ~1,800 tests.

`Swift` `Expo` `FastAPI` `Supabase` `MCP` `OAuth 2.1`
</td>
<td width="33%" valign="top">
<a href="https://gymwigas.app"><img alt="Gym Wigas: work out, have a blast doing it" src="https://www.carlosnava.dev/assets/projects/gym-wigas-preview.webp" width="100%"></a>

**🏋️ [Gym Wigas](https://gymwigas.app)**<br>
<sub>iOS + Android · founder, solo dev · 2026 – now</sub>

A fitness game: your character levels up only when you really train. Live video duels for 8, push-ups counted by the camera, verified gym check-ins. 898 commits in 43 days.

`Next.js` `Expo` `Supabase` `LiveKit` `MediaPipe` `Stripe`
</td>
</tr>
</table>

<details>
<summary>🏗️ <b>Under the hood:</b> how each one is built</summary>

#### 📡 Telecom ops platform

```mermaid
flowchart LR
  owner(["👤 Owner"]) --> app["🖥️ Ops platform<br/>React · Django · DDD + TDD"]
  app -->|"SOAP over AWS Site-to-Site VPN"| att["📡 AT&T"]
  app --> mov["📡 Movistar"]
  jobs["⏱️ Scheduled pipelines"] --> app
  app --> dash["📊 Sales · inventory · health"]
  owner <-->|"asks in plain words"| agent["🤖 AI ops agent<br/>Claude API · tool use · evals"]
  agent -->|"MCP tools, live data"| app
  agent -.->|"corrective actions wait for approval"| owner
```

#### 📚 Relic

```mermaid
flowchart LR
  kindle["📥 Kindle import<br/>Playwright"] --> core[("🗄️ Library<br/>FastAPI · Supabase")]
  paper["📷 Paper books<br/>OCR · dictation"] --> core
  core --> ios["📱 iOS app<br/>Swift · Expo · 44 languages"]
  ios --> daily["🌅 One highlight every morning"]
  claude["Claude"] -->|"OAuth 2.1"| mcp["🔌 Remote MCP server<br/>official Python SDK"]
  chatgpt["ChatGPT"] -->|"OAuth 2.1"| mcp
  mcp --> core
```

#### 🏋️ Gym Wigas

```mermaid
flowchart LR
  phone["📱 iOS · Android<br/>Expo · React Native"] -->|"pose landmarks"| reps["💪 Push-up counter<br/>MediaPipe · TF Lite"]
  phone <-->|"WebRTC, up to 8 players"| duel["🎥 Live duels<br/>LiveKit"]
  phone -->|"check-in"| places["📍 Google Places<br/>verifies the gym"]
  phone <--> api["⚙️ Next.js · Supabase"]
  reps --> xp["⭐ XP · levels · leaderboards"]
  places --> xp
  api --> pay["💳 Stripe · RevenueCat"]
```

</details>

## 📈 Results I've shipped

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/impact-dark.svg">
  <img alt="96% of activations and recharges succeed. About MXN $1M processed a month. 60% less operating time. 80% more accurate candidate classification. 70% less manual work. 60% faster reaction to threats. 40% of warehouse work automated. 50K+ flight bookings a month with 30% less downtime." src="assets/impact-light.svg" width="100%">
</picture>

## 🧰 Stack

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=py%2Cts%2Cjs%2Cgo%2Cswift%2Cdjango%2Cfastapi%2Cgraphql%2Cpostgres%2Cmongodb%2Csupabase%2Creact%2Cnextjs%2Cvue%2Cnuxtjs%2Cangular%2Caws%2Cdocker%2Cgithubactions%2Clinux%2Cgit%2Ctensorflow%2Copencv&perline=12&theme=dark">
  <img alt="Python, TypeScript, JavaScript, Go, Swift, Django, FastAPI, GraphQL, PostgreSQL, MongoDB, Supabase, React, Next.js, Vue, Nuxt, Angular, AWS, Docker, GitHub Actions, Linux, Git, TensorFlow, OpenCV" src="https://skillicons.dev/icons?i=py%2Cts%2Cjs%2Cgo%2Cswift%2Cdjango%2Cfastapi%2Cgraphql%2Cpostgres%2Cmongodb%2Csupabase%2Creact%2Cnextjs%2Cvue%2Cnuxtjs%2Cangular%2Caws%2Cdocker%2Cgithubactions%2Clinux%2Cgit%2Ctensorflow%2Copencv&perline=12&theme=light">
</picture>

![Claude API](https://img.shields.io/badge/Claude_API-d97757?style=flat-square&logo=anthropic&logoColor=white)
![OpenAI API](https://img.shields.io/badge/OpenAI_API-15171c?style=flat-square)
![MCP servers](https://img.shields.io/badge/MCP_servers-1e50d4?style=flat-square&logo=modelcontextprotocol&logoColor=white)
![AI agents](https://img.shields.io/badge/AI_agents_·_tool_use_·_evals-5b606b?style=flat-square)
![React Native](https://img.shields.io/badge/React_Native-20232a?style=flat-square&logo=react&logoColor=61dafb)
![Expo](https://img.shields.io/badge/Expo-000020?style=flat-square&logo=expo&logoColor=white)
![LiveKit](https://img.shields.io/badge/LiveKit-1f1f1f?style=flat-square&logo=livekit&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0097a7?style=flat-square&logo=mediapipe&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-635bff?style=flat-square&logo=stripe&logoColor=white)

<sub>🔎 Senior Full-Stack Engineer · Forward Deployed Engineer · Backend Engineer · AI Engineer · Python · Django · FastAPI · TypeScript · React · Next.js · React Native · Expo · Swift · iOS · PostgreSQL · Supabase · MongoDB · REST · GraphQL · SOAP · AWS (EC2, S3, VPN) · Docker · CI/CD · GitHub Actions · LLM · AI agents · Claude API · OpenAI API · Model Context Protocol (MCP) · OAuth 2.1 · Playwright · web scraping · data pipelines · Domain-Driven Design · TDD · Spec-Driven Development · remote · Mexico · LATAM · English · Spanish</sub>

## 💼 Experience

| 📅 | 🏢 | 👨‍💻 Role | 📈 Impact |
|---|---|---|---|
| 2025 – now | Freelance | Forward Deployed Engineer | Telecom ops platform built solo · AI ops agent on Claude + MCP |
| 2024 – 25 | Alluxi | Software Engineer | AI recruiting on the OpenAI API, **80%** more accurate classification |
| 2023 – 24 | Jüsto | Backend Developer | Backend **30%** faster, **40%** of warehouse work automated |
| 2023 | Scitum | Cybersecurity Engineer | Incident response on Cortex xSOAR + Python, **60%** faster |
| 2021 – 23 | Alluxi | Full-Stack Engineer · Team Lead | Led **5** engineers · **50K+** bookings a month, **30%** less downtime |
| 2021 | Nómada | Full-Stack Engineer | HR platform with React, GraphQL, Go and AWS |
| 2020 – 21 | Sysy.mx | Backend Developer | Scraping bots for insurance data, **70%** less manual work |

🎓 B.Sc. Software Engineering, UANL · 🗣️ Spanish (native), English (professional) · 📄 [Full CV](https://www.carlosnava.dev/cv)

## 📊 Activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/activity-dark.svg">
  <img alt="GitHub contributions per year: 2019 27, 2020 1,258, 2021 891, 2022 554, 2023 122, 2024 1,005, 2025 683, 2026 3,141 so far, with 2,903 commits and 229 pull requests." src="assets/activity-light.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/yeguacelestial/yeguacelestial/output/snake-dark.svg">
  <img alt="A snake eating my contribution graph" src="https://raw.githubusercontent.com/yeguacelestial/yeguacelestial/output/snake-light.svg" width="100%">
</picture>

<details>
<summary>🗂️ <b>Public projects</b> (most of my code is private: client work under NDA and my own apps)</summary>

- 📰 [fake-news-detection](https://github.com/yeguacelestial/fake-news-detection): Django web app that flags fake news with a passive-aggressive classifier
- 🎵 [amram-ai](https://github.com/yeguacelestial/amram-ai): desktop app that splits a song into stems with Demucs, fully offline
- 🌦️ [reservamos-challenge](https://github.com/yeguacelestial/reservamos-challenge): Django REST API that compares weather forecasts across destinations
- ✅ [puul-challenge](https://github.com/yeguacelestial/puul-challenge): task management API with NestJS and Docker
- 🎙️ [podcast-multicam-editor](https://github.com/yeguacelestial/podcast-multicam-editor): cuts between two cameras based on who is speaking
- 📍 [mclp-sto](https://github.com/yeguacelestial/mclp-sto): heuristics for the Maximal Covering Location Problem

</details>

<p align="center"><sub>🎸 guitar · 🎹 piano · 🎻 orchestral music · 📚 books (where Relic came from) · 🏋️ the gym (where Gym Wigas came from)</sub></p>
