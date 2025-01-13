<a id="readme-top"></a>
<p align="center">
  <a href="https://theblockheads.net">
    <img alt="The Blockheads" src="https://github.com/user-attachments/assets/8f162932-0a4d-429d-9f3e-bd97d980e893">
  </a>
</p>

<div align="center">
<h3 align="center">The Blockheads Game Server for Linux and MacOS</h3>
   
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<p align="center">This repository contains the server files for running a Blockheads multiplayer server.</p>
<div align="left"><b>Warning:</b></div>
<div align="left">Running curl to bash scripts from the internet can be risky. It's always recommended to review the code before executing it to ensure it is safe and does not contain any malicious content</div><br>
<a href="https://github.com/JonCastaway/BHS/wiki"><strong>Explore the docs »</strong></a>
<br />
<br />
<a href="https://github.com/JonCastaway/BHS/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
·
<a href="https://github.com/JonCastaway/BHS/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#1. Installation (Linux)">Linux Install</a></li>
    <li><a href="#2. Installation (MacOS)">MacOS Install</a></li>
    <li><a href="#3. Original Binaries (Manual Install)">Manual Install</a></li>
    <li><a href="#4. Contributing">Contributing</a></li>
    <li><a href="#5. License">License</a></li>
    <li><a href="#6. Contact">Contact</a></li>
  </ol>
</details>

# The Blockheads Game Server for Linux and MacOS

## Getting Started
![GettingStarted](https://github.com/user-attachments/assets/181856ca-8597-43d3-97c4-cf13a99c924d)

### 1. Installation (Linux)

Follow the instructions below to install and set up the Blockheads server on your system.

Download and run the server script:
```bash
curl -sL https://raw.githubusercontent.com/JonCastaway/BHS/main/start.sh | bash -s -
```

Create Your server:
```bash
./blockheads_server171 -n MyFirstServer
```

For more options and help use:
```bash
./blockheads_server171 -h
```

Configure Your server:
`You'll need to replace the WORLD_ID and PORT inside the run.sh script.`

```bash
nano run.sh
```

`Replace the placeholders with your WORLD_ID and PORT. You can find your WORLD_ID by typing:`

```bash
./blockheads_server171 -l
```

`Save and exit the file by pressing CTRL+X, then Y, and ENTER.`

### 2. Installation (MacOS)

Download the Blockheads Server App

[Download from App Store](https://apps.apple.com/us/app/blockheadsserver/id662633568)

### 3. Original Binaries (Manual Install)

You can download the original server binaries from the links below

- [Download The Blockheads Server Binary - archive.org](https://archive.org/download/BHSv171/blockheads_server171.tar.gz)
- [Download The Blockheads Server Binary - majicdave.com](https://majicdave.com/share/blockheads_server171.tar.gz)

### 4. Contributing
![contributing](https://github.com/user-attachments/assets/5059e3bc-ea8c-4965-96c4-c6c500d0ba06)

Contributions are welcome! Feel free to fork this repository and submit pull requests.

#### Contributors
<a href="https://github.com/JonCastaway/BHS/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=JonCastaway/BHS&t=1" />
</a>

### 5. License
This project is Licensed under the GPL-3.0 License. See the [License](https://github.com/JonCastaway/BHS/blob/main/LICENCE) file for details.

### 6. Contact
![contact](https://github.com/user-attachments/assets/2b40e187-309b-4a58-be5f-fc71d045298a)

For any questions or support, please reach out or open an issue on GitHub.

[contributors-shield]: https://img.shields.io/github/contributors/JonCastaway/BHS.svg?style=for-the-badge
[contributors-url]: https://github.com/JonCastaway/BHS/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/JonCastaway/BHS.svg?style=for-the-badge
[forks-url]: https://github.com/JonCastaway/BHS/network/members
[stars-shield]: https://img.shields.io/github/stars/JonCastaway/BHS.svg?style=for-the-badge
[stars-url]: https://github.com/JonCastaway/BHS/stargazers
[issues-shield]: https://img.shields.io/github/issues/JonCastaway/BHS.svg?style=for-the-badge
[issues-url]: https://github.com/JonCastaway/BHS/issues
