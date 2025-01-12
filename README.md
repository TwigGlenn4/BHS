# The Blockheads Server for Linux and Mac

This repository contains the server files for running a Blockheads multiplayer server.

**Warning:** Running `curl` to bash scripts from the internet can be risky. It's always recommended to review the code before executing it to ensure it is safe and does not contain any malicious content.
   
## Installation

Follow the instructions below to install and set up the Blockheads server on your system (Deban/Ubuntu - APT based distros).

### Linux

1. **Download and Run the Server Script:**
   ```bash
   curl -sL https://raw.githubusercontent.com/JonCastaway/BHS/main/start.sh | bash -s -
   ```

2. **Create Your Server:**
   ```bash
   ./blockheads_server171 -n MyFirstServer
   ```

3. **For more options and help use:**
   ```bash
   ./blockheads_server171 -h
   ```

4. **Configure Your Server:**

   `You'll need to replace the WORLD_ID and PORT inside the run.sh script.`

   ```bash
   nano run.sh
   ```

   `Replace the placeholders with your WORLD_ID and PORT. You can find your WORLD_ID by typing:`

   ```bash
   ./blockheads_server171 -l
   ```

   `Save and exit the file by pressing CTRL+X, then Y, and ENTER.`

### macOS

1. **Download the Blockheads Server App:**
   [Download from App Store](https://apps.apple.com/us/app/blockheadsserver/id662633568)

## Original Binaries

You can download the original server binaries from the links below:

- [Download The Blockheads Server Binary - archive.org](https://archive.org/download/BHSv171/blockheads_server171.tar.gz)
- [Download The Blockheads Server Binary - majicdave.com](https://majicdave.com/share/blockheads_server171.tar.gz)

## Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests.

## License

This project is licensed under the GPL-3.0 License. See the [LICENSE](https://github.com/JonCastaway/BHS/blob/main/LICENCE) file for details.

## Contact

For any questions or support, please reach out or open an issue on GitHub.
